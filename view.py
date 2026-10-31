import tkinter as tk
from tkinter import messagebox


class WeatherView:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard: Clock & Weather")
        self.root.geometry("450x600")
        self.root.configure(bg="#1E293B")
        self.root.resizable(False, False)

        # --- TOP TAB SWITCHER NAVBAR ---
        self.tab_frame = tk.Frame(self.root, bg="#0F172A")
        self.tab_frame.pack(fill="x", pady=(0, 15))

        self.clock_tab_btn = tk.Button(
            self.tab_frame, text="⏰ Clock", font=("Helvetica", 12, "bold"),
            bg="#334155", fg="white", bd=0, relief="flat", padx=20, pady=10,
            cursor="hand2", command=self.show_clock_view
        )
        self.clock_tab_btn.pack(side="left", expand=True, fill="x")

        self.weather_tab_btn = tk.Button(
            self.tab_frame, text="⛅ Weather", font=("Helvetica", 12, "bold"),
            bg="#1E293B", fg="#94A3B8", bd=0, relief="flat", padx=20, pady=10,
            cursor="hand2", command=self.show_weather_view
        )
        self.weather_tab_btn.pack(side="left", expand=True, fill="x")

        # --- CONTAINER FOR DIFFERENT VIEWS ---
        self.container = tk.Frame(self.root, bg="#1E293B")
        self.container.pack(fill="both", expand=True, padx=20, pady=5)

        # ==================== CLOCK VIEW FRAME ====================
        self.clock_frame = tk.Frame(self.container, bg="#1E293B")

        # Timezone Search Sub-Area
        clock_search_frame = tk.Frame(self.clock_frame, bg="#1E293B")
        clock_search_frame.pack(pady=(10, 5))

        self.clock_city_entry = tk.Entry(clock_search_frame, font=("Helvetica", 12), width=16, justify="center")
        self.clock_city_entry.pack(side="left", padx=5, ipady=2)
        self.clock_city_entry.insert(0, "Local (System)")

        self.clock_search_btn = tk.Button(clock_search_frame, text="Set Timezone", font=("Helvetica", 9, "bold"),
                                          bg="#00E5FF", fg="#0F172A", padx=6, pady=2, cursor="hand2")
        self.clock_search_btn.pack(side="left", padx=5)

        self.timezone_label = tk.Label(
            self.clock_frame, text="🌍 Timezone: Local System Time", font=("Helvetica", 11), bg="#1E293B", fg="#38BDF8"
        )
        self.timezone_label.pack(pady=(0, 15))

        self.time_label = tk.Label(
            self.clock_frame, text="00:00:00", font=("Helvetica", 48, "bold"), bg="#1E293B", fg="#00E5FF"
        )
        self.time_label.pack(pady=(10, 5))

        self.date_label = tk.Label(
            self.clock_frame, text="Loading date...", font=("Helvetica", 14), bg="#1E293B", fg="#94A3B8"
        )
        self.date_label.pack(pady=5)

        # ==================== WEATHER VIEW FRAME ====================
        self.weather_frame = tk.Frame(self.container, bg="#1E293B")

        search_sub_frame = tk.Frame(self.weather_frame, bg="#1E293B")
        search_sub_frame.pack(pady=(10, 10))

        self.city_entry = tk.Entry(search_sub_frame, font=("Helvetica", 13), width=18, justify="center")
        self.city_entry.pack(side="left", padx=5, ipady=3)
        self.city_entry.insert(0, "London")

        self.search_btn = tk.Button(search_sub_frame, text="Search", font=("Helvetica", 10, "bold"),
                                    bg="#3B82F6", fg="white", padx=8, pady=2, cursor="hand2")
        self.search_btn.pack(side="left", padx=5)

        self.city_label = tk.Label(self.weather_frame, text="", font=("Helvetica", 18, "bold"), bg="#1E293B", fg="white")
        self.city_label.pack(pady=(10, 0))

        self.emoji_label = tk.Label(self.weather_frame, text="🌍", font=("Segoe UI Emoji", 45), bg="#1E293B", fg="white")
        self.emoji_label.pack(pady=0)

        self.temp_label = tk.Label(self.weather_frame, text="--°C", font=("Helvetica", 36, "bold"), bg="#1E293B", fg="white")
        self.temp_label.pack(pady=0)

        self.desc_label = tk.Label(self.weather_frame, text="Enter a city to start", font=("Helvetica", 12), bg="#1E293B", fg="#94A3B8")
        self.desc_label.pack(pady=5)

        self.details_frame = tk.Frame(self.weather_frame, bg="#1E293B")
        self.details_frame.pack(pady=10)

        self.humidity_label = tk.Label(self.details_frame, text="💧 Humidity: --%", font=("Helvetica", 11), bg="#1E293B", fg="white")
        self.humidity_label.pack(side="left", padx=10)

        self.wind_label = tk.Label(self.details_frame, text="💨 Wind: -- km/h", font=("Helvetica", 11), bg="#1E293B", fg="white")
        self.wind_label.pack(side="left", padx=10)

        self.show_clock_view()

    def show_clock_view(self):
        self.clock_tab_btn.config(bg="#334155", fg="white")
        self.weather_tab_btn.config(bg="#1E293B", fg="#94A3B8")
        self.weather_frame.pack_forget()
        self.clock_frame.pack(fill="both", expand=True)

    def show_weather_view(self):
        self.weather_tab_btn.config(bg="#334155", fg="white")
        self.clock_tab_btn.config(bg="#1E293B", fg="#94A3B8")
        self.clock_frame.pack_forget()
        self.weather_frame.pack(fill="both", expand=True)

    def bind_search(self, callback):
        self.search_btn.config(command=lambda: callback(self.city_entry.get()))
        self.root.bind('<Return>', lambda event: callback(self.city_entry.get()))

    def bind_clock_search(self, callback):
        self.clock_search_btn.config(command=lambda: callback(self.clock_city_entry.get()))
        # Note: Enter key handles active tab search context cleanly

    def update_clock_display(self, time_str, date_str, tz_name):
        self.time_label.config(text=time_str)
        self.date_label.config(text=date_str)
        self.timezone_label.config(text=f"🌍 Timezone: {tz_name}")

    def update_display(self, data):
        self.city_label.config(text=data["city"])
        self.emoji_label.config(text=data["emoji"])
        self.temp_label.config(text=f"{data['temp']}°C")
        self.desc_label.config(text=f"{data['desc']} | Feels like {data['feels_like']}°C")
        self.humidity_label.config(text=f"💧 Humidity: {data['humidity']}%")
        self.wind_label.config(text=f"💨 Wind: {data['wind_speed']} km/h")

    def show_error(self, message):
        messagebox.showerror("Dashboard Error", message)