import sys
import os
import subprocess
import threading

# ANSI Color Codes for clean terminal output
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


def stream_logs(pipe, prefix, color):
    """Stream subprocess logs with a color-coded prefix."""
    try:
        for line in iter(pipe.readline, ""):
            if line:
                print(f"{color}{BOLD}[{prefix}]{RESET} {line.strip()}", flush=True)
    except Exception:
        pass


def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.join(root_dir, "frontend")

    # Locate Python in virtual environment
    if os.name == "nt":
        venv_python = os.path.join(root_dir, "venv", "Scripts", "python.exe")
    else:
        venv_python = os.path.join(root_dir, "venv", "bin", "python")

    python_exe = venv_python if os.path.exists(venv_python) else sys.executable

    print(f"\n{YELLOW}{BOLD}===================================================={RESET}")
    print(f"{YELLOW}{BOLD}  ⚡ Starting AURA Full-Stack Multi-Agent Assistant {RESET}")
    print(f"{YELLOW}{BOLD}===================================================={RESET}")
    print(f"  • {CYAN}Backend API:{RESET}  http://127.0.0.1:8000/docs")
    print(f"  • {GREEN}Frontend UI:{RESET}  http://localhost:5173")
    print(f"  • {YELLOW}Press Ctrl+C to stop both servers{RESET}\n", flush=True)

    # Start FastAPI Backend process
    backend_cmd = [
        python_exe,
        "-m",
        "uvicorn",
        "backend.src.main:app",
        "--reload",
        "--port",
        "8000",
    ]
    backend_proc = subprocess.Popen(
        backend_cmd,
        cwd=root_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    # Start Vite React Frontend process
    npm_cmd = "npm run dev"
    frontend_proc = subprocess.Popen(
        npm_cmd,
        cwd=frontend_dir,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    # Start background threads to stream output
    t_backend = threading.Thread(
        target=stream_logs,
        args=(backend_proc.stdout, "FastAPI", CYAN),
        daemon=True,
    )
    t_frontend = threading.Thread(
        target=stream_logs,
        args=(frontend_proc.stdout, "React", GREEN),
        daemon=True,
    )

    t_backend.start()
    t_frontend.start()

    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[AURA] Shutting down backend and frontend servers...{RESET}", flush=True)
        try:
            backend_proc.terminate()
            frontend_proc.terminate()
            if os.name == "nt":
                subprocess.run(
                    f"taskkill /F /T /PID {backend_proc.pid}",
                    shell=True,
                    capture_output=True,
                )
                subprocess.run(
                    f"taskkill /F /T /PID {frontend_proc.pid}",
                    shell=True,
                    capture_output=True,
                )
        except Exception:
            pass
        print(f"{GREEN}[AURA] All services stopped cleanly. Goodbye!{RESET}\n", flush=True)


if __name__ == "__main__":
    main()
