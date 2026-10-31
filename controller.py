from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class WeatherController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Clock timezone state (None = local system time)
        self.active_timezone = None
        self.timezone_display_name = "Local System Time"

        # Bind event triggers
        self.view.bind_search(self.handle_weather_search)
        self.view.bind_clock_search(self.handle_clock_search)

        # Start ticking the clock loop
        self.update_clock()

        # Fetch initial weather data for default weather view
        self.handle_weather_search(self.view.city_entry.get())

    def update_clock(self):
        """Ticks every 1 second to update the clock view using the active timezone."""
        try:
            if self.active_timezone:
                now = datetime.now(self.active_timezone)
            else:
                now = datetime.now()  # Fallback to local system clock

            current_time = now.strftime("%H:%M:%S")
            current_date = now.strftime("%A, %B %d, %Y")
        except Exception:
            current_time = "00:00:00"
            current_date = "Timezone Error"

        # Send formatted strings to the view
        self.view.update_clock_display(current_time, current_date, self.timezone_display_name)

        # Loop again in 1000ms (1 second)
        self.view.root.after(1000, self.update_clock)

    def handle_clock_search(self, city_name):
        city_name = city_name.strip()
        if not city_name or city_name.lower() in ["local", "local (system)"]:
            self.active_timezone = None
            self.timezone_display_name = "Local System Time"
            return

        # Query the model to find coordinates and timezone data
        success, result = self.model.fetch_weather(city_name)

        if success and "timezone" in result:
            tz_str = result["timezone"]
            try:
                self.active_timezone = ZoneInfo(tz_str)
                self.timezone_display_name = f"{result['city']} ({tz_str})"
            except ZoneInfoNotFoundError:
                self.view.show_error(f"Timezone '{tz_str}' is not recognized.")
        else:
            self.view.show_error(f"Could not find timezone info for '{city_name}'.")

    def handle_weather_search(self, city_name):
        if not city_name or city_name.strip() == "":
            self.view.show_error("Please enter a valid city name!")
            return

        success, result = self.model.fetch_weather(city_name.strip())

        if success:
            self.view.update_display(result)
        else:
            self.view.show_error(result)