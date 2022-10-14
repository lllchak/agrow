import numpy as np

int8 = np.dtype("int8")
int16 = np.dtype("int16")

_all_dtypes = (
	int8,
	int16
)

_dtype_categories = {
	"all": _all_dtypes
}

_promotion_table = {
	(int8, int8): int8,
	(int8, int16): int16,
}


def result_type(
		type1: np.dtype,
		type2: np.dtype
) -> np.dtype:
	if (type1, type2) in _promotion_table:
		return _promotion_table[type1, type2]
	raise TypeError(f"{type1} and {type2} cannot be type promoted together")
