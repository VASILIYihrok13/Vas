# Questions

## What's `stdint.h`?

назва стандартної бібліотеки в Сі. Затвердженої в Сі99 її стандартами. Містить декілька цілочисельних типів даних і якісь макроси.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

вказують на тип даних. На точне число бітів і наявність символів. Якщо тільки іnt8_t  - це вісім бітів і може містити знак. тобто від'ємне значення. u - вказує на те. що береться до уваги тільки додатні числа і довжина порівняно з відсутністю цього символа, збілюшується вдвоє.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

BYTE - 1, DWORD - 4, LONG - 4, WORD - 2.  

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

 Перші два байти виділені на на символи 0x424D в 16 - системі. в десятковій це 66 і 77. в аскі це звичайне BM.

## What's the difference between `bfSize` and `biSize`?

bisize - розміщене в bitmapinfoheader. вказує на кількість байтів необхідних структурі. 
bfsize - розміщене в bitmapfileheader вказує на розмір в байтах. розмір файлу в байтах

## What does it mean if `biHeight` is negative?

Це значить що початок кольорів в картинці починається зверху ( бо зазвичай знизу) в лівому куті.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

можливо тому, що в назві функції вказано Char *argv[]  а при присвоєні просто argv. або можливо тому що після копі ми нічого не пишемо й [1 i 2] не має тому нуль.

## Why is the third argument to `fread` always `1` in our code? (For example, see lines 40, 44, and 75.)

бо повертає по одному байті. або по одному пікселю.

## What value does line 63 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

3

## What does `fseek` do?

встановлює якусь точку в Файлі. Вказує на певні байти в ньому 

## What is `SEEK_CUR`?

що додавання йде від поточного положення в файлі, а не від початку - SEEK_SET/ і не від кінця - SEEK_END.
