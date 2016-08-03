#
#   TBD:
#
#   1. PIE Chart - kind of done - needs some more work...
#   2. Multiple years - Democrats and Republican States - Think of a nice chart...
#
#


import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from mpl_toolkits.basemap import Basemap as Basemap

from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon

import operator


from common import *;
from state_gdp_spend import *;
from gdp_spend_years import *;


class StateSpendGDPDraw:

    @staticmethod
    def do_draw_states_map(spend_dependence):

        # Lambert Conformal map of lower 48 states.
        m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
                    projection='lcc',lat_1=33,lat_2=45,lon_0=-95)

        # alaska:
        # m = Basemap(llcrnrlon=-180,llcrnrlat=50,urcrnrlon=-125,urcrnrlat=75,
                      #projection='lcc',lat_0=63,lon_0=-153)

        # hawaii:
        # m = Basemap(llcrnrlon=-161,llcrnrlat=18,urcrnrlon=-154,urcrnrlat=23,
                    #projection='lcc',lat_0=21,lon_0=-158)

        # draw state boundaries.
        # data from U.S Census Bureau
        # http://www.census.gov/geo/www/cob/st2000.html
        shp_info = m.readshapefile('states','states',drawbounds=True)

        print(shp_info)

        # choose a color for each state based on population density.
        colors={}
        statenames=[]
        print(m.states_info[0].keys())

        dependence_colors = { 10: "gray", 15: "green", 20: "blue", 25: "yellow", 30: "red" }

        for shapedict in m.states_info:
            statename = shapedict['STATE_NAME']

            # skip DC and Puerto Rico.
            if statename not in ['District of Columbia','Puerto Rico']:
                dependence = spend_dependence[Globals.state_names[statename]]

                # make the dependence go to the lowest multiple of 5:
                colors_index = 5 * (int(dependence) / 5 )
                colors[statename] = dependence_colors[colors_index]
            statenames.append(statename)
        # cycle through state names, color each one.
        ax = plt.gca() # get current axes instance
        for nshape,seg in enumerate(m.states):
            # skip DC and Puerto Rico.
            if statenames[nshape] not in ['District of Columbia','Puerto Rico']:
                color = colors[statenames[nshape]]
                poly = Polygon(seg,facecolor=color,edgecolor=color)
                ax.add_patch(poly)

        # draw meridians and parallels.
        #m.drawparallels(np.arange(25,65,20),labels=[1,0,0,0])
        #m.drawmeridians(np.arange(-120,-40,20),labels=[0,0,0,1])

        plt.title('State GDP Dependence on Federal Spend')
        gray_patch = mpatches.Patch(color="gray", label="10-15%")
        green_patch = mpatches.Patch(color="green", label="15-20%")
        blue_patch = mpatches.Patch(color="blue", label="20-25%")
        yellow_patch = mpatches.Patch(color="yellow", label="25-30%")
        red_patch = mpatches.Patch(color="red", label="30-35%")

        plt.legend(handles=[gray_patch, green_patch, blue_patch, yellow_patch, red_patch],
                   loc='lower left')

        plt.show()

    @staticmethod
    # draw horizontal bars with states
    # the X axis is the dependence.
    def do_draw_bars(spend_dependence):

        sorted_dependence = sorted(spend_dependence.items(), key=operator.itemgetter(1))

        yaxe = range(50)
        yval = [elem[1] for elem in sorted_dependence]
        ynames = [Globals.state_codes[elem[0]] for elem in sorted_dependence]

        print ynames

        colors = [Globals.party_colors[Globals.state_names_party[elem]] for elem in ynames]

        print colors



        plt.barh(yaxe, yval, height=0.2, color=colors)
        plt.yticks(yaxe, ynames)
        plt.xlabel('Dependence')
        plt.title('State GDP Dependence on Federal Spend')
        plt.grid(True)

        gray_patch = mpatches.Patch(color="gray", label="Undecided")
        blue_patch = mpatches.Patch(color="green", label="Democrats")
        red_patch = mpatches.Patch(color="blue", label="Republican")

        plt.legend(handles=[gray_patch, blue_patch, red_patch],
                   loc='lower right')


        plt.show()


    @staticmethod
    def do_draw_pie(parties_dependence):
        # Data to plot
        labels = 'Dependency > 20%', 'Dependency < 20%'

        print "Inside do_draw_pies"
        print parties_dependence
        party_color = {
            "R": "red", "D": "blue", "U": "gray"
        }

        plot_count = 1
        plt.legend("Dependencies more than 20% across parties")
        for party_code, party_name in Globals.parties.iteritems():
            plt.subplot(1,3,plot_count)
            sizes = [parties_dependence[party_code][2], parties_dependence[party_code][1] ]
            colors = [party_color[party_code], 'yellowgreen']
            explode = (0.1, 0)  # explode 1st slice

            # Plot
            plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                      autopct='%1.1f%%', shadow=True, startangle=140)
            plt.xlabel( party_name )

            plt.axis('equal')
            plot_count += 1
        plt.show()

class YearPartyDependence:
    @staticmethod
    def do_draw_linegraph():
        gdp_spend_years = GDPSpendYears()

        x = range(1,11)
        plt.title( "States Dependence For Different Parties")
        plt.xlabel("Year")
        plt.ylabel("Dependency (Percent of States)")

        party_label = { "R": 'Republic', "D": "Democrat", "U": "Undecided"}
        handles_list= []

        for party in Globals.parties.keys():
            # draw republic percentages:
            sorted_years_depend = sorted(gdp_spend_years.pgsy[party].items(), key=operator.itemgetter(0))

            years = [elem[0] for elem in sorted_years_depend]
            dependencies = [elem[1] for elem in sorted_years_depend]

            print "years:"
            print years
            print "dependencies"
            print dependencies

            plt.plot(x, dependencies, color=Globals.party_colors[party], label=party_label[party])

        #plt.axis([0, 9, 30, 100])

        plt.xticks(x, years, rotation='vertical')
        plt.legend()
        plt.show()

def main():
    Globals()

    # read the file:
    state_gdp_spend = StateSpendGDPReader.process_state_spend_gdp()

    print state_gdp_spend.spend_dependence

    print "Global information: Globals.state_names"
    print Globals.state_names

    StateSpendGDPDraw.do_draw_states_map(state_gdp_spend.spend_dependence)
    StateSpendGDPDraw.do_draw_bars(state_gdp_spend.spend_dependence)
    StateSpendGDPDraw.do_draw_pie(state_gdp_spend.parties_dependence)

    YearPartyDependence.do_draw_linegraph()

if __name__=="__main__":
    main()