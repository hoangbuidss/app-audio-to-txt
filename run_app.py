import os
import threading
import webbrowser

def open_browser():
    webbrowser.open_new("http://localhost:8501")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    os.system("streamlit run app.py --server.headless true")
