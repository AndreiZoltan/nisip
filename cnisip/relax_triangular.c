inline long long graph_i(int i, int j, int cols){
    return i*2*cols + 2*j;
}
inline long long bound_i(int i, int j, int cols){
    return i*2*cols + 2*j+1;
}

void flush_boundary(long long *ptr, int rows, int cols, int trivial){
    if (trivial){
        for (int i = 0; i < rows; i+=rows-1){
            for (int j = 0; j < cols; j ++){
                ptr[i*cols + j] = 0;
            }
        }
        for (int j = 0; j < cols; j+=cols-1){
            for (int i = 0; i < rows; i ++){
                ptr[i*cols + j] = 0;
            }
        }
    }
    else{
        for (int i = 0; i < rows; i++){
            for (int j = 0; j < cols; j ++){
                if (ptr[bound_i(i, j, cols)] == 1){
                    ptr[graph_i(i, j, cols)] = 0;
                }
            }
        }
    }
}

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
    flush_boundary(ptr, rows, cols);
}

void relax_triangular_non_trivial_boundary(long long *ptr, int rows, int cols){
    long long pile;
    int flag = 1;
    while (flag != 0){
        flag = 0;
        for (int i = 1; i < rows-1; i ++){
            for (int j = 1; j < cols-1; j ++){
                if (ptr[graph_i(i, j, cols)] >= 6 && ptr[bound_i(i, j, cols)] == 0){
                    flag = 1;
                    pile = ptr[graph_i(i, j, cols)] / 6;
                    ptr[graph_i(i, j, cols)] %= 6;
                    ptr[graph_i(i, j + 1, cols)] += pile;
                    ptr[graph_i(i, j - 1, cols)] += pile;
                    ptr[graph_i(i + 1, j, cols)] += pile;
                    ptr[graph_i(i - 1, j, cols)] += pile;
                    ptr[graph_i(i + 1, j + 1, cols)] += pile;
                    ptr[graph_i(i - 1, j - 1, cols)] += pile;
                }
            }
        }
    }
    flush_boundary(ptr, rows, cols);
}