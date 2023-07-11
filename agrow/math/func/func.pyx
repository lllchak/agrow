from libcpp cimport bool


cdef extern from "core/func.h":
    # base
    bool ag_is_zero(double source)
    long int ag_abs(long int source)
    long double ag_fabs(double source)
    long double ag_ceil(double source)
    long double ag_floor(double source)
    long double ag_fmod(double x, double y)

    # base func
    long double ag_sqrt(double source)
    long double ag_exp(double x)
    long double ag_log(double x)
    long double ag_pow(double base, double exp)

    # trigonometry
    long double ag_asin(double source)
    long double ag_acos(double source)
    long double ag_atan(double source)
    long double ag_sin(double source)
    long double ag_cos(double source)
    long double ag_tan(double source)


def is_zero(double source):
    return ag_is_zero(source)


def abs(long int source):
    return ag_abs(source)


def fabs(double source):
    return ag_fabs(source)


def ceil(double source):
    return ag_ceil(source)


def floor(double source):
    return ag_floor(source)


def fmod(double x, double y):
    return ag_fmod(x, y)


def sqrt(double source):
    return ag_sqrt(source)


def exp(double source):
    return ag_exp(source)


def log(double source):
    return ag_log(source)


def pow(double base, double exp):
    return ag_pow(base, exp)


def asin(double source):
    return ag_asin(source)


def acos(double source):
    return ag_acos(source)


def atan(double source):
    return ag_atan(source)


def sin(double source):
    return ag_sin(source)


def cos(double source):
    return ag_cos(source)


def tan(double source):
    return ag_tan(source)
