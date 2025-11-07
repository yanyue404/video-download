@echo off
REM =====================================================
REM  YouTube 视频下载为 MP4 脚本（可指定清晰度）
REM  作者：Grok（基于 yt-dlp）
REM  功能：下载视频 + 音频合并为 MP4
REM  依赖：yt-dlp + ffmpeg
REM  使用：双击运行 → 粘贴链接 → 选择清晰度
REM =====================================================

chcp 65001 >nul
title YouTube to MP4 下载器

echo.
echo ==========================================
echo   YouTube 视频 → MP4（支持选择清晰度）
echo ==========================================
echo.

set /p url=请输入 YouTube 视频/播放列表链接: 

if "%url%"=="" (
    echo.
    echo [错误] 链接不能为空！
    echo.
    pause
    exit /b 1
)

echo.
echo 正在检测可用清晰度...
yt-dlp -F "%url%" | findstr /i "mp4"

echo.
echo ==========================================
echo 请输入想要的清晰度（示例：1080p / 720p / 480p / best / worst）
echo 直接回车 = 下载最佳 MP4 质量（推荐）
echo ==========================================
set /p quality=清晰度选择: 

if "%quality%"=="" set quality=best

REM 根据输入生成格式过滤
if /i "%quality%"=="best" (
    set format=bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best
) else if /i "%quality%"=="worst" (
    set format=worstvideo[ext=mp4]+worstaudio/best[ext=mp4]/worst
) else (
    REM 自动匹配常见分辨率（如 1080p → 137）
    set format=bestvideo[height<=%quality:~0,-1%][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best
)

echo.
echo 正在下载：%quality% 质量的 MP4...
echo.

yt-dlp -f "%format%" ^
       -o "%%(title)s [%%(height)sP].%%(ext)s" ^
       "%url%"

if %errorlevel% equ 0 (
    echo.
    echo [成功] MP4 下载完成！
    echo 文件名示例：视频标题 [1080P].mp4
    echo.
) else (
    echo.
    echo [失败] 下载失败，请检查清晰度是否可用。
    echo.
)

pause