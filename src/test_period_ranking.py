"""
    file: test_period_ranking.py 
    description: 
    Test the period_ranking.py module
    author: bksteele, bksvcs@rit.edu
"""

import index_tools
import period_ranking # subject of test


def test1():
    """
        tests period_ranking.quarter_data() and period_ranking.annual_data().
    """
    print( 'testing state data processing...')
    fname = "HPI_PO_state.txt"
    data = index_tools.read_state_house_price_data( "data/" + fname )

    answer = dict()
    answer["HPI_PO_state.txt 1993 1"] = [('UT', 117.69), ('OR', 116.94)]
    answer["HPI_PO_state.txt 1993 3"] = [('UT', 128.49), ('CO', 125.16)]
    answer["HPI_PO_state.txt 1993 None"] = [('UT', 125.77499999999999), ('CO', 122.3775)]
    answer["HPI_PO_state.txt 1997 1"] = [('OR', 162.61), ('MT', 162.09)]
    answer["HPI_PO_state.txt 1997 3"] = [('OR', 166.34), ('CO', 162.8)]
    answer["HPI_PO_state.txt 1997 None"] = [('OR', 164.875), ('MT', 162.20499999999998)]
    answer["HPI_PO_state.txt 2010 1"] = [('MT', 298.92), ('WY', 281.91)]
    answer["HPI_PO_state.txt 2010 3"] = [('MT', 293.55), ('WY', 281.33)]
    answer["HPI_PO_state.txt 2010 None"] = [('MT', 292.9875), ('WY', 281.6325)]

    for year in [ 1993, 1997, 2010]:
        for qtr in [ 1, 3, None]:

            if qtr != None:
                results = period_ranking.quarter_data( data, year, qtr )
            else:
                results = period_ranking.annual_data( index_tools.annualize( data), year )
            key = fname + " " + str(year) + " " + str(qtr) 
            #print( key )
            #if key in answer:
            print( fname, year, qtr, ":", ( results[1:3] == answer[ key] ))
            #else:
            #    print( fname, year, qtr, ":", "incorrect", results[1:3] )
    return


def test2():
    """
        tests period_ranking.annual_data() 
    """
    print( 'testing ZIP data processing...')
    fname = "HPI_AT_ZIP5.txt"

    data = index_tools.read_zip_house_price_data( "data/" + fname )

    answer = dict()
    answer["HPI_AT_ZIP5.txt 1996"] = [('95129', 580.09), ('94086', 533.61)]
    answer["HPI_AT_ZIP5.txt 2003"] = [('93117', 1156.19), ('94112', 1056.11)]
    answer["HPI_AT_ZIP5.txt 2006"] = [('95129', 1592.33), ('95127', 1535.7)]
    answer["HPI_AT_ZIP5.txt 2014"] = [('95014', 1999.64), ('94110', 1765.75)]
    
    for year in [ 1996, 2003, 2006, 2014]:
        results = period_ranking.annual_data( data, year)
        key = fname + " " + str(year)
        #print( key )
        if key in answer:
            print( fname, str( year), ":", ( results[1:11:9] == answer[ key] ))
        else:
            print( fname, str( year), ":", "incorrect", results[1:11:9] )
    return

if __name__ == '__main__':
    print( "\ntesting period_ranking...")
    # runs only when directly invoking this module
    print( '=' * 72 ); print()
    test1()
    print( '=' * 72 ); print()
    test2()

# end of program file
