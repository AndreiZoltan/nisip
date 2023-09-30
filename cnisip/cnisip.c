
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <numpy/arrayobject.h>
#include <stdio.h>
#include "square_relax2.c"




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
    if (!PyArray_Check(arr))
    {
        PyErr_SetString(PyExc_TypeError, "Argument must be numpy array.");
        return NULL;
    }
    // if (PyArray_TYPE(arr) != NPY_INT)
    // {
    //     PyErr_SetString(PyExc_TypeError, "Argument must be numpy array of type int.");
    //     return NULL;
    // }
    // if (!PyArray_IS_C_CONTIGUOUS(arr))
    // {
    //     PyErr_SetString(PyExc_TypeError, "Argument must be C contiguous.");
    //     return NULL;
    // }
    if (PyErr_Occurred())
    {
        printf("error after **data\n");
        return NULL;
    }
    
    long long **_data;
    int64_t size = PyArray_SIZE(arr);
    npy_intp *dims = PyArray_DIMS(arr);
    PyArray_AsCArray((PyObject **)&arr, &_data, dims, 2, PyArray_DescrFromType(NPY_INT64));
    if (PyErr_Occurred())
    {
        return NULL;
    }
    printf("dims[0] = %ld\n", dims[0]);
    printf("dims[1] = %ld\n", dims[1]);
    long long *data;
    data = malloc(size*sizeof(long long));
    for (int i = 0; i < (int)dims[0]; i++)
    {
        for(int j = 0; j < (int)dims[1]; j++)
        {
            data[i*dims[0] + j] = _data[i][j];
        }
    }
    printf("BEFORE\n");
    square_relax_simple(data, (int)dims[0], (int)dims[1]);
    printf("AFTER\n");
    PyObject *result = PyArray_SimpleNew(2, dims, NPY_INT64);
    long long *result_data = PyArray_DATA((PyArrayObject *)result);
    for (int i = 0; i < (int)dims[0]; i++)
    {
        for(int j = 0; j < (int)dims[1]; j++)
        {
            result_data[i*dims[1] + j] = data[i*dims[1] + j];
        }
    }
    return result;
};


static PyMethodDef methods[] = {
    {"add", add, METH_VARARGS, "Add two numbers."},
    {"sum", sum, METH_VARARGS, "Sum all numbers in a matrix."},
    {"sumpy", sumpy, METH_VARARGS, "Sum all numbers in a matrix."},
    {"square_relax", square_relax, METH_VARARGS, "Sum all numbers in a matrix."},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef relax = {
    PyModuleDef_HEAD_INIT,
    "relax",
    "relax the sandpile",
    -1,
    methods};

PyMODINIT_FUNC PyInit_cnisip(void) { // here we set the name of the module
    printf("cnisip init\n");
    PyObject *module = PyModule_Create(&relax);
    import_array();
    return module;
};