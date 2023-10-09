inline long long graph_i2(int i, int j, int cols){
    /*2 means every second element is graph element*/
    return i*2*cols + 2*j;
}

inline long long bound_i2(long long *ptr, int i, int j, int cols){
    return ptr[i*2*cols + 2*j + 1];
}

void flush_trivial_boundary(long long *ptr, int rows, int cols){
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

void flush_non_trivial_boundary(long long *ptr, int rows, int cols){
    for (int i = 0; i < rows; i++){
        for (int j = 0; j < cols; j ++){
            if (bound_i2(ptr, i, j, cols) == 1){
                ptr[graph_i2(i, j, cols)] = 0;
            }
        }
    }
}