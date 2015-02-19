from __future__ import absolute_import
try:
    from cStringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO

import struct

import pytest

from tchannel.parser import read_number
from tchannel.parser import read_key_value
from tchannel.parser import write_number
from tchannel.parser import write_key_value


def test_read_char():
    """Ensure reading a single character works."""
    assert read_number(StringIO(b'\x10'), 1) == 16


def test_read_long():
    """Ensure we can read 4-byte longs."""
    value = 12345
    assert read_number(StringIO(
        struct.pack('>I', value)
    ), 4) == value


def test_read_invalid():
    """Ensure size validation is enforced."""
    with pytest.raises(ValueError):
        read_number(None, 42)


def test_read_zero_length_value():
    """Test edge case around 0-length value."""
    buff = StringIO(
        b'\x00\x03key'
    )
    assert read_key_value(buff, 2, 0) == (
        'key',
        None,
        len('key') + 2
    )


def test_write_number():
    """Verify we pack structs properly."""
    assert write_number(0x01, 1) == b'\x01'


def verify_key_value(stream, key, value, key_size, value_size):
    assert read_number(stream, key_size) == len(key)
    assert stream.read(len(key)).decode('utf-8') == key

    if value:
        assert read_number(stream, value_size) == len(value)
        assert stream.read(len(value)).decode('utf-8') == value
    else:
        assert read_number(stream, value_size) == 0


@pytest.mark.parametrize('key_size,value_size,value', [
    (2, None, 'value'),
    (2, 4, 'value'),
    (2, 2, None),
])
def test_write_key_value(key_size, value_size, value, stringio):
    """Verify we write variable-width values properly."""
    key = 'key'

    stream = write_key_value(
        key, value, key_size=key_size, value_size=value_size
    )
    verify_key_value(
        stringio(stream),
        key,
        value,
        key_size=key_size,
        value_size=value_size or key_size,
    )
