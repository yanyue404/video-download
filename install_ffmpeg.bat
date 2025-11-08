@echo off
chcp 65001 >nul
title 一键安装 ffmpeg

echo 正在检测 winget...
where winget >nul 2>&1
if %errorlevel% equ 0 (
    echo 使用 winget 安装 ffmpeg...
    winget install -e --id Gyan.FFmpeg
) else (
    echo winget 未找到，跳转手动下载...
    start https://www.gyan.dev/ffmpeg/builds/
    echo 请下载 ffmpeg-release-full.7z 并解压到 C:\ffmpeg
    echo 然后手动添加 C:\ffmpeg\bin 到 Path 环境变量
)

echo.
echo 安装完成！请重启终端后运行： ffmpeg -version
pause
