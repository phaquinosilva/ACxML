#%%
#!! Dedicated n-bit comparator

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

#%%
#!! ADC2 n bit
def n_edc(a, b, n):
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

#%%
#!! Dedicated chained 8bit comparator (can be extended to any number n of bits, if n%4 == 0)

def comp_exact(a,b):
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
    
def comp8bit(a,b):
    msb_a = format(a & (15<<4),'#06b')[2:]
    msb_b = format(b & (15<<4),'#06b')[2:]
    lsb_a = format(a & 15,'#06b')[2:]
    lsb_b = format(b & 15,'#06b')[2:]
    msb_comp, msb_eq = comp_exact(msb_a,msb_b)
    lsb_comp = comp_exact(lsb_a,lsb_b)
    greater = msb_comp | (msb_eq & lsb_comp)
    return greater&1 == 1
