#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
string rotate(string text, int key);
int main(int argc, string argv[])
{
    // Make sure program was run with just one command-line argument
    if (argc != 2)
    {
        printf("Please specify key through a single command line argument\n");
        return 1;
    }
    // Make sure every character in argv[1] is a digit
    int n = strlen(argv[1]);
    for (int i = 0; i < n; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    // Convert argv[1] from a `string` to an `int`
    int key = atoi(argv[1]);
    // Prompt user for plaintext
    string plain_text = get_string("plaintext: ");
    // Carry out rotate function (defined below)
    string answer = rotate(plain_text, key);
    // Print answer
    printf("ciphertext: %s\n ", answer);
}

// Rotate the character if it's a letter

string rotate(string text, int key)
{
    int lenght = strlen(text);
    int base;
    for (int i = 0; i < lenght; i++)
    {
        if (isalpha(text[i]))
        {

            if (isupper(text[i]))
            {
                base = 65;
            }

            else
            {
                base = 97;
            }

            // shift the character
            text[i] = ((text[i] + key - base) % 26) + base;
        }
    }
    // return the answer in function
    return text;
}