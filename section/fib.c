#include <cs50.h>
#include <stdio.h>

int main(void)
{
    printf("%i", fib(5));
}

int fib(int n)
{

    if (n == 0)
        {return 0};
    elseif (n == 1)
        {return 1};
    else
    {
        return fib(n-2) + fib(n-1);
    }
}

