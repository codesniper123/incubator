import csv;
from common import *;
import operator


class GDPYears:
    def __init__(self, filename):
        # state, year, GDP
        self.syg = {}
        self.read_file(filename)

    # file name and list of columns
    def read_file(self, filename):
        print "opening file {}".format(filename),

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

                self.process_line(count, columns, line)

        f.close()
        print " - lines read: {}".format(Utils.put_comma(count))

    def process_line(self, count, columns, line):
        # we will read from 2005 through 2014.
        COL_STATE = 1
        COL_DESCRIPTION=7
        COL_2005=16

        if line[COL_DESCRIPTION] == "All industry total":
            state = line[COL_STATE]
            if state not in self.syg:
                self.syg[state] = {}
            state_info = self.syg[state]
            for i in range(COL_2005, COL_2005+(2014-2005)+1):
                state_info[ columns[i] ] = int(line[i])

    @staticmethod
    def process():
        return GDPYears( "/Volumes/Personal2/data/gdp/gsp_naics_all_C_2014.csv")


class SpendYears:
    def __init__(self, filename):
        # state, year, spend
        self.sys = {}
        self.read_file(filename)

    # file name and list of columns
    def read_file(self, filename):
        print "opening file {}".format(filename),

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

                self.process_line(count, columns, line)

        f.close()
        print " - lines read: {}".format(Utils.put_comma(count))

    def process_line(self, count, columns, line):
        # we will read from 2005 through 2014.
        COL_STATE = 1
        COL_2005=2

        state = line[COL_STATE]
        if state not in self.sys:
            self.sys[state] = {}
        state_info = self.sys[state]
        first = True if len(state_info) == 0 else False
        for i in range(COL_2005, COL_2005+(2014-2005)+1):
            dollar_string = line[i].translate(None, "$, " )
            if first:
                state_info[ columns[i] ] = int(dollar_string)/Utils.oneMillion
            else:
                state_info[ columns[i] ] += int(dollar_string)/Utils.oneMillion

    @staticmethod
    def process():
        return SpendYears( "/Volumes/Personal2/data/usa_spend_data_2/federal_spending_by_state.csv")


class GDPSpendYears:
    def __init__(self):
        # party, year, dependence
        self.pgsy = {}

        print "Creating the GDP Info:"
        gdp_years = GDPYears.process()
        for state, state_info in gdp_years.syg.iteritems():
            print state
            years = sorted(state_info.items(), key=operator.itemgetter(0))
            print years

        print "Creating the Spend Info:"
        spend_years = SpendYears.process()
        for state, state_info in spend_years.sys.iteritems():
            print state
            years = sorted(state_info.items(), key=operator.itemgetter(0))
            print years

        # self.merge_gdp_spend_years(gdp_years.syg, spend_years.sys)
        self.do_party_years(gdp_years.syg, spend_years.sys)


    def do_party_years(self, gdp_years, spend_years):
        for party in Globals.parties:
            self.pgsy[party] = {}

        for state_name, party in Globals.state_names_party.iteritems():
            gdp_hash =  gdp_years[state_name]
            spend_hash = spend_years[state_name]

            for year, gdp in gdp_hash.iteritems():
                spend = spend_hash[year]
                dependency = float(spend)/gdp
                count = 0
                if dependency > 0.2:
                    count = 1
                party_year_hash = self.pgsy[party]
                if year in party_year_hash:
                    party_year_hash[year] += count
                else:
                    party_year_hash[year] = count

        print self.pgsy

        # do it in percentage now:
        for party, party_year_hash in self.pgsy.iteritems():
            for year in party_year_hash.keys():
                party_year_hash[year] = (float(party_year_hash[year])/Globals.parties_totals[party]) * 100

        for party, party_year_hash in self.pgsy.iteritems():
            print party
            for year, dependency in party_year_hash.iteritems():
                dependence_percent_str = "{0:.2f}".format(dependency)
                print year, dependence_percent_str


    def merge_gdp_spend_years(self, gdp_years, spend_years):
        arrayout = []

        header = [ "State", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014" ]

        # write the output to the file:
        with open("/Volumes/Personal2/data/output/years_state_spend_gdp.csv", 'w+') as fout:
            writer = csv.writer(fout)
            # write the header:
            arrayout = header
            writer.writerow(arrayout)

            for state_code in Globals.state_codes_list:
                state_name = Globals.state_codes[state_code]

                gdp_hash =  gdp_years[state_name]
                spend_hash = spend_years[state_name]

                print state_code, state_name

                arrayout = [state_code]
                for year in range(2005, 2015):
                    gdp = gdp_hash [str(year)]
                    spend = spend_hash[ str(year)]
                    dependence_percent_str = "{0:.2f}".format((float(spend)/gdp)*100)

                    arrayout.append(dependence_percent_str)

                writer.writerow(arrayout)

        fout.close()



def main():
    Globals()
    GDPSpendYears()


if __name__=='__main__':
    main()