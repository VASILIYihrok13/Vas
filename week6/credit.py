from cs50 import get_int


def main():
    # отримаємо номер картки від користувача
    while True:
        card = get_int("Number: ")
        if card > 0:
            break
    
    fakecard, fakecard1, add, mult = card, (card // 10), 0, 0
    
    # Додаємо кожне наступне число починаючи з останнього
    while fakecard > 0:
        add += fakecard % 10
        fakecard //= 100
        
    # перемножуємо кожне друге число починаючи з передостаннього
    while fakecard1 > 0:
        if (2*(fakecard1 % 10) > 9):
            mult += (2*(fakecard1 % 10)) // 10
            mult += (2*(fakecard1 % 10)) % 10
        else:
            mult += 2*(fakecard1 % 10)
        fakecard1 //= 100
        
    # якщо карточка дійсна то викликаємо функцію аби побачити чи є вона в списку    
    if not (mult + add) % 10:
        credition(card)
    else:
        print("INVALID")
        

# фунція для перевірки декількох кредиток
def credition(c):
    if (c//10000000000000 == 34 or c//10000000000000 == 37):
        print("AMEX")
        return 0

    elif (c//100000000000000 == 51 or c//100000000000000 == 52 or c//100000000000000 == 53 or c//100000000000000 == 54 or c//100000000000000 == 55):
        print("MASTERCARD")
        return 0

    elif (c//1000000000000 == 4 or c//1000000000000000 == 4):
        print("VISA")
        return 0
        
    else:
        print("INVALID")
        return 0
    
    
# Виклик головної функції    
if __name__ == "__main__":
    main()
    