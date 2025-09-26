import csv
import re
from collections import defaultdict

# --- Читаем исходный файл ---
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

header = contacts_list[0]
data = contacts_list[1:]

cleaned = []

for row in data:
    # 1️⃣ Приводим ФИО к формату: Фамилия, Имя, Отчество
    fio = " ".join(row[:3]).split()
    lastname  = fio[0] if len(fio) > 0 else ""
    firstname = fio[1] if len(fio) > 1 else ""
    surname   = fio[2] if len(fio) > 2 else ""

    organization = row[3]
    position     = row[4]
    phone        = row[5]
    email        = row[6]

    # 2️⃣ Приводим телефоны к формату +7(999)999-99-99 (доб.XXXX)
    phone_pattern = re.compile(
        r"(?:\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(?:\s*\(?(доб\.?)\s*(\d+)\)?)?"
    )
    phone = phone_pattern.sub(
        lambda m: f"+7({m.group(1)}){m.group(2)}-{m.group(3)}-{m.group(4)}"
                  + (f" {m.group(5)}{m.group(6)}" if m.group(5) else ""),
        phone
    )

    cleaned.append([lastname, firstname, surname, organization, position, phone, email])

# 3️⃣ Объединяем дубли (ключ — Фамилия+Имя)
merged = defaultdict(lambda: ["", "", "", "", "", "", ""])

for c in cleaned:
    key = (c[0], c[1])  # Фамилия + Имя
    for i, val in enumerate(c):
        if val and not merged[key][i]:
            merged[key][i] = val

result = [header] + list(merged.values())

# --- Записываем итог ---
with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerows(result)

print("Готово! Создан файл phonebook.csv")
