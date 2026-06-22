@echo off
chcp 65001 >nul
echo ========================================
echo   检查Python环境
echo ========================================
echo.
python --version
echo.

python -c "import sys; print(f'Python路径: {sys.executable}')"
echo.

:: 检查Python版本是否兼容
python -c "import sys; v=sys.version_info; exit(0 if v.major==3 and 8<=v.minor<=11 else 1)"
if errorlevel 1 (
    echo ⚠️ 警告: 当前Python版本可能不兼容
    echo 推荐使用 Python 3.8 - 3.11
    echo 当前版本可能无法安装pygame
) else (
    echo ✅ Python版本兼容
)

echo.
echo 推荐安装Python 3.11:
echo https://www.python.org/downloads/release/python-3119/
echo.
pause