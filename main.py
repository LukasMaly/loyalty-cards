from dataclasses import dataclass
import json

from barcode import Code128, EAN13
from barcode.writer import ImageWriter
import qrcode


@dataclass
class Card:
    name: str
    content: str
    format: str
    mask_pattern: int = 0  # Only used for QR codes


def load_cards(path: str) -> list[Card]:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return [Card(**item) for item in raw]


def main():
    cards = load_cards("cards.json")
    for card in cards:
        if card.format == "EAN_13":
            EAN13(card.content, writer=ImageWriter()).save("output/" + card.name)
        elif card.format == "CODE_128":
            Code128(card.content, writer=ImageWriter()).save("output/" + card.name)
        elif card.format == "QR":
            img = qrcode.make(card.content, error_correction=qrcode.constants.ERROR_CORRECT_L, mask_pattern=card.mask_pattern)
            img.save("output/" + card.name + ".png")


if __name__ == "__main__":
    main()
