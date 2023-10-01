void relax_square_trivial_boundary(long long *ptr, int rows, int cols){
    int pile;
    long flag = 1;
    while (flag != 0){
        flag = 0;
        for (int i = 1; i < rows-1; i ++){
            for (int j = 1; j < cols-1; j ++){
                if (ptr[i*cols + j] >= 4){
                    flag = 1;
                    pile = ptr[i*cols + j] / 4;
                    ptr[i*cols + j] = ptr[i*cols + j] % 4;
                    ptr[i*cols + j + 1] += pile;
                    ptr[i*cols + j - 1] += pile;
                    ptr[(i + 1)*cols + j] += pile;
                    ptr[(i - 1)*cols + j] += pile;
                }
            }
        }
    }
    for (int i = 0; i < rows; i++){
        for (int j = 0; j < cols; j += cols - 1){
            ptr[i*cols + j] = 0;
        }
    }
    for (int j = 0; j < cols; j++){
        for (int i = 0; i < rows; i += rows - 1){
            ptr[i*cols + j] = 0;
        }
    }
}