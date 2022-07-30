class TextCommand:
    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.format = True  # This must be set False on commands that need to keep the text formatting from the user

    async def run(self):
        # Here every command should execute themself and send the message to the channel
        # A custom run must be created if the desired channel is not the one where the user put the input
        await self.message.channel.send(self.execute())

    def execute(self):
        # Here ever command should contain it's resolving logic
        pass

    def parse_message(self, command):
        # Here every command should parse the message itself if the self.format is set to True
        self.parsed_content = self.message.content[4:].lower().strip()
        self.parsed_content = " ".join(
            word for word in self.parsed_content.split(" ") if word != " "
        )  # Removing all the eccessive space and lowercasing it to reach a standard for every command
        for key in command.keywords:
            if self.parsed_content.startswith(key):
                self.parsed_content = self.parsed_content.replace(key + " ", "")


class Ping(TextCommand):
    keywords = ["ping"]

    async def run(self):
        await self.message.channel.send(self.client.latency)


class Roller(TextCommand):
    keywords = ["roll"]

    def execute(self):
        from diceroller.diceroller import DiceRoller

        roller = DiceRoller(self.parsed_content)
        return roller.result()


class Echo(TextCommand):
    keywords = ["echo"]

    def __init__(self, client, message):
        super().__init__(client, message)
        self.format = False

    def parse_message(self, command):
        self.parsed_content = " ".join(self.message.content.split(" ")[2:])

    def execute(self):
        return self.parsed_content
