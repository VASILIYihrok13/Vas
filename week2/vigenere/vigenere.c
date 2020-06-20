#include <cs50.h>
#include <stdio.h>
#include<string.h>
#include<ctype.h>
int shift(char c);

int main(int argc, string argv[])
{
    if (argc != 2)
        {
            printf("Usage: %s keyword\n", argv[0]);
            return 1;
        }

    for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            if (isalpha(argv[1][i])) // якщо символ із рядка є буквою, то вірно
                {
                    true;
                }
            else
                {
                    printf("Usage: %s keyword\n", argv[0]);
                    return 2;
                }
        } // створення змінних типу і потрібних нижче
    int parol = strlen(argv[1]),j = 0, key;
    //отримання тексту для шифрування від користувача
    string plain = get_string("plaintext: ");
    printf("ciphertext: ");

    for( int i = 0, n = strlen(plain); i < n; i++)
        {// процес шифрування. для маленьких і великих букв окремо.
            char text = plain[i];
            if(isalpha(text))
               {
                    key = shift(argv[1][j]);
                    if(islower(text))
                        {
                            printf("%c", (text - 'a' + key)%26+'a');
                        }
                    else
                        {
                            printf("%c", (text - 'A' + key)%26+'A');
                        }
                    j = (j+1)%parol;
                }
            else
                {
                    printf("%c", text);
                }
        }
    printf("\n");
    return 0;
}

// нова функція
int shift(char c)
{// присвоюємо цифрове значення для букв від 0=А.
    char big = toupper(c);
    int shift = (int) big -'A';
    return shift;
}
