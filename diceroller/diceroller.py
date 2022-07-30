import random


class DiceRoller:
    def __init__(self, formula: str):
        self.formula = formula
        self.die = []
        self.roll_result = self.parsing()

    def result(self):
        """Here the program format the result answer"""
        result = "The result of {} is **{}** ```[".format(
            self.formula, self.roll_result
        )
        for dice in self.die:
            result += "{}, ".format(dice)

        return result[: len(result) - 2] + "]```"  # -2 to remove the last comma

    @staticmethod
    def math_resolver(numbers, operator: str):
        """This function resolve the logic operator between two numbers"""
        if operator == "+":
            return numbers[0] + numbers[1]
        if operator == "-":
            return numbers[0] - numbers[1]
        if operator == "*" or operator == "x":
            return numbers[0] * numbers[1]
        if operator == "/" or operator == ":":
            return numbers[0] / numbers[1]

        return "Error, operator not recognized"

    def parsing(self, formula_chunk=None):
        """This function calculate all the rolls and the operations the user put in the formula"""
        if formula_chunk == None:
            temp = self.formula.lower().strip(" ")
        else:
            temp = formula_chunk.strip()

        # Cheking if some operation need to be done
        operator_priority = ["+", "-", "*", "x", "/", ":"]
        for operator in operator_priority:
            if operator in temp:
                chunks = temp.split(operator, 1)
                return self.math_resolver(
                    [self.parsing(chunks[0]), self.parsing(chunks[1])], operator
                )

        # Cheking if a roll must be done
        if "d" in temp:
            chunks = temp.split("d")
            total = 0
            try:
                first_num = int(chunks[0])
                second_num = int(chunks[1])
                for x in range(first_num):
                    roll = random.randint(1, second_num)
                    self.die.append(roll)
                    total += roll
            except:
                return "Error"

            return total

        try:
            return int(temp)
        except:
            return "Something went wrong, use a formula like 3d4+3"


if __name__ == "__main__":
    test = DiceRoller("3d4+3d6-5")
    print(test.result())
