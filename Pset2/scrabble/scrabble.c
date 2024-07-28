#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// abstract computation of score and declare it
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
int compute_score(string word);
int main(void)

{
    // get word input from both players

    string word1 = get_string("Enter player 1's word:  ");
    string word2 = get_string("Enter player 2's word:  ");

    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // check which score is higher and print it
    if (score1 > score2)
    {
        printf("Player 1 wins!!");
    }

    else if (score2 > score1)
    {
        printf("Player 2 wins!!");
    }
    else
    {
        printf("Tie");
    }

    // compute score of each
}

int compute_score(string word)

// compute points
{
    int score = 0;

    for (int i = 0, lenght = strlen(word); i < lenght; i++)

    {
        if (isupper(word[i]))
        {
            score += POINTS[word[i] - 'A'];
        }
        else if (islower(word[i]))
        {
            score += POINTS[word[i] - 'a'];
        }
    }

    return score;
}