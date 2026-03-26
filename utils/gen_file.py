import os
import random
import uuid

RUSSIAN_LETTERS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
TARGET_WORD = "житель"

output_dir = "./test/files"
os.makedirs(output_dir, exist_ok=True)

def generate_random_word(min_len=3, max_len=10):
    """Генерирует случайную последовательность букв (псевдо-слово)"""
    length = random.randint(min_len, max_len)
    return "".join(random.choice(RUSSIAN_LETTERS) for _ in range(length))

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
            words_in_line = [generate_random_word() for _ in range(random.randint(10, 30))]

            # С шансом 20% подмешиваем в строку наше целевое слово в разных формах
            if random.random() < 0.2:
                forms = ["житель", "жителем", "жители", "жителей", "жителя"]
                words_in_line.insert(random.randint(0, len(words_in_line)), random.choice(forms))

            line = " ".join(words_in_line) + "\n"
            f.write(line)

    print("Готово!")
    return file_name

if __name__ == "__main__":
    gen_file_env()