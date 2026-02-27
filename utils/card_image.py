"""
Provides a function for getting the filename for a card.
"""

from models.deck import Number, Skip, Reverse, DrawTwo, Wild, DrawFourWild


def get_card_filename(card) -> str:
    """
    Gets the filename for the image associated with a card for displaying to the user.
    """
    if isinstance(card, Number):
        return f"{card.color.name.capitalize()}_{card.number}.jpg"

    if isinstance(card, Skip):
        return f"{card.color.name.capitalize()}_Skip.jpg"

    if isinstance(card, Reverse):
        return f"{card.color.name.capitalize()}_Reverse.jpg"

    if isinstance(card, DrawTwo):
        return f"{card.color.name.capitalize()}_Draw_2.jpg"

    if isinstance(card, Wild):
        return "Wild.jpg"

    if isinstance(card, DrawFourWild):
        return "Wild_Draw_4.jpg"

    raise ValueError("Unknown card type")
