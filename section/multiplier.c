#include <cs50.h>
#include <stdio.h>

int array[5];

int main(void)

{
    array[0] = 1;

    for(int i = 0; i < 5; i++)

    {
       printf("%i\n", array[i]);
        array[i+1] = array[i]*2;
    }

}
