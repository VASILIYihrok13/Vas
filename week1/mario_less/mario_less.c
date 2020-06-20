#include <cs50.h>
#include <stdio.h>


int main(void)

{
 int h,j,k,i;
 do
  {
   h = get_int("Height: ");
  }
 while (h<1 || h > 8);
     
 for ( i = 0; i < h; i++)
  {
   for (k = (h-1) - i;k !=0;k -- )
    {
      printf(" ");
    }
   for ( j = 0; j < i+1; j++)
    {
      printf("#");
    }
   printf("\n");
  }
}
