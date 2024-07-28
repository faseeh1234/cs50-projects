#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

// initiate abstraction for letters, words and sentences;
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
int main(void)
{
    // get input from user
    string text = get_string("Type in your sentence:  ");

    // count the number of letters, words and sentences in a text

    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);
    // Use the formula and print answer
    float index = 0.0588 * ((float) letters * 100 / (float) words) - 0.296 * ((float) sentences * 100 / (float) words) - 15.8;
    int indexLH = round(index);
    
    if (indexLH < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (indexLH > 16)

    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", indexLH);
    }
}
// Abstraction for letters
// Return the number of letters
int count_letters(string text)

{
    int count_letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))

        {
            count_letters++;
        }
    }

    return count_letters;
}

// Abstraction for words
// Return the number of words
int count_words(string text)
{
    int count_words = 1;
    for (int j = 0; j < strlen(text); j++)
    {
        if (text[j] == ' ')

        {
            count_words++;
        }
    }
    return count_words;
}
// Abstraction for sentences
// Return the number of sentences
int count_sentences(string text)

{
    int count_sentences = 0;
    int n = strlen(text);
    for (int k = 0; k < n; k++)
    {
        if (text[k] == '.' || text[k] == '?' || text[k] == '!')

        {
            count_sentences++;
        }
    }
    return count_sentences;
}