
# funções que simulam o comportamento lógico de cada FA aproximado
def sma(a, b, c_in):
    sum = [0,1,0,0,0,0,0,1]
    c_out = [0,0,1,1,0,1,1,1]
    pos = ((a<<2) + (b<<1) + c_in)
    return (sum & 1, c_out & 1)

def ama1(a, b, c_in):
    sum = [1,1,0,0,1,0,0,0]
    c_out = [0,0,1,1,0,1,1,1]
    pos = ((a<<2) + (b<<1) + c_in)
    return (sum & 1, c_out & 1)

def ama2(a, b, c_in):
    sum = [0,1,0,1,0,0,0,1]
    c_out = [0,0,0,0,1,1,1,1]
    pos = ((a<<2) + (b<<1) + c_in)
    return (sum & 1, c_out & 1)


def axa2(a, b, c_in):
    sum = [1,1,0,0,0,0,1,1]
    c_out = [0,0,0,1,0,1,1,1]
    pos = ((a<<2) + (b<<1) + c_in)
    return (sum & 1, c_out & 1)

def axa3(a, b, c_in):
    sum = [0,1,0,0,0,0,0,1]
    c_out = [0,0,0,1,0,1,1,1]
    pos = ((a<<2) + (b<<1) + c_in)
    return (sum & 1, c_out & 1)

def exact(a, b, c_in):
    sum = [0,1,1,0,1,0,0,1]
    c_out = [0,0,0,1,0,1,1,1]
    pos = ((a<<2) + (b<<1) + c_in)
    return (sum[pos], c_out[pos])

def bxfa(a, b, c_in):
    return (a & 1, b & 1)