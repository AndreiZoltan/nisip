
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <numpy/arrayobject.h>
#include <stdio.h>
#include "relax_square.c"
#include "relax_triangular.c"


PyObject *add(PyObject *self, PyObject *args)
{
    double x, y;
    PyArg_ParseTuple(args, "dd", &x, &y);
    return PyFloat_FromDouble(x + y);
};


static PyObject *relax_square(PyObject *self, PyObject *args)
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
    if (PyErr_Occurred())
    {
        printf("error after **data\n");
        return NULL;
    }
    
    long long **data;
    int64_t size = PyArray_SIZE(arr);
    npy_intp *dims = PyArray_DIMS(arr);
    arr = PyArray_Cast(arr, NPY_INT64);
    PyArray_AsCArray((PyObject **)&arr, &data, dims, 2, PyArray_DescrFromType(NPY_INT64));
    if (PyErr_Occurred())
    {
        return NULL;
    }
    PyObject *result = PyArray_SimpleNew(2, dims, NPY_INT64);
    long long *result_data = PyArray_DATA((PyArrayObject *)result);
    for (int i = 0; i < (int)dims[0]; i++)
    {
        for(int j = 0; j < (int)dims[1]; j++)
        {
            result_data[i*dims[0] + j] = data[i][j];
        }
    }
    relax_square_trivial_boundary(result_data, (int)dims[0], (int)dims[1]);
    return result;
};

static PyObject *relax_triangular(PyObject *self, PyObject *args)
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
    if (PyErr_Occurred())
    {
        printf("error after **data\n");
        return NULL;
    }
    
    long long **data;
    int64_t size = PyArray_SIZE(arr);
    npy_intp *dims = PyArray_DIMS(arr);
    arr = PyArray_Cast(arr, NPY_INT64);
    PyArray_AsCArray((PyObject **)&arr, &data, dims, 2, PyArray_DescrFromType(NPY_INT64));
    if (PyErr_Occurred())
    {
        return NULL;
    }
    PyObject *result = PyArray_SimpleNew(2, dims, NPY_INT64);
    long long *result_data = PyArray_DATA((PyArrayObject *)result);
    for (int i = 0; i < (int)dims[0]; i++)
    {
        for(int j = 0; j < (int)dims[1]; j++)
        {
            result_data[i*dims[1] + j] = data[i][j];
        }
    }
    relax_triangular_trivial_boundary(result_data, (int)dims[0], (int)dims[1]);
    return result;
};

static PyObject *relax_triangular_directed(PyObject *self, PyObject *args)
{
    PyArrayObject *arr;
    int x, y, z;
    PyArg_ParseTuple(args, "Oiii", &arr, &x, &y, &z);
    if (PyErr_Occurred())
    {
        return NULL;
    }
    if (!PyArray_Check(arr))
    {
        PyErr_SetString(PyExc_TypeError, "Argument must be numpy array.");
        return NULL;
    }
    if (PyErr_Occurred())
    {
        printf("error after **data\n");
        return NULL;
    }
    
    long long **data;
    int64_t size = PyArray_SIZE(arr);
    npy_intp *dims = PyArray_DIMS(arr);
    arr = PyArray_Cast(arr, NPY_INT64);
    PyArray_AsCArray((PyObject **)&arr, &data, dims, 2, PyArray_DescrFromType(NPY_INT64));
    if (PyErr_Occurred())
    {
        return NULL;
    }
    PyObject *result = PyArray_SimpleNew(2, dims, NPY_INT64);
    long long *result_data = PyArray_DATA((PyArrayObject *)result);
    for (int i = 0; i < (int)dims[0]; i++)
    {
        for(int j = 0; j < (int)dims[1]; j++)
        {
            result_data[i*dims[1] + j] = data[i][j];
        }
    }
    relax_triangular_directed_trivial_boundary(result_data, (int)dims[0], (int)dims[1], x, y, z);
    return result;
};

static PyMethodDef methods[] = {
    {"add", add, METH_VARARGS, "Add two numbers."},
    {"relax_square", relax_square, METH_VARARGS, "Relax sandpile on square lattice graph"},
    {"relax_triangular", relax_triangular, METH_VARARGS, "Relax sandpile on triangular lattice graph"},
    {"relax_triangular_directed", relax_triangular_directed, METH_VARARGS, "Relax sandpile on triangular lattice graph with directed edges"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef cnisip = {
    PyModuleDef_HEAD_INIT,
    "cnisip",
    "C module for sandpile manipulations",
    -1,
    methods};

PyMODINIT_FUNC PyInit_cnisip(void) { // here we set the name of the module
    printf("cnisip init\n");
    PyObject *module = PyModule_Create(&cnisip);
    import_array();
    return module;
};