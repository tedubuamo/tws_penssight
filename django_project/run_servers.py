import subprocess
import threading

def run_django():
    subprocess.run(["python", "manage.py", "runserver", "0.0.0.0:8000"])

def run_fastapi():
    subprocess.run(["uvicorn", "my_app.fastapi:app", "--host", "0.0.0.0", "--port", "8001"])

# Jalankan dalam thread terpisah
django_thread = threading.Thread(target=run_django)
fastapi_thread = threading.Thread(target=run_fastapi)

django_thread.start()
fastapi_thread.start()

# Tunggu keduanya selesai
django_thread.join()
fastapi_thread.join()
