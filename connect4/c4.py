import random
from connect4.c4_buttons_menu import Buttons
from .c4_visualizer import Visualizer


class C4:
    def __init__(self, player_1, player_2, message):
        self.p1 = player_1
        self.p2 = player_2
        self.random_starter()
        self.message = message
        self.visualizer = Visualizer(self.p1, self.p2, self.message)
        self.grid = self.initialize_grid()
        self.surrender = False
        self.last_token = (0, 0)

    def random_starter(self):
        if random.randint(0, 1) == 1:
            temp = self.p2
            self.p2 = self.p1
            self.p1 = temp

    @staticmethod
    def initialize_grid():
        # c = cursor, h = no_cursor, v = void, r = p1, b = p2
        matrix = [["c", "h", "h", "h", "h", "h", "h"]]
        for x in range(6):
            matrix.append(["v", "v", "v", "v", "v", "v", "v"])
        return matrix

    def move_cursor(self, value):
        index = self.grid[0].index("c")
        if value + index < 0:
            self.grid[0][6] = "c"
            self.grid[0][0] = "h"
        elif value + index > 6:
            self.grid[0][0] = "c"
            self.grid[0][6] = "h"
        else:
            self.grid[0][index] = "h"
            self.grid[0][index + value] = "c"

    async def run(self):
        player_turn = self.p1
        while await self.turn(player_turn) != "end":
            if player_turn == self.p1:
                player_turn = self.p2
            else:
                player_turn = self.p1
        if self.surrender:
            await self.visualizer.send(
                self.grid,
                player_turn,
                adds="**" + player_turn.name + " ha scelto la resa!**",
            )

    async def turn(self, player):
        result = None
        while True:
            if result == "full":
                await self.visualizer.send(
                    self.grid,
                    player,
                    adds="La colonna è già piena, scegli un'altra colonna!",
                )
            else:
                await self.visualizer.send(self.grid, player)
            result = await self.choose_column(player, self.message)
            if result == "stop":
                if self.check_win():
                    await self.visualizer.send(
                        self.grid, player, adds="**" + player.name + " HA VINTO!**"
                    )
                    return "end"
                else:
                    await self.visualizer.send(self.grid, player)
                    return "next"
            elif result == "lost":
                self.surrender = True
                return "end"

    async def choose_column(self, player, message):
        view = Buttons(player.name)
        await message.edit(view=view)
        await view.wait()
        if view.value == -1 or view.value == +1:
            self.move_cursor(view.value)
            return "loop"
        elif view.value == "drop":
            if self.drop(player):
                return "stop"
            else:
                return "full"
        else:
            return "lost"

    def drop(self, player):
        index = self.grid[0].index("c")
        depth = 6
        token = "r" if player.name == self.p1.name else "b"
        while depth > 0:
            if self.grid[depth][index] == "v":
                self.grid[depth][index] = token
                self.last_token = (depth, index)
                return True
            else:
                depth -= 1
        return False

    def check_win(self):
        return self.check_row() or self.check_column() or self.check_diagonals()

    def check_row(self):
        previous = "v"
        counter = 0
        for x in self.grid[self.last_token[0]]:
            if x == previous and previous != "v":
                counter += 1
            else:
                previous = x
                counter = 1
            if counter == 4:
                return True
        return False

    def check_column(self):
        previous = "v"
        counter = 0
        for x in self.grid:
            if x[self.last_token[1]] == previous and previous != "v":
                counter += 1
            else:
                previous = x[self.last_token[1]]
                counter = 1
            if counter == 4:
                return True
        return False

    def check_diagonals(self):
        counter = 1
        bl_tr_diagional = self.last_token
        tl_br_diagional = self.last_token
        # calculating the first avaible spot for the diagonal
        while True:
            if tl_br_diagional[0] - 1 >= 1 and tl_br_diagional[1] - 1 >= 0:
                tl_br_diagional = (tl_br_diagional[0] - 1, tl_br_diagional[1] - 1)
            else:
                break
        previous = self.grid[tl_br_diagional[0]][tl_br_diagional[1]]
        next_x = tl_br_diagional[0] + 1
        next_y = tl_br_diagional[1] + 1
        while True:
            if next_x <= 6 and next_y <= 6:
                if self.grid[next_x][next_y] == previous and previous != "v":
                    counter += 1
                else:
                    counter = 1
                    previous = self.grid[next_x][next_y]
                if counter == 4:
                    return True
            else:
                break
            next_x += 1
            next_y += 1

        # calculating the first avaible spot for the diagonal
        counter = 1
        while True:
            if bl_tr_diagional[0] + 1 <= 6 and bl_tr_diagional[1] - 1 >= 0:
                bl_tr_diagional = (bl_tr_diagional[0] + 1, bl_tr_diagional[1] - 1)
            else:
                break
        previous = self.grid[bl_tr_diagional[0]][bl_tr_diagional[1]]
        next_x = bl_tr_diagional[0] - 1
        next_y = bl_tr_diagional[1] + 1
        while True:
            if next_x >= 1 and next_y <= 6:
                if self.grid[next_x][next_y] == previous and previous != "v":
                    counter += 1
                else:
                    previous = self.grid[next_x][next_y]
                    counter = 1
                if counter == 4:
                    return True
            else:
                break
            next_x -= 1
            next_y += 1
        return False
