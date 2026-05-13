import csv
import re
from pprint import pprint

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

header = contacts_list[0]
contacts_list = contacts_list[1:]

print("=== Исходные данные (первые 5 строк) ===")
pprint(contacts_list[:5])

def split_fio(row):
    fio_parts = " ".join(row[:3]).split()
    lastname  = fio_parts[0] if len(fio_parts) > 0 else ""
    firstname = fio_parts[1] if len(fio_parts) > 1 else ""
    surname   = fio_parts[2] if len(fio_parts) > 2 else ""


    return [lastname, firstname, surname] + row[3:]

contacts_list = [split_fio(row) for row in contacts_list]

print("\n=== После разбивки ФИО (первые 5 строк) ===")
pprint(contacts_list[:5])

def normalize_phone(phone):
    """Приводит телефон к формату +7(999)999-99-99 [доб.XXXX]"""
    if not phone:
        return phone

    ext_match = re.search(r"[дД]о[бп]\.?\s*(\d+)", phone)
    ext = ""
    if ext_match:
        ext = " доб." + ext_match.group(1)
        phone = phone[:ext_match.start()]

    digits = re.sub(r"\D", "", phone)

    if len(digits) == 11:
        digits = "7" + digits[1:]
    elif len(digits) == 10:
        digits = "7" + digits

    formatted = f"+7({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]}"

    return formatted + ext

contacts_list = [
    row[:5] + [normalize_phone(row[5])] + row[6:]
    for row in contacts_list
]

print("\n=== После нормализации телефонов (первые 5 строк) ===")
pprint(contacts_list[:5])


def merge_contacts(contacts):
    result = {}

    for row in contacts:
        key = (row[0], row[1])

        if key not in result:

            result[key] = row
        else:

            existing = result[key]
            merged = [

                existing[i] if existing[i] else row[i]
                for i in range(len(existing))
            ]
            result[key] = merged

    return list(result.values())

contacts_list = merge_contacts(contacts_list)

print("\n=== После объединения дублей ===")
pprint(contacts_list)

with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=",")
    datawriter.writerow(header)
    datawriter.writerows(contacts_list)

print("\n✅ Готово! Файл phonebook.csv сохранён.")