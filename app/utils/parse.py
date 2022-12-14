import csv
import os
from pathlib import Path


UTILS_PATH = Path(__file__).parent.resolve()
PATH_TO_FIXTURE = os.path.join(UTILS_PATH, "data", "city.csv")


def insert_data():
    """Функция для парсинга файла .csv и загрузки данных в БД."""
    data = []
    with open(PATH_TO_FIXTURE, "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            location = {
                "location": row["city"] or row["settlement"] or row["region"],
                "point": "POINT({lat} {lon})".format(lat=row["geo_lat"], lon=row["geo_lon"]),
            }
            data.append(location)

    return data
