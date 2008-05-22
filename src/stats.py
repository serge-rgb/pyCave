import pstats

s = pstats.Stats('startup')
d = pstats.Stats('prof')

def dumpS(regex):
    s.print_stats(regex)
def dumpD(regex):
    d.strip_dirs().sort_stats('cumulative').print_stats(regex)
