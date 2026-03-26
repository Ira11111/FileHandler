import os
import random
import uuid

# Наш набор фраз для генерации
phrases = [
    "Просто текст без нужного слова.\n",
    "Один местный житель пошел в магазин.\n",
    "Жители и только ЖИТЕЛИ! Много жителей.\n",
    "Какой-то случайный лог системы...\n",
    "Я поговорил с жителем соседнего дома.\n"
]

output_dir = "./test"
os.makedirs(output_dir, exist_ok=True)

string_count = int(os.getenv("COUNT", 20_000))
print(f"Генерируем файл на {string_count} строк. Подождите пару секунд...")

# Открываем файл на запись
with open(f"./test/{string_count}_{uuid.uuid4()}.txt", "w", encoding="utf-8") as f:
    for _ in range(string_count):
        f.write(random.choice(phrases))

print("Готово!")