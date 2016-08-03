#
#   Generates the following file:
#
#   State   GDP     "Federal Spend to State"      "% of GDP"
#
#



import numpy;
import os;
import operator;
import math;


import matplotlib.pyplot as plt
import pandas as pd
#import seaborn as sns

from common import *;

DEBUG=False

#
#   Reads the RAW Spend File
#
class SpendFile(BaseFile):
    def __init__(self, use_state_code=True, remove_dollars_commas_spaces=False):
        BaseFile.__init__(self)
        self.use_state_code = use_state_code
        self.remove_dollars_commas_spaces = remove_dollars_commas_spaces

    def do_init(self):
        # Dollars and State
        self.sd = {}

    def do_populate(self, count, line, col_list):
        # install it in the dollars hash:
        col_state = col_list[0]
        col_dollars = col_list[1]

        state = line[col_state]

        if not self.use_state_code:
            if state in Globals.state_names:
                state = Globals.state_names[state]

        if state not in self.sd:
            self.sd[state] = 0.0

        dollar_string = line[col_dollars]
        if self.remove_dollars_commas_spaces:
            dollar_string = dollar_string.translate(None, "$, " )

        # print "after conversion - dollar_string is [{}]".format(dollar_string)

        f = float(dollar_string)
        if f > 0:
            self.sd[state] += f
            self.total += f
        else:
            self.negative_records += 1
            self.negative_dollars += abs(f)

        if BaseFile.PRINT_SAMPLE:
            print "Record [{}] State [{}] Dollars [{}]".format(count, state, f)

    def write_file(self, output):
        if not BaseFile.WRITE:
            return

        arrayout = []

        # write the output to the file:
        countState = 0
        totalStateDollars = 0
        countNonState = 0
        totalNonStateDollars = 0
        with open(output, 'w+') as fout:
            writer = csv.writer(fout)
            for state, dollars in self.sd.iteritems():
                if  state in Globals.state_codes:
                    countState += 1
                    totalStateDollars += dollars
                    dollars_str = Utils.millions(dollars)
                    arrayout = [state, dollars_str]
                    writer.writerow(arrayout)
                else:
                    countNonState += 1
                    totalNonStateDollars += dollars

        fout.close()

        print "Wrote {} state records {}M state dollars {} non state records {}M nonstate dollars".format(
                                Utils.put_comma(countState),
                                Utils.millions(totalStateDollars),
                                Utils.put_comma(countNonState),
                                Utils.millions(totalNonStateDollars))


    @staticmethod
    def process_spend_total():
        # file type : file name, state, dollars
        input_files = {
            "contract": ('/Volumes/Personal2/data/usa_spend_data/contracts_{}.csv', 56, 2),
            "grants": ('/Volumes/Personal2/data/usa_spend_data/grants_{}.csv', 55, 19),
            "loans": ('/Volumes/Personal2/data/usa_spend_data/loans_{}.csv', 55, 44),
            "ofa": ('/Volumes/Personal2/data/usa_spend_data/ofa_{}.csv', 55, 19)
        }

        STATE_SPEND_FILE = '/Volumes/Personal2/data/output/state_spend_{}.csv'

        try:
            os.remove( STATE_SPEND_FILE )
        except OSError:
            pass

        s = SpendFile()
        for year in [2014]:
            for filetype, info in input_files.iteritems():
                s.read_file(info[0].format(year), [info[1], info[2]] )

            s.write_file(STATE_SPEND_FILE.format(year))

            print "Cumulative lines read across all files: {}".format(s.total_records, Utils.put_comma(s.total_records))
            print "Total amount in spend files {};  Negative Records {} Negative Dollars {}M".format(
                                                Utils.millions(s.total),
                                                Utils.put_comma(s.negative_records),
                                                Utils.millions(s.negative_dollars))

        return s




    #
    #   Reads the summary:
    #
    @staticmethod
    def process_spend_summary():
        # file type : file name, state, dollars
        input_files = {
            "summary": ('/Volumes/Personal2/data/usa_spend_data_2/federal_spending_by_state.csv', 1, 11),
        }

        STATE_SPEND_SUMMARY_FILE = '/Volumes/Personal2/data/output/state_spend_summary_{}.csv'

        try:
            os.remove( STATE_SPEND_SUMMARY_FILE )
        except OSError:
            pass

        # here we are looking for the full state name:
        s = SpendFile(use_state_code=False, remove_dollars_commas_spaces = True)

        for year in [2014]:
            for filetype, info in input_files.iteritems():
                s.read_file(info[0].format(year), [info[1], info[2]] )

            s.write_file(STATE_SPEND_SUMMARY_FILE.format(year))

            print "Cumulative lines read across all files: {}".format(s.total_records, Utils.put_comma(s.total_records))
            print "Total amount in spend files {};  Negative Records {} Negative Dollars {}M".format(
                                                Utils.millions(s.total),
                                                Utils.put_comma(s.negative_records),
                                                Utils.millions(s.negative_dollars))

        return s





#
#   Reads the GDP File
#
class GDPFile(BaseFile):
    def do_init(self):
        self.sg = {}

    def do_populate(self, count, line, col_list):
        # install it in the GDP hash:

        col_state = col_list[0]
        col_industry = col_list[1]
        col_dollars = col_list[2]

        industry = line[col_industry]

        # only add the rows that have "All industry total"
        if industry != "All industry total":
            return

        state_name = line[col_state]
        if state_name in Globals.state_names:
            state_code = Globals.state_names[state_name]
        else:
            state_code = state_name

        if state_code not in self.sg:
            self.sg[state_code] = 0.0

        f = float(line[col_dollars])
        if f > 0:
            self.sg[state_code] += f
            self.total += f
        else:
            self.negative_records += 1
            self.negative_dollars += abs(f)

        if BaseFile.PRINT_SAMPLE:
            print "Record [{}] State [{}] Dollars [{}]".format(count, state_code, f)

    def write_file(self, output):
        if not BaseFile.WRITE:
            return

        arrayout = []

        # write the output to the file:
        countState = 0
        totalStateDollars = 0
        countNonState = 0
        totalNonStateDollars = 0
        with open(output, 'w+') as fout:
            writer = csv.writer(fout)
            for state, dollars in self.sg.iteritems():
                if  state in Globals.state_codes:
                    countState += 1
                    totalStateDollars += dollars
                    dollars_str = Utils.put_comma(int(dollars))
                    arrayout = [state, dollars_str]
                    writer.writerow(arrayout)
                else:
                    countNonState += 1
                    totalNonStateDollars += dollars

        fout.close()

        print "Wrote {} state records {}M state dollars {} non state records {}M nonstate dollars".format(
                                Utils.put_comma(countState),
                                Utils.millions(totalStateDollars),
                                Utils.put_comma(countNonState),
                                Utils.millions(totalNonStateDollars))

    @staticmethod
    def process_gdp():
        # file type : file name, state, dollars

        # this file has the GDP for ALL years.
        # we choose the 2014 one.
        input_files = {
            "generic": ('/Volumes/Personal2/data/gdp/gsp_naics_all_C_{}.csv', 1, 7, 25),
        }

        STATE_GDP_FILE = '/Volumes/Personal2/data/output/state_gdp_{}.csv'

        try:
            os.remove(STATE_GDP_FILE)
        except OSError:
            pass

        s = GDPFile()
        for year in [2014]:
            for filetype, info in input_files.iteritems():
                s.read_file(info[0].format(year), [info[1], info[2], info[3]])

                s.write_file(STATE_GDP_FILE.format(year))

                print "Cumulative lines read across all files: {}".format(s.total_records,
                                                                          Utils.put_comma(s.total_records))
                print "Total amount in spend files {};  Negative Records {} Negative Dollars {}M".format(
                    Utils.millions(s.total),
                    Utils.put_comma(s.negative_records),
                    Utils.millions(s.negative_dollars))

        return s


#
#   Reads a file that has State, Spend, GDP, and Percentage of Dependence
#
class StateSpendGDPReader(BaseFile):
    def do_init(self):
        # Percentage of spend / gdp
        self.spend_dependence = {}
        self.parties_dependence = {}

    def do_populate(self, count, line, col_list):
        # install it in the dollars hash:
        col_state = col_list[0]
        col_percent = col_list[1]

        state = line[col_state]

        if state not in self.spend_dependence:
            self.spend_dependence[state] = 0.0

        dependence_percent = float(line[col_percent])
        self.spend_dependence[state] = dependence_percent

        if BaseFile.PRINT_SAMPLE:
            print "Record [{}] State [{}] Dollars [{}]".format(count, state, dependence_percent)

    # we build a hash as {"party": (total, less than 15, more than 15)}
    def do_parties_dependence(self):
        for state, dependence in self.spend_dependence.iteritems():
            # get party:
            party = Globals.state_names_party[Globals.state_codes[state]]
            if party not in self.parties_dependence:
                self.parties_dependence[party] = [0,0,0]
            l = self.parties_dependence[party]

            l[0] += 1
            if dependence < 20:
                l[1] += 1
            else:
                l[2] += 1
            self.parties_dependence[party] = l


    @staticmethod
    def process_state_spend_gdp():
        STATE_SPEND_GDP_FILE = "/Volumes/Personal2/data/output/state_spend_gdp_{}.csv"

        # the first index is the State and the last one is the Percent:
        state_gdp_spend = StateSpendGDPReader()
        state_gdp_spend.read_file(STATE_SPEND_GDP_FILE.format(2014), [0,3])

        print "Spend Depencies"
        print state_gdp_spend.spend_dependence

        state_gdp_spend.do_parties_dependence()

        print "Parties Dependencies."
        print state_gdp_spend.parties_dependence

        return state_gdp_spend


def main():
    # initialize the Globals:
    globals = Globals()
    timer = MyTimer()
    
    #spend = SpendFile.process_spend_total()
    spend = SpendFile.process_spend_summary()
    gdp = GDPFile.process_gdp()

    STATE_SPEND_GDP_FILE = "/Volumes/Personal2/data/output/state_spend_gdp_{}.csv"
    BaseFile.do_merge_spend_gdp(STATE_SPEND_GDP_FILE.format(2014),spend.sd, gdp.sg, ["State", "Spend", "GDP", "Dependence"])

    print "Total Elapsed Time [{}] seconds".format(timer.stop())

if __name__=="__main__":
    main()