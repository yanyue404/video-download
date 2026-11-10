"""运行：cd server; pip install -r requirements.txt httpx pytest; pytest -q（不联网）"""
import os

os.environ["TOKEN"] = "secret"

from fastapi.testclient import TestClient  # noqa: E402

from app import app, video_id  # noqa: E402

client = TestClient(app)
GOOD = "https://www.youtube.com/watch?v=qhH8yP26GfU"
AUTH = {"Authorization": "Bearer secret"}


def test_video_id():
    for u in [GOOD, "https://youtu.be/qhH8yP26GfU?t=5", "https://m.youtube.com/shorts/qhH8yP26GfU",
              "https://music.youtube.com/watch?v=qhH8yP26GfU&list=x"]:
        assert video_id(u) == "qhH8yP26GfU", u
    for u in ["", "hello", "file:///etc/passwd", "https://example.com/watch?v=qhH8yP26GfU",
              "https://evilyoutube.com/watch?v=qhH8yP26GfU", "https://www.youtube.com/playlist?list=abc",
              "https://www.youtube.com/watch?v=short"]:
        assert video_id(u) is None, u


def test_auth_and_validation():
    assert client.get("/convert", params={"url": GOOD}).status_code == 401
    assert client.get("/convert", params={"url": GOOD}, headers={"Authorization": "Bearer x"}).status_code == 401
    assert client.get("/convert", params={"url": "https://example.com"}, headers=AUTH).status_code == 400
    assert client.get("/convert", params={"url": GOOD, "fmt": "exe"}, headers=AUTH).status_code == 400
    assert client.get("/convert", params={"url": GOOD, "q": 999}, headers=AUTH).status_code == 400
    assert client.get("/health").json() == {"ok": True}
