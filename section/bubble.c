#include <cs50.h>
#include <stdio.h>

int main(void)

{
    int n = get_int("How many values?  ");
    int values[n];
    for (int i = 0; i < n; i++)
    {
        values[i] = get_int("Value %i: ", i);
    }

for (int i = 0; i < n - 1; i++)
    for (int j = 0; j < n - 1; j++)
        if (values[j] > values[j+1])
        {
            int a = values[j];
            values[j] = values[j + 1];
            values[j+1] = a;
        }
for (int i = 0; i < n; i++)
    printf("%i\n", values[i]);
}
