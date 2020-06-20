from cs50 import get_float

# створюємо головну програму


def main():
    while True:
        dolar = get_float("Change owed: ")  # отримуємо число від користувача
        if dolar > 0:
            break
    # Змінюємо центи в долари
    cent = round(dolar*100)
    changeOwed(cent)  # Виклик програми для розрахунку
   
# Програма яка буде розраховувати


def changeOwed(n):
    rest = n // 25  # кількість 25
    n %= 25

    rest += n // 10  # + 10-ok
    n %= 10

    rest += n // 5  # + 5-ok
    n %= 5

    rest += n // 1  # + 1-ok
    n %= 1

    print(rest) 


# Виклик головної фунції
if __name__ == "__main__":
    main()
