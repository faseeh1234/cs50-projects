// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>

#include <stdio.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// DONE: Choose number of buckets in hash table
const unsigned int N = 4999;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int h = hash(word);
    node *ptr = table[h];

    while (ptr != NULL)
    {

        if (strcasecmp(ptr->word, word) == 0)
        {
            return true;
        }

        ptr = ptr->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int h = 1;
    int length = strlen(word);
    for (int i = 0; i < length; i++)
    {
        h = (((int) tolower(word[i])) * h) % N;
    }

    return h;
}


int word_count = 0;

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // Loading dict file into memory
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        return false;
    }

    char word[LENGTH + 1];
    int h;

    // Scanning each word in dictionary
    while (fscanf(dict, "%s", word) != EOF)
    {
        // Allocating memory for node
        node *n = NULL;
        n = malloc(sizeof(node));
        if (n == NULL)
        {
            unload();
            return false;
        }
        else
        {
            // Storing word into node and calculating hash
            strcpy(n->word, word);
            h = hash(n->word);
            node *root = table[h];

            // Inserting node into linked list
            n->next = table[h];
            table[h] = n;
            if (root != NULL)
            {
                n->next = root;
            }
            word_count++;
        }
    }
    fclose(dict);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    node *ptr = NULL;
    node *temp = NULL;
    for (int i = 0; i < N; i++)
    {
        ptr = table[i];
        while (ptr != NULL)
        {
            temp = ptr;
            ptr = ptr->next;
            free(temp);
        }
    }
    return true;
}
