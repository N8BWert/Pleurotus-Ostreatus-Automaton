from enum import Enum, auto

class state(Enum):
    INIT = auto()
    BUDDING = auto()
    FLOWERING = auto()
    HARVEST = auto()


def main():
    state = state.INIT
    while (True):
        if state == state.INIT:
            pass

        elif state == state.BUDDING:
            pass

        elif state == state.FLOWERING:
            pass

        elif state == state.HARVEST:
            pass


if __name__ == '__main__':
    state = state.INIT
    main()