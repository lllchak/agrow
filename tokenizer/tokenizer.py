from tokenizer import RegexTokenizer


class WhitespaceTokenizer(RegexTokenizer):
    """
    Tokenize a string on a whitespace (space, tab, newline)
    In general, can be replaced by using string.split() built-in method.
    It inherits from RegexTokenizer (inherits all methods).   
    """

    def __init__(self) -> None:
        """
        Initializes WhitespaceTokenizer object with whitespace search 
        pattern for RegexTokenizer. Also inherit all methods from parent class.

        Makes ["string", "to", "tokenize"] from "string\tto\n tokenize".
        """

        RegexTokenizer.__init__(self, pattern=r"\s+", find_gaps=True)


class NaivePunctTokenizer(RegexTokenizer):
    """
    Tokenize string processing all punctuation characters like
    separate token. Using r"\w+|[^\w\s]+" regular expressing.
    It inherits from RegexTokenizer (inherits all methods).
    """

    def __init__(self) -> None:
        """
        Itializes NaivePunctTokenizer object with search using 
        r"\w+|[^\w\s]+" regular expression.

        Makes ["doughnut", "cost", "$", "10", ".", "48"]
        from  "doughnut cost $10.48".
        """

        RegexTokenizer.__init__(self, pattern=r"\w+|[^\w\s]+")
