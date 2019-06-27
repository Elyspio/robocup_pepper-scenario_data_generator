from __future__ import print_function

import time
from copy import deepcopy
from threading import Thread

import keyboard
from colorama import Fore, init as colorama_init

colorama_init()

checked_char = Fore.GREEN + 'V' + Fore.RESET
unchecked_char = Fore.RED + 'X' + Fore.RESET


class Direction:

    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    def move_cursor(self):
        print("\x1b[" + self._value, end="")


# A, B, C, D are AINSI_escape_codes
Direction.LEFT = Direction("D")
Direction.RIGHT = Direction("C")
Direction.UP = Direction("A")
Direction.DOWN = Direction("B")


class CustomCLI:

    def __init__(self, main_title, behaviours):
        """
        :type behaviours list
        """
        self.initial_pos = {'x': 2, 'y': 1}

        self.behaviour_list = behaviours

        for behaviour in self.behaviour_list:
            if not 'callback' in behaviour:
                self.initial_pos['y'] += 1
            else:
                break

        self.behaviour_list.append({'main': "Confirm", 'description': "Validate your actions"})
        self.key_map_listed = [key for key in self.behaviour_list]

        self.map_length = len(self.behaviour_list)

        self.cursor_pos = {'x': 1, 'y': 1}

        self.offset = {'x': 0, 'y': 1}

        self.checked_cases = []
        # Thread(target=self.wait_key).start()

        self.callback_todo = []

        self.clear_screen()
        self.move_to(1, 1)
        for behaviour in self.behaviour_list:  # type: dict

            if 'flags' in behaviour:
                if 'title' in behaviour['flags']:
                    separator = "-" * 10
                    print("{2}{0}{1:^20}{0}{3}".format(separator, behaviour['main'], Fore.CYAN, Fore.RESET),
                          end="\n")

            if 'description' in behaviour:
                print('[{0:}] {1:} : {2:40}'.format(unchecked_char, behaviour['main'], behaviour['description']),
                      end="\n")

        self.move_to_first_choice()

        keyboard.on_release_key('Up', self.upper_action)
        keyboard.on_release_key('Down', self.downer_action)
        keyboard.on_release_key('Space', self.space_action)

        Thread(target=self.prevent_stop).start()

    def move_cursor(self, direction, nb=1):
        if (direction == Direction.UP):
            self.cursor_pos['y'] -= nb
        elif (direction == Direction.DOWN):
            self.cursor_pos['y'] += nb
        for _ in range(nb):
            direction.move_cursor()

    @staticmethod
    def prevent_stop():
        while True:
            if keyboard.is_pressed("ctrl+c"):
                exit(0)
            time.sleep(0.1)

    def move_to_first_choice(self):
        self.move_to(self.initial_pos['x'], self.initial_pos['y'])
        self.cursor_pos = deepcopy(self.initial_pos)

    def move_to(self, x, y):
        self.cursor_pos = {'x': x, 'y': y}
        print('\x1b[{0};{1}H'.format(y, x), end="")

    def clear_screen(self):
        print("\x1b[2J", end="")
        self.move_to(1, 1)

    def clear_end(self):
        print("\x1b[0J", end="")

    def clear_beginning(self):
        print("\x1b[1J", end="")
        self.move_to(1, 1)

    def upper_action(self, *args):
        if self.cursor_pos['y'] - 1 >= self.initial_pos['y']:
            self.move_cursor(Direction.UP)
            behaviour = self.get_key_option()
            if 'flags' in behaviour:
                if 'title' in behaviour['flags']:
                    self.upper_action()

    def downer_action(self, *args):
        if self.cursor_pos['y'] + 1 < self.map_length + self.initial_pos['y']:
            self.move_cursor(Direction.DOWN)
            behaviour = self.get_key_option()
            if 'title' in behaviour['flags']:
                self.downer_action()
        pass

    def space_action(self, *args):
        key = self.get_key_option()

        if self.cursor_pos['y'] == self.initial_pos['y'] + self.map_length - 1 and len(self.callback_todo) > 0:
            # callback time
            self.move_to(1, self.map_length + 3)
            print("Start actions:", end="")

            # erase previous callback ouptput
            self.clear_end()

            # run callbacks
            self.move_to(1, self.map_length + 5)
            for todo in self.callback_todo:
                self.move_to(1, self.cursor_pos['y'] + 3)
                print("Running " + todo['main'], end="")
                self.move_to(1, self.cursor_pos['y'] + 2)
                todo['callback']()

            for checked in self.checked_cases:
                self.move_to(checked['x'], checked['y'])
                print(unchecked_char, end="")

            # clear lists
            del self.checked_cases[:]
            del self.callback_todo[:]

            # go back to the top of CLI
            self.move_to_first_choice()
        else:

            if self.cursor_pos in self.checked_cases:
                print(unchecked_char, end="")
                self.move_cursor(Direction.LEFT, 1)
                self.checked_cases.remove(self.cursor_pos)
                self.callback_todo.remove(key)

            else:
                print(checked_char, end="")
                self.move_cursor(Direction.LEFT, 1)
                self.checked_cases.append(deepcopy(self.cursor_pos))
                self.callback_todo.append(deepcopy(key))

    def get_key_option(self):
        """
        :rtype str
        :return: the key in behaviour list of the behaviour where carret is.
        """
        return self.key_map_listed[self.cursor_pos['y'] - self.offset['y'] - 1]

    def debug(self, str):
        print("\x1b[s", end="")
        print("\x1b[30;1H)", end="")
        print(str, end="\x1b[u")

        pass


class BehaviorBuilder:
    def __init__(self, main):
        """
        :type: main str
        :param: main The most significant definition of this behaviour
        :return: this builder instance
        :rtype: BehaviorBuilder
        """
        self._current_behavior = {
            'main': main,
            'flags': []
        }

    def set_description(self, description):
        """
        :type: description: str
        :param: description: The description that you want to set to this behaviour
        :return: this builder instance
        :rtype: BehaviorBuilder
        """
        self._current_behavior['description'] = description
        return self

    def _add_flag(self, flag):
        """
        :type: flag: str
        :param: flag: A flag that you want to add to this behaviour
        :return: this builder instance
        :rtype: BehaviorBuilder
        """
        self._current_behavior['flags'].append(flag)
        return self

    def _remove_flag(self, flag):
        """
        :type: flag: str
        :param: flag: A flag that you want to remove to this behaviour
        :return: this builder instance
        :rtype: BehaviorBuilder
        """
        try:
            self._current_behavior['flags'].remove(flag)
        except ValueError as e:
            print(" Current behavior doesn't have flag " + str(flag))
        return self

    def is_title(self, _bool=True):
        """
        :type: _bool: bool
        :param _bool: Indicate if this behaviour is only a title (no description)
        :return: this builder instance
        :rtype: BehaviorBuilder
        """
        if _bool:
            self._add_flag("title")
        else:
            self._remove_flag("title")
        return self

    def add_callback(self, cb):
        """
        :type: cb: callable
        :param: cb: The function that you want to be called when this behavior is triggered.
        :return: this builder instance
        :rtype: BehaviorBuilder
        """
        self._current_behavior['callback'] = cb
        return self

    def build(self):
        return deepcopy(self._current_behavior)


def a():
    print("A")


def c():
    print("C")


def b():
    print("B")


if __name__ == '__main__':
    behaviors = [
        BehaviorBuilder("Images").is_title(),
        BehaviorBuilder("Drinks").set_description("Resize drinks images to 200 x 200 pixels").add_callback(a),
        BehaviorBuilder("Location").set_description("Resize locations images to 800 x 600 pixels").add_callback(c),

        BehaviorBuilder("System").is_title(),
        BehaviorBuilder("ALMemory Clearer").set_description("Wipe all custom ALMemory (R2019)").add_callback(b)
    ]

    cli = CustomCLI("", [behavior.build() for behavior in behaviors])
    # print([behavior for behavior in behaviors])
