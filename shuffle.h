#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void swap(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

// A utility function to print an array
void printArray(int arr[], int n)
{
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

// A function to generate a random permutation of arr[]
void randomize(int arr[], int n)
{
    // Use the same seed value so that we get the
    // same result each time we run this program for a
    // given value of "n"
    srand(n);

    // Start from the last element and swap one by one. We don't
    // need to run for the first element that's why i > 0
    for (int i = n - 1; i > 0; i--)
    {
        // Pick a random index from 0 to i
        int j = rand() % (i + 1);

        // Swap arr[i] with the element at random index
        swap(&arr[i], &arr[j]);
    }
}

// returns a array with n randomized numbers from 0 to n-1
// caller has to free the array.
int *getShuffled(int n, int randomize_array)
{
    int *arr = (int *)malloc(sizeof(int) * n);
    // assert(arr != NULL);

    for (int i = 0; i < n; i++)
    {
        arr[i] = i;
    }
    if (randomize_array)
    {
        randomize(arr, n);
    }
    return arr;
}