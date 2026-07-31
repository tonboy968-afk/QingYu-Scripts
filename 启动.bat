@echo off
chcp 65001 >nul
echo ========================================
echo   客服话术管理系统 - 启动中...
echo ========================================
echo.

cd /d "%~dp0backend"

echo [1/2] 正在启动后端服务 (端口: 8010)...
start "KefuScriptBackend" cmd /k "python -m uvicorn app.main:app --host 127.0.0.1 --port 8010 --reload"

echo [2/2] 等待服务启动...
timeout /t 3 > nul

echo 正在打开浏览器...
start http://127.0.0.1:8010

echo ========================================
echo   启动完成！
echo   - 后端服务日志请在弹出的窗口中查看
echo   - 系统界面已在浏览器中自动打开
echo   - 关闭后端窗口即停止服务
echo ========================================
echo.
