"""Predict how many customers to expect, using the saved model.

    python predict.py Saturday 31 0
    python predict.py Monday 14 12 --holiday
"""
import argparse

import joblib
import pandas as pd

parser = argparse.ArgumentParser(description="How busy will Corner Café be?")
parser.add_argument("day", help="day of the week, like Saturday")
parser.add_argument("temp", type=float, help="forecast maximum temperature in °C")
parser.add_argument("rain", type=float, help="forecast rain in mm")
parser.add_argument("--holiday", action="store_true", help="it's a public holiday")
parser.add_argument("--school-holidays", action="store_true", help="it's the school holidays")
args = parser.parse_args()

model = joblib.load("customers_model.joblib")
day = pd.DataFrame([{"max_temp": args.temp, "rain_mm": args.rain, "public_holiday": int(args.holiday),
                     "school_holidays": int(args.school_holidays), "day_of_week": args.day.capitalize()}])
customers = model.predict(day)[0]
print(f"{args.day.capitalize()}, {args.temp:g}°C, {args.rain:g} mm rain: expect about {customers:.0f} customers")
print(f"That's about {customers * 0.8:.0f} coffees — roster {max(2, round(customers / 60))} baristas.")
