#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // take money input and prompt user again if negative
    int money;
    do
    {
        money = get_int("Change owed: ");
    }
    while (money < 0);
    // different coins used

    int quarters;
    int dimes;
    int nickels;
    int cents;

    // calculation of number of each type of coins
    quarters = money / 25;
    money = money - (25 * quarters);

    dimes = money / 10;
    money = money - (10 * dimes);

    nickels = money / 5;
    money = money - (5 * nickels);

    cents = money;

    int coins;
    coins = cents + nickels + dimes + quarters;

    printf("%i\n", coins);
}
