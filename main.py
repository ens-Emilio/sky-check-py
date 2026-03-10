import tkinter as tk
from app import WeatherApp

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
