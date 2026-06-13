import os
import requests
import smtplib
from email.message import EmailMessage

# =========================
# CONFIG (FROM GITHUB SECRETS)
# =========================
API_KEY = os.environ.get("API_KEY")
CITY = "Thiruvananthapuram"

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

# =========================
# GET WEATHER DATA
# =========================
url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(url)
data = response.json()

print("API Response:", data)

# =========================
# CHECK DATA VALIDITY
# =========================
if data.get("cod") != 200:
    print("API Error:", data)
else:
    temperature = data["main"]["temp"]
    weather = data["weather"][0]["main"]

    print("Temperature:", temperature)
    print("Weather:", weather)

    # =========================
    # ALERT CONDITION
    # =========================
    if temperature > 25 or weather.lower() == "rain":

        print("Alert triggered!")

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()

            server.login(EMAIL, PASSWORD)

            msg = EmailMessage()
            msg["Subject"] = "Weather Alert!"
            msg["From"] = EMAIL
            msg["To"] = EMAIL

            msg.set_content(
                f"Weather Alert!\n\n"
                f"City: {CITY}\n"
                f"Temperature: {temperature}°C\n"
                f"Weather: {weather}"
            )

            server.send_message(msg)

            print("Email sent successfully!")

        except Exception as e:
            print("Failed to send email:", e)

        finally:
            server.quit()

    else:
        print("No alert needed. Weather is normal.")
   
