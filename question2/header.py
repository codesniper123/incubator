def main():
    file = "Historic_Secured_Property_Tax_Rolls.csv"
    with open(file) as f:
        for line in f:
            processHeader(line)
            break
    f.close()

def processHeader(line):
    tokens = line.split(',')

    count = 0
    for token in tokens:
        token = token.strip().upper().replace(" ", "_")
        print "{}={}".format(token, count)
        count += 1


if __name__=="__main__":
    main()