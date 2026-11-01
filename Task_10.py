# Задача 10
# Исследование реального текста

import heapq
import math
from collections import Counter
from itertools import count


def build_tree(freq):
    heap = []
    order = count()

    for char, frequency in sorted(freq.items()):
        heapq.heappush(heap, (frequency, next(order), char))

    while len(heap) > 1:
        f1, _, left = heapq.heappop(heap)
        f2, _, right = heapq.heappop(heap)

        heapq.heappush(
            heap, (f1 + f2, next(order), (left, right))
        )

    return heap[0][2]


def build_codes(tree):
    codes = {}

    def traverse(node, code):
        if isinstance(node, str):
            codes[node] = code or "0"
            return

        left, right = node
        traverse(left, code + "0")
        traverse(right, code + "1")

    traverse(tree, "")
    return codes


def calculate_metrics(freq, codes):
    total = sum(freq.values())
    H = 0
    L = 0

    for char, frequency in freq.items():
        p = frequency / total
        H -= p * math.log2(p)
        L += p * len(codes[char])

    eta = H / L if L else 0
    redundancy = 1 - eta

    return H, L, eta, redundancy


text = """
Информационная безопасность играет важную роль в современном
обществе. Каждый день люди используют компьютеры, смартфоны
и различные информационные системы для работы, обучения
и общения. При передаче данных необходимо обеспечивать
их конфиденциальность, целостность и доступность.
Одним из способов эффективного представления информации
является кодирование. Алгоритм Хаффмана позволяет уменьшить
объем данных благодаря использованию коротких кодов для
часто встречающихся символов и длинных кодов для редких.
Такой подход применяется при сжатии текстовой информации.
"""

# Пробелы и знаки препинания учитываются.
# Регистр не учитывается.
# Переводы строк заменяются пробелами.
text = " ".join(text.lower().split())

freq = dict(Counter(text))

tree = build_tree(freq)
codes = build_codes(tree)

print("Количество символов:", len(text))
print("Уникальных символов:", len(freq))

print("\nТаблица кодирования:")
print("Символ | Частота | Код")

for char in sorted(freq):
    print(f"{repr(char):8} | {freq[char]:7} | {codes[char]}")

H, L, eta, redundancy = calculate_metrics(freq, codes)

print(f"\nЭнтропия: {H:.4f} бит/символ")
print(f"Средняя длина: {L:.4f} бит/символ")
print(f"Эффективность: {eta * 100:.2f}%")
print(f"Избыточность: {redundancy * 100:.2f}%")

# Кодирование текста
encoded = "".join(codes[char] for char in text)

# Размер исходного текста UTF-8
original_bytes = len(text.encode("utf-8"))

# Размер битового потока
bit_count = len(encoded)
packed_bytes = (bit_count + 7) // 8

# Выравнивание последнего байта
padding_bits = packed_bytes * 8 - bit_count

# Служебные данные:
# 4 байта — количество символов текста
# 2 байта — количество уникальных символов
# Для каждого символа:
# UTF-8 символ + 1 байт длины кода + само кодовое слово
# Биты кодовых слов в таблице упакованы подряд

table_bits = 0

for char, code in codes.items():
    table_bits += len(char.encode("utf-8")) * 8
    table_bits += 8
    table_bits += len(code)

table_bytes = (table_bits + 7) // 8
header_bytes = 6
service_bytes = header_bytes + table_bytes

compressed_bytes = packed_bytes + service_bytes

saving = (1 - compressed_bytes / original_bytes) * 100

print("\nСравнение размеров:")
print("Исходный UTF-8:", original_bytes, "байт")
print("Битовый поток:", bit_count, "бит")
print("Упакованный поток:", packed_bytes, "байт")
print("Выравнивание:", padding_bits, "бит")
print("Таблица кодов:", table_bytes, "байт")
print("Заголовок:", header_bytes, "байт")
print("Служебные данные:", service_bytes, "байт")
print("Итоговый размер:", compressed_bytes, "байт")
print(f"Экономия: {saving:.2f}%")

if compressed_bytes < original_bytes:
    print("\nВывод: сжатие выгодно.")
else:
    print("\nВывод: сжатие невыгодно.")
