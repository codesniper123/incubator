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
            return str(num)
        return Utils.put_comma2(num/1000) + "," + (Utils.put_comma2(num%1000)).zfill(3)

print Utils.put_comma(1)
print "[{}]".format(Utils.millions(1111999))
print Utils.put_comma(123999)
print Utils.put_comma(992123999)
print Utils.put_comma(0)
print Utils.put_comma(-123456)

