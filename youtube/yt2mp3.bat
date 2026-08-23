@echo off
REM =====================================================
REM  YouTube 视频快速转 MP3 脚本
REM  作者：Grok（基于 yt-dlp）
REM  功能：提取音频 → 转为 MP3（最高 320kbps）
REM  依赖：yt-dlp + ffmpeg（需提前安装）
REM  使用：双击运行 → 粘贴链接 → 回车
REM =====================================================

REM 切换代码页为 UTF-8，避免中文乱码
chcp 65001 >nul

REM 设置控制台标题（可选）
title YouTube to MP3 转换器

echo.
echo ==========================================
echo   YouTube 视频 → MP3（最高音质 320kbps）
echo ==========================================
echo.

REM 提示用户输入 YouTube 链接
set /p url=请输入 YouTube 视频/播放列表链接:

if "%url%"=="" (
    echo.
    echo [错误] 链接不能为空！
    echo.
    pause
    exit /b 1
)

echo.
echo 正在下载并转换为 MP3（最高音质）...
echo.

REM yt-dlp 核心命令
REM -x                 : 仅提取音频
REM --audio-format mp3 : 转为 MP3
REM --audio-quality 0  : 最高音质（VBR 0 ≈ 320kbps）
REM --embed-thumbnail  : 自动嵌入封面图（如果可用）
REM -o "%(title)s.%(ext)s" : 文件名 = 标题.mp3
yt-dlp -x ^
       --audio-format mp3 ^
       --audio-quality 0 ^
       --embed-thumbnail ^
       -o "%%(title)s.%%(ext)s" ^
       "%url%"

REM 检查是否成功
if %errorlevel% equ 0 (
    echo.
    echo [成功] 转换完成！文件保存在当前文件夹。
    echo.
) else (
    echo.
    echo [失败] 下载或转换出错，请检查链接或网络。
    echo.
)

pause
