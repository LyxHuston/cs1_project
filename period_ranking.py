"""
period_ranking.py
Author: Lyx Huston
part 1
"""

import index_tools


def binary_insert(data: list, checked, ins, length: int = None) -> None:
    """
    inserts efficiently into list using a modified binary search technique
    :param data: list to insert in
    :param checked: what to check with.  This was added mainly as a speed-up.
    :param ins: what to insert
    :param length: length of list, if given
    :return: None
    """
    if length is None:
        length = len(data)
    if length > 1:
        jump = length // 2
        look = length // 2
        look_record = []
        while True:
            look_record.append(look)
            if look >= length:
                if data[-1][1] >= checked:
                    break
                else:
                    look -= jump
            elif data[look][1] <= checked:
                if data[look - 1][1] >= checked or look <= 0:
                    break
                else:
                    look -= jump
            else:
                look += jump
            if jump != 1:
                jump = jump // 2
        data.insert(look, ins)
    elif length == 1:
        if data[0][1] > checked:
            data.append(ins)
        else:
            data.insert(0, ins)
    else:
        data.append(ins)


def quarter_data(data: dict, year: int, qtr: int) -> list:
    """
    gets quarter data for each region
    :param data: dict of state region to list of qtrHPI
    :param year: year looking at
    :param qtr: quarter looking at
    :return: list of tuples (Region, HPI)
    """
    res = []
    length = 0
    for reg in data:
        for h in data[reg]:
            if h.year == year and h.qtr == qtr:
                binary_insert(res, h.index, (reg, h.index), length)
                length += 1
    return res


def annual_data(data: dict, year: int) -> list:
    """
    gets annual data for each region
    :param data: dict of state region to list of annualHPI
    :param year: year looking at
    :return: list of tuples (Region, HPI)
    """
    res = []
    length = 0
    for reg in data:
        for h in data[reg]:
            if h.year == year:
                binary_insert(res, h.index, (reg, h.index), length)
                length += 1
    return res


def main():
    """
    main function
    runs if module is run
    prints top 10 and bottom 10 for year in file
    """
    filepath = "data/" + input(
        "Enter region-based house price index filename: "
    )
    year = int(input("Enter year of interest for house prices: "))
    if "state" in filepath:
        data = index_tools.annualize(
            index_tools.read_state_house_price_data(filepath)
        )
    else:
        data = index_tools.read_zip_house_price_data(filepath)
    dat = annual_data(data, year)
    index_tools.print_ranking(dat, f"{year} Annual Ranking")


if __name__ == "__main__":
    main()