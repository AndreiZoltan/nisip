
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <numpy/arrayobject.h>
#include <stdio.h>


PyObject *add(PyObject *self, PyObject *args)
{
    double x, y;
    PyArg_ParseTuple(args, "dd", &x, &y);
    return PyFloat_FromDouble(x + y);
};

// Sum all numbers in a matrix.
static PyObject *sum(PyObject *self, PyObject *args)
{
    PyArrayObject *arr;
    PyArg_ParseTuple(args, "O", &arr);
    if (PyErr_Occurred())
    {
        return NULL;
    }
    if (!PyArray_Check(arr) || PyArray_TYPE(arr) != NPY_DOUBLE || !PyArray_IS_C_CONTIGUOUS(arr)){
        PyErr_SetString(PyExc_TypeError, "Argument must be C contiguous numpy array of type double.");
        return NULL;
    }

    double *data = PyArray_DATA(arr);
    int64_t size = PyArray_SIZE(arr);

    double total = 0;
    for (int i = 0; i < size; i++) 
    {
        total += data[i];
    }
    return PyFloat_FromDouble(total);
};

static PyObject *sumpy(PyObject *self, PyObject *args)
{
    PyArrayObject *arr;
    PyArg_ParseTuple(args, "O", &arr);
    if (PyErr_Occurred())
    {
        return NULL;
    }
    if (!PyArray_Check(arr)){
        PyErr_SetString(PyExc_TypeError, "Argument must be C contiguous numpy array of type double.");
        return NULL;
    }

    double *data;
    int64_t size = PyArray_SIZE(arr);
    npy_intp dims[] = {[0] = size};
    PyArray_AsCArray((PyObject **)&arr, &data, dims, 1, PyArray_DescrFromType(NPY_DOUBLE));
    if (PyErr_Occurred())
    {
        return NULL;
    }

    double total = 0;
    for (int i = 0; i < size; i++) 
    {
        total += data[i];
    }
    return PyFloat_FromDouble(total);
};

static PyObject *square_relax(PyObject *self, PyObject *args)
{
    PyArrayObject *arr;
    PyArg_ParseTuple(args, "O", &arr);
    if (PyErr_Occurred())
    {
        return NULL;
    }
    // if (!PyArray_Check(arr) || PyArray_TYPE(arr) != NPY_INT || !PyArray_IS_C_CONTIGUOUS(arr)){
    //     PyErr_SetString(PyExc_TypeError, "Argument must be C contiguous numpy array of type int.");
    //     return NULL;
    // }
    if (!PyArray_Check(arr))
    {
        PyErr_SetString(PyExc_TypeError, "Argument must be numpy array.");
        return NULL;
    }
    if (PyArray_TYPE(arr) != NPY_INT)
    {
        PyErr_SetString(PyExc_TypeError, "Argument must be numpy array of type int.");
        return NULL;
    }
    if (!PyArray_IS_C_CONTIGUOUS(arr))
    {
        PyErr_SetString(PyExc_TypeError, "Argument must be C contiguous.");
        return NULL;
    }

    printf("after checks\n");
    if (PyErr_Occurred())
    {
        printf("error after **data\n");
        return NULL;
    }
    printf("before size\n");

    int **data;
    int64_t size = PyArray_SIZE(arr);
    npy_intp dims[2];
    dims[0] = size;
    dims[1] = size;
    // int** data = (int**)PyArray_DATA(arr);
    PyArray_AsCArray((PyObject **)&arr, &data, dims, 2, PyArray_DescrFromType(NPY_INT));
    if (PyErr_Occurred())
    {
        return NULL;
    }
    // int** data = (int**)PyArray_DATA(arr);

    // PyObject* copyArray = PyArray_Copy((PyArrayObject*)arr);
    // int** data = (int**)PyArray_DATA(copyArray);
    // int64_t size = PyArray_SIZE(arr);
    // npy_intp dims[2];
    // dims[0] = size;
    // dims[1] = size;
    printf("after size\n");


    printf("%d\n", data[0][0]);

    int total = 0;
    // printf("%ld\n", dims[0]);
    // printf("%ld\n", dims[1]);
    // for (int i = 0; i < dims[0]; i++) 
    // {
    //     for(int j = 0; j < dims[1]; j++)
    //     {
    //         // printf("%d\n", data[i][j]);
    //         total += data[i];//[j];
    //     }   
    // }
    return PyLong_FromLong(total);
};


static PyObject *square_relax2(PyObject *self, PyObject *args)
{
    PyArrayObject *arr;
    PyArg_ParseTuple(args, "O", &arr);
    if (PyErr_Occurred())
    {
        return NULL;
    }
    // if (!PyArray_Check(arr) || PyArray_TYPE(arr) != NPY_INT || !PyArray_IS_C_CONTIGUOUS(arr)){
    //     PyErr_SetString(PyExc_TypeError, "Argument must be C contiguous numpy array of type int.");
    //     return NULL;
    // }
    if (!PyArray_Check(arr))
    {
        PyErr_SetString(PyExc_TypeError, "Argument must be numpy array.");
        return NULL;
    }
    if (PyArray_TYPE(arr) != NPY_INT)
    {
        PyErr_SetString(PyExc_TypeError, "Argument must be numpy array of type int.");
        return NULL;
    }
    if (!PyArray_IS_C_CONTIGUOUS(arr))
    {
        PyErr_SetString(PyExc_TypeError, "Argument must be C contiguous.");
        return NULL;
    }

    printf("after checks\n");
    if (PyErr_Occurred())
    {
        printf("error after **data\n");
        return NULL;
    }
    printf("before size\n");

    int *data;
    int64_t size = PyArray_SIZE(arr);
    npy_intp dims[2];
    dims[0] = size;
    dims[1] = size;
    data = (int*)PyArray_DATA(arr);
    // PyArray_AsCArray((PyObject **)&arr, &data, dims, 2, PyArray_DescrFromType(NPY_INT));
    // if (PyErr_Occurred())
    // {
    //     return NULL;
    // }
    // int** data = (int**)PyArray_DATA(arr);

    // PyObject* copyArray = PyArray_Copy((PyArrayObject*)arr);
    // int** data = (int**)PyArray_DATA(copyArray);
    // int64_t size = PyArray_SIZE(arr);
    // npy_intp dims[2];
    // dims[0] = size;
    // dims[1] = size;
    printf("after size\n");


    printf("%d\n", data[0]);

    int total = 0;
    // printf("%ld\n", dims[0]);
    // printf("%ld\n", dims[1]);
    // for (int i = 0; i < dims[0]; i++) 
    // {
    //     for(int j = 0; j < dims[1]; j++)
    //     {
    //         // printf("%d\n", data[i][j]);
    //         total += data[i];//[j];
    //     }   
    // }
    return PyLong_FromLong(total);
};


static PyMethodDef methods[] = {
    {"add", add, METH_VARARGS, "Add two numbers."},
    {"sum", sum, METH_VARARGS, "Sum all numbers in a matrix."},
    {"sumpy", sumpy, METH_VARARGS, "Sum all numbers in a matrix."},
    {"square_relax", square_relax, METH_VARARGS, "Sum all numbers in a matrix."},
    {"square_relax2", square_relax2, METH_VARARGS, "Sum all numbers in a matrix."},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef relax = {
    PyModuleDef_HEAD_INIT,
    "relax",
    "relax the sandpile",
    -1,
    methods};

PyMODINIT_FUNC PyInit_relax(void) { // here we set the name of the module
    printf("cnisip init\n");
    PyObject *module = PyModule_Create(&relax);
    import_array();
    return module;
};