import nextcord

class Buttons(nextcord.ui.View):
    def __init__(self, player, *, timeout=180):
        super().__init__(timeout=timeout)
        self.value = None
        self.player = player

    @nextcord.ui.button(label="⬅️", style=nextcord.ButtonStyle.gray)
    async def previous(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = -1
        self.stop()

    @nextcord.ui.button(label="⬇️", style=nextcord.ButtonStyle.green)
    async def drop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = "drop"
        self.stop()

    @nextcord.ui.button(label="➡️", style=nextcord.ButtonStyle.gray)
    async def next(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = +1
        self.stop()

    @nextcord.ui.button(label="💀", style=nextcord.ButtonStyle.red)
    async def leave(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = "surrender"
        self.stop()

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        if self.player == interaction.user.name or self.player == "Tester M":
            return True
        else:
            return False

    async def on_timeout(self) -> None:
        self.value = "surrender"