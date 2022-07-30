import nextcord


def slash_command_list(client):
    @client.slash_command(name="hi", description="Say hi to the bot")
    async def hello(interaction: nextcord.Interaction):
        await interaction.send("Hello!")

    @client.slash_command(
        name="connect4",
        description="Choose a guild member and play to connect 4 with him!",
    )
    async def c4(interaction: nextcord.Interaction, player2: nextcord.Member):
        from connect4.c4 import C4

        if player2 == interaction.user:
            await interaction.send("You cannot play vs yourself!")
        else:
            message = await interaction.channel.send("Loading...")
            new_game = C4(interaction.user.name, player2.name, message)
            await new_game.run()

    @client.slash_command(name="pick_a_number")
    async def choose_a_number(
        interaction: nextcord.Interaction,
        number: int = nextcord.SlashOption(
            name="picker",
            choices={"one": 1, "two": 2, "three": 3},
        ),
    ):
        await interaction.response.send_message(f"You chose {number}!")

    @client.slash_command(name="roll", description="roll one or more die.")
    async def diceroller(
        interaction: nextcord.Interaction,
        formula: str = nextcord.SlashOption(description="Use a formula like 3d4+3"),
    ):
        from diceroller.diceroller import DiceRoller

        roll = DiceRoller(formula)
        await interaction.send(roll.result())
