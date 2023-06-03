"""
timeline_plot.py
Author: Lyx Huston
part 3
the one with a lot of imports


Most of the imports seem to not be necessary in the code?
"""

import numpy.ma as ma
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import copy

from index_tools import AnnualHPI, sort, annualize, read_zip_house_price_data
from index_tools import read_state_house_price_data, print_range


def build_plottable_array(
        xyears: list[int],
        regiondata: list[AnnualHPI]
) -> ma.masked_array:
    """
    "bridges gaps" in data in regiondata that correspond to xyears
    constructs a plottable array
    for a single region?
    :param xyears: list of years to put on the x axis
    :param regiondata: list of AnnualHPI objects
    :return: a plottable array with given data
    """

    mask = []
    graph = []
    for year in xyears:
        mask.append(1)
        graph.append(None)
    for hpi in regiondata:
        if hpi.year in xyears:
            look = xyears.index(hpi.year)
            graph[look] = hpi.index
            mask[look] = 0
    return ma.masked_array(ma.array(graph), mask)


def filter_years(
        data: dict[str: list[AnnualHPI]],
        year0: int,
        year1: int
) -> dict[str: list[AnnualHPI]]:
    """
    filters data from the dictionary that aren't part of the range of years

    precondition: year0<=year1

    :param data: dictionary of regions to annualHPI datas, unfiltered
    :param year0: beginning year
    :param year1: end year
    :return: data set above, but with items taken out that are not in the year
    range, sorted in ascending order by year
    """
    res = dict()
    for reg in data:
        work = list()
        for hpi in data[reg]:
            if year0 <= hpi.year <= year1:
                work.append(hpi)
        sort(work)
        res[reg] = work
    return res


def plot_HPI(
        data: dict[str: list[AnnualHPI]],
        regionList: list[str]
) -> None:
    """
    plots a timeline of point to point over data
    pre-condition: lists in data are sorted in ascending year order
    :param data: dataset to plot
    :param regionList: regions to plot
    :return:
    """
    low, high = get_highest_lowest_years(
        get_all_data_from_all_regions(data, regionList)
    )
    ran = list(range(low, high + 1))
    plt.title(f"Home Price Indexes: {low}-{high}")
    for reg in regionList:
        plot = build_plottable_array(ran, data[reg])
        plt.plot(ran, plot, marker="D", scalex=True)
    plt.legend(regionList)
    ticks = range(((low + 1) // 2) * 2, ((high + 3) // 2) * 2, 2)
    plt.xticks(ticks)
    plt.xlim(low, high)
    print("Close display window to continue.")
    plt.show()


def plot_whiskers(
        data: dict[str: list[AnnualHPI]],
        regionList: list[str]
) -> None:
    """
    displays a whisker plot of data
    :param data: dictionary of regions to list of API
    :param regionList: list of regions to plot
    :return: None
    """
    work = []
    for reg in regionList:
        work.append([])
        for hpi in data[reg]:
            work[-1].append(hpi.index)
    plt.boxplot(work, labels=regionList, showmeans=True)
    plt.title(
        "Home Price Index Comparison.  Median is a line.  Mean is a triangle."
    )
    print("Close display window to continue.")
    plt.show()


def get_all_data_from_all_regions(
        data: dict[str: list[AnnualHPI]], regs: list[str]
) -> list[AnnualHPI]:
    """
    a helper function to use with get_highest_lowest that isolates all data
    related to the regions to a single list
    :param data: a dictionary of regions to lists of annual hpi
    :param regs: list of regions to target
    :return: lists, added
    """
    res = []
    for reg in regs:
        res += data[reg]
    return res


def get_highest_lowest_years(lst: list[AnnualHPI]) -> tuple[int, int]:
    """
    finds highest and lowest years from given list
    :param lst: list of AnnualHPI objects
    :return: tuple, lowest then highest
    """
    low = lst[0].year
    high = lst[1].year
    for hpi in lst[1:]:
        if hpi.year > high:
            high = hpi.year
        elif hpi.year < low:
            low = hpi.year
    return low, high


def main() -> None:
    """
    main function
    runs if module is run
    gets file, years, and regions of interest, creates plots and prints ranges

    !!!NOTE!!! instructions showed printed ranges for state files, not for ZIP
    files.  It was also in specifically QuarterHPI format.  This was not
    specified anywhere else, either in reading state function instructions, or
    written instructions.  I did so.

    :return: None
    """
    filepath = "data/" + input("Enter house price index file: ")
    year0 = int(input("Enter start year of range to plot: "))
    year1 = int(input("Enter ending year of range to plot: "))
    regs = [input("First region for plots: ")]
    while True:
        inp = input("Next region for plots (Hit ENTER to stop): ")
        if inp == "":
            break
        else:
            regs.append(inp)
    if "state" in filepath:
        unanualized_data = read_state_house_price_data(filepath)
        for reg in regs:
            print_range(unanualized_data, reg)
        dat = annualize(unanualized_data)
    else:
        dat = read_zip_house_price_data(filepath)
    filtered_data = dict()
    # the next loop is to make filtering the years *much* quicker
    for reg in regs:
        filtered_data[reg] = dat[reg]
    filtered_data = filter_years(filtered_data, year0, year1)
    plot_HPI(filtered_data, regs)
    plot_whiskers(filtered_data, regs)


if __name__ == "__main__":
    main()