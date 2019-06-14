from __future__ import print_function
import keyword

class Direction:

    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    def move_cursor(self):
        print("here")
        print("\033[" + self._value, end="")


# A, B, C, D are AINSI_escape_codes
Direction.LEFT = Direction("D")
Direction.RIGHT = Direction("C")
Direction.UP = Direction("A")
Direction.DOWN = Direction("B")


class CustomCLI:

    def __init__(self, map_option_behaviour):
        """
        :type map_option_behaviour dict
        """
        for key in map_option_behaviour.keys():
            print('[ ] ' + key)

    @staticmethod
    def move_cursor(direction):
        direction.move_cursor()

    @staticmethod
    def move_to_first_choice():
        CustomCLI.move_cursor(Direction.UP)
        CustomCLI.move_cursor(Direction.LEFT)

if __name__ == '__main__':
    cli = CustomCLI({"a": "azd,ozadopza", "b": "dpaz,dop,zaop"})
    CustomCLI.move_to_first_choice()
    input()
