import numpy;
import csv;

def testMedian():
    items = [1,2,3,4]
    print numpy.median(numpy.array(items))

def testCSV():

    ifile  = open('test.csv', "rb")
    reader = csv.reader(ifile)

    rownum = 0
    for row in reader:
        # Save header row.
        if rownum == 0:
            header = row
        else:
            colnum = 0
            for col in row:
                print '%-8s: %s' % (header[colnum], col)
                colnum += 1

        rownum += 1

    ifile.close()

def main():
    # testMedian()
    testCSV()


if __name__=="__main__":
    main()