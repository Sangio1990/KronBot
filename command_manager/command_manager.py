from commands.text_commands import *


class CommandManager:
    command_list = [Ping, Roller, Echo]

    def __init__(self, client) -> None:
        self.client = client

    def is_a_command(self, user_string):
        for command in self.command_list:
            for key in command.keywords:
                if key in user_string.lower():
                    return command
        return False

    async def manage_command(self, message):
        command = self.is_a_command(message.content)
        if not command:
            return
        command = command(self.client, message)
        command.parse_message(command)
        await command.run()
