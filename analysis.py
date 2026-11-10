import pandas as pd
import json
import matplotlib
matplotlib.use("Agg") # Будем сохранять в .png формате
import matplotlib.pyplot as plt
from datetime import datetime # Название снимка = дата его создания
import os # Для создания папки, если её нет
os.makedirs("static/analysis", exist_ok=True)
import numpy as np

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
    how="left"
)

with open("data/statuses.json", encoding="utf-8") as f:
    statuses = json.load(f)
statuses_df = pd.DataFrame(statuses)

statuses_df = statuses_df.rename(columns={"id": "status_id"})
merged = merged.merge(
    statuses_df,
    left_on="status",
    right_on="status_id",
    how="left"
)
'''
Создаём "объединённый" DataFrame, ставя в соответствие колонке "district_id"
из csv файла колонку "id из districts_df.
'''

by_district = merged.groupby("name").size().sort_values(ascending=False)
by_status = merged.groupby("status_name").size()
'''
Нахождение количества запросов по округам
'''
date_str = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
output_dir = f"static/analysis/{date_str}"
os.makedirs(output_dir, exist_ok=True)

by_district.plot(kind="bar")
plt.xlabel("Округи")
plt.ylabel("Количество запросов")
plt.tight_layout()
plt.savefig(f"{output_dir}/reports_by_district.png")
plt.close()

by_status.plot(kind="pie", autopct="%1.1f%%")
plt.ylabel("")
plt.title("Доля сообщений по статусам")
plt.tight_layout()
plt.savefig(f"{output_dir}/statuses_pie.png")
plt.close()

merged["date"] = pd.to_datetime(merged["date"])
by_month = merged.groupby(merged["date"].dt.to_period("M")).size()

by_month.plot(kind="line", marker="o")
plt.xlabel("Месяц")
plt.ylabel("Количество сообщений")
plt.title("Динамика сообщений по месяцам")
plt.tight_layout()
plt.savefig(f"{output_dir}/dynamics_by_month.png")
plt.close()

merged["resolved_date"] = pd.to_datetime(merged["resolved_date"])
merged["days_to_resolve"] = (merged["resolved_date"] - merged["date"]).dt.days

days = merged["days_to_resolve"].dropna()

days.plot(kind="hist", bins=10, edgecolor="black")
plt.xlabel("Дней до устранения")
plt.ylabel("Количество сообщений")
plt.title("Распределение времени устранения")
plt.tight_layout()
plt.savefig(f"{output_dir}/resolution_time_hist.png")
plt.close()
'''
Сохраняем график в формате png, в названии которого дата и время,
когда он был создан
'''
'''
merge - склеиваем таблицы, строку рядом со строкой, но очерёдность вторых строк
определяется по сравнению с первой по данным колонок, в нашем случае id
'''
print("\n=== Статистика времени устранения ===")
if len(days) > 0:
    print(f"Устранено: {len(days)} из {len(merged)}")
    print(f"Среднее: {np.nanmean(days):.1f} дн.")
    print(f"Медиана: {np.nanmedian(days):.1f} дн.")
    print(f"Максимум: {np.nanmax(days):.0f} дн.")
else:
    print("Нет устранённых сообщений")