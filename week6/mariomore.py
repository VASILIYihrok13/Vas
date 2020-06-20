from cs50 import get_int

# отримуємо висоту таблиці від користувача
while True:
    height = get_int("Height: ")
    if height < 9 and height > 0:  # створюємо умови за умовами задачі
        break

# виводимо східці на екран
for i in range(height):
    print(" " * ((height - 1) - i), end="")  # end - не закінчувати рядок.
    print("#" * (i+1), end="")
    print("  ", end="")
    print("#" * (i+1))
    
