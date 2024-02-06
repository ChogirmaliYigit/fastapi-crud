import subprocess


def run_application():
    APP_DIR = "app"
    FILE_NAME = "base_app"
    FASTAPI_APP_NAME = "app"

    subprocess.call([
        "uvicorn",
        f"{APP_DIR}.{FILE_NAME}:{FASTAPI_APP_NAME}"
    ])


if __name__ == "__main__":
    try:
        run_application()
    except KeyboardInterrupt:
        pass
