import ctypes

CFUNCLIB = ctypes.CDLL("../build/func.so")

# test
def tan(x: float) -> float:
    ctan = CFUNCLIB.ag_tan
    ctan.argtypes = [ctypes.c_double]
    ctan.restype = ctypes.c_longdouble

    return ctan(x)
