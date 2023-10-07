#include <stdlib.h>
#include <time.h>
#include <stdio.h>
void random_triangular(long long *ptr, int rows, int cols){
    srand(time(NULL));
    // int random_number = rand() % 2;
    long long *ptr2 = ptr + rows*cols;
    // go through vertical edges
    for (int i = 0; i < rows; i++){
        for (int j = 0; j < cols-1; j++){
            if (rand() % 2 == 0){
                ptr2[i*cols + j] ++;
                ptr[i*cols + j] += (1<<0);
            }
            else{
                ptr2[i*cols + j+1] ++;
                ptr[i*cols + j+1] += (1<<1);
            }
        }
    }
    // go through horizontal edges
    for (int i = 0; i < rows-1; i++){
        for (int j = 0; j < cols; j++){
            if (rand() % 2 == 0){
                ptr2[i*cols + j] ++;
                ptr[i*cols + j] += (1<<2);
            }
            else{
                ptr2[(i+1)*cols + j] ++;
                ptr[(i+1)*cols + j] += (1<<3);
            }
        }
    }
    // go through diagonal edges
    for (int i = 0; i < rows-1; i++){
        for (int j = 0; j < cols-1; j++){
            if (rand() % 2 == 0){
                ptr2[i*cols + j] ++;
                ptr[i*cols + j] += (1<<4);
            }
            else{
                ptr2[(i+1)*cols + j+1] ++;
                ptr[(i+1)*cols + j+1] += (1<<5);
            }
        }
    }
}