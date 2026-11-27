"""Validate and deliver the make.fun news-image entry for 27 November 2026.

The entry image is a 1024x1024 newspaper front page, "THE WORLD TODAY --
FRIDAY, 27 NOVEMBER 2026", summing up the day's world news in 14 stories:
a hero panel on the drones over Kuwait in which two Italian technicians
were killed, plus panels on Gaza, the Ibiza tanker, Black Friday, and chess,
and an ALSO TODAY footer covering UK migration, Depardieu, Zelenskyy, the
India court ruling, the Hormuz tanker, and the Hong Kong anniversary.

The image lives in this repository as ``entry.png`` (756,087 bytes). This
program reads it, checks it thoroughly, and copies it to the output
directory make.fun expects::

    $MAKEFUN_OUTPUT_DIR/entry.png        (default: /output/entry.png)

Only the Python standard library is used. Any problem -- a bad signature,
an oversized file, a dimension over 1024, a chunk with a wrong CRC, a
missing or misplaced IEND chunk, a truncated file, or a written copy that
does not match the source byte for byte -- is a hard failure: the program
prints an error to stderr and exits non-zero. On success it prints the
byte count and the dimensions.
"""

from __future__ import annotations

import os
import struct
import sys
import zlib
from pathlib import Path

# The eight bytes every PNG file starts with.
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

# make.fun's limits for this bounty.
MAX_FILE_BYTES = 1_048_576
MAX_SIDE_PIXELS = 1024

# Chunk layout: 4-byte big-endian length, 4-byte type, payload, 4-byte CRC.
_CHUNK_HEADER = 8   # length + type
_CHUNK_FOOTER = 4   # CRC
_IHDR_PAYLOAD = 13


class EntryProblem(Exception):
    """Raised when the entry image (or its written copy) fails a check."""


def _u32be(raw: bytes) -> int:
    """Decode one big-endian unsigned 32-bit integer."""
    return struct.unpack(">I", raw)[0]


def _crc_matches(chunk_type: bytes, payload: bytes, stored_crc: int) -> bool:
    """True when the stored CRC equals the CRC of type + payload."""
    return zlib.crc32(chunk_type + payload) & 0xFFFFFFFF == stored_crc


def examine_png(blob: bytes) -> tuple[int, int]:
    """Walk a PNG byte string end to end and return ``(width, height)``.

    Checks, in order: overall size, the PNG signature, a well-formed
    first chunk (IHDR, exactly 13 payload bytes, sane dimensions), then
    every chunk in turn -- length fields that stay inside the file, a
    matching CRC for each chunk -- and finally that the file ends exactly
    at the end of the IEND chunk, with no trailing bytes and no chunk
    after IEND.
    """
    if len(blob) > MAX_FILE_BYTES:
        raise EntryProblem(
            f"entry.png is {len(blob)} bytes, over the limit of "
            f"{MAX_FILE_BYTES} bytes"
        )
    if len(blob) < len(PNG_MAGIC) + _CHUNK_HEADER + _IHDR_PAYLOAD + _CHUNK_FOOTER:
        raise EntryProblem("entry.png is too short to be a PNG file")
    if blob[: len(PNG_MAGIC)] != PNG_MAGIC:
        raise EntryProblem("entry.png does not start with the PNG signature")

    width = height = 0
    offset = len(PNG_MAGIC)
    saw_iend = False

    while True:
        if saw_iend:
            # A chunk after IEND, or bytes after IEND, is not allowed.
            raise EntryProblem("data found after the IEND chunk")
        if offset + _CHUNK_HEADER > len(blob):
            raise EntryProblem("truncated PNG: chunk header runs past the end")
        payload_len = _u32be(blob[offset : offset + 4])
        chunk_type = blob[offset + 4 : offset + 8]
        payload_start = offset + _CHUNK_HEADER
        payload_end = payload_start + payload_len
        chunk_end = payload_end + _CHUNK_FOOTER
        if chunk_end > len(blob):
            raise EntryProblem(
                f"truncated PNG: {chunk_type.decode('latin-1')} chunk "
                f"runs past the end of the file"
            )

        payload = blob[payload_start:payload_end]
        stored_crc = _u32be(blob[payload_end:chunk_end])
        if not _crc_matches(chunk_type, payload, stored_crc):
            raise EntryProblem(
                f"bad CRC in {chunk_type.decode('latin-1')} chunk"
            )

        if offset == len(PNG_MAGIC):
            if chunk_type != b"IHDR":
                raise EntryProblem("first chunk is not IHDR")
            if payload_len != _IHDR_PAYLOAD:
                raise EntryProblem(
                    f"IHDR payload is {payload_len} bytes, expected "
                    f"{_IHDR_PAYLOAD}"
                )
            width = _u32be(payload[0:4])
            height = _u32be(payload[4:8])
            if width == 0 or height == 0:
                raise EntryProblem("PNG has a zero width or height")
            if width > MAX_SIDE_PIXELS or height > MAX_SIDE_PIXELS:
                raise EntryProblem(
                    f"dimensions {width}x{height} exceed the "
                    f"{MAX_SIDE_PIXELS}x{MAX_SIDE_PIXELS} limit"
                )

        if chunk_type == b"IEND":
            if payload_len != 0:
                raise EntryProblem(
                    f"IEND chunk carries {payload_len} payload bytes, "
                    f"expected 0"
                )
            saw_iend = True
            if chunk_end != len(blob):
                raise EntryProblem("trailing bytes after the IEND chunk")
            break

        offset = chunk_end

    if not saw_iend:
        raise EntryProblem("PNG has no IEND chunk")
    return width, height


def _source_path() -> Path:
    """The repository's entry.png, sitting beside this program."""
    return Path(__file__).resolve().parent / "entry.png"


def _output_path() -> Path:
    """Where make.fun wants the entry: $MAKEFUN_OUTPUT_DIR/entry.png."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return Path(out_dir) / "entry.png"


def run() -> int:
    """Read, validate, deliver, and re-verify the entry image."""
    source = _source_path()
    try:
        original = source.read_bytes()
    except OSError as exc:
        print(f"error: cannot read {source}: {exc}", file=sys.stderr)
        return 1

    try:
        width, height = examine_png(original)
    except EntryProblem as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    target = _output_path()
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(original)
        written = target.read_bytes()
    except OSError as exc:
        print(f"error: cannot write {target}: {exc}", file=sys.stderr)
        return 1

    if written != original:
        print(
            f"error: written copy {target} differs from {source}",
            file=sys.stderr,
        )
        return 1

    try:
        re_width, re_height = examine_png(written)
    except EntryProblem as exc:
        print(f"error: written copy failed validation: {exc}", file=sys.stderr)
        return 1
    if (re_width, re_height) != (width, height):
        print(
            "error: written copy dimensions "
            f"{re_width}x{re_height} differ from source {width}x{height}",
            file=sys.stderr,
        )
        return 1

    print(
        f"entry.png OK: {len(original)} bytes, {width}x{height}, "
        f"delivered to {target}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
