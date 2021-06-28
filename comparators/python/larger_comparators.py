## !! This file contains functions that simulate the behaviour
## of each n-bit comparator. These comparators are:
## -> Exact Dedicated Comparator (EDC)
## -> Approximate Dedicated Comparator 2 (ADC2)
## -> Approximate Dedicated Comparator 6 (ADC6)
## -> 4-bit Reduced Chain Comparator (RCC4)
## -> 8-bit Reduced Chain Comparator (RCC8)

#!! Exact Dedicated Comparator (EDC)
def n_edc(a, b, n):
    # formatting stuff
    a = format(a, '#0%db' % (n+2))[:1:-1]
    b = format(b, '#0%db' % (n+2))[:1:-1]
    a = list(map(int, a))
    b = list(map(int, b))
    # compute xnors
    eq = [0]*n
    for i in range(1,n):
        eq[i] = ~(a[i] ^ b[i])
    # compute greater for each bit
    g = [0]*n
    for i in range(n):
        temp = 1
        for k in range(i+1, n):
            temp &= eq[k]
        g[i] = temp & a[i] & ~b[i]
    # compute final comparison
    greater = 0
    for i in range(n):
        greater |= g[i]
    return greater&1 == 1


#!! Approximate Dedicated Comparator 2 (ADC2)
def n_adc2(a, b, n):
    # formatting stuff
    a = format(a, '#0%db' % (n+2))[:1:-1]
    b = format(b, '#0%db' % (n+2))[:1:-1]
    a = list(map(int, a))
    b = list(map(int, b))
    # compute xnors
    eq = [0]*n
    for i in range(n/4+1,n):
        eq[i] = ~(a[i] ^ b[i])
    # compute greater for each bit
    g = [0]*n
    for i in range(n/4,n):
        temp = 1
        for k in range(i+1, n):
            temp &= eq[k]
        g[i] = temp & a[i] & ~b[i]
    # compute final comparison
    greater = 0
    for i in range(n/4,n):
        greater |= g[i]
    return greater&1 == 1

#!! Approximate Dedicated Comparator 6 (ADC6)
def n_adc6(a, b, n):
    # formatting stuff
    a = format(a, '#0%db' % (n+2))[:1:-1]
    b = format(b, '#0%db' % (n+2))[:1:-1]
    a = list(map(int, a))
    b = list(map(int, b))
    # compute xnors
    eq = [0]*n
    for i in range(n/2+1,n):
        eq[i] = ~(a[i] ^ b[i])
    # compute greater for each bit
    g = [0]*(n/2)
    for i in range(n/2, n):
        temp = 1
        for k in range(i+1, n):
            temp &= eq[k]
        g[i] = temp & a[i] & ~b[i]
    # compute final comparison
    greater = 0
    for i in range(n/4, n/2):
        greater |= b[i]
    for i in range(n/2, n):
        greater |= g[i]
    return greater&1 == 1

#!! 4-bit Reduced Chain Comparator (RCC4)
def rcc4(a,b):
    a = [int(i) for i in a][::-1]
    b = [int(i) for i in b][::-1]
    eq1 = ~(a[1] ^ b[1])
    eq2 = ~(a[2] ^ b[2])
    eq3 = ~(a[3] ^ b[3])
    eq0 = ~(a[0] ^ b[0])  # mais uma xnor
    n3 = ~(a[3] & ~b[3])
    n2 = ~(a[2] & ~b[2] & eq3)
    n1 = ~(a[1] & ~b[1] & eq3 & eq2)
    n0 = ~(a[0] & ~b[0] & eq3 & eq2 & eq1)
    return ~(n0 & n1 & n2 & n3) & 1, (eq0 & eq1 & eq2 & eq3) & 1 # mais uma and

#!! 8-bit Reduced Chain Comparator (RCC8)
def rcc8(a,b):
    msb_a = format(a & (15<<4),'#06b')[2:]
    msb_b = format(b & (15<<4),'#06b')[2:]
    lsb_a = format(a & 15,'#06b')[2:]
    lsb_b = format(b & 15,'#06b')[2:]
    msb_comp, msb_eq = rcc4(msb_a,msb_b)
    lsb_comp = rcc4(lsb_a,lsb_b)
    greater = msb_comp | (msb_eq & lsb_comp)
    return greater&1 == 1