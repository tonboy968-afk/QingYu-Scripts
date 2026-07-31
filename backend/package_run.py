"""打包版启动入口（PyInstaller 冻结后使用）

- 自动建表
- 空库时填充一次种子数据（不覆盖用户已有数据）
- 启动 uvicorn 服务并自动打开浏览器
开发模式下请用 `python -m uvicorn app.main:app`，本文件仅用于打包发布。
"""
import os
import sys
import time
import threading
import webbrowser

# 冻结打包（PyInstaller -w 无控制台）时，sys.stdout/stderr 为 None，
# uvicorn 日志写入会报错导致服务启动失败。这里重定向到 exe 同目录的日志文件，
# 既保持无黑窗口体验，又保留运行日志。
if getattr(sys, "frozen", False):
    _log_path = os.path.join(os.path.dirname(sys.executable), "QingYu-Scripts.log")
    _log_file = open(_log_path, "a", encoding="utf-8", buffering=1)
    sys.stdout = _log_file
    sys.stderr = _log_file

from app.main import app
from app.db import init_db, SessionLocal
from app.models import Store

HOST = "127.0.0.1"
PORT = 8010


def _base_dir() -> str:
    """打包后资源根目录：冻结态在 sys._MEIPASS，开发态在 backend/。"""
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def _scripts_dir() -> str:
    """种子脚本目录：冻结态在 _MEIPASS/backend/scripts，开发态在 backend/scripts。"""
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, "backend", "scripts")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")


def seed_if_empty() -> None:
    init_db()
    db = SessionLocal()
    try:
        if db.query(Store).count() > 0:
            return  # 已有数据，不重复种子
    finally:
        db.close()

    # 动态加载种子脚本
    scripts_dir = _scripts_dir()
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import seed  # noqa: E402

    print("首次启动：写入示例数据...")
    seed.main()


def open_browser() -> None:
    time.sleep(1.5)
    webbrowser.open(f"http://{HOST}:{PORT}/")


if __name__ == "__main__":
    seed_if_empty()
    threading.Thread(target=open_browser, daemon=True).start()
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
