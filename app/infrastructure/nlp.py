import re
import pymorphy3
from openpyxl import Workbook


def generate_word_statistics(input_filepath: str, output_filepath: str, target_lemma: str = "житель"):
    """
    Анализирует текст построчно и собирает статистику только по конкретной словоформе (по умолчанию 'житель').
    """
    morph = pymorphy3.MorphAnalyzer()
    word_pattern = re.compile(r'[а-яА-ЯёЁa-zA-Z]+')

    stats = {"total": 0, "lines": {}}
    total_lines = 0


    with open(input_filepath, 'r', encoding='utf-8') as f:
        for line_idx, line in enumerate(f, start=1):
            total_lines = line_idx

            words = word_pattern.findall(line)

            for word in words:
                word_lower = word.lower()

                # Получаем нормальную форму слова
                lemma = morph.parse(word_lower)[0].normal_form

                if lemma != target_lemma:
                    continue

                stats[lemma]["total"] += 1
                stats[lemma]["lines"][line_idx] = stats["lines"].get(line_idx, 0) + 1

    print(f"Анализ завершен. Всего строк содержащих словоформу: {total_lines}.")
    print(f"Формируем Excel файл: {output_filepath}")

    wb = Workbook(write_only=True)
    ws = wb.create_sheet(title="Статистика слов")
    ws.append(["Словоформа", "Кол-во во всём документе", "Кол-во в каждой строке"])

    total_count = stats["total"]

    # Генерируем массив строк
    line_counts = (
        str(stats["lines"].get(i, 0)) for i in range(1, total_lines + 1)
    )
    line_counts_str = ",".join(line_counts)

    # Добавляем единственную строку с результатами в Excel
    ws.append([target_lemma, total_count, line_counts_str])

    wb.save(output_filepath)
    print("Файл успешно сохранен!")

