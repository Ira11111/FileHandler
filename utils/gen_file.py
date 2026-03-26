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

def gen_file_env():
    return gen_file(int(os.getenv("COUNT", 20_000)))

def gen_file(string_count: int) -> str:
    print(f"Генерируем файл на {string_count} строк. Подождите пару секунд...")

    file_name = f"./test/files/{string_count}_{uuid.uuid4()}.txt"
    # Открываем файл на запись
    with open(file_name, "w", encoding="utf-8") as f:
        for _ in range(string_count):
            f.write(random.choice(phrases))

    print("Готово!")
    return file_name

if __name__ == "__main__":
    gen_file_env()