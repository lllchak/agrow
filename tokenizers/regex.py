import re
import dtypes

from tokenizers import BaseTokenizer


class RegexTokenizer(BaseTokenizer):
    """
    Regex tokenizer base class. Inherit tokenizer, stokenize and gstopwords
    methods from BaseTokenizer. Perform tokenization based on the regex
    pattern
    """

    def __init__(
        self,
        pattern: str = r'.',
        find_gaps: bool = False,
        remove_empty: bool = True,
        rflags: re.RegexFlag = re.UNICODE | re.MULTILINE | re.DOTALL
    ) -> None:
        """
        Initializes RegexTokenizer object with given parameters. Also
        compiles regular expression.

        Args:
            pattern (str)         : Pattern in rstring (regex string) representation
            find_gaps (bool)      : If pattern should be used to find separators between
                                    tokens flag (True to find separator; False to find token itself)
            remove_empty (bool)   : If empty tokens (`''`) should be removed flag
            rflags (re.RegexFlag) : Regex compilation flags

        Returns:
            None (only initializes RegexTokenizer instance)
        """

        self.pattern = pattern
        self.find_gaps = find_gaps
        self.remove_empty = remove_empty
        self.rflags = rflags
        self.regex = re.compile(pattern=pattern, flags=rflags)

    def __repr__(self) -> str:
        """
        Defines RegexTokenizer class representation. When print() on RegexTokenizer
        instance is called, __repr__ invokes and prints out given object info.

        Args:
            self : Current instance pointer

        Returns:
            RegexTokenizer string representation
        """

        return "{}(\n\tpattern={!r},\n\tfind_gaps={},\n\tremove_empty={},\n\trflags={!r}\n)".format(
            self.__class__.__name__,
            self.pattern,
            self.find_gaps,
            self.remove_empty,
            self.rflags
        )

    def tokenize(self, string: str) -> dtypes.List[str]:
        """
        RegexTokenizer tokenization method implementation. Simply splits
        string (sentence/context) with the respect to given regex.

        Args:
            string (str) : String (sentence/context) to be tokenized

        Returns:
            List of tokens, i.e "string to tokenize" -> ["string", "to", "tokenize"]
                                                            (rstring == r"\s+")
        """

        if self.find_gaps:
            if self.remove_empty: return [tk for tk in self.regex.split(string) if tk]
            else: return self.regex.split(string)
        else: return self.regex.findall(string)
