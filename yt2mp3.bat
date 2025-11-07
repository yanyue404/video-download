@echo off
chcp 65001 >nul
title YouTube to MP3 音质可调版

echo.
echo ==========================================
echo   YouTube → MP3（支持选择音质）
echo ==========================================
echo  0 = 最高 (~320kbps)   2 = 高 (~240kbps)  推荐
echo  5 = 标准 (~160kbps)   7 = 省空间 (~120kbps)
echo  9 = 最低 (~80kbps)
echo ==========================================
set /p quality=请选择音质等级 (0-9，推荐 2): 

REM 验证输入
if "%quality%"=="" set quality=2
echo %quality%| findstr /r "^[0-9]$" >nul
if errorlevel 1 (
    echo [错误] 请输入 0-9 的数字！
    pause
    exit /b 1
)

set /p url=请输入 YouTube 链接: 
if "%url%"=="" (
    echo [错误] 链接不能为空！
    pause
    exit /b 1
)

echo.
echo 正在以 VBR %quality% (~最高音质) 转换...
yt-dlp -x ^
       --audio-format mp3 ^
       --audio-quality %quality% ^
       --embed-thumbnail ^
       -o "%%(title)s [%%(audio_bitrate)skbps].%%(ext)s" ^
       "%url%"

echo.
echo [完成] 文件已保存，文件名含实际比特率！
pause