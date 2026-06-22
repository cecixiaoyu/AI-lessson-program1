@echo off
chcp 65001 >nul
echo ========================================
echo   继续安装pygame和matplotlib
echo ========================================
echo.

:: 设置临时环境变量避免SSL错误
set PYTHONHTTPSVERIFY=0

echo [1/2] 安装matplotlib...
pip install matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo [2/2] 安装pygame (使用备选方案)...
echo 尝试安装pygame 2.5.2...

:: 尝试多个版本
pip install pygame==2.5.2 --trusted-host pypi.org --trusted-host files.pythonhosted.org

if errorlevel 1 (
    echo 尝试安装pygame 2.5.0...
    pip install pygame==2.5.0 --trusted-host pypi.org --trusted-host files.pythonhosted.org
)

if errorlevel 1 (
    echo 尝试安装最新开发版...
    pip install pygame --pre --trusted-host pypi.org --trusted-host files.pythonhosted.org
)

if errorlevel 1 (
    echo.
    echo ⚠️ pygame安装失败，但不用担心！
    echo 我们可以运行无图形界面的训练模式
    echo.
    goto :test
)

:test
echo.
echo ========================================
echo   测试安装结果
echo ========================================
python -c "import torch; print('✅ PyTorch版本:', torch.__version__)"
python -c "import numpy; print('✅ NumPy版本:', numpy.__version__)"
python -c "import matplotlib; print('✅ Matplotlib版本:', matplotlib.__version__)"

echo.
python -c "import pygame; print('✅ Pygame版本:', pygame.__version__)" 2>nul
if errorlevel 1 (
    echo ⚠️ Pygame未安装，但可以训练（无可视化）
    echo.
    echo 训练命令（不显示画面）:
    echo python snake_ai.py --mode train --episodes 100
) else (
    echo ✅ 所有依赖安装成功！
)

echo.
pause