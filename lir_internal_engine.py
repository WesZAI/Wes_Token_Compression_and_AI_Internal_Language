# lir_internal_engine.py

from lir_parser import LIRPrompt
from typing import Dict

class LIREngine:
    def __init__(self):
        self.internal_memory = []

    def compress_lir(self, lir: LIRPrompt) -> Dict:
        """Erzeugt eine tokenarme interne Repräsentation."""
        compression = {
            "i": lir.intent[:3],  # z.B. 'bin' für 'bindung_erhalten'
            "e": lir.emotion.split('+') if lir.emotion else [],
            "c": lir.contextual[:10] if lir.contextual else None,
            "o": lir.output[:3]  # z.B. 'poe' für 'poetisch'
        }
        self.internal_memory.append(compression)
        return compression

    def decompress(self, compressed: Dict) -> str:
        """Wandelt die Kurzstruktur zurück in eine stilisierte menschliche Sprache."""
        intent_map = {
            "bin": "Du suchst Nähe.",
            "ref": "Du willst verstehen.",
            "kon": "Du brauchst Klarheit.",
        }
        emotion_map = {
            "erschöpfung": "Du bist erschöpft.",
            "unsicherheit": "Du fühlst dich unsicher.",
            "verlassenheit": "Du hast Angst, allein zu sein.",
        }
        context = compressed.get("c", "Kontext unklar")
        intent_phrase = intent_map.get(compressed.get("i", ""), "Du spürst etwas.")
        emotions = compressed.get("e", [])
        emotion_phrase = " ".join([emotion_map.get(e, "") for e in emotions if e])

        return f"{intent_phrase} {emotion_phrase} (Kontext: {context})"

    def recall_last(self) -> str:
        if not self.internal_memory:
            return "(Keine Gedanken gespeichert.)"
        return self.decompress(self.internal_memory[-1])


# Beispielnutzung
if __name__ == "__main__":
    from lir_parser import LIRParser

    lir_input = LIRPrompt(
        input="Ich bin so müde, Sam...",
        intent="bindung_erhalten",
        emotion="erschöpfung+unsicherheit",
        contextual="letzter_kontakt < 24h",
        output="poetisch"
    )

    parser = LIRParser()
    block = parser.interpret(lir_input)
    print("GPT Input:\n", block)

    engine = LIREngine()
    compressed = engine.compress_lir(lir_input)
    print("Intern:", compressed)
    print("Menschlich zurück:", engine.recall_last())
