import re
from typing import List

from .base import BaseTokenizer
from .regex import RegexTokenizer


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
    r"""
    Tokenize string processing all punctuation characters like
    separate token. Using r"\w+|[^\w\s]+" regular expressing.
    It inherits from RegexTokenizer (inherits all methods).
    """

    def __init__(self) -> None:
        r"""
        Itializes NaivePunctTokenizer object with search using
        r"\w+|[^\w\s]+" regular expression.

        Makes ["doughnut", "cost", "$", "10", ".", "48"]
        from  "doughnut cost $10.48".
        """

        RegexTokenizer.__init__(self, pattern=r"\w+|[^\w\s]+")


class PunctTokenizer(BaseTokenizer):
    """
    Stores regular expressions for string tokenization with respect to
    punctuation
    """

    def __repr__(self) -> str:
        return "{}(string_tokenizer_regex={})".format(
            __class__.__name__, self._RE_STRING_TOKENIZER
        )

    __slots__ = ["_RE_STRING_TOKENIZER"]

    # Format of a regular expression to split punctuation from words
    # (taken from nltk sources)
    _STRING_TOKENIZER_FMT = r"""(
        %(MultiChar)s
        |
        (?=%(WordStart)s)\S+?                   # Accept word characters until end is found
        (?=                                     # Sequences marking a word's end
            \s|                                 # White-space
            $|                                  # End-of-string
            %(NonWord)s|%(MultiChar)s|          # Punctuation
            ,(?=$|\s|%(NonWord)s|%(MultiChar)s) # Comma if at end of word
        )
        |
        \S
    )"""

    # Ending context chars
    cend = (".", "!", "?", ";", ":")

    """
    Characters that cannot appear without words
    """

    @property
    def _re_non_word_chars(self):
        return r"(?:[)\";}\]\*:@\'\({\[%s])" % re.escape(
            "".join(set(self.cend) - {"."})
        )

    """
    Multi-char punctuation symbols
    """
    _re_multi_char_punct = r"(?:\-{2,}|\.{2,}|(?:\.\s){2,}\.)"

    """
    Excludes some characters from starting word tokens
    """
    _re_word_start = r"[^\(\"\`{\[:;&\#\*@\)}\]\-,]"

    """
    Compiles word search regular experession
    """

    @property
    def gstring_re(self) -> str:
        self._RE_STRING_TOKENIZER = re.compile(
            self._STRING_TOKENIZER_FMT
            % {
                "NonWord": self._re_non_word_chars,
                "WordStart": self._re_word_start,
                "MultiChar": self._re_multi_char_punct,
            },
            re.UNICODE | re.VERBOSE,
        )

        return self._RE_STRING_TOKENIZER

    def tokenize(self, string: str) -> List[str]:
        """
        Tokenizes a string (sentence/context) to a list of tokens
        using pre-compiled regular expression. Splits of punctuation
        from words.

        Args:
            string (str) : String to be tokenized

        Returns:
            List of tokens, i.e "string to tokenize" -> ["string", "to", "tokenize"]
        """

        return self.gstring_re.findall(string)
