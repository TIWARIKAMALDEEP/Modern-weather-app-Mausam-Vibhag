import customtkinter as ctk
import requests
from PIL import Image, ImageTk
from io import BytesIO
import config

ctk.set_appearance_mode("dark")

# ------------------ CONFIG ------------------
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

BG_COLOR = "#380505"
CARD_COLOR = "#a57171"
ACCENT = "#00b4d8"

unit_mode = "metric"  # default Celsius

# ------------------ FUNCTIONS ------------------

def get_current_weather(city):
    try:
        params = {
            "q": city,
            "appid": config.API_KEY,
            "units": unit_mode
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data["cod"] != 200:
            return None

        return data

    except:
        return None


def get_forecast(city):
    try:
        params = {
            "q": city,
            "appid": config.API_KEY,
            "units": unit_mode
        }
        response = requests.get(FORECAST_URL, params=params)
        data = response.json()

        if data["cod"] != "200":
            return None

        return data["list"][:5]

    except:
        return None


def get_icon(icon_code):
    url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    response = requests.get(url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    return ImageTk.PhotoImage(img)


def update_ui():
    city = city_entry.get()

    weather = get_current_weather(city)
    forecast = get_forecast(city)

    if weather is None:
        status_label.configure(text="❌ City not found")
        return

    status_label.configure(text="")

    temp = weather["main"]["temp"]
    desc = weather["weather"][0]["description"].title()
    humidity = weather["main"]["humidity"]
    wind = weather["wind"]["speed"]
    pressure = weather["main"]["pressure"]
    temp_min = weather["main"]["temp_min"]
    temp_max = weather["main"]["temp_max"]
    icon_code = weather["weather"][0]["icon"]

    icon_img = get_icon(icon_code)
    icon_label.configure(image=icon_img)
    icon_label.image = icon_img

    unit_symbol = "°C" if unit_mode == "metric" else "°F"

    temp_label.configure(text=f"{temp}{unit_symbol}")
    desc_label.configure(text=desc)
    details_label.configure(
        text=f"Humidity: {humidity}%\nWind: {wind}\nPressure: {pressure}\nMin: {temp_min}{unit_symbol} | Max: {temp_max}{unit_symbol}"
    )

    # Forecast
    for widget in forecast_frame.winfo_children():
        widget.destroy()

    if forecast:
        for item in forecast:
            frame = ctk.CTkFrame(forecast_frame, fg_color=CARD_COLOR, corner_radius=10)
            frame.pack(pady=5, padx=10, fill="x")

            t = item["main"]["temp"]
            d = item["weather"][0]["description"]
            time = item["dt_txt"].split(" ")[0]

            ctk.CTkLabel(frame, text=f"{time} | {t}{unit_symbol} | {d}").pack(pady=5)


def toggle_unit():
    global unit_mode
    unit_mode = "imperial" if unit_mode == "metric" else "metric"
    update_ui()


# ------------------ UI ------------------

# ------------------ UI ------------------

app = ctk.CTk()
app.title("MAUSAM VIBHAG")
app.geometry("500x700")
app.configure(fg_color="#0f172a")  # deep dark blue

# -------- HEADER (Gradient style feel) --------
header_frame = ctk.CTkFrame(app, fg_color="#111827", corner_radius=0)
header_frame.pack(fill="x")

header = ctk.CTkLabel(
    header_frame,
    text="🌤️ Mausam Vibhag",
    font=("Poppins", 26, "bold"),
    text_color="#00b4d8"
)
header.pack(pady=15)

# -------- SEARCH BAR --------
search_frame = ctk.CTkFrame(app, fg_color="transparent")
search_frame.pack(pady=10)

city_entry = ctk.CTkEntry(
    search_frame,
    placeholder_text="Enter City...",
    width=260,
    height=40,
    corner_radius=20,
    fg_color="#1e293b"
)
city_entry.pack(side="left", padx=5)
city_entry.insert(0, "Delhi")

search_btn = ctk.CTkButton(
    search_frame,
    text="🔍",
    width=50,
    height=40,
    corner_radius=20,
    fg_color="#00b4d8",
    hover_color="#0096c7",
    command=update_ui
)
search_btn.pack(side="left", padx=5)

# -------- UNIT TOGGLE --------
toggle_btn = ctk.CTkButton(
    app,
    text="🌡 Toggle °C / °F",
    fg_color="#1e293b",
    hover_color="#334155",
    command=toggle_unit
)
toggle_btn.pack(pady=5)

status_label = ctk.CTkLabel(app, text="", text_color="red")
status_label.pack()

# -------- MAIN WEATHER CARD (Glass Effect) --------
card = ctk.CTkFrame(
    app,
    fg_color="#1e293b",
    corner_radius=25
)
card.pack(pady=20, padx=20, fill="both")

icon_label = ctk.CTkLabel(card, text="")
icon_label.pack(pady=10)

temp_label = ctk.CTkLabel(
    card,
    text="--",
    font=("Poppins", 48, "bold"),
    text_color="#00b4d8"
)
temp_label.pack()

desc_label = ctk.CTkLabel(
    card,
    text="Weather",
    font=("Poppins", 18)
)
desc_label.pack()

details_label = ctk.CTkLabel(
    card,
    text="Details...",
    font=("Poppins", 14),
    justify="center"
)
details_label.pack(pady=10)

# -------- FORECAST TITLE --------
forecast_title = ctk.CTkLabel(
    app,
    text="📅 Forecast",
    font=("Poppins", 20, "bold"),
    text_color="#00b4d8"
)
forecast_title.pack(pady=10)

# -------- SCROLLABLE FORECAST --------
forecast_frame = ctk.CTkScrollableFrame(
    app,
    width=450,
    height=200,
    fg_color="transparent"
)
forecast_frame.pack(pady=10)

# -------- FOOTER --------
footer = ctk.CTkLabel(
    app,
    text="Built with ❤️ using Python",
    font=("Poppins", 12),
    text_color="#64748b"
)
footer.pack(pady=10)

# Initial load
update_ui()

app.mainloop()