import unicodedata

def generate_utf8_table(start=0x0020, end=0x024F, include_nonprintable=False):
    """
    Erstellt eine UTF-8-Tabelle von Unicode-Codepoints im angegebenen Bereich.
    Standardbereich: Basic Latin bis Latin Extended-B
    """

    print(f"{'Char':^6} {'Unicode':^10} {'UTF-8 (hex)':^15} {'Name':^40}")
    print("-" * 80)

    for codepoint in range(start, end + 1):
        char = chr(codepoint)
        try:
            name = unicodedata.name(char)
        except ValueError:
            if not include_nonprintable:
                continue
            name = "<non-printable>"

        utf8_bytes = char.encode("utf-8")
        utf8_hex = " ".join(f"{b:02X}" for b in utf8_bytes)

        print(f"{char:^6} U+{codepoint:04X}   {utf8_hex:<15} {name}")

if __name__ == "__main__":
    # Beispiel: Basic Latin (U+0020–U+007F) und Latin-1 Supplement (U+00A0–U+00FF)
    generate_utf8_table(start=0x0020, end=0x00FF)
