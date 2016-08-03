import csv;
import numpy;
import os;
import operator;

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DEBUG=False

class SpendFile:
    SAMPLE_COUNT=10000
    PRINT_SAMPLE = False
    SAMPLE = False
    WRITE = True

    def __init__(self):
        self.dsa = {}

    def read_file(self, spend_type, filename, col_state, col_agency, col_dollars):
        print "opening file {}".format(filename)

        count = 0
        columns = None
        with open(filename) as f:
            reader = csv.reader(f)

            for line in reader:

                count += 1

                # assign header:
                if count == 1:
                    columns = line
                    continue

                if SpendFile.PRINT_SAMPLE:
                    # just print one sample:
                    if count < 5:
                        for i in range(0, len(line)):
                            print "{} {}: {}".format(i, columns[i], line[i])

                if SpendFile.WRITE:
                    self.populate_dsa(line, col_state, col_agency, col_dollars)

                if SpendFile.SAMPLE and count > SpendFile.SAMPLE_COUNT:
                    break

        f.close()
        print "\nnumber of lines read: {}".format(count)

    def populate_dsa(self, line, col_state, col_agency, col_dollars):
        # install it in the dollars hash:
        state = line[col_state]
        agency = line[col_agency]

        if state not in self.dsa:
            self.dsa[state] = {}
        dollars_state = self.dsa[state]
        if agency not in dollars_state:
            dollars_state[agency] = float(line[col_dollars])
        else:
            dollars_state[agency] += float(line[col_dollars])

    def write_dsa(self, output):
        arrayout = []

        # write the output to the file:
        count = 0
        with open(output, 'a') as fout:
            writer = csv.writer(fout)
            for state, dollars_state in self.dsa.iteritems():
                for agency, dollars in dollars_state.iteritems():
                    arrayout = [state, agency, dollars]
                    writer.writerow(arrayout)
                    count += 1

        fout.close()

        print "Wrote {} records".format(count)

        # now create the plots:

        self.doPlots()

    def doPlots(self):
        # draw the plot:
        # we need states as a list and the individual agencies as lists:

        # create the states list:
        state_codes = [ "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA",
                        "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT",
                        "VA", "WA", "WV", "WI", "WY"]

        states_str = []
        for state in self.dsa.keys():
            if len(state) == 2 and state in state_codes:
                states_str.append(state)
        states_val = range(1, len(states_str)+1)

        # we maintain each agency list in a dictionary:
        agencies = {}
        for agency in self.dsa["CA"].keys():
            agencies[agency] = []

        if DEBUG:
            print states_str
            print agencies

        for state in states_str:
            agency_dollars = self.dsa[state]
            for agency in agencies.keys():
                if agency in self.dsa[state]:
                    agencies[agency].append(self.dsa[state][agency] / 1000000000.0)
                else:
                    agencies[agency].append(0)

        # we sort the totals;   we keep only the top 5:
        agencies_totals = {}
        for agency, l in agencies.iteritems():
            # zero any negative amounts:
            for i in range(0, len(l)):
                if l[i] < 0:
                    l[i] = 0

            sum = numpy.sum(numpy.array(l))
            agencies_totals[agency] = sum

        top_agencies = sorted(agencies_totals.items(), key=operator.itemgetter(1), reverse=True)

        print "******"
        print states_val
        print agencies[top_agencies[0][0]]
        print len(states_val)
        print len(agencies[top_agencies[0][0]])

        sns.set(style="whitegrid")
        sns.set_color_codes("pastel")

        for i in range(0,5):
            plt.plot(states_val, agencies[top_agencies[i][0]], label=top_agencies[i][0])

        #plt.xlim(1,3)
        plt.xlabel('State')
        plt.ylabel('Amount in Billions of $')
        plt.title( 'Federal Allocation by Department to States')
        plt.xticks(states_val, states_str)
        legend = plt.legend(loc='upper left', bbox_to_anchor=(0, 1), frameon=True)

        plt.show()

        ## Plot 2: RED, BLUE, and COMMON
        blue =   [ "CA", "OR", "WA", "NM", "IL", "MI", "PA", "NY", "MD", "DE", "NJ", "CT", "RI", "MA", "ME", "VT", "HI"]
        red =    [ "ID", "UT", "MT", "WY", "ND", "SD", "NE", "KS", "OK", "AR", "MS", "AL", "TN", "IN", "AK", "SC", "MO", "TX", "VA" ]
        common = [ "NV", "AZ", "CO", "LA", "FL", "NC", "WV", "OH", "IA", "MN", "WI", "GA", "KY", "NH"]

        # Since we already have the State Array and the Agency Array, we will just total the sum:
        parties = { "Democratic": blue, "Republican": red, "Common": common}
        parties_agencies = {}

        for agency in top_agencies:
            parties_agencies[agency[0]] = [0.0,0.0,0.0]

        # go through each state.
        # locate which party index it belongs to.
        # go through all agencies and add in the destination agency:
        for orig_state_index in range(0, len(states_str)):
            state = states_str[orig_state_index]
            # get the index:
            dest_state_index = None
            if state in blue:
                dest_state_index = 0
            elif state in red:
                dest_state_index = 1
            elif state in common:
                dest_state_index = 2
            else:
                print "error - cannote locate state {}".format(state)

            # now go through all agencies:
            for agency_tuple in top_agencies:
                agency = agency_tuple[0]
                print "loop: agency {}".format(agency)
                print "value {}".format(agencies[agency][orig_state_index])

                parties_agencies[agency][dest_state_index] += agencies[agency][orig_state_index]


        # print the details:
        print "Printing party details"
        parties_str = parties.keys()
        parties_val = [1,2,3]
        print parties_str
        for agency in parties_agencies.keys():
            print parties_agencies[agency]

        sns.set(style="whitegrid")
        sns.set_color_codes("pastel")

        for i in range(0,5):
            plt.plot(parties_val, parties_agencies[top_agencies[i][0]], label=top_agencies[i][0])

        plt.xlim(1,3)
        plt.xlabel('Party')
        plt.ylabel('Amount in Billions of $')
        plt.title( 'Federal Allocation by Department to Parties')
        plt.xticks(parties_val, parties_str)
        legend = plt.legend(loc='upper left', bbox_to_anchor=(0, 1), frameon=True)

        plt.show()



    def write_file(self, output):
        if SpendFile.WRITE:
            self.write_dsa(output)


def main():
    input_files = {
        "contract": ('/Volumes/Personal2/usa_spend_data/contracts_{}.csv', 56, 5, 2),
        "grants": ('/Volumes/Personal2/usa_spend_data/grants_{}.csv', 55, 51, 19),
        "loans": ('/Volumes/Personal2/usa_spend_data/loans_{}.csv', 55, 51, 44),
        "ofa": ('/Volumes/Personal2/usa_spend_data/ofa_{}.csv', 55, 51, 19)
    }

    STATE_DEPT_FILE = '/Volumes/Personal2/usa_spend_data/state_dept_{}.csv'

    try:
        os.remove( STATE_DEPT_FILE )
    except OSError:
        pass

    for year in [2014]:
        s = SpendFile()
        for spend_filetype, info in input_files.iteritems():
            s.read_file(spend_filetype, info[0].format(year), info[1], info[2], info[3])

        s.write_file(STATE_DEPT_FILE.format(year))


if __name__=="__main__":
    main()