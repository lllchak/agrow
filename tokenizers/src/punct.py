# import re

# from tokenizer import BaseTokenizer


"""
Might be useful in the future, but deprecated for now
"""
# class PunctToken:
#     """
#     String (sentence/context) token class. Stores token value, its type
#     and if its final string token flag.
#     """
        
#     # Numeric token (contains only number(-s))
#     _NUMERIC = re.compile(r"^-?[\.,]?\d[\d,\.-]*\.?$")
#     # Alpha token (contains only alphabetical characters)
#     _ALPHA = re.compile(r"[^\W\d]+$", re.UNICODE)

#     def __init__(self, tk: str) -> None:
#         self.tk = tk
#         self.type = self.__stype(tk)
#         self.tfinal = tk.endswith('.') | \
#                       tk.endswith('?') | \
#                       tk.endswith('!') | \
#                       tk.endswith(';')

#     def __stype(self, tk) -> None:
#         return self._NUMERIC.sub("NUMERIC", tk.lower())

#     @property
#     def tk_no_endchar(self):
#         return self.type[:-1] \
#                if len(self.type) > 1 and self.type[-1] in ['.', '?', '!', "..."] \
#                else self.type

#     @property
#     def fupper(self) -> bool:
#         return self.tk[0].isupper()

#     @property
#     def flower(self) -> bool:
#         return self.tk[0].islower()

#     @property
#     def is_num(self) -> bool:
#         return self.type.startwith("NUMERIC")

#     @property
#     def is_alpha(self) -> bool:
#         return self._ALPHA.match(self.tk)
    