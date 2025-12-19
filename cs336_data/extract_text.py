from fastwarc.warc import ArchiveIterator, WarcRecordType
from fastwarc.stream_io import FileStream
from resiliparse.extract.html2text import extract_plain_text
from resiliparse.parse.encoding import detect_encoding

def extracts_text_from_byte_string(html_bytes: bytes):
    encoding = detect_encoding(html_bytes)
    return extract_plain_text(html_bytes.decode(encoding, errors="ignore"))

if __name__ == "__main__":
    with open("../../CC-MAIN-20250417135010-20250417165010-00065.warc.gz", "rb") as f:
        with open("../../CC-MAIN-20250417135010-20250417165010-00065.warc.txt", "w") as f_text:
            for record in ArchiveIterator(f):
                f_text.writelines([f"Record Type: {record.record_type.name}"])
                f_text.writelines([f"Record Type: {record.record_type.name}"])

                if record.headers.get('WARC-Target-URI'):
                    f_text.writelines([f"Target URI: {record.headers['WARC-Target-URI']}"])
                    
                f_text.writelines(["-" * 50])
                f_text.writelines([extracts_text_from_byte_string(record.reader.read())])

            