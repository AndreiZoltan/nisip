void square_relax_simple(long long *ptr, int rows, int cols){
    printf("rows = %d\n", rows);
    printf("cols = %d\n", cols);
    // Square each element in the 2D array
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            // printf("ptr[%d] = %lld\n", i * cols + j, ptr[i * cols + j]);
            ptr[i * cols + j] *= 2;
            // printf("ptr[%d] = %lld\n", i * cols + j, ptr[i * cols + j]);
        }
    }
}