# Задача 9
# Программная реализация алгоритма Хаффмана

import heapq
import math
from itertools import count


def build_tree(freq):
    if not freq:
        raise ValueError("Словарь частот пуст")

    heap = []
    order = count()

    for char, frequency in sorted(freq.items()):
        if frequency <= 0:
            raise ValueError("Частоты должны быть положительными")
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


def encode(text, codes):
    return "".join(codes[char] for char in text)


def decode(bits, tree):
    if any(bit not in "01" for bit in bits):
        raise ValueError("Недопустимый бит")

    if isinstance(tree, str):
        if any(bit != "0" for bit in bits):
            raise ValueError("Неверный код")
        return tree * len(bits)

    result = []
    node = tree

    for bit in bits:
        node = node[0] if bit == "0" else node[1]

        if isinstance(node, str):
            result.append(node)
            node = tree

    if node is not tree:
        raise ValueError("Неполное кодовое слово")

    return "".join(result)


def calculate_metrics(freq, codes):
    total = sum(freq.values())
    H = 0
    L = 0

    for char, frequency in freq.items():
        p = frequency / total
        H -= p * math.log2(p)
        L += p * len(codes[char])

    eta = H / L if L else 0

    return H, L, eta


freq = {
    "A": 5,
    "B": 2,
    "C": 3,
    "D": 1,
    "E": 1
}

tree = build_tree(freq)
codes = build_codes(tree)

print("Таблица кодовых слов:")
print("Символ | Частота | Код")

for char in sorted(freq):
    print(f"{char:^6} | {freq[char]:^7} | {codes[char]}")

H, L, eta = calculate_metrics(freq, codes)

print(f"\nЭнтропия H(X): {H:.4f}")
print(f"Средняя длина L: {L:.4f}")
print(f"Эффективность η: {eta * 100:.2f}%")

text = str(input("/nИсходный текст: ")).upper
encoded = encode(text, codes)
decoded = decode(encoded, tree)

print("Закодированный:", encoded)
print("Декодированный:", decoded)
print("Проверка:", decoded == text)

assert decoded == text

# Случай одного уникального символа
single_tree = build_tree({"A": 10})
single_codes = build_codes(single_tree)

single_text = "AAAAAA"
single_bits = encode(single_text, single_codes)

print("\nОдин уникальный символ:")
print("Код:", single_codes)
print("Закодировано:", single_bits)
print("Декодировано:", decode(single_bits, single_tree))

assert single_codes["A"] == "0"
assert decode(single_bits, single_tree) == single_text
