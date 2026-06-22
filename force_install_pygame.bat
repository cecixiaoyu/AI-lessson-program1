@echo off
chcp 65001 >nul
echo ========================================
echo   强制安装pygame (使用本地wheel)
echo ========================================
echo.

:: 下载pygame wheel文件
echo 正在下载pygame wheel...
powershell -Command "Invoke-WebRequest -Uri 'https://files.pythonhosted.org/packages/5f/4c/ef677f6259ce4a2e9fda2c6b0b97e3b9ad73e8dca4791c23fafcf8003c1e/pygame-2.5.2-cp311-cp311-win_amd64.whl' -OutFile 'pygame-2.5.2-cp311-cp311-win_amd64.whl'"

if exist "pygame-2.5.2-cp311-cp311-win_amd64.whl" (
    echo 安装pygame...
    pip install pygame-2.5.2-cp311-cp311-win_amd64.whl
    del pygame-2.5.2-cp311-cp311-win_amd64.whl
) else (
    echo 下载失败，请手动下载pygame wheel
    echo 下载地址: https://pypi.org/project/pygame/#files
)

echo.
echo 测试pygame...
python -c "import pygame; print('✅ Pygame安装成功')"

pause