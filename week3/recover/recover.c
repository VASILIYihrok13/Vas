#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
typedef uint8_t  BYTE;

int main(int argc, char *argv[])
{   // перевірка, чи користувач ввів саме два рядки.
    if (argc != 2)
        {
            fprintf(stderr, "%s namefile\n", argv[0]);
            return 1;
        }
    // відкриття файлу який ввів користувач.
    char *infile = argv[1];
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL) // перевірка чи можливо відкрити файл, який ввів користувач.
        {
            fprintf(stderr, "Could not open %s\n", infile);
            return 2;
        }
    FILE *outptr;
    char filename [8];   // набір символів для імен відновлених фото формату ###.jpg і \0
    int counter = 0;      // лічильник аби рахувати скільки файлів відновимо.
    BYTE buffer [512];    // побітна змінна для того аби можна було аналізувати блок пам'яті.
    while( fread(buffer, 512, 1, inptr)) // виконувати доки читання буде можливе саме по 512 байтів
        {
            if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer [3] & 0xf0) == 0xe0) // перевірка чи файл є початком файлу jpg/.
                {
                    if (counter !=0) // якщо лічильник не нуль. тобто це вже не перший файл. то закрити попередній.
                        {
                            fclose(outptr);
                        }
                    sprintf(filename,"%03i.jpg", counter); // лічильник фаайлів / ще не зовсім розумію як він працює.
                    outptr = fopen(filename, "w");
                    counter ++;
                }
            if ( outptr != NULL) // якщо файл для запису відкритий то записати ))
                {
                      fwrite(buffer, 512, 1, outptr);
                }
        }
    fclose(outptr); //    закриття всіх файлів.
    fclose(inptr);
    return 0;
}
