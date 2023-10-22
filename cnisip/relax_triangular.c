// #include "relax_triangular.h"

void relax_triangular_trivial_boundary(long long *ptr, int rows, int cols){
    long long pile;
    int flag = 1;
    while (flag != 0){
        flag = 0;
        for (int i = 1; i < rows-1; i ++){
            for (int j = 1; j < cols-1; j ++){
                if (ptr[i*cols + j] >= 6){
                    flag = 1;
                    pile = ptr[i*cols + j] / 6;
                    ptr[i*cols + j] %= 6;
                    ptr[i*cols + j + 1] += pile;
                    ptr[i*cols + j - 1] += pile;
                    ptr[(i + 1)*cols + j] += pile;
                    ptr[(i - 1)*cols + j] += pile;
                    ptr[(i + 1)*cols + j + 1] += pile;
                    ptr[(i - 1)*cols + j - 1] += pile;
                }
            }
        }
    }
    flush_trivial_boundary(ptr, rows, cols);
}

void relax_triangular_non_directed_non_trivial_boundary(long long *ptr, int rows, int cols){
    long long pile;
    int flag = 1;
    while (flag != 0){
        flag = 0;
        for (int i = 1; i < rows-1; i ++){
            for (int j = 1; j < cols-1; j ++){
                if (ptr[graph_i2(i, j, cols)] >= 6 && bound_i2(ptr, i, j, cols) == 0){
                    flag = 1;
                    pile = ptr[graph_i2(i, j, cols)] / 6;
                    ptr[graph_i2(i, j, cols)] %= 6;
                    ptr[graph_i2(i, j + 1, cols)] += pile;
                    ptr[graph_i2(i, j - 1, cols)] += pile;
                    ptr[graph_i2(i + 1, j, cols)] += pile;
                    ptr[graph_i2(i - 1, j, cols)] += pile;
                    ptr[graph_i2(i + 1, j + 1, cols)] += pile;
                    ptr[graph_i2(i - 1, j - 1, cols)] += pile;
                }
            }
        }
    }
    flush_non_trivial_boundary(ptr, rows, cols);
}