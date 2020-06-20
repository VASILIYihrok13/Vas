// Implements a dictionary's functionality
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

//змінна для рахування кількості слів зі словника.
unsigned int count = 0;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // отримання пам'яті для нового вузла
        node *new_node = malloc(sizeof(node));
        if ( new_node == NULL) // перевірка чи є доступна пам'ять.
            {
                unload ();
                return false;
            }
        strcpy(new_node->word, word);  // запис слова до нового вузла.
        for (int i = 0; i < N; i++)
        {
            if(hash(&new_node ->word[0]) == i) // прирівняння букви до числа за типом hash фунції вище
            {
                new_node ->next = hashtable[i]; // запис до певної лінії. запис в комірку де всі перші букви одинакові.
                hashtable[i] = new_node;
                break;
            }
        }
        count ++;
    }


    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (count != 0)
        return count;
    else
        return 0;

}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int letter = hash(&word[0]);
    // порівняти два слова за допомогою strcasecmp.
    node *cursor = hashtable[letter];
    while (cursor != NULL)
        {
            if (strcasecmp(word, cursor -> word) == 0 )
                {
                    return true;
                }
            else
                {
                    cursor = cursor -> next;
                }
        }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    int p = 0;
    // звільнити всю використану пам'ять.
    for ( int i = 0; i < N; i++)
        {
            node *cursor = hashtable[i];
            while (cursor != NULL)
            {
                node*temp = cursor;
                cursor = cursor -> next;
                free (temp);
            }
        }
        return true;
}
