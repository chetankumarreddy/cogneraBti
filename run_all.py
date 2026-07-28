#!/usr/bin/env python3
import argparse
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROCS = []

def exists(name):
    return shutil.which(name) is not None

def run(label, cmd, cwd=ROOT):
    print(f"[Cognira BTI] {label}: {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=str(cwd))

def start(label, cmd, cwd=ROOT):
    print(f"[Cognira BTI] starting {label}: {' '.join(cmd)}")
    proc = subprocess.Popen(cmd, cwd=str(cwd))
    PROCS.append((label, proc))
    return proc

def stop(*_args):
    print("\n[Cognira BTI] stopping modules...")
    for _, proc in PROCS:
        if proc.poll() is None:
            proc.terminate()
    time.sleep(1)
    for _, proc in PROCS:
        if proc.poll() is None:
            proc.kill()
    print("[Cognira BTI] shutdown complete")
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="Run Cognira BTI")
    parser.add_argument("--skip-install", action="store_true")
    parser.add_argument("--backend-only", action="store_true")
    parser.add_argument("--api-port", default="8000")
    parser.add_argument("--frontend-port", default="5173")
    args = parser.parse_args()
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    py = sys.executable

    if not args.skip_install:
        run("install Python dependencies", [py, "-m", "pip", "install", "-r", "requirements.txt"])
    if not args.backend_only and not exists("npm"):
        print("[Cognira BTI][ERROR] npm not found. Install Node.js or run with --backend-only.")
        sys.exit(1)
    if not args.skip_install and not args.backend_only:
        run("install React frontend dependencies", ["npm.cmd", "install", "--force"], ROOT / "frontend")

    start("FastAPI backend", [py, "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", args.api_port], ROOT / "backend")
    time.sleep(2)
    if not args.backend_only:
        start("React frontend", ["npm.cmd", "run", "dev", "--", "--host", "0.0.0.0", "--port", args.frontend_port], ROOT / "frontend")

    print(f"""
Cognira BTI running:
API:      http://localhost:{args.api_port}/docs
Frontend: http://localhost:{args.frontend_port}
Demo:     TXN-000421
Press Ctrl+C to stop.
""")
    while True:
        for label, proc in PROCS:
            if proc.poll() is not None:
                print(f"[Cognira BTI] {label} stopped with code {proc.returncode}")
                stop()
        time.sleep(3)

if __name__ == "__main__":
    main()
