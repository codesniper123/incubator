def mytranslate(str):
    return str.translate(None, "$, ")

print "[ $124,456 ] translated to [{}]".format(mytranslate(" $123,456 " ))


def named_args(arg1=True, arg2=20):
    print "arg1 = {} arg2 = {}".format(arg1, arg2)

named_args()
named_args(arg1=False, arg2=1000)
named_args(arg2=999)


