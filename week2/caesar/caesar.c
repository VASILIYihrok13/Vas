#include <cs50.h>
#include<stdio.h>
#include<string.h>
#include<ctype.h>
#include<stdlib.h>
void cipher(int di);
// створюємо змінні для отримання інформації з назви програми
int main(int argc, string argv[])
{  // рядок прирівнюємо до другого рядка в назві програми
    string c = argv[1];
    int digit;
    //тільки якщо в назві програми два рядки ( два слова) то програма виконується далі, якщо ні, то дивитися з самого низу елсе)
    if (argc == 2)
    {   //цикл для отримання доступу до кожного символу рядка
        for(int i = 0, n = strlen(c); i < n; i ++)
            {  
                //змінюємо символ на ціле число
                digit = atoi(&c[i]);
                //Якщо число нуль, то введено або нуль, або не число, 
                if( digit == 0)
                    {
                        printf("Usage: %s key\n", argv[0]);
                        return 2;
                    }
                    //якщо всі символи є числами то беремо ці символи як число
                else
                    {
                        digit = atoi(argv[1]);
                    }
            }
            // використання функції для шифрування. дивитися рядок 44
            cipher( digit);
    } 
   else 
    {
        printf("Usage: %s key\n", argv[0]);
        return 1;
    } 
}




void cipher( int di)
{
   string plain = get_string("plaintext: ");
        printf("cirhertext: ");
        for( int i = 0, n = strlen(plain); i < n; i++)
            {
                // процес шифрування. для маленьких і великих букв окремо.
                char text = plain[i];
                if(isalpha(text))
                {
                    if(islower(text))
                    {
                        printf("%c", (text - 'a' + di)%26+'a');
                    }
                    else
                    {printf("%c", (text - 'A' + di)%26+'A');}
                }
                else
                    {printf("%c", text);}
            }
        
        printf("\n"); 
}
