import re
from typing import Tuple


EMAIL_RE = re.compile(r"""(?xi)
    ([a-z0-9!#$%&'*+/=?^_`{|}~-]+      # local part
      (?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*
    @
    (?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}  # domain
      |\[(?:\d{1,3}\.){3}\d{1,3}\])                  # or literal IPv4
    )
""")


def mask_emails(text: str) -> Tuple[str, int]:
    """Replace all email addresses in ``text`` with the token
    "|||EMAIL_ADDRESS|||" and return (masked_text, count).

    The regex used is a reasonably strict, commonly used email pattern and
    should cover most real-world addresses while avoiding many false
    positives.
    """
    if not text:
        return text, 0

    def _repl(match: re.Match) -> str:
        return "|||EMAIL_ADDRESS|||"

    masked_text, n = EMAIL_RE.subn(_repl, text)
    return masked_text, n


PHONE_RE = re.compile(r"""(?x)
    (?<!\w)                           # not preceded by a word char
    (?:\+?\d{1,3}[-.\s]*)?          # optional country code
    (?:\(?\d{2,4}\)?[-.\s]*)?      # optional area code (with parentheses)
    (?:\d{3}[-.\s]*\d{4}             # 7-digit like 555-1234 or 5551234
     |\d{2}[-.\s]*\d{3}[-.\s]*\d{3} # variants like 12-345-678
     |\d{7,10}                         # plain run of 7-10 digits
    )
    (?!\w)                            # not followed by a word char
""")


def mask_phone_numbers(text: str) -> Tuple[str, int]:
    """Replace phone-number-like tokens in ``text`` with the token
    "|||PHONE_NUMBER|||" and return (masked_text, count).

    This uses a permissive but conservative regex that matches common
    international, spaced, dotted, dashed, and parenthesized formats.
    """
    if not text:
        return text, 0

    def _repl(_m: re.Match) -> str:
        return "|||PHONE_NUMBER|||"

    masked_text, n = PHONE_RE.subn(_repl, text)
    return masked_text, n

import re as _re

IP_RE = _re.compile(r"(?<!\w)(?:"
                    r"(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}"
                    r"(?:25[0-5]|2[0-4]\d|1?\d?\d)(?!\w)")

def mask_ips(text: str) -> Tuple[str, int]:
    """Replace IPv4 addresses with |||IP_ADDRESS||| and return (text, count)."""
    if not text:
        return text, 0
    def _r(_m: _re.Match) -> str:
        return "|||IP_ADDRESS|||"
    masked, n = IP_RE.subn(_r, text)
    return masked, n


if __name__ == "__main__":
    sample = (
        "Contact us at help@example.com or sales@my-company.co.uk for info. "
        "You can also call +1 (555) 123-4567 or 020 7946 0958."
    )
    # add some IPs to the sample for demonstration
    sample = sample + " Connect to 192.168.1.10 or 8.8.8.8 for DNS."
    masked_e, cnt_e = mask_emails(sample)
    masked_p, cnt_p = mask_phone_numbers(sample)
    # mask IPs
    

    masked_i, cnt_i = mask_ips(sample)
    print("emails masked:", masked_e)
    print("email replacements:", cnt_e)
    print("phones masked:", masked_p)
    print("phone replacements:", cnt_p)
    print("ips masked:", masked_i)
    print("ip replacements:", cnt_i)