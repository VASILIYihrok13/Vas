from cs50 import get_string
from sys import argv
import sys


def main():
    # перевірка чи є всі символи ключа користувача буквами
    if len(argv) is not 2 or argv[1].isalpha() == False:
        print(f"Usage:{argv[0]} key")
        sys.exit(1)

    text = get_string("plaintext: ")  # текст користувача для шифру
    print("ciphertext: ", end="")

    cipher(text)
    print()


def cipher(text):
    c = 0
    # шифруємо текст
    for i in range(len(text)):
        if text[i].isalpha():

            key = ord(argv[1][c].upper()) - 65  # ключ

            if text[i].islower():
                print(f"{ chr((ord(text[i]) - 97 + key )%26 + 97)}", end="")
            else:
                print(f"{ chr((ord(text[i]) - 65 + key)%26 + 65)}", end="")

            c = (c+1) % len(argv[1])  # переходимо на наступну букву ключа

        else:
            print(f"{text[i]}", end="")


if __name__ == "__main__":
    main()