## !! This file contains functions that generate the SPICE circuits for 
## dedicated comparator circuits based on the number of bits 

from adders import *
#%%
# generate EDC
def spicegen_edc(n):
    # output file
    f = open("edc_%db.cir" % n, "w+")
    # signal information
    a_in = ['a%d' % i for i in range(n)]
    b_in = ['b%d' % i for i in range(n)]

    # initialize file
    f.write("* %d-bit Exact Dedicated Comparator\n\n.include gates.cir\n\n.subckt edc%db %s %s leq vdd\n" % \
            (n, n, ' '.join(a_in), ' '.join(b_in)))
    
    # compute xnors
    for i in range(1,n):
        f.write("   Xeq%d a%d b%d eq%d vdd xnor\n" % (i,i,i,i))
    f.write("\n")

    # negate B
    for i in range(n):
        f.write("   Xnb%d b%d nb%d vdd inv\n" % (i,i,i))
    f.write("\n")
    
    # compute greater for each bit
    count = 0
    for i in range(n-1, -1, -1):
        eqs = ['eq%d' % j for j in range(n-1, i, -1)]
        f.write("   Xn%d a%d nb%d %s n%d vdd nand%d\n" % (i, i, i, ' '.join(eqs), i, (2 + len(eqs))))
    f.write('\n')
    # compute less or equal than 
    ns = ['n%d' % i for i in range(n)]
    f.write("   Xgr %s gr vdd nand%d\n" % (' '.join(ns), len(ns)))
    f.write("   Xleq gr leq vdd inv\n.ends")
    f.close()

spicegen_edc(16)
#%%
# generate ADC2
def spicegen_adc2(n):
    # output file
    f = open("adc2_%db.cir" % n, "w+")
    # signal information
    a_in = ['a%d' % i for i in range(n)]
    b_in = ['b%d' % i for i in range(n)]
    n_4 = int(n/4)
    # initialize file
    f.write("* %d-bit Approximate Dedicated Comparator 2\n\n.include gates.cir\n\n.subckt adc2%db %s %s leq vdd\n" % \
            (n, n, ' '.join(a_in), ' '.join(b_in)))
    
    # compute xnors
    for i in range(n_4+1,n):
        f.write("   Xeq%d a%d b%d eq%d vdd xnor\n" % (i,i,i,i))
    f.write("\n")

    # negate B
    for i in range(n_4,n):
        f.write("   Xnb%d b%d nb%d vdd inv\n" % (i,i,i))
    f.write("\n")
    
    # compute greater for each bit
    count = 0
    for i in range(n-1, n_4-1, -1):
        eqs = ['eq%d' % j for j in range(n-1, i, -1)]
        f.write("   Xn%d a%d nb%d %s n%d vdd nand%d\n" % (i, i, i, ' '.join(eqs), i, (2 + len(eqs))))
    f.write('\n')
    # compute less or equal than 
    ns = ['n%d' % i for i in range(n_4,n)]
    f.write("   Xgr %s gr vdd nand%d\n" % (' '.join(ns), len(ns)))
    f.write("   Xleq gr leq vdd inv\n.ends")
    f.close()

# generate ADC6
def spicegen_adc6(n):
    # output file
    f = open("adc6_%db.cir" % n, "w+")
    # signal information
    a_in = ['a%d' % i for i in range(n)]
    b_in = ['b%d' % i for i in range(n)]
    n_2 = int(n/2)
    n_4 = int(n/4)
    # initialize file
    f.write("* %d-bit Approximate Dedicated Comparator 6\n\n.include gates.cir\n\n.subckt adc2%db %s %s leq vdd\n" % \
            (n, n, ' '.join(a_in), ' '.join(b_in)))
    
    # compute xnors
    for i in range(n_2+1,n):
        f.write("   Xeq%d a%d b%d eq%d vdd xnor\n" % (i,i,i,i))
    f.write("\n")

    # negate B
    for i in range(n_2,n):
        f.write("   Xnb%d b%d nb%d vdd inv\n" % (i,i,i))
    f.write("\n")
    
    # compute greater for each bit
    count = 0
    for i in range(n-1, n_2-1, -1):
        eqs = ['eq%d' % j for j in range(n-1, i, -1)]
        f.write("   Xn%d a%d nb%d %s n%d vdd nand%d\n" % (i, i, i, ' '.join(eqs), i, (2 + len(eqs))))
    f.write('\n') 
    
    # buffer b inputs
    for i in range(n_4, n_2):
        f.write("   Xib%d b%d ib%d vdd inv\n   Xbb%d ib%d bb%d vdd inv\n" % (i,i,i,i,i,i))
    f.write('\n')

    # compute less or equal than
    ns = ['n%d' % i for i in range(n_2,n)]
    bs = ['bb%d' %i for i in range(n_4, n_2)]
    f.write("   Xgr %s %s gr vdd nand%d\n" % (' '.join(ns), ' '.join(bs), len(ns) + len(bs)))
    f.write("   Xleq gr leq vdd inv\n.ends")
    f.close()

# generate any full adder based comparator (uses ripple carry architecture)
def spicegen_add(add, n):
    pass

# generate large NOR and NAND gates in SPICE for use in dedicated comparators
def gates(n):
    pass