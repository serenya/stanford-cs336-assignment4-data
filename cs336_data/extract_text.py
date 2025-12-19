from fastwarc.warc import ArchiveIterator, WarcRecordType
from fastwarc.stream_io import FileStream
from resiliparse.extract.html2text import extract_plain_text
from resiliparse.parse.encoding import detect_encoding

def extracts_text_from_byte_string(html_bytes: bytes):
    encoding = detect_encoding(html_bytes)
    print(encoding)
    return extract_plain_text(html_bytes.decode(encoding))

if __name__ == "__main__":
    with open("../../CC-MAIN-20250417135010-20250417165010-00065.warc.gz", "rb") as f:
        
        for record in ArchiveIterator(f):
            # Print record type and target URI if available
            print(f"Record Type: {record.record_type.name}")
            if record.headers.get('WARC-Target-URI'):
                print(f"Target URI: {record.headers['WARC-Target-URI']}")
            print("-" * 50)
            text = extracts_text_from_byte_string(record.reader.read())

            