// #include "relax_triangular.h"

void relax_triangular_directed_trivial_boundary(long long *ptr, int rows, int cols, int x, int y, int z){
    long long pile;
    int flag = 1;
    while (flag != 0){
        flag = 0;
        for (int i = 1; i < rows-1; i ++){
            for (int j = 1; j < cols-1; j ++){
                if (ptr[i*cols + j] >= 3){
                    flag = 1;
                    pile = ptr[i*cols + j] / 3;
                    ptr[i*cols + j] %= 3;
                    ptr[i*cols + j + x] += pile;
                    ptr[(i + y)*cols + j] += pile;
                    ptr[(i + z)*cols + j + z] += pile;
                }
            }
        }
    }
    flush_trivial_boundary(ptr, rows, cols);
}


inline long long degree_i(long long *ptr, int i, int j, int cols){
    return (ptr[i*2*cols + 2*j + 1]>>6)&0x3F;
}
inline long long direction_i(long long *ptr, int i, int j, int cols){
    return ptr[i*2*cols + 2*j + 1]&0x3F;
}
inline long long bound_i(long long *ptr, int i, int j, int cols){
    return ptr[i*2*cols + 2*j + 1]>>12;
}

void relax_triangular_directed_irregular_trivial_boundary(long long *ptr, int rows, int cols){
    int i, j;
    long long pile;
    int flag = 1;
    while (flag!=0){
        flag = 0;
        for(i = 1; i < rows-1; i ++){
            for(j = 1; j < cols-1; j ++){
                if((bound_i(ptr, i, j, cols)==0)&&ptr[graph_i2(i, j, cols)]>=degree_i(ptr, i, j, cols)&&degree_i(ptr, i, j, cols)!=0){
                    flag = 1;
                    pile = ptr[graph_i2(i, j, cols)]/degree_i(ptr, i, j, cols);
                    // printf("%d %d %lld = pile\n", i, j, pile);
                    ptr[i*2*cols + 2*j] %= degree_i(ptr, i, j, cols);
                    if (direction_i(ptr, i, j, cols) & (1<<0))
                        ptr[graph_i2(i, j+1, cols)] += pile;
                    if (direction_i(ptr, i, j, cols) & (1<<1))
                        ptr[graph_i2(i, j-1, cols)] += pile;
                    if (direction_i(ptr, i, j, cols) & (1<<2))
                        ptr[graph_i2(i+1, j, cols)] += pile;
                    if (direction_i(ptr, i, j, cols) & (1<<3))
                        ptr[graph_i2(i-1, j, cols)] += pile;
                    if (direction_i(ptr, i, j, cols) & (1<<4))
                        ptr[graph_i2(i+1, j+1, cols)] += pile;
                    if (direction_i(ptr, i, j, cols) & (1<<5))
                        ptr[graph_i2(i-1, j-1, cols)] += pile;
                }
            }
        }
    }
    for (int i = 0; i < rows; i+=rows-1){
        for (int j = 0; j < cols; j ++){
            ptr[graph_i2(i, j, cols)] = 0;
        }
    }
    for (int j = 0; j < cols; j+=cols-1){
        for (int i = 0; i < rows; i ++){
            ptr[graph_i2(i, j, cols)] = 0;
        }
    }
    for (int i = 0; i < rows; i++){
        for (int j = 0; j < cols; j ++){
            if (degree_i(ptr, i, j, cols) == 0){
                ptr[graph_i2(i, j, cols)] = 0;
            }
        }
    }
}

void relax_triangular_directed_irregular_with_boundary(long long *ptr, int rows, int cols){
    int i, j;
    long long pile;
    int flag = 1;
    while (flag!=0){
        flag = 0;
        for(i = 1; i < rows-1; i ++){
            for(j = 1; j < cols-1; j ++){
                if((bound_i(ptr, i, j, cols)==0)&&ptr[graph_i2(i, j, cols)]>=degree_i(ptr, i, j, cols)&&degree_i(ptr, i, j, cols)!=0){
                    flag = 1;
                    pile = ptr[graph_i2(i, j, cols)]/degree_i(ptr, i, j, cols);
                    // printf("%d %d %lld = pile\n", i, j, pile);
                    ptr[i*2*cols + 2*j] %= degree_i(ptr, i, j, cols);
                    if (direction_i(ptr, i, j, cols) & (1<<0))
                        ptr[graph_i2(i, j+1, cols)] += pile;
                    if (direction_i(ptr, i, j, cols) & (1<<1))
                        ptr[graph_i2(i, j-1, cols)] += pile;
                    if (direction_i(ptr, i, j, cols) & (1<<2))
                        ptr[graph_i2(i+1, j, cols)] += pile;
                    if (direction_i(ptr, i, j, cols) & (1<<3))
                        ptr[graph_i2(i-1, j, cols)] += pile;
                    if (direction_i(ptr, i, j, cols) & (1<<4))
                        ptr[graph_i2(i+1, j+1, cols)] += pile;
                    if (direction_i(ptr, i, j, cols) & (1<<5))
                        ptr[graph_i2(i-1, j-1, cols)] += pile;
                }
            }
        }
    }
    for (int i = 0; i < rows; i++){
        for (int j = 0; j < cols; j ++){
            if (degree_i(ptr, i, j, cols) == 0 || bound_i(ptr, i, j, cols) == 1){
                ptr[graph_i2(i, j, cols)] = 0;
            }
        }
    }
}