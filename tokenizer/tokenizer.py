import dtypes
from tokenizer import RegexTokenizer


class WhitespaceTokenizer(RegexTokenizer):
    """
    Whitespace tokenizer. Tokenize a string on a whitespace (space, tab, newline)
    In general, can be replace by using string.split() built-in method.        
    """

    def __init__(self) -> None:
        """
        Initializes WhitespaceTokenizer with whitespace search pattern for 
        RegexTokenizer. Also inherit all methods from parent class.

        Makes ["string", "to", "tokenize"] from "string\tto\n tokenize".
        """

        RegexTokenizer.__init__(self, pattern=r"\s+", find_gaps=True)