import numpy;
import math;
import csv;

class SFHouse:
    ASSESSED_YEAR=0
    NEIGHBORHOOD_CODE=2
    BLOCK_LOT=4
    VOLUME_NUMBER=5
    CLASS_CODE=6
    YEAR_PROPERTY_BUILT=8
    NUMBER_OF_BEDROOMS=10
    NUMBER_OF_UNITS=13
    PROPERTY_AREA_IN_SQUARE_FEET=19
    LOT_AREA=21
    LOT_CODE=22
    CURRENT_SALES_DATE=34
    ASSESSED_IMPROVEMENT_VALUE=36
    ASSESSED_LAND_VALUE=37
    ZIPCODE_OF_PARCEL=39

    def __init__(self, errors, count, tokens):
        self.block_lot = tokens[SFHouse.BLOCK_LOT]
        self.cc = tokens[SFHouse.CLASS_CODE]
        self.nc = tokens[SFHouse.NEIGHBORHOOD_CODE]
        self.zipcode = tokens[SFHouse.ZIPCODE_OF_PARCEL]

        self.year = -1
        self.aiv = 0
        self.lv = 0
        self.units = 0;
        self.year_built = -1
        self.bedrooms = 0
        self.prop_area = 0
        self.lot_area = 0

        try:
            self.year = int(tokens[SFHouse.ASSESSED_YEAR])
            self.aiv = int(tokens[SFHouse.ASSESSED_IMPROVEMENT_VALUE])
            self.lv = int(tokens[SFHouse.ASSESSED_LAND_VALUE])
            self.units = int(tokens[SFHouse.NUMBER_OF_UNITS])
            self.bedrooms = int(tokens[SFHouse.NUMBER_OF_BEDROOMS])
            if len(tokens[SFHouse.YEAR_PROPERTY_BUILT]) > 0:
                self.year_built = int(tokens[SFHouse.YEAR_PROPERTY_BUILT])
            self.prop_area = float(tokens[SFHouse.PROPERTY_AREA_IN_SQUARE_FEET])
            self.lot_area = float(tokens[SFHouse.LOT_AREA])

        except ValueError:
            errors["readerror "+ str(count)] = tokens


class SFHouses:
    def __init__(self):
        self.houses = list()
        self.cc = {}
        self.block_lot = {}
        self.errors = {}
        self.nc = {}
        self.lv = {}
        self._1950 = { "before1950" : {}, "after1950": {} }
        self.bu = {}

    def readFile(self, filename):
        print "Reading file {}".format(filename)

        count = 0
        with open(filename) as f:
            reader = csv.reader(f)
            for line in reader:
                # skip the header:
                if count > 0:
                    house = SFHouse(self.errors, count, line)
                    self.houses.append(house)

                    self.doFrequentClass(house)
                    self.doAssessedValue(house)
                    self.doNAV(house)
                    self.doLandValues(house)
                    self.doUnits1950(house)
                    self.doBU(house)

                count += 1
                if count % 100000 == 0:
                    print ".",
        f.close()

        print "\nCompleted reading {} records - {} errors".format(count, len(self.errors))
        for k, v in self.errors.iteritems():
            print "{}: {}".format(k,v)

    def doFrequentClass(self, house):
        if house.cc not in self.cc:
            self.cc[house.cc] = 1
        else:
            self.cc[house.cc] += 1

    def doAssessedValue(self, house):
        if house.aiv > 0:
            if house.block_lot not in self.block_lot:
                self.block_lot[house.block_lot] = house
            else:
                old_house = self.block_lot[house.block_lot]
                if house.year > old_house.year:
                    self.block_lot[house.block_lot] = house

    def doNAV(self, house):
        if house.aiv > 0 and len(house.nc) > 0:
            if house.nc not in self.nc:
                self.nc[house.nc] = {}
            this_nc = self.nc[house.nc]

            if house.block_lot not in this_nc:
                this_nc[house.block_lot] = house
            else:
                old_house = this_nc[house.block_lot]
                if house.year > old_house.year:
                    this_nc[house.block_lot] = house

    def doLandValues(self, house):
        if house.year not in self.lv:
            self.lv[house.year] = [0,0]
        if house.lv > 0:
            current = self.lv[house.year]
            current[0] += house.lv
            current[1] += 1

    def doUnits1950(self, house):
        if house.year_built < 1776 or house.year_built > 2015:
            if house.year_built != -1:
                if "year_built_errors" not in self.errors:
                    self.errors["year_built_errors"] = 1
                else:
                    self.errors["year_built_errors"] += 1
            return

        houses = self._1950["before1950"] if house.year_built <= 1950 else self._1950["after1950"]

        if house.block_lot not in houses:
            houses[ house.block_lot ] = house
        else:
            # get the earliest record (this may have zero units that we should skip!
            old_house = houses[house.block_lot]
            if house.year < old_house.year:
                houses[house.block_lot] = house


    def doBU(self, house):
        if house.zipcode not in self.bu:
            self.bu[house.zipcode] = {}
        thisZC = self.bu[house.zipcode]
        if house.block_lot not in thisZC:
            thisZC[house.block_lot] = house
        else:
            old_house = thisZC[house.block_lot]
            if house.year >  old_house.year:
                thisZC[house.block_lot] = house


    def printMaxClassFraction(self):
        max_v = 0
        max_k = None
        total = 0
        for k,v in self.cc.iteritems():
            if v > max_v:
                max_v = v
                max_k = k
            total += v

        print "Max Class [{}] Total [{}] Max Class Frequency [{}] Percentage [{}]".format(max_k, total, max_v, (float(max_v)/total))

    def printAssessedValue(self):
        l = []

        for k,home in self.block_lot.iteritems():
            l.append(float(home.aiv))

        print "No of houses with improvements {} Median {} ".format(len(self.block_lot), numpy.median(numpy.array(l)))

    def printNAV(self):
        print "no of neighborhoods with houses having assessed improved value {}".format( len(self.nc) )
        min = -1
        min_n = None
        max = 0
        max_n = None
        for nb, houses in self.nc.iteritems():
            total = 0
            for k, house in houses.iteritems():
                total += house.aiv
            avg = float(total) / len(houses) if total > 0 else 0
            if avg > max:
                max = avg
                max_n = nb
            if min == -1 or avg < min:
                min = avg
                min_n = nb

        print "max neighborhood [{}] max val {}".format(max_n, max)
        print "min neighborhood [{}] min val {}".format(min_n, min)
        print "Difference is {}".format(max-min)


    def printLandValues(self):
        min = -1
        max = 0
        for year,value in self.lv.iteritems():
            if value[1] == 0:
                continue
            avg = float(value[0]) / value[1]
            if avg > max:
                max = avg
                maxyear = year
            if min == -1 or avg < min:
                min = avg
                minyear = year

        print "min [{}] minyear [{}] max [{}] maxyear [{}]".format(min, minyear, max, maxyear)
        if (maxyear-minyear) > 0:
            print "growth rate is {}".format ( (math.log(max/min)) / (maxyear - minyear) )

    def printUnits1950(self):
        bef_avg = 0.0
        bef_total = 0;
        aft_avg = 0.0
        aft_total = 0
        for year, houses in self._1950.iteritems():
            units = 0
            total = 0
            for k, house in houses.iteritems():
                if house.units > 0:
                    units += house.units
                    total += 1
            if year == "before1950":
                bef_avg = float(units) / total
                bef_total = total
            else:
                aft_avg = float(units) / total
                aft_total = total

        print "Before - all houses {} units > 0 {} avg = {} ".format(
            len(self._1950["before1950"]), bef_total, bef_avg )
        print "After - all houses {} units > 0 {} avg = {} ".format(
            len(self._1950["after1950"]), aft_total, aft_avg )
        print "Difference {}".format(aft_avg-bef_avg)

    def printBU(self):
        l = []
        for zc,houses in self.bu.iteritems():
            bedrooms = 0
            units = 0
            count = 0
            for k, house in houses.iteritems():
                if house.units > 0 and house.bedrooms > 0:
                    bedrooms += house.bedrooms
                    units += house.units
                    count += 1

            if units == 0:
                print "0 units for zipcode {}".format(zc)
                continue

            b_mean = float(bedrooms) / count
            u_mean = float(units) / count

            l.append(b_mean/u_mean)

        print "max BU Ratio [{}]".format(numpy.max(numpy.array(l)))

    def printBuiltUp(self):
        max = 0
        max_zc = 0
        for zc, houses in self.bu.iteritems():
            current = 0
            lot_area  = 0.0
            prop_area = 0.0
            for k, house in houses.iteritems():
                lot_area += house.lot_area
                prop_area += house.prop_area

            current = prop_area / lot_area
            if current > max:
                max = current
                max_zc = zc

        print "max Builtout [{}] in zipcode [{}]".format(max, max_zc)


def main():
    sfh = SFHouses()

    sfh.readFile('Historic_Secured_Property_Tax_Rolls.csv')

    if len(sfh.houses) == 0:
        return

    sfh.printMaxClassFraction()
    sfh.printAssessedValue()
    sfh.printNAV()
    sfh.printLandValues()
    sfh.printUnits1950()
    sfh.printBU()
    sfh.printBuiltUp()


if __name__ =="__main__":
    main()

