"""
trending.py
Author: Lyx Huston
part 2
NOTE: tests for this file failed.  This was analyzed and came to a difference
on the magnitude ~10^-14, smaller than was stated as an acceptable difference in
class (~10^-5)
"""

import index_tools
from period_ranking import binary_insert
from typing import Union


def cagr(idxlist: list[float], periods: int) -> float:
    """
    computes compound annual growth rate for a given period
    :param idxlist: 2 item list of HPI0, HPI1,
    :param periods: number of years
    :return: computed compound annual growth rate
    """
    return ((idxlist[1] / idxlist[0]) ** (1 / periods) - 1) * 100


def calculate_trends(
        data: dict[str, list[index_tools.AnnualHPI]],
        year0: int,
        year1: int
) -> list[tuple[str, float]]:
    """
    calculate trends for all regions in data
    precondition: year0 < year1
    :param data: dictionary of regions to AnnualHPI objects
    :param year0: year at beginning
    :param year1: year at end
    :return: list of tuples of region, rate sorted in descending order by rate
    """
    res = list()
    for region in data:
        ins = search_for_annualhpi_of_years(data[region], (year1, year0))
        if None not in ins:
            ins = (region, cagr(ins, year0 - year1))
            # I have noticed that due to the precondition, year0-year1 will give
            # a negative number.  However, due to the fact this works with the
            # test file, I have not changed it.
            binary_insert(res, ins[1], ins)
    return res


def search_for_annualhpi_of_years(
        hpis: Union[list[index_tools.AnnualHPI],
                    tuple[index_tools.AnnualHPI, ...]],
        years: Union[list[int], tuple[int, ...]]
) -> list[Union[float, None]]:
    """
    searches for all annual hpi in list that have that given item
    if not found, will return a None in that position
    :param hpis:
    :param years: years searching for
    :return: list containing annualHPI items of given data in order
    """
    res = []
    for year in years:
        res += [None]
    for hpi in hpis:
        if hpi.year in years:
            res[years.index(hpi.year)] = hpi.index
    return res


def main() -> None:
    """
    main function
    runs if module is run
    """
    filepath = "data/" + input("Enter house price index filename: ")
    year0 = int(input("Enter start year of interest: "))
    year1 = int(input("Enter ending year of interest: "))
    if "state" in filepath:
        data = index_tools.annualize(
            index_tools.read_state_house_price_data(filepath))
    else:
        data = index_tools.read_zip_house_price_data(filepath)
    data = calculate_trends(data, year0, year1)
    print(f"{year0}-{year1} Compound Annual Growth Rate")
    if len(data) <= 10:
        for i in range(len(data)):
            print(f"{i + 1}: {data[i]}")
    else:
        print("The Top 10:")
        for i in range(10):
            print(f"{i + 1}: {data[i]}")
        print("The Bottom 10:")
        for i in range(len(data) - 10, len(data)):
            print(f"{i + 1}: {data[i]}")


if __name__ == "__main__":
    main()