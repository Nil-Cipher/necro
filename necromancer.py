

from typing import Dict, Tuple
import math


def maintaining(num_spells: Dict[int, int], num_z) -> Dict[int, int]:
    if num_z <= 0:
        return {}
    maintaining_spells = {}
    for i in range(3, 10):
        if i in num_spells:
            old = 4 + 2 * (i - 3)
            used = min(num_spells[i], int(math.ceil(num_z / old)))
            num_z = num_z - used * old
            maintaining_spells[i] = used
        if num_z <= 0:
            return maintaining_spells
    # all spell slots used
    return maintaining_spells


def creating(maintaining_spells: Dict[int, int], num_spells: Dict[int, int]) -> Tuple[Dict[int, int], int]:
    creating = {}
    total = 0
    for i in range(3, 10):
        if i in num_spells:
            c = num_spells[i] - maintaining_spells.get(i, 0)
            if not c == 0:
                creating[i] = c
                total += (i-2) * c
    return (creating, total)


def print_spells(spells: Dict[int, int], desc: str) -> None:
    if any(spells):
        print(desc, end=': ')
        for i in range(3, 10):
            if i in spells:
                print(f"({i}: {spells[i]}) ", end='')
        print()


def main():
    lines = []
    num_spells = {}
    new = 0
    # spell slots
    with open('spells.txt') as f:
        lines = f.readlines()
    for l in lines:
        lvl, num = list(map(int, l.split(" ")))
        if lvl < 0 or lvl > 9:
            raise ValueError('Invalid spell level.')
        if num < 0:
            raise ValueError(f'Invalid spell slots for level {lvl} spell.')
        num_spells[lvl] = num
        new += (lvl-2) * num

    existing = 0
    day = 1
    # parameters
    with open("params.txt") as f:
        lines = f.readlines()
    for l in lines:
        p, num = l.split(" ")
        if p.lower() == "existing":
            existing = int(num)

    maintaining_spells = maintaining(num_spells, existing)
    creating_spells, new = creating(maintaining_spells, num_spells)
    while creating_spells:
        print("\nDay ", day, "-------------------------")
        print(f"Existing zombies: {existing}, new zombies: {new}")
        print_spells(maintaining_spells, "Maintaining Spells")
        print_spells(creating_spells, "Creating Spells")
        existing += new
        maintaining_spells = maintaining(num_spells, existing)
        creating_spells, new = creating(maintaining_spells, num_spells)
        day += 1
    print("-------------------------")
    print("Max zombie number reached:", existing)


if __name__ == "__main__":
    main()
