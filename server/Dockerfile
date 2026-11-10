FROM python:3.12-slim
# ffmpeg 用于转 MP3 和合并音视频；deno 是 yt-dlp 解 YouTube 签名所需的 JS 运行时
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*
COPY --from=denoland/deno:bin /deno /usr/local/bin/deno
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
