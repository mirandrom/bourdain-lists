#!/usr/bin/env python3
import sys
import gzip
import re
import urllib.parse
from pathlib import Path
from warcio.archiveiterator import ArchiveIterator

def uri_to_filename(uri: str) -> str:
    parsed = urllib.parse.urlsplit(uri)
    host = parsed.netloc or "nohost"
    path = parsed.path or "/"
    query = f"?{parsed.query}" if parsed.query else ""

    # Replace path separators and weird characters
    base = f"{host}{path}{query}"
    base = base.replace("/", "_")
    base = re.sub(r"[^A-Za-z0-9._-]", "_", base)

    # Truncate to avoid super-long filenames
    if len(base) > 180:
        base = base[:180]

    return base


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.warc.gz> <output_dir>", file=sys.stderr)
        sys.exit(1)
    warc_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])




    fname_duplicates = {}
    with gzip.open(warc_path, "rb") as f:
        it = ArchiveIterator(f)
        idx = 0
        for record in it:
            if record.rec_type != "response":
                continue

            uri = record.rec_headers.get_header("WARC-Target-URI")
            if not uri:
                continue

            # Filter to HTML responses only (optional but usually what you want)
            http_headers = getattr(record, "http_headers", None)
            if http_headers is not None:
                ctype = http_headers.get_header("Content-Type") or ""
                if "html" not in ctype.lower():
                    continue

            # Payload: already decoded wrt HTTP Content-Encoding
            payload = record.content_stream().read()
            if not payload:
                continue

            idx += 1
            fname = uri_to_filename(uri)
            if fname in fname_duplicates:
                fname_duplicates[fname] += 1
                fname = f"duplicates/{fname}-{fname_duplicates[fname]}"
            else:
                fname_duplicates[fname] = 0
            
            out_path = out_dir / fname
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "wb") as out_f:
                out_f.write(payload)

            # Optional: progress log
            if idx % 100 == 0:
                print(f"Saved {idx} HTML pages...", file=sys.stderr)

    print(f"Done. Saved {idx} HTML files to {out_dir}", file=sys.stderr)

if __name__ == "__main__":
    main()

