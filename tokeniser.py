import string
from enum import Enum

class ControlTokens(Enum):
    NEWLINE = 0
    PERIOD = 1
    QUOTE = 2


# Simple buffered tokeniser
class Tokeniser:
    BUF_SZ = 512

    def __init__(self, stream, ignore_newline=True):
        self._stream = stream
        self._ignore_newline = ignore_newline
    
    def __iter__(self):
        tok_buf = ""
        # Prefill the buffer
        self._fill_buf()
        while not self._is_eof:
            next_char = self._get_next_char()
            if not self._ignore_newline and next_char in ('\n', '\r'):
                if len(tok_buf):
                    yield tok_buf
                    tok_buf = ''
                yield ControlTokens.NEWLINE
            elif next_char == '.':
                if len(tok_buf):
                    yield tok_buf
                    tok_buf = ''
                yield ControlTokens.PERIOD
            elif next_char in ('\'', '"', '`'):
                if len(tok_buf):
                    yield tok_buf
                    tok_buf = ''
                yield ControlTokens.QUOTE
            elif next_char in (' ', '\t', ',', '\n', '\r'):
                if len(tok_buf):
                    yield tok_buf
                    tok_buf = ''
            else:
                tok_buf += next_char.upper()

    @property
    def _is_eof(self):
        return len(self._text_buf) == 0
    
    def _fill_buf(self):
        self._text_buf = self._stream.read(self.BUF_SZ)
        self._text_buf_offs = 0

    def _get_next_char(self):
        # We assume we can always get a char so deal with buffer filling after getting result
        assert len(self._text_buf) and self._text_buf_offs < len(self._text_buf), "Tried to read empty buffer"
        result = self._text_buf[self._text_buf_offs]
        self._text_buf_offs += 1
        #  Refill buffer if this was the last char
        if not self._text_buf_offs < len(self._text_buf):
            self._fill_buf()
        return result


