from dataclasses import dataclass
import json

import barcode
from barcode.writer import ImageWriter
import qrcode


@dataclass
class Card:
    name: str
    type: str
    data: str
    mask: int = 0  # Only used for QR codes


def load_cards(path: str) -> list[Card]:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return [Card(**item) for item in raw]


def main():
    cards = load_cards("cards.json")
    for card in cards:
        if card.type == "qrcode":
            img = qrcode.make(card.data, version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, mask_pattern=card.mask)
        else:
            img = barcode.get(card.type, card.data, writer=ImageWriter()).render(writer_options={'write_text': False})
        img.save("output/" + card.name + ".png")


if __name__ == "__main__":
    main()
