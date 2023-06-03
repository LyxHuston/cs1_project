"""
    file: test_trending.py 
    description: 
    Test the trending.py module
    author: bksteele, bksvcs@rit.edu
"""

import index_tools
import trending # subject of test

"""
Tested interface functions:
	trending.calculate_trends( data, year0, year1 )
Tested implicitly:
	trending.cagr( idxlist, periods)
"""


def test1():
    """
        tests state-keyed data
    """

    print( 'testing state data processing...')
    fname = "HPI_PO_state.txt"
    data = index_tools.read_state_house_price_data( "data/" + fname )

    annual = index_tools.annualize( data)

    answer = dict()
    answer[ "HPI_PO_state.txt 1994 2002" ] = \
      [('MA', 8.927726257507196), ('NJ', 6.07279996720127), ('HI', 1.1529363923406422)]
    answer[ "HPI_PO_state.txt 1995 1996" ] = \
      [('MI', 8.165561829936996), ('SD', 4.714654541250818), ('HI', -5.63621724111062)]
    answer[ "HPI_PO_state.txt 2006 2008" ] = \
      [('WY', 4.268849486063586), ('WV', 1.450495211395464), ('CA', -17.73558710889268)]


    for year in [ (1994,2002), (1995,1996), (2006,2008) ]:

        print( '= ' * 27 )
        # compute growth rates only for annual averages of HPI values.
        trends = trending.calculate_trends( annual, year[0], year[1] )

        results = [ trends[0], trends[9], trends[-1] ]    # sampling

        key = fname + " " + str(year[0]) + " " + str(year[1])

        print( fname, str(year[0]), str(year[1]), ":", ( results == answer[ key ] ))

    return

def test2():
    """
        test2 tests zip file processing
    """
    print( 'testing ZIP data processing...')
    fname = "HPI_AT_ZIP5.txt"
    annual = index_tools.read_zip_house_price_data( "data/" + fname )

    answer = dict()
    answer[ "HPI_AT_ZIP5.txt 1994 2002" ] = \
      [('80205', 13.660048147719017), ('02143', 11.966500098655452), ('96792', -2.854788072761205)]
    answer[ "HPI_AT_ZIP5.txt 1995 1996" ] = \
      [('02650', 60.7489425230157), ('46186', 26.705136694730868), ('13204', -35.465021912027275)]
    answer[ "HPI_AT_ZIP5.txt 2006 2008" ] = \
      [('52037', 20.656522375739293), ('47231', 16.33947277520282), ('93635', -35.20316697877354)]



    for year in [ (1994,2002), (1995,1996), (2006,2008) ]:

        print( '= ' * 27 )
        trends = trending.calculate_trends( annual, year[0], year[1] )

        results = [ trends[0], trends[9], trends[-1] ]    # sampling

        key = fname + " " + str(year[0]) + " " + str(year[1])

        print( fname, str(year[0]), str(year[1]), ":", ( results == answer[ key ] ))

    return

if __name__ == '__main__':

    print( "\ntesting trending...")
    print( '=' * 72 ); print()
    test1()
    print( '=' * 72 ); print()
    test2()

# end of program file
