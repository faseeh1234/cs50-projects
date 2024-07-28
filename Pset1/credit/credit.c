#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long card;
    card = get_long("Please enter card number:  ");
    char str[16];

    sprintf(str, "%ld", card);
    // if card number is not 13,15,16: print invalid
    int digits;
    long card2;
    card2 = card;
    while (card2 > 0)
    {
        card2 = card2 / 10;
        digits = digits + 1;
    }
    if ((digits != 13) && (digits != 15) && (digits != 16))
    {
        printf("INVALID\n");
    }
    // Calculation of checksum
    int fetch;
    int doubles;
    long card3;
    card3 = card;
    doubles = 0;
    while (card3 > 0)
    {
        card3 = card3 / 10.0;
        fetch = card3 % 10;
        // printf ("%i ", fetch);
        fetch = fetch * 2;

        if (fetch / 10 > 0)
        {
            fetch = fetch / 10 + fetch % 10;
        }
        doubles = doubles + fetch;
        card3 = card3 / 10.0;
    }
    int fetch2;
    int doubles2 = 0;
    while (card > 0)
    {
        fetch2 = card % 10;

        card = card / 10.0;
        doubles2 = doubles2 + fetch2;
        card = card / 10;
    }

    // Invalid or valid according to checksum
    int checksum;
    checksum = doubles + doubles2;

    if (checksum % 10 == 0)
    {
        // Visa, Mastercard or AMEX
        // printf ("hello amex");
        if (str[0] == '3' && (str[1] == '4' || str[1] == '7'))
        {
            printf("AMEX\n");
        }
        else if (str[0] == '4')
        {
            printf("VISA\n");
        }
        else if (str[0] == '5' && (str[1] == '1' || str[1] == '2' || str[1] == '3' || str[1] == '4' || str[1] == '5'))
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {

        printf("INVALID\n");
    }
}
