<# 打包独立 exe（Windows）
# 前置：本机已安装 Python 3.11+ 与 Node.js 18+
# 用途：大版本更新后，重新构建 QingYu-Scripts.exe 供非技术用户双击使用
# 源码日常迭代不受影响，仅在大版本时执行本脚本。
#>
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
cd $root

# 1. Python 虚拟环境 + 依赖
if (-not (Test-Path ".venv")) { py -3.11 -m venv .venv }
& ".venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller

# 2. 前端静态构建
cd "$root\frontend"
npm install
npm run build
cd $root

# 3. PyInstaller 打包（单文件 + 无控制台窗口）
cd "$root\backend"
pyinstaller -F -w `
  --name QingYu-Scripts `
  --distpath "$root\release" `
  --workpath "$root\build_tmp" `
  --add-data "..\frontend\dist;frontend\dist" `
  --add-data "scripts;backend\scripts" `
  --hidden-import app.routers.categories `
  --hidden-import app.routers.dashboard `
  --hidden-import app.routers.rules `
  --hidden-import app.routers.scripts `
  --hidden-import app.routers.stores `
  package_run.py
cd $root

Remove-Item "build_tmp" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host ""
Write-Host "✅ 打包完成：release\QingYu-Scripts.exe"
