#include <cs50.h>
#include <stdio.h>

int main(void)

// taking name input and printing it

{
    string name = get_string("What's your name? ");
    printf("Hello, %s\n", name);
}
