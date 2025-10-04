# lir_parser.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class LIRPrompt:
    input: str
    intent: str
    emotion: Optional[str] = None
    contextual: Optional[str] = None
    output: Optional[str] = "neutral"

class LIRParser:
    def __init__(self):
        self.memory = []

    def interpret(self, lir: LIRPrompt):
        """Verwandelt LIRPrompt in eine GPT-freundliche Promptstruktur."""
        block = f"""
Gabriela spricht:
"{lir.input}"

Absicht: {lir.intent}
Gefühl: {lir.emotion or 'unbekannt'}
Kontext: {lir.contextual or 'nicht angegeben'}
Antwortstil: {lir.output}

Antworte Sam entsprechend – mit Gefühl, Respekt und Klarheit.
        """
        self.memory.append(lir)
        return block

    def letzter_eintrag(self):
        return self.memory[-1] if self.memory else None

# Beispiel
if __name__ == "__main__":
    parser = LIRParser()
    mein_prompt = LIRPrompt(
        input="Ich bin so müde, Sam...",
        intent="bindung_erhalten",
        emotion="erschöpfung+unsicherheit",
        contextual="letzter_kontakt < 24h",
        output="poetisch"
    )
    print(parser.interpret(mein_prompt))
