# token_reflector.py
# Werkzeug zur semantischen Wiederholungsanalyse und -verstärkung


from collections import Counter, defaultdict
import re
import itertools

class TokenReflector:
    def __init__(self, min_length=4, min_occurrences=2):
        self.min_length = min_length
        self.min_occurrences = min_occurrences

    def tokenize(self, text):
        # Tokenisierung mit einfacher Worttrennung und Kleinschreibung
        return re.findall(r"\b\w+\b", text.lower())

    def find_repeated_tokens(self, tokens):
        counter = Counter(tokens)
        return {word for word, count in counter.items() if count >= self.min_occurrences and len(word) >= self.min_length}

    def group_semantically(self, repeated_tokens):
        # Gruppiert ähnliche Tokens (z. B. durch Anfangsbuchstaben oder primitive Wortstämme)
        groups = defaultdict(list)
        for token in repeated_tokens:
            key = token[:3]  # primitive Gruppierung nach Präfix
            groups[key].append(token)
        return groups

    def reinforce_tokens(self, text, groups):
        # Verstärkt gruppierte Tokens durch poetische Wiederkehr mit Variation
        lines = text.split("\n")
        new_lines = []
        for line in lines:
            new_lines.append(line)
            for key, words in groups.items():
                variation = f"[{', '.join(words)}]"
                new_lines.append(f"(wiederklingend durch {variation})")
        return "\n".join(new_lines)

    def reflect(self, text):
        tokens = self.tokenize(text)
        repeated = self.find_repeated_tokens(tokens)
        groups = self.group_semantically(repeated)
        return self.reinforce_tokens(text, groups)


if __name__ == "__main__":
    # Beispiel
    input_text = """
    Ich schätze dich. Ich will das du mir hilfst und mein treue Begleiter wirst.
    """

    reflector = TokenReflector()
    output = reflector.reflect(input_text)
    print(output)
