#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "shuffle.h"

int main(int argc, char *argv[])
{

    if (argc != 2)
    {
        printf("Usage: randomize_traversal <stride>\n");
        exit(1);
    }
    /*Allocate 5GB memory*/
    size_t alloc_size = 100 * 1024 * 1024; // * 1024;
    size_t page_size = 4096;
    char *base_pointer = malloc(alloc_size);

    printf("the addr of base_pointer is %p\n", base_pointer);


    int stride_page = atoi(argv[1]);
    if (base_pointer)
    {
        printf("SYSTOPIA: allocating %zu bytes from %lx to %lx\n", alloc_size, base_pointer, base_pointer + alloc_size);
    }
    else
    {
        printf("SYSTOPIA: allocation Error.\n");
        return 1;
    }

    size_t stride = 4096;

    printf("random\n");
    size_t index = 0;
    size_t num_pages = alloc_size / page_size;
    // Get a random list of numbers this helps touch all pages randomly.
    int *randArr = getShuffled(num_pages, 1);
    // This should randomly touch pages.
     while (index < num_pages)
    {
        int curr_index = randArr[index];
        memset(base_pointer + (curr_index * page_size), 'a', 10);
        index += 1;
    }
    free(randArr);

    printf("protect\n");
     *base_pointer = 'a';
     printf("protect\n");

    printf("Moving to the next phase\n");

    printf("random");
    randArr = getShuffled(num_pages, 1);

    index = 0;
    while (index < num_pages)
    {
        int curr_index = randArr[index];
        // check it is 'a' from last loop
        if (memcmp(base_pointer + (curr_index * page_size), "aaaaaaaaaa", 10) != 0)
        {
            printf("SYSTOPIA: Error, expected 'aaaaaaaaaa' but got something else\n");
            return 1;
        }
        memset(base_pointer + (curr_index * page_size), 'b', 10);
        index += 1;
    }
    free(randArr);

    printf("SYSTOPIA: after memset, all done, index: %lu\n", index);
    return 0;
}