from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    words = []
    for line in a.split('\n'):  # функція спліт робить лист з кожним окремим елементом, який закінчується на \n
        if line in b.split('\n') and line not in words:
            words.append(line.rstrip("\n"))  # рстріп забирає \n з кожного елемента нового списку.

    return words


def sentences(a, b):
    """Return sentences in both a and b"""

    words = []
    a = sent_tokenize(a)  # токенізація тут розбиває на окремі речення текст може бути ще на слова
    b = sent_tokenize(b)
    for line in a:
        if line in b and line not in words:
            words.append(line)

    return words


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    words = []
    # довжина файлу відняти Н - це аби не брало до уваги останні символи які точно не підходять.
    
    for i in range(1 + len(a) - n):              
        subs = a[i:i+n]                              # змінна для переходу за умовами завдання по рядк
        if subs.isalpha() and subs in b:             # якщо всі символи в рядку є буквами і не має у нас в другому файлі
            if len(subs) == n and subs not in words: # довижина - нам потрібна така кількість яку вказав користувач і чи є в нашому списку
                words.append(subs)
    
    return words
