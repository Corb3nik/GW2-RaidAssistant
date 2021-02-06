from discord import Color, Embed


class RaidEmbed(Embed):

    default_description = "react for headcount"
    default_time = "Daily Reset + 1"

    description_template = """
        {}

        **Time**
        {}
        """

    def __init__(self, raid):
        super().__init__()

        self.title = raid.title or "Raid"
        self.type = "rich"
        self.color = Color.red()

        self.event_description = raid.description or self.default_description
        self.event_time = raid.time or self.default_time

        self.description = self.description_template.format(
            self.event_description, self.event_time)
