"""
    file: test_timeline_plot.py 
    description: 
    Test the timeline_plot.py program internal functions and interface.
    author: bksteele, bksvcs@rit.edu
"""

import index_tools
import timeline_plot

def test1():
    """
        The function reads a dataset file, 
        annualizes the dataset values, and
        uses a canned sequence of names to plot to get plot data and
        check it against expected values.
    """

    # test with subset of data files
    for fname in [ "HPI_PO_state.txt", "HPI_AT_ZIP5.txt"]:

        print( "=" * 72 )
        print( "\nReading", fname, "..." )

        if "ZIP" in fname:
            # read a house price index file with Zip code key.
            # note: Zip data is already annualized
            annual = index_tools.read_zip_house_price_data( 'data/' + fname )

            # this keylist has data with some gaps
            keylist = [ "04083", "14625", "48210", "12202" ]

        else:
            data = index_tools.read_state_house_price_data( 'data/' + fname )
            # state data must be annualized for the timeline plots.
            annual = index_tools.annualize( data )

            keylist = [ "NY", "IL", "MA", "VT", "MS" ]

        # filter the data to get a subrange
        annual = timeline_plot.filter_years( annual, 1988, 2008 )

        # call the functions for plotting

        timeline_plot.plot_HPI( annual, keylist)

        timeline_plot.plot_whiskers( annual, keylist)

    return

if __name__ == '__main__':
    print( "\ntesting timeline_plot...")
    # run only when directly invoking this module
    test1()

# end of program file
