"""
index_tools.py
Author: Lyx Huston
part 0
no test for this module, tested indirectly by other modules working
"""

from dataclasses import dataclass
from typing import Union


@dataclass()
class QuarterHPI:
    """
    holds data for quarter
    """
    year: int
    qtr: int
    index: float


@dataclass()
class AnnualHPI:
    """
    holds data for year
    """
    year: int
    index: float


def read_state_house_price_data(filepath: str) -> dict:
    """
    given file path computes dictionary with mapping of state abbrev to
    QuarterHPI.  prints warning if data value unavailable
    ("data unavailable" and then print line content)
    ex:
    data unavailable:
    VT 1976 1 . . warning: data unavailable in original source.
    :param filepath: string, path to file
    :return: dictionary mapping state abbreviation strings to
    list of QuarterHPI objects
    """
    file = open(filepath, "r")
    line = file.readline()
    read = line.strip().split()
    res = dict()
    if read[0] != "state":
        if "." in read[1:4]:
            print("Data unavailable")
            print(line)
        else:
            res[read[0]] = [QuarterHPI(int(read[1]), int(read[2]), float(read[3]))]
    for line in file:
        read = line.strip().split()
        if "." in read[1:4]:
            print("Data unavailable")
            print(line)
            continue
        elif read[0] in res.keys():
            res[read[0]].append(
                QuarterHPI(int(read[1]), int(read[2]), float(read[3]))
            )
        else:
            res[read[0]] = [QuarterHPI(
                int(read[1]), int(read[2]), float(read[3])
            )]
    return res


def read_zip_house_price_data(filepath: str) -> dict:
    """
    constructs dict of lists
    prints count of lines read and lines uncounted because incomplete
    count: {counted} uncounted: {uncounted}
    :param filepath: string, path to ZIP5 file
    :return: dictionary mapping state abbreviation strings to
    list of AnnualHPI objects
    """
    file = open(filepath, "r")
    counted = 0
    uncounted = 0
    line = file.readline()
    read = line.strip().split()
    res = dict()
    if read[0] != "Five-Digit":
        if "." == read[1] or "." == read[3]:
            uncounted += 1
        else:
            counted += 1
            res[read[0]] = [AnnualHPI(
                int(read[1]), float(read[3])
            )]
    for line in file:
        read = line.strip().split()
        if "." == read[1] or "." == read[3]:
            uncounted += 1
            continue
        elif read[0] in res.keys():
            counted += 1
            res[read[0]].append(
                AnnualHPI(
                    int(read[1]), float(read[3])
                )
            )
        else:
            counted += 1
            res[read[0]] = [AnnualHPI(
                int(read[1]), float(read[3])
            )]
    return res


def index_range(
        data: dict[str, list[Union[AnnualHPI, QuarterHPI]]], region: str
) -> tuple[float, float]:
    """
    finds high and how for region
    :param data: dict produced by either read_zip or read_state functions
    :param region: region indicator
    :return: tuple of highest and lowest index values
    """
    res = get_hpi_extremes(data, region)
    return res[0].index, res[1].index


def get_hpi_extremes(
        data: dict[str, list[Union[AnnualHPI, QuarterHPI]]], region: str
) -> tuple[Union[AnnualHPI, QuarterHPI], Union[AnnualHPI, QuarterHPI]]:
    """
    helper function for print range and index_range
    :param data: dictionary of region to list of HPI objects
    :param region: region looking at
    :return: tuple of HPI objects with highest and lowest values
    """
    get = data[region]
    low = get[0]
    high = get[0]
    for hpi in get[1:]:
        if low.index > hpi.index:
            low = hpi
        elif high.index < hpi.index:
            high = hpi
    return high, low


def print_range(
        data: dict[str, list[Union[AnnualHPI, QuarterHPI]]], region: str
) -> None:
    """
    prints low and high for region
    Region: {Region}
    Low: year/quarter/index: {yr} / {qtr} / {ind}
    High: year/quarter/index: {yr} / {qtr} / {ind}
    omits qtr if annualHPI
    :param data: dict from read functions, region to list of HPI
    :param region: region to look at
    :return: None
    """
    high, low = get_hpi_extremes(data, region)
    print(f"Region: {region}")
    if isinstance(low, AnnualHPI):
        print(f"Low: year/index: {low.year} / {low.index}")
    else:
        print(f"Low: year/quarter/index: {low.year} / {low.qtr} / {low.index}")
    if isinstance(high, AnnualHPI):
        print(f"High: year/index: {high.year} / {high.index}")
    else:
        print(f"High: year/quarter/index: {high.year} / {high.qtr} / {high.index}")


def print_ranking(
        data: list[tuple[str, float]], heading: str = "Ranking"
) -> None:
    """
    prints top 10 and bottom 10 list data
    :param data: sorted list of tuples of region and index
    :param heading: heading describing data
    :return:
    """
    print(heading)
    print("The Top 10:")
    for i in range(10):
        print(f"{i + 1}: {data[i]}")
    print("The Bottom 10:")
    for i in range(len(data) - 10, len(data)):
        print(f"{i + 1}: {data[i]}")


def annualize(data: dict[str, list[QuarterHPI]]) -> dict[str, list[AnnualHPI]]:
    """
    averages quarter API objects to create annual API
    :param data: dictionary of region to list of quarter HPI objects
    :return: dict of region to list of annual HPI objects
    """
    res = dict()
    for reg in data:
        work = dict()
        for h in data[reg]:
            if h.year in work.keys():
                work[h.year] = (work[h.year][0] + h.index, work[h.year][1] + 1)
            else:
                work[h.year] = (h.index, 1)
        res[reg] = []
        for y in work:
            res[reg].append(AnnualHPI(
                y, work[y][0] / work[y][1]
            ))
    return res


def main() -> None:
    """
    main function
    runs if module is run
    prompts for data file, can be state or ZIP file
    determine function to use
    prompt list of regions
    (prompts once per region)
    crash if inputs invalid
    1. A heading line of ’=’ characters;
    2. A heading starting with Region: followed by the region key;
    3. The quarterly high and low index values for the region if the dataset is
    state-keyed; use this format:
    <High>or<Low>: year/quarter/index: <YEAR> / <QUARTER> / <INDEX>
    4. The annualized high and low index values for the region;
    5. A heading of the form Annualized Index Values for <REGION>; and
    6. The list of annualized index values for all the years available for the
    (state or zip code) region.
    """
    filepath = "data/" + input("Enter house price index file: ")
    if "state" in filepath:
        unanualized_data = read_state_house_price_data(filepath)
        dat = annualize(unanualized_data)
    else:
        dat = read_zip_house_price_data(filepath)
    regs = [input("First region of interest: ")]
    while True:
        inp = input("Next region of interest (Hit ENTER to stop): ")
        if inp == "":
            break
        else:
            regs.append(inp)
    if "state" in filepath:
        for reg in regs:
            print("=" * 40)
            # noinspection PyUnboundLocalVariable
            print_range(unanualized_data, reg)
            print_range(dat, reg)
            print(f"Annualized Index Values for {reg}")
            data = sort(dat[reg])
            print(data[0])
            for i in range(1, len(data)):
                if data[i].year - data[i - 1].year == 2:
                    print(f"    . . . output elided for {data[i].year - 1}")
                elif data[i].year - data[i - 1].year > 2:
                    print("    . . . output elided for "
                          f"{data[i - 1].year + 1} - {data[i].year - 1}")
                print(data[i])
    else:
        for reg in regs:
            print("=" * 40)
            print_range(dat, reg)
            print(f"Annualized Index Values for {reg}")
            data = sort(dat[reg])
            print(data[0])
            for i in range(1, len(data)):
                if data[i].year - data[i - 1].year == 2:
                    print(f"    . . . output elided for {data[i].year - 1}")
                elif data[i].year - data[i - 1].year > 2:
                    print("    . . . output elided for "
                          f"{data[i - 1].year + 1} - {data[i].year - 1}")
                print(data[i])


def sort(data: list[Union[AnnualHPI, QuarterHPI]]) -> list:
    """
    sorts a list from smallest to largest in place
    insertion sort
    preconditions: all items of list integers or floats
    postconditions: the list is given
    :param data: A list to be sorted
    :return: the list
    """
    for i in range(len(data)):
        rep = 0
        while i - rep > 0:
            if data[i - rep].year >= data[i - rep - 1].year:
                break
            else:
                data.insert(i - rep - 1, data.pop(i - rep))
            rep += 1
    return data


if __name__ == "__main__":
    main()