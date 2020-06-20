from cs50 import get_string
from sys import argv
import sys


def main():
    
    if len(argv) != 2:  # перевірка скільки аргументів в запуску програми користувача
        print(f"Usage: python {argv[0]} dictionary")
        sys.exit(1)
        
    # списки (треба почитати який саме)
    words = set()
    text = list()
    
    # відкриваємо файл для читання
    file = open(argv[1], "r")
    if not file:  # перевірка чи добре читається файл
        print(f"Could not open {argv[1]}")
        sys.exit(1)
    
    # запис слів зі словника до вордс
    for line in file:
        words.add(line.rstrip("\n"))
    file.close()

    print("What massage would you like to censor?")
    c = get_string("")  # для вводу користувача
    text = c.split()  # створення списку зі рядка

    # перевірка 
    for i in text:
        if i.lower() in words:
            print("*"*len(i), end=" ")
        else:
            print(i, end=" ")
        
    print()    
            

if __name__ == "__main__":
    main()