import pandas as pd
import json
import matplotlib
matplotlib.use("Agg") # Будем сохранять в .png формате
import matplotlib.pyplot as plt
from datetime import datetime # Название снимка = дата его создания
import os # Для создания папки, если её нет
os.makedirs("static/analysis", exist_ok=True)

'''
Сделали .use("Agg") перед импортом pyplot, чтобы по умолчанию
не выбралось создание отдельного окна
'''

reports = pd.read_csv("data/reports.csv")

with open("data/districts.json", encoding="utf-8") as f:
    districts = json.load(f)
districts_df = pd.DataFrame(districts)

merged = reports.merge(
    districts_df,
    left_on="district_id",
    right_on="id",
    how="left",
)
'''
Создаём "объединённый" DataFrame, ставя в соответствие колонке "district_id"
из csv файла колонку "id из districts_df.
'''

by_district = merged.groupby("name").size().sort_values(ascending=False)
'''
Нахождение количества запросов по округам
'''
date_str = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

by_district.plot(kind="bar")
plt.xlabel("Округи")
plt.ylabel("Количество запросов")
plt.tight_layout()
plt.savefig(f"static/analysis/reports_by_district_{date_str}.png")
plt.close()
print('Сохранено')
'''
Сохраняем график в формате png, в названии которого дата и время,
когда он был создан
'''