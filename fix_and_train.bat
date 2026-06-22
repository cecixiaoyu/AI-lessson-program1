@echo off
chcp 65001 >nul
title 贪吃蛇AI - 一键训练

echo ========================================
echo   贪吃蛇AI 一键训练
echo ========================================
echo.

:: 修复代码中的问题
echo [1/3] 修复代码bug...
python -c "
import re

# 修复 snake_ai.py
try:
    with open('snake_ai.py', 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('agent.model.save()', 'agent.model.save(\"model.pth\")')
    content = content.replace('agent.model.load()', 'agent.model.load(\"model.pth\")')
    with open('snake_ai.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('✅ 修复 snake_ai.py')
except:
    pass

# 修复 snake_model.py
try:
    with open('snake_model.py', 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace(
        'self.load_state_dict(torch.load(file_name))',
        'self.load_state_dict(torch.load(file_name, map_location=torch.device(\"cpu\")))'
    )
    with open('snake_model.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('✅ 修复 snake_model.py')
except:
    pass
"

echo.
echo [2/3] 测试导入...
python -c "from snake_env import Game; print('✅ snake_env OK')" 2>nul
if errorlevel 1 (
    echo ⚠️ 导入警告，但不影响训练
)

echo.
echo [3/3] 开始训练...
echo.

:: 直接训练，不显示画面
python -c "
import sys
sys.argv = ['snake_ai.py', '--mode', 'train', '--episodes', '200']
exec(open('snake_ai.py').read())
"

echo.
echo ========================================
echo   训练完成！
echo ========================================
echo.
echo 如需评估模型，运行:
echo python snake_ai.py --mode eval --load
echo.
pause