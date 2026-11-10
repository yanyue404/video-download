# video-download

主流视频站点的下载方式，推荐 [IDM](https://www.internetdownloadmanager.com/) 多线程下载。

**v.qq.com**

> 测试下载链接：https://v.qq.com/x/cover/ki7cjbwwf8ud0sd/l32290t9gjr.html

方式 1：[猫抓 chrome资源嗅探扩展](https://github.com/xifangczy/cat-catch) + [N_m3u8DL-CLI m3u8下载器](https://github.com/nilaoda/N_m3u8DL-CLI)

方式 2： Stream Recorder - download HLS as MP4 chrome 扩展

**bilibili.com**

> 测试下载链接： https://www.bilibili.com/video/BV1ez4y127Ks/

B站下载助手 bilibili-helper

**youtube.com**

在线入口（GitHub Pages，聚合下方可用站点）：<https://yanyue404.github.io/video-download/>，源码 `index.html`。

> 测试下载链接： https://www.youtube.com/watch?v=qhH8yP26GfU

翻墙打开视频转换网站（2026-11-11 校对）：  

网站1：<https://y2down.cc/zhD8/youtube-mp3> （MP4 最高 4K，音频 MP3 320kbps / M4A / FLAC / WAV 等）

网站2：<https://ytmp3.gl/> （MP3 / MP4，无需注册，输入框下方 `change to MP4` 切换格式）

网站3：[https://youtube4kdownloader.com](https://youtube4kdownloader.com/) （视频质量最高设置为4k）

网站4：<https://yt5s.biz/zh-cn> （视频质量最高设置为4K）

网站5：<https://ddownr.com/zh/youtube-video-downloader> （视频质量最高设置为4k）

网站6：<https://downmp3.yt/zhCH/youtube-video-downloader> （视频质量最高设置为4k）

网站7：<https://yt1d.com/zh-tw> （视频质量最高设置为4k）

网站8：[https://cobalt.tools](https://cobalt.tools/) （视频质量默认1080p,settings-video-video quality可设置2k、4k清晰度）

> 已移除：`y2meta.app`（404）、`freesave.co`（跳转到域名停放页）、`youtube-convert.com` / `savemp4.cc` / `y2mate.com` / `9convert.com`（无法访问），以及依赖 y2meta 的油猴脚本 Y2meta Converter Button；Local YouTube Downloader 作者已停更。

**自建转换服务**（可选，`server/`）：FastAPI + yt-dlp + ffmpeg，在线入口页的“自建后端”填上地址和口令后可直接转换下载。

```bash
cd server
docker build -t video-download .
docker run -d -p 8000:8000 -e TOKEN=你的口令 -e ALLOW_ORIGIN=https://yanyue404.github.io video-download
# 接口：GET /convert?url=<YouTube链接>&fmt=mp3|mp4&q=1080  头部 Authorization: Bearer 你的口令
```

- 需部署在能访问 YouTube 的服务器上，并用 https 反代（Pages 是 https，不能请求 http 接口）。
- 机房 IP 常被 YouTube 返回 403 或要求登录：挂载 cookies（`-v ./cookies.txt:/app/cookies.txt -e COOKIES_FILE=/app/cookies.txt`）或设置 `-e PROXY=...`；并定期重新 build 以升级 yt-dlp。
- 仅支持 YouTube 单视频；默认单个最长 120 分钟（`MAX_MINUTES`），同时最多转换 2 个。
- 测试：`pip install -r requirements.txt httpx pytest; pytest -q`（不联网）。

## yt-dlp

使用 **yt-dlp** 下载 YouTube 视频和音频非常方便，以下是详细步骤和参数设置说明，涵盖如何选择分辨率和格式。

---

### 1. 安装 yt-dlp
确保已安装 yt-dlp：
- **Windows/Linux/macOS**：
  使用 pip 安装：
  ```bash
  pip install -U yt-dlp
  ```
  或下载最新 release 的可执行文件（Windows 可直接使用 `yt-dlp.exe`）。
- **验证安装**：
  ```bash
  yt-dlp --version
  ```

---

### 2. 基本下载命令
下载 YouTube 视频或音频的基本命令：
```bash
yt-dlp <YouTube视频URL>
```
- 默认会下载最佳质量的视频（通常是视频+音频合并的格式）。
- 示例：
  ```bash
  yt-dlp https://www.youtube.com/watch?v=VIDEO_ID
  ```

---

### 3. 下载视频并选择分辨率
yt-dlp 允许通过 `-f`（格式）参数选择特定分辨率或格式。YouTube 视频通常有多种分辨率（如 360p、720p、1080p、4K）和编码格式（如 H.264、VP9）。

#### 查看可用格式
运行以下命令列出视频的所有可用格式：
```bash
yt-dlp -F <YouTube视频URL>
```
输出示例：
```
ID  EXT RESOLUTION FPS | FILESIZE  | CODEC
137 mp4 1920x1080  30 | ~50.2MiB  | avc1
248 webm 1920x1080  30 | ~45.1MiB  | vp9
136 mp4 1280x720   30 | ~25.3MiB  | avc1
247 webm 1280x720   30 | ~22.7MiB  | vp9
...
```
- `ID` 是格式代码，用于指定下载的分辨率和编码。
- `EXT` 是文件扩展名（如 mp4、webm）。
- `RESOLUTION` 是分辨率。
- `CODEC` 是视频编码格式。

#### 下载特定分辨率的视频
使用 `-f` 参数指定格式代码。例如：
- 下载 1080p 的 mp4 视频（格式 ID 为 137，需合并音频）：
  ```bash
  yt-dlp -f 137+140 <YouTube视频URL>
  ```
  - `137` 是 1080p 视频流（无音频）。
  - `140` 是默认的 m4a 音频流。
  - `+` 表示合并视频和音频。

- 下载最佳质量的 720p 视频：
  ```bash
  yt-dlp -f "bestvideo[height<=720]+bestaudio/best[height<=720]" <YouTube视频URL>
  ```
  - `bestvideo[height<=720]` 选择分辨率不超过 720p 的最佳视频。
  - `bestaudio` 选择最佳音频。

#### 下载最佳质量视频
下载最高质量的视频+音频（自动合并）：
```bash
yt-dlp -f "bestvideo+bestaudio/best" <YouTube视频URL>
```

---

### 4. 下载音频
如果只需要音频，可以使用 `--extract-audio` 参数。

#### 下载音频（默认 MP3 格式）
```bash
yt-dlp --extract-audio --audio-format mp3 <YouTube视频URL>
```
- `--extract-audio`：提取音频。
- `--audio-format mp3`：指定输出为 MP3 格式（支持 mp3、m4a、wav 等）。

#### 下载特定质量的音频
查看音频格式：
```bash
yt-dlp -F <YouTube视频URL>
```
选择音频格式（例如 ID 为 140 的 m4a 音频）：
```bash
yt-dlp -f 140 <YouTube视频URL>
```

#### 下载最佳质量音频
```bash
yt-dlp -f bestaudio --extract-audio --audio-format mp3 <YouTube视频URL>
```

---

### 5. 常用参数设置
以下是一些常用的参数，用于优化下载体验：

- **指定输出文件名**：
  ```bash
  yt-dlp -o "输出文件名.%(ext)s" <YouTube视频URL>
  ```
  示例：`-o "my_video.%(ext)s"`

- **下载整个播放列表**：
  ```bash
  yt-dlp <播放列表URL>
  ```
  - 添加 `--no-playlist` 只下载单个视频。

- **下载字幕**：
  ```bash
  yt-dlp --write-subs --sub-langs en,zh-CN <YouTube视频URL>
  ```
  - `--sub-langs` 指定语言（如 `en` 为英语，`zh-CN` 为简体中文）。

- **限制下载速度**：
  ```bash
  yt-dlp --limit-rate 500K <YouTube视频URL>
  ```
  - 限制为 500KB/s。

- **设置代理（若需要翻墙）**：
  ```bash
  yt-dlp --proxy http://proxy_address:port <YouTube视频URL>
  ```

---

### 6. 高级分辨率选择示例
- **下载 4K 视频**：
  ```bash
  yt-dlp -f "bestvideo[height<=2160]+bestaudio/best" <YouTube视频URL>
  ```

- **下载 1080p 或更低分辨率（优先 VP9 编码）**：
  ```bash
  yt-dlp -f "bestvideo[height<=1080][vcodec^=vp9]+bestaudio/best" <YouTube视频URL>
  ```

- **下载所有可用分辨率**：
  ```bash
  yt-dlp -f "bestvideo+bestaudio" --merge-output-format mp4 --recode-video mp4 <YouTube视频URL>
  ```

---

### 7. 常见问题
- **格式不可用或需要登录**：
  某些视频可能需要登录或受地区限制。使用 `--cookies` 导入浏览器导出的 cookies 文件：
  ```bash
  yt-dlp --cookies cookies.txt <YouTube视频URL>
  ```

- **合并失败**：
  如果合并视频和音频失败，安装 **ffmpeg**（yt-dlp 依赖 ffmpeg 进行格式合并）：
  - Windows：下载 ffmpeg 并添加到系统 PATH。
  - Linux：`sudo apt install ffmpeg`
  - macOS：`brew install ffmpeg`

- **更新 yt-dlp**：
  定期更新以支持最新的 YouTube 格式：
  ```bash
  pip install -U yt-dlp
  ```

---

### 8. 配置文件（可选）
可以创建 `yt-dlp.conf` 文件保存常用参数，避免每次输入。例如：
```bash
# 文件路径：~/.yt-dlp.conf (Linux/macOS) 或 %APPDATA%\yt-dlp.conf (Windows)
-f bestvideo+bestaudio/best
-o %(title)s.%(ext)s
--embed-subs
--merge-output-format mp4
```
然后直接运行：
```bash
yt-dlp <YouTube视频URL>
```

### 参考

- https://www.v2ex.com/t/1060206#reply39
- https://github.com/Alvin9999/new-pac/wiki/YouTube%E4%B8%8B%E8%BD%BD1080%E6%95%99%E7%A8%8B



