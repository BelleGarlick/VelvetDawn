import dataclasses

from base_test import BaseTest
from velvet_dawn.map import get_distance


@dataclasses.dataclass
class Position:
    x: int
    y: int


def pad_text(x):
    """ Pad out the text for printing the grid """
    val = "-" if x in {3, 6, 9, 12, 15} else str(x)

    while len(val) < 5:
        if len(val) < 5:
            val += " "
        if len(val) < 5:
            val = " " + val

    return val


class TestMap(BaseTest):

    def test_get_distance(self):
        # Print example for visually testing
        width, height = 17, 11
        pos = Position(7, 10)

        for y in range(height):
            for x in range(width):
                distance = get_distance(Position(x, y), pos)
                print(pad_text(distance if x % 2 == 0 else ""), end="")
            print()

            for x in range(width):
                distance = get_distance(Position(x, y), pos)
                print(pad_text(distance if x % 2 == 1 else ""), end="")
            print()

        # Check correct distances
        self.assertEqual(15, get_distance(Position(0, 0), Position(10, 10)))
        self.assertEqual(10, get_distance(Position(10, 0), Position(10, 10)))
        self.assertEqual(4, get_distance(Position(7, 7), Position(10, 10)))

        self.assertEqual(14, get_distance(Position(0, 0), Position(7, 10)))
        self.assertEqual(12, get_distance(Position(10, 0), Position(7, 10)))
        self.assertEqual(3, get_distance(Position(7, 7), Position(7, 10)))
