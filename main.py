#!/usr/bin/env python3
"""news-image-20261123 entrypoint: validate entry.png, copy it byte-for-byte.

Reads entry.png next to this file, validates it as a whole PNG
(1024x1024 RGB, <= 1 MiB, magic, IHDR, per-chunk CRCs, IEND trailer,
no trailing bytes, IDAT inflates to the exact raw size the header
describes), copies the exact bytes to $MAKEFUN_OUTPUT_DIR/entry.png,
then re-reads the copy and re-validates it. Stdlib only, no network.

Exit 2 when MAKEFUN_OUTPUT_DIR is unset (nothing is written then);
exit 1 on any validation failure; exit 0 on success.
"""

import hashlib
import os
import struct
import sys
import zlib

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
WANT_W, WANT_H = 1024, 1024


def fail(msg):
    print("main.py: invalid entry.png: " + msg, file=sys.stderr)
    return 1


def validate(data):
    """Return (width, height) or raise ValueError with the reason."""
    if len(data) == 0:
        raise ValueError("empty file")
    if len(data) > MAX_BYTES:
        raise ValueError("file larger than 1 MiB (%d bytes)" % len(data))
    if data[:8] != PNG_MAGIC:
        raise ValueError("bad PNG magic")
    pos = 8
    seen_ihdr = False
    seen_iend = False
    width = height = None
    bit_depth = color_type = None
    idat = bytearray()
    while pos < len(data):
        if pos + 8 > len(data):
            raise ValueError("truncated chunk header")
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        if pos + 12 + length > len(data):
            raise ValueError("truncated chunk %r" % ctype)
        chunk_data = data[pos + 8:pos + 8 + length]
        crc_stored = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])[0]
        crc_actual = zlib.crc32(ctype)
        crc_actual = zlib.crc32(chunk_data, crc_actual) & 0xFFFFFFFF
        if crc_stored != crc_actual:
            raise ValueError("bad CRC in chunk %r" % ctype)
        if ctype == b"IHDR":
            if seen_ihdr:
                raise ValueError("duplicate IHDR")
            if length != 13:
                raise ValueError("bad IHDR length")
            (width, height, bit_depth, color_type, comp, filt, interlace) = \
                struct.unpack(">IIBBBBB", chunk_data)
            if comp != 0 or filt != 0 or interlace != 0:
                raise ValueError("unsupported compression/filter/interlace")
            if bit_depth != 8 or color_type != 2:
                raise ValueError("expected 8-bit RGB, got depth %d type %d"
                                 % (bit_depth, color_type))
            if (width, height) != (WANT_W, WANT_H):
                raise ValueError("expected 1024x1024, got %dx%d"
                                 % (width, height))
            seen_ihdr = True
        elif ctype == b"IDAT":
            if not seen_ihdr:
                raise ValueError("IDAT before IHDR")
            idat.extend(chunk_data)
        elif ctype == b"IEND":
            if length != 0:
                raise ValueError("IEND must be empty")
            if pos + 12 != len(data):
                raise ValueError("trailing bytes after IEND")
            seen_iend = True
            pos += 12
            break
        pos += 12 + length
    if not seen_ihdr:
        raise ValueError("missing IHDR")
    if not seen_iend:
        raise ValueError("missing IEND trailer")
    if not idat:
        raise ValueError("missing IDAT")
    expected_raw = WANT_H * (1 + WANT_W * 3)
    try:
        raw = zlib.decompress(bytes(idat))
    except zlib.error as exc:
        raise ValueError("IDAT does not inflate: %s" % exc)
    if len(raw) != expected_raw:
        raise ValueError("IDAT inflates to %d bytes, expected %d"
                         % (len(raw), expected_raw))
    return width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("main.py: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 2
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    try:
        with open(src, "rb") as f:
            data = f.read()
    except OSError as exc:
        print("main.py: cannot read entry.png: %s" % exc, file=sys.stderr)
        return 1
    try:
        validate(data)
    except ValueError as exc:
        return fail(str(exc))
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        copy = f.read()
    if copy != data:
        return fail("copy differs from source")
    try:
        validate(copy)
    except ValueError as exc:
        return fail("copy failed re-validation: %s" % exc)
    print("main.py: ok, wrote %s (%d bytes, sha256 %s)"
          % (dst, len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
