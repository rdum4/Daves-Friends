#!/usr/bin/python3

import atheris

with atheris.instrument_imports():
  from models import deck
  from models.deck import Color
  import sys

def create_random_card(fdp):
  card_types = [0, 1, 2, 3, 4, 5]
  card_type = card_types[fdp.ConsumeIntInRange(0, 4)]
  colors = [Color.RED, Color.YELLOW, Color.BLUE, Color.GREEN]
  color = colors[fdp.ConsumeIntInRange(0, 3)]

  match card_type:
    case 0:
      number = fdp.ConsumeIntInRange(0, 9)
      return deck.Number(color, number)
    case 1:
      if fdp.ConsumeBool():
        color = None
      return deck.Wild(color)
    case 2:
      if fdp.ConsumeBool():
        color = None
      return deck.DrawFourWild(color)
    case 3:
      return deck.Skip(color)
    case 4:
      return deck.DrawTwo(color)
    case 5:
      return deck.Reverse(color)

def TestDeck(data):
  fdp = atheris.FuzzedDataProvider(data)

  card1 = create_random_card(fdp)
  card2 = create_random_card(fdp)
  
  deck.can_play_card(card1, card2)

atheris.Setup(sys.argv, TestDeck)
atheris.Fuzz()
