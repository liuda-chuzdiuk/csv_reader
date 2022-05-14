import csv
import codecs
from datetime import datetime, timedelta
from calendar import monthrange


def add_value_to_dict(dict_, key_, value_):
    if key_ in dict_:
        dict_[key_] += value_
    else:
        dict_[key_] = value_


def perform_month_value(key_, value_):
    date_from_month_year = datetime.strptime(key_, "%m.%Y")
    value_ /= monthrange(date_from_month_year.year, date_from_month_year.month)[1]
    value_ /= results_per_day
    return value_


with codecs.open("weather_data.csv", "r", encoding="utf-8") as weather_file:
    reader_obj = csv.DictReader(weather_file)
    average_wind_speed_per_month, wind_month = 0, ""
    average_min_temperature_per_month, cold_month = 0, ""
    min_temperature_per_day, cold_day = 0, ""
    average_max_temperature_per_month, warm_month = 0, ""
    average_max_temperature_per_day, warm_day = 0, ""
    max_amount_of_precipitation_per_week, precipitation_week = 0, ""

    wind_month_dict = {}
    temperature_month_dict = {}
    temperature_day_dict = {}
    precipitation_dict = {}

    results_per_day = 8

    for row in reader_obj:
        date_row = row["Местное время в Харькове (аэропорт)"]
        wind = float(row["Ff"])
        temperature = float(row["T"])

        date_object = datetime.strptime(date_row, "%d.%m.%Y %H:%M")
        date_ = date_object.date()
        month = f"{date_object.month}.{date_object.year}"
        week = date_object.isocalendar().week

        add_value_to_dict(temperature_day_dict, date_, temperature)
        add_value_to_dict(wind_month_dict, month, wind)
        add_value_to_dict(temperature_month_dict, month, temperature)

        try:
            precipitation = float(row["RRR"])
            add_value_to_dict(precipitation_dict, week, precipitation)
        except ValueError:
            pass

    for key, value in wind_month_dict.items():
        value = perform_month_value(key, value)

        if value > average_wind_speed_per_month:
            average_wind_speed_per_month = round(value, 2)
            wind_month = key

    for key, value in temperature_month_dict.items():
        value = perform_month_value(key, value)
        if value > average_max_temperature_per_month:
            average_max_temperature_per_month = round(value, 2)
            warm_month = key
        if value < average_min_temperature_per_month:
            average_min_temperature_per_month = round(value, 2)
            cold_month = key

    for key, value in temperature_day_dict.items():
        value /= results_per_day
        if value > average_max_temperature_per_day:
            average_max_temperature_per_day = round(value, 2)
            warm_day = key
        if value < min_temperature_per_day:
            min_temperature_per_day = round(value, 2)
            cold_day = key

    for key, value in precipitation_dict.items():
        value /= results_per_day
        if value > max_amount_of_precipitation_per_week:
            max_amount_of_precipitation_per_week = round(value, 2)
            precipitation_week = key

    first_day_of_rainy_week = datetime.strptime(f'{2016}-W{int(precipitation_week) - 1}-1', "%Y-W%W-%w").date()
    last_day_of_rainy_week = first_day_of_rainy_week + timedelta(days=6.9)


report = f"1. The windiest month in Kharkiv was {wind_month} with average wind speed " \
         f"{average_wind_speed_per_month} (meters per second).\n" \
         f"2. The coldest month in Kharkiv was {cold_month} with average temperature " \
         f"{average_min_temperature_per_month} (degrees Celsius).\n" \
         f"3. The coldest day in Kharkiv was {cold_day} with average temperature " \
         f"{min_temperature_per_day} (degrees Celsius).\n" \
         f"4. The warmest month in Kharkiv was {warm_month} with average temperature " \
         f"{average_max_temperature_per_month} (degrees Celsius).\n" \
         f"5. The warmest day in Kharkiv was {warm_day} with average temperature " \
         f"{average_max_temperature_per_day} (degrees Celsius).\n" \
         f"6. The rainiest week in Kharkiv was in period from {first_day_of_rainy_week} to {last_day_of_rainy_week} " \
         f"and amount of precipitation was {max_amount_of_precipitation_per_week} (millimeters)."

print(report)
