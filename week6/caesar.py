from cs50 import get_string
from sys import argv


def main():
   
   # перевірка чи всі символи в введеному ключі користувачем є цифрами
    if argv[1].isdigit() == False or len(argv) != 2:
        print(f"Usage:{argv[0]} key")
        return 1
    
    key = int(argv[1])  # Перетворення ключа з рядка в число
    
    text = get_string("plaintext: ")  # текст користувача для шифру
    print("ciphertext: ", end="")
    
    # шифруємо текст
    for i in range(len(text)):
        if text[i].isalpha():
            if text[i].islower():
                print(f"{ chr((ord(text[i]) - 97 + key)%26 + 97)}", end="")    
            else: 
                print(f"{ chr((ord(text[i]) - 65 + key)%26 + 65)}", end="")
        else:
            print(f"{text[i]}", end="")
    
    print()
    
           
if __name__ == "__main__":
    main()