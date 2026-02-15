import random

from discord import Colour
import discord


class BaseViews:
    def __init__(self):
        self._pretty_colors = [0xd69cbc, 0x51074a, 0xff007f, 0x40e0e0, 0x98ff98, 0xfff44f, 0xcdffdb, 0xcfafdd, 0xb9cefb,
                               0xffb8ea, 0Xb4be89, 0Xcb736e, 0Xfe7e0f, 0Xfaebd7, 0X008080]
        self._cool_gifs = [
            "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjVoYXFxM3g2ZWRsaDYyOHozOW53MTYxd2J6MmtrejhnNm1vNG90dyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/wrmVCNbpOyqgJ9zQTn/giphy.gif",
            "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExajFhZTQwaWpoN3E5dTltYmxsZGF6bXJ0Y2tuYXhmNGhuYTl0ajZtZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1351TySLYhyXII/giphy.gif",
            "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbGJpcWs1OWdvZWIxbzIyMnpyZDJrM2cwY3ozOGgzaTF4N25sd2Z3dyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/KbdF8DCgaoIVC8BHTK/giphy.gif",
        ]
        self._error_color = Colour(0xD21F3C)
        self._footer = "Uno Discord Bot • Class Project for UWB 360"

    def get_random_color(self) -> Colour:
        return random.choice(self._pretty_colors)

    def get_random_gif(self) -> str:
        return random.choice(self._cool_gifs)

    def update_embed(self, title: str, desc: str, gif=True) -> discord.Embed:
        return self._build_embed("UPDATE: " + title, desc=desc, color=self.get_random_color(), gif=True,
                                 time_stamp=True)

    def error_embed(self, title: str, desc: str, gif=True) -> discord.Embed:
        return self._build_embed("ERROR: " + title, desc, self._error_color, True)

    def _build_embed(self, title: str, desc: str, color: Colour, gif: bool = True, footer: bool = True,
                     time_stamp: bool = True, random_gif: bool = False,
                     author: discord.Interaction.user = None) -> discord.Embed:
        embed = discord.Embed(
            title=title,
            description=desc,
            colour=color,
        )

        if gif:
            embed.set_image(url=self.get_random_gif())

        if footer:
            embed.set_footer(text=self._footer)

        if time_stamp:
            embed.timestamp = discord.utils.utcnow()

        if random_gif:
            embed.set_image(url=self.get_random_gif())

        if author:
            embed.set_author(name=author.name, icon_url=author.avatar.url)

        return embed
