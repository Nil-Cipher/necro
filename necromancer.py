from typing import Dict, Tuple
import math
import json


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


def creating(maintaining_spells: Dict[int, int],
             num_spells: Dict[int, int]) -> Tuple[Dict[int, int], int]:
    creating = {}
    total = 0
    for i in range(3, 10):
        if i in num_spells:
            c = num_spells[i] - maintaining_spells.get(i, 0)
            if not c == 0:
                creating[i] = c
                total += (i - 2) * c
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
    new = 0
    params: Dict[str, int] = json.load(open("params.json"))
    # spell slots
    num_spells: Dict[int, int] = dict(
        [int(a), x]
        for a, x in params.get("spells", {}).items())  #convert keys to ints
    # reserved spells
    reserved_spells: Dict[int, int] = dict([int(a), x] for a, x in params.get(
        "reserve_spells", {}).items())  #convert keys to ints
    is_subclass = params["subclass"]
    limited_max = 0
    #input checks
    for lvl, num in num_spells.items():
        if lvl < 0 or lvl > 9:
            raise ValueError('Invalid spell level.')
        if num < 0:
            raise ValueError(f'Invalid spell slots for level {lvl} spell.')
        new += (lvl - 2) * num
        limited_max += (4 + 2 *
                        (lvl - 3)) * (num - reserved_spells.get(lvl, 0))

    existing = params.get("existing", 0)
    day = 1

    maintaining_spells = maintaining(num_spells, existing)
    creating_spells, new = creating(maintaining_spells, num_spells)
    while creating_spells and existing < limited_max:
        print("\nDay ", day, "-------------------------")
        print(f"Existing zombies: {existing}, new zombies: {new}")
        print_spells(maintaining_spells, "Maintaining Spells")
        print_spells(creating_spells, "Creating Spells")
        existing += new
        maintaining_spells = maintaining(num_spells, existing)
        creating_spells, new = creating(maintaining_spells, num_spells)
        day += 1
    if existing > limited_max: existing = limited_max
    print("\n-------------------------")
    print("Max zombie number reached:", existing)
    print_spells(reserved_spells, "Reserved Spells")


if __name__ == "__main__":
    main()
