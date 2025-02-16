import webbrowser
import time

def open_browser():
    webbrowser.get('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s').open('http://127.0.0.1:8000')
    time.sleep(2)  # Espera 5 segundos

if __name__ == "__main__":
    open_browser()