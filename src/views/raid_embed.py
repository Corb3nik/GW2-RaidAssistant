from discord import Color, Embed
from typing import Optional


class RaidEmbed(Embed):

    default_description = "React for headcount"
    default_time = "Daily Reset + 1"

    description_template = """
        {}

        **Time**
        {}
        """

    def __init__(self, title: Optional[str], description: Optional[str], time: Optional[str]):
        super().__init__()

        self.title = title or "Raid"
        self.type = "rich"
        self.color = Color.red()

        self.event_description = description or self.default_description
        self.event_time = time or self.default_time

        self.description = self.description_template.format(
            self.event_description, self.event_time)
