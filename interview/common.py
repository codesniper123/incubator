import time;
import csv;

class Globals:
    # we need states as a list and the individual agencies as lists:
    state_codes = {}
    state_names = {}
    state_names_party = {}
    state_codes_list = [ "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA",
                                 "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                                 "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT",
                                 "VA", "WA", "WV", "WI", "WY"]

    state_names_list = [ "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
                                 "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
                                 "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
                                 "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
                                 "New Jersey",
                                 "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
                                 "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
                                 "Utah", "Vermont",
                                 "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming" ]

    state_names_party = {
        "Vermont":"D", "Hawaii":"D", "Rhode Island":"D", "Massachusetts":"D","New York":"D", "California":"D",
        "Maryland":"D", "New Mexico":"D", "Illinois":"D", "Connecticut":"D", "New Jersey":"D", "Washington":"D",
        "Delaware":"D", "Oregon":"D",
        "Michigan":"U", "Pennsylvania":"U", "Florida":"U", "Minnesota":"U", "North Carolina":"U",
        "Ohio":"U", "Wisconsin":"U", "Arizona":"R", "Colorado":"U", "Louisiana":"D", "Virginia":"R",
        "Kentucky":"D", "Iowa":"U",
        "Maine":"D", "Georgia":"U", "Nevada":"D",
        "Mississippi":"R", "Texas":"R", "Indiana":"R", "West Virginia":"R", "Arkansas":"R", "Missouri":"R",
        "Nebraska":"R", "New Hampshire":"R", "Tennessee":"R", "South Carolina":"R","Kansas":"R", "Oklahoma":"R",
        "Montana":"R","South Dakota":"R", "Alaska":"R", "Alabama":"R", "North Dakota":"R", "Utah":"R", "Idaho":"R",
        "Wyoming":"R"
    }

    parties = {
        "R": "Republic Party", "D" : "Democratic Party", "U": "Undecided"
    }

    parties_totals = {
        "R": 0, "D" : 0, "U": 0
    }

    party_colors = { "R":"red", "D":"blue", "U":"gray"}


    # create the states list:
    def __init__(self):

        for i in range(0,len(Globals.state_codes_list)):
            Globals.state_codes[ Globals.state_codes_list[i] ] = Globals.state_names_list[i]

        for i in range(0, len(Globals.state_names_list)):
            Globals.state_names[ Globals.state_names_list[i] ] =  Globals.state_codes_list[i]

        for state, party in Globals.state_names_party.iteritems():
            Globals.parties_totals[party] += 1


class MyTimer:
    def __init__(self):
        self.start = time.clock()

    def stop(self):
        return time.clock() - self.start

class Utils:
    oneMillion = 1000000

    @staticmethod
    def millions(f):
        return Utils.put_comma((int(f)/Utils.oneMillion))

    @staticmethod
    def put_comma(num):
        prefix = "-" if num < 0 else ""
        return prefix + Utils.put_comma2(abs(num))

    @staticmethod
    def put_comma2(num):
        if num <= 999:
            return "{}".format(num)
        return Utils.put_comma2(num/1000) + "," + (Utils.put_comma2(num%1000)).zfill(3)

class BaseFile:
    SAMPLE_COUNT=10000
    PRINT_SAMPLE = False
    SAMPLE = True
    WRITE = True

    def __init__(self):
        self.do_init();

        self.negative_records = 0
        self.negative_dollars = 0
        self.total_records = 0
        self.total = 0

    # file name and list of columns
    def read_file(self, filename, col_list):
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

                if BaseFile.PRINT_SAMPLE:
                    # just print one sample:
                    if count == 2:
                        for i in range(0, len(line)):
                            print "{} {}: {}".format(i, columns[i], line[i])

                if BaseFile.WRITE:
                    self.do_populate(count, line, col_list)

                if BaseFile.SAMPLE and count > BaseFile.SAMPLE_COUNT:
                    break

        f.close()
        print " - lines read: {}".format(Utils.put_comma(count))
        self.total_records += count

    @staticmethod
    # state is the common key
    def do_merge_spend_gdp(filename, spend, gdp, header):
        merged = {}

        print "inside do_merge_spend"
        print "spend:"
        print spend
        print "gdp:"
        print gdp

        for key1, val1 in spend.iteritems():
            if key1 in gdp:
                val2 = gdp[key1]
                merged[key1] = (val1, val2)

        print merged

        # write it into the file:
        if not BaseFile.WRITE:
            return

        arrayout = []

        # write the output to the file:
        with open(filename, 'w+') as fout:
            writer = csv.writer(fout)
            # write the header:
            arrayout = header
            writer.writerow(arrayout)
            for state in Globals.state_codes_list:
                tuple = merged[state]
                spend = int(tuple[0]) / Utils.oneMillion
                gdp = int(tuple[1])
                spend_percent = 100.0 * spend / gdp
                spend_percent_str = "{0:.2f}".format(spend_percent)
                arrayout = [state, spend, gdp, spend_percent_str]
                writer.writerow(arrayout)

        fout.close()


if __name__=='__main__':
    g = Globals()
    print g.state_names