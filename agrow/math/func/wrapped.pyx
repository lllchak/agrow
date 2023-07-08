from libcpp cimport bool

cdef extern from "core/func.h":
    bool ag_is_zero(double source)

def is_zero(double source):
    return ag_is_zero(source)