import tkinter as tk
from tkinter import messagebox
from urllib import *
import requests

# Function to fetch weather data
def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    api_key = "f372604a7d6438efe6923c7fe935a72c"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            messagebox.showerror("Error", data["message"].capitalize())
            return

        # Extract weather details
        weather = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        # Update the labels
        weather_label.config(text=f"Weather: {weather}")
        temp_label.config(text=f"Temperature: {temp}°C")
        humidity_label.config(text=f"Humidity: {humidity}%")
        wind_label.config(text=f"Wind Speed: {wind_speed} m/s")
    except Exception as e:
        messagebox.showerror("Error", f"Unable to fetch data: {e}")

# Create the main window
app = tk.Tk()
app.title("Weather App")
app.geometry("300x300")

# Input field for city name
city_entry = tk.Entry(app, font=("Arial", 14))
city_entry.pack(pady=10)
city_entry.insert(0, "Enter city name")

# Search button
search_button = tk.Button(app, text="Get Weather", command=get_weather, font=("Arial", 14))
search_button.pack(pady=10)

# Labels to display weather info
weather_label = tk.Label(app, text="Weather: --", font=("Arial", 12))
weather_label.pack(pady=5)

temp_label = tk.Label(app, text="Temperature: --°C", font=("Arial", 12))
temp_label.pack(pady=5)

humidity_label = tk.Label(app, text="Humidity: --%", font=("Arial", 12))
humidity_label.pack(pady=5)

wind_label = tk.Label(app, text="Wind Speed: -- m/s", font=("Arial", 12))
wind_label.pack(pady=5)

# Run the app
app.mainloop()
