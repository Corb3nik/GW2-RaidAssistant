from discord import Color, Embed


class StaticRunEmbed(Embed):

    default_description = "HoT raid clear. React with the roles you wish to play"
    default_time = "Daily Reset + 1"
    default_composition = "TBD"

    description_template = """
        {}

        **Time**
        {}

        **Links**
        [Raid Planner](https://docs.google.com/spreadsheets/d/1ruJHWY-ZCgnk0CuEmeeBj7CmpJ6lHAcVGaV31xBjs9A/edit#gid=0)

        **Team Composition**
        {}
        """

    def __init__(self, raid):
        super().__init__()

        self.title = "HoT Raid Clear"
        self.type = "rich"
        self.color = Color.red()

        self.event_description = raid.description or self.default_description
        self.event_time = raid.time or self.default_time
        self.event_composition = raid.composition or self.default_composition

        self.description = self.description_template.format(
            self.event_description, self.event_time, self.event_composition)
