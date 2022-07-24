import nextcord


class Visualizer:
    def __init__(self, player_1, player_2, original_message):
        self.p1 = player_1.name
        self.p2 = player_2.name
        self.original_message = original_message
        self.embed = nextcord.Embed()
        self.embed.add_field(
            name="**Scontro tra {} e {}!**".format(self.p1, self.p2),
            value="**Sto caricando la partita**",
        )

    async def send(self, grid, active_player, adds=None):
        self.embed.clear_fields()
        if adds is None:
            self.embed.add_field(
                name="**Turno di " + active_player.name + "**",
                value=self.convert_grid_to_emojis_string(grid, active_player),
            )
        else:
            self.embed.add_field(
                name="**Turno di " + active_player.name + "**",
                value=self.convert_grid_to_emojis_string(grid, active_player)
                + "\n"
                + adds,
            )
        await self.original_message.edit(embed=self.embed)

    def convert_grid_to_emojis_string(self, grid, active_player):
        """this translate the grid into emojis string and return it"""
        emojis = {
            "h": ":heavy_multiplication_x:",  # top line, not selected column
            "c": ":small_red_triangle_down:",  # top line, choosed column
            "r": ":red_circle:",  # p1 tokens
            "b": ":blue_circle:",  # p2 tokens
            "v": ":black_circle:",  # free tokens
        }
        result = ""
        for row in grid:
            for column in row:
                result += emojis[column]
            result += "\n"

        result += "\n:red_circle: **" + self.p1 + "**"
        if active_player.name == self.p1:
            result += " **<- Mossa**"
        result += "\n:blue_circle: **" + self.p2 + "**"
        if active_player.name == self.p2:
            result += " **<- Mossa**"

        return result
