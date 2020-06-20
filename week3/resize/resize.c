// resize a BMP file
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "bmp.h"
#include <ctype.h>
#include <stdbool.h>
int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: resize f infile outfile\n");
        return 1;
    } //перевірка чи кожен символ argv [1] є числом або крапкою
     for ( int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            if (isdigit(argv[1][i]) || argv [1][i] == '.')
                {
                   true;
                }
            else
                {
                    printf("Usage: resize n(need float) infile outfile\n");
                    return 1;
                }
        }
        //зміна набору символів argv [1] на число типу флоат і заокруглення до десятих
    float g = atof(argv[1]);
    float grow = floor(g * 10)/10;
    int growint = 1/grow;

    if (grow > 100)
        {
            printf("your integer too big\n");
            return 1;
        }
    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }
    BITMAPFILEHEADER bf, bf_new;
    // read infile's BITMAPFILEHEADER and create the new same;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    bf_new = bf;

    // read infile's BITMAPINFOHEADER and create the new same;
    BITMAPINFOHEADER bi, bi_new;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    bi_new = bi;

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }
            bi_new.biWidth *= grow;
            bi_new.biHeight *= grow;

    // old and new padding.
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int new_padding = (4 - (bi_new.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // new SizeImage and bfSize.
    bi_new.biSizeImage = ((sizeof(RGBTRIPLE) * bi_new.biWidth) + new_padding) * abs(bi_new.biHeight);
    bf_new.bfSize = bf.bfSize - bi.biSizeImage + bi_new.biSizeImage;
    // write outfile's BITMAPFILEHEADER
    fwrite(&bf_new, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi_new, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight;i++)
    {
        for (int t = 0; t < grow; t++)
        {
            // iterate over pixels in scanline
            for (int j = 0; j < bi.biWidth; j++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
                // якщо гров менше 1 то проскакувати один піксель
                if (grow < 1)
                     {
                        if ((j+1)%growint == 0)
                         fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                        else
                         true;
                     }
                else
                    for( int p = 0; p < grow; p++)
                        {
                            // write RGB triple to outfile
                            fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                        }
            }

            // then add it back (to demonstrate how)
            for (int k = 0; k < new_padding; k++)
                {
                    fputc(0x00, outptr);
                }

             if(grow < 1 && t < grow)
                     fseek(inptr,( bi.biWidth * sizeof(RGBTRIPLE)) + (padding * growint), SEEK_CUR);

            else if( t < grow -1 && grow >= 1)
                {
                     fseek(inptr, -bi.biWidth * sizeof(RGBTRIPLE), SEEK_CUR);
                }
            else
                {
                    // skip over padding, if any
                    fseek(inptr, padding, SEEK_CUR);
                }
        }
        if ( grow < 1)
            {i += (growint -1); }
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}