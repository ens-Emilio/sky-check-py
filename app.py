import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading
import config
import weather_service

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌤️ Previsão do Tempo")
        self.root.geometry("400x550")
        self.root.resizable(False, False)

        # Configuração de Cores (Polimento Fase 5)
        self.bg_color = "#2c3e50"
        self.fg_color = "#ecf0f1"
        self.accent_color = "#3498db"
        
        self.root.configure(bg=self.bg_color)
        
        # Estilo do ttk
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=("Helvetica", 12))
        self.style.configure("Main.TLabel", font=("Helvetica", 14, "bold"))
        self.style.configure("Temp.TLabel", font=("Helvetica", 40, "bold"))
        self.style.configure("Desc.TLabel", font=("Helvetica", 16, "italic"))
        self.style.configure("Search.TButton", padding=5, font=("Helvetica", 10, "bold"))

        self.setup_ui()

    def setup_ui(self):
        # Frame de Busca
        search_frame = tk.Frame(self.root, bg=self.bg_color, pady=20)
        search_frame.pack(fill="x")

        self.city_entry = ttk.Entry(search_frame, font=("Helvetica", 14), width=20)
        self.city_entry.pack(side="left", padx=(20, 10))
        self.city_entry.bind("<Return>", lambda event: self.start_search())

        self.search_btn = ttk.Button(search_frame, text="Buscar", style="Search.TButton", command=self.start_search)
        self.search_btn.pack(side="left")

        # Loading Progress Bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", mode="indeterminate", length=360)
        # Oculto por padrão

        # Frame de Exibição de Dados
        self.data_frame = tk.Frame(self.root, bg=self.bg_color)
        
        self.city_label = ttk.Label(self.data_frame, text="", style="Main.TLabel")
        self.city_label.pack(pady=(20, 0))

        self.icon_label = tk.Label(self.data_frame, bg=self.bg_color)
        self.icon_label.pack()

        self.temp_label = ttk.Label(self.data_frame, text="", style="Temp.TLabel")
        self.temp_label.pack()

        self.desc_label = ttk.Label(self.data_frame, text="", style="Desc.TLabel")
        self.desc_label.pack(pady=(0, 20))

        # Detalhes (Umidade, Vento, Sensação)
        self.details_frame = tk.Frame(self.data_frame, bg=self.bg_color)
        self.details_frame.pack(fill="x", padx=40)

        self.humidity_label = ttk.Label(self.details_frame, text="")
        self.humidity_label.grid(row=0, column=0, sticky="w", pady=5)

        self.wind_label = ttk.Label(self.details_frame, text="")
        self.wind_label.grid(row=0, column=1, sticky="e", pady=5)

        self.feels_label = ttk.Label(self.details_frame, text="")
        self.feels_label.grid(row=1, column=0, sticky="w", pady=5)

    def start_search(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Aviso", "Por favor, digite o nome de uma cidade.")
            return

        # Bloquear UI e mostrar loading
        self.search_btn.config(state="disabled")
        self.progress.pack(pady=5)
        self.progress.start()
        
        # Iniciar busca em thread separada
        threading.Thread(target=self.search_weather, args=(city,), daemon=True).start()

    def search_weather(self, city):
        try:
            raw_data = weather_service.get_weather(city)
            parsed_data = weather_service.parse_weather(raw_data)
            
            # Baixar ícone (usando PhotoImage nativo para evitar dependência do PIL)
            icon_url = config.ICON_URL.format(parsed_data["icon_code"])
            icon_response = requests.get(icon_url)
            photo = tk.PhotoImage(data=icon_response.content)

            self.root.after(0, self.update_ui, parsed_data, photo)
        except Exception as e:
            self.root.after(0, self.show_error, str(e))

    def update_ui(self, data, photo):
        self.data_frame.pack(fill="both", expand=True)
        
        self.city_label.config(text=f"{data['city']}, {data['country']}")
        self.icon_label.config(image=photo)
        self.icon_label.image = photo # Manter referência
        self.temp_label.config(text=f"{data['temp']}°C")
        self.desc_label.config(text=data['description'])
        
        self.humidity_label.config(text=f"💧 Umidade: {data['humidity']}%")
        self.wind_label.config(text=f"🌬️ Vento: {data['wind_speed']} km/h")
        self.feels_label.config(text=f"🌡️ Sensação: {data['feels_like']}°C")

        # Desbloquear UI
        self.stop_loading()

    def show_error(self, message):
        messagebox.showerror("Erro", message)
        self.stop_loading()

    def stop_loading(self):
        self.progress.stop()
        self.progress.pack_forget()
        self.search_btn.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
