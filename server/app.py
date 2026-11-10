"""YouTube 转 MP3 / MP4 小服务。GET /convert?url=&fmt=mp3|mp4&q=1080，头部 Authorization: Bearer <TOKEN>。

环境变量：
  TOKEN         必填，访问口令
  ALLOW_ORIGIN  允许的页面来源，默认 https://yanyue404.github.io（本地调试可设 *）
  MAX_MINUTES   单个视频最长分钟数，默认 120
  COOKIES_FILE  可选，Netscape 格式 cookies，机房 IP 被要求登录时使用
  PROXY         可选，如 http://127.0.0.1:7890
"""
import os
import secrets
import shutil
import tempfile
import threading
from urllib.parse import parse_qs, urlparse

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.background import BackgroundTask
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError, match_filter_func

TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise RuntimeError("必须设置环境变量 TOKEN")

MAX_MINUTES = int(os.environ.get("MAX_MINUTES", "120"))
QUALITIES = {360, 480, 720, 1080, 1440, 2160}
_slots = threading.Semaphore(2)  # 同时最多转换 2 个，超出返回 429

app = FastAPI(title="video-download")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("ALLOW_ORIGIN", "https://yanyue404.github.io")],
    allow_headers=["Authorization"],
    expose_headers=["Content-Disposition"],
)
bearer = HTTPBearer(auto_error=False)


def check_token(cred: HTTPAuthorizationCredentials | None = Depends(bearer)) -> None:
    if not cred or not secrets.compare_digest(cred.credentials, TOKEN):
        raise HTTPException(401, "口令错误")


def video_id(url: str) -> str | None:
    """只接受 YouTube 单个视频链接，返回视频 ID；其它一律 None（防止被当成任意站点的下载代理）。"""
    u = urlparse(url.strip())
    if u.scheme not in ("http", "https"):
        return None
    host = (u.hostname or "").removeprefix("www.").removeprefix("m.").removeprefix("music.")
    if host == "youtu.be":
        vid = u.path[1:]
    elif host == "youtube.com":
        parts = u.path.strip("/").split("/")
        if u.path == "/watch":
            vid = (parse_qs(u.query).get("v") or [""])[0]
        elif parts[0] in ("shorts", "embed", "live") and len(parts) > 1:
            vid = parts[1]
        else:
            return None
    else:
        return None
    return vid if len(vid) == 11 and all(c.isalnum() or c in "-_" for c in vid) else None


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.get("/convert", dependencies=[Depends(check_token)])
def convert(url: str, fmt: str = "mp3", q: int = 1080) -> FileResponse:
    vid = video_id(url)
    if not vid:
        raise HTTPException(400, "只支持 YouTube 单个视频链接")
    if fmt not in ("mp3", "mp4") or q not in QUALITIES:
        raise HTTPException(400, "fmt 只能是 mp3 / mp4，q 只能是 " + "/".join(map(str, sorted(QUALITIES))))
    if not _slots.acquire(blocking=False):
        raise HTTPException(429, "服务忙，请稍后再试")

    tmp = tempfile.mkdtemp(prefix="vd-")
    opts = {
        "outtmpl": os.path.join(tmp, "%(title).100B.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "match_filter": match_filter_func(f"duration <= {MAX_MINUTES * 60}"),
        "cookiefile": os.environ.get("COOKIES_FILE") or None,
        "proxy": os.environ.get("PROXY") or None,
    }
    if fmt == "mp3":
        opts.update(
            format="bestaudio/best",
            postprocessors=[{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "0"}],
        )
    else:
        opts.update(format=f"bv*[height<={q}]+ba/b[height<={q}]/b", merge_output_format="mp4")

    def cleanup() -> None:
        shutil.rmtree(tmp, ignore_errors=True)
        _slots.release()

    try:
        with YoutubeDL(opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={vid}"])
        files = os.listdir(tmp)
        if not files:  # 被时长限制过滤掉时 yt-dlp 不报错也不产出文件
            raise HTTPException(422, f"视频超过 {MAX_MINUTES} 分钟或无法下载")
    except HTTPException:
        cleanup()
        raise
    except DownloadError as e:
        cleanup()
        raise HTTPException(502, str(e).splitlines()[-1][:300])
    except Exception:
        cleanup()
        raise
    return FileResponse(os.path.join(tmp, files[0]), filename=files[0], background=BackgroundTask(cleanup))
