@echo off
chcp 65001 >nul
echo ========================================
echo   贪吃蛇AI 环境配置脚本 (修复版)
echo ========================================
echo.

echo [1/5] 检查Python版本...
python --version
echo.

echo [2/5] 删除旧虚拟环境...
if exist "snake_venv" (
    echo 正在删除旧环境...
    rmdir /s /q snake_venv
)
echo.

echo [3/5] 创建新虚拟环境...
python -m venv snake_venv
echo.

echo [4/5] 激活环境并升级pip...
call snake_venv\Scripts\activate.bat

:: 使用国内镜像源避免SSL问题
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

:: 先安装numpy和torch（这些没问题）
echo 安装numpy...
pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple

echo 安装torch...
pip install torch --index-url https://download.pytorch.org/whl/cpu -i https://pypi.tuna.tsinghua.edu.cn/simple

:: 使用预编译的wheel安装pygame（避免编译）
echo 安装pygame...
pip install pygame --pre -i https://pypi.tuna.tsinghua.edu.cn/simple

:: 如果上面失败，尝试安装旧版本
if errorlevel 1 (
    echo 尝试安装pygame 2.5.2...
    pip install pygame==2.5.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
)

echo 安装matplotlib...
pip install matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple
echo.

echo [5/5] 测试安装...
python -c "import torch; import numpy; import pygame; import matplotlib; print('✅ 所有依赖安装成功！')"
if errorlevel 1 (
    echo.
    echo ⚠️ 部分依赖安装失败，尝试备选方案...
    echo.
    
    :: 备选：只安装必要的包
    echo 安装最小依赖集...
    pip install numpy torch matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple
    
    :: 安装pygame的wheel文件（如果预编译版本存在）
    pip install pygame-2.5.2-cp314-cp314-win_amd64.whl 2>nul
)

echo.
echo ========================================
echo   配置完成！
echo ========================================
echo 启动方式:
echo 1. 激活环境: snake_venv\Scripts\activate
echo 2. 运行训练: python snake_ai.py --mode train --episodes 100
echo.
pause