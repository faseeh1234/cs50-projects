#include <cs50.h>
#include <stdio.h>

int main(void)

{
    // ask the user for an input

    int height;
    do
    {
        // the loop makes sure input is an integar greater than 1
        height = get_int("Height: ");
    }
    while (height < 1);

    // print pyramid
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < height; j++)
        {
            if (height - j > i + 1)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }
        printf("\n");
    }
}
