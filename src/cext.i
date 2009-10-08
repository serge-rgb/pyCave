%module cext

%typemap (in) double*{
  /*Check for list*/
  if (PyTuple_Check ($input)){
    int size = PyTuple_Size($input);
    $1 = (double *) malloc (size*sizeof(double));
    int i;
    for (i =0; i<size;i++){
      PyObject *tmp = PyTuple_GetItem ($input,i);
      if (PyFloat_Check (tmp)){
	$1[i] = PyFloat_AsDouble(tmp);
      }else if (PyInt_Check (tmp)){
	$1[i] = (double) PyInt_AsLong (tmp);
      }else{
	PyErr_SetString(PyExc_TypeError,"CEXT: not a float or int inside tuple");
	return NULL;
      }
    }
  }else {
    PyErr_SetString(PyExc_TypeError,"CEXT: not a tuple");
    return NULL;
  }

 }
%typemap (freearg) double*{
  free ((int*) $1);
 }

%{
#define SWIG_FILE_WITH_INIT
#include "cext.h"
%}
void sendVertex (double *,double*);
