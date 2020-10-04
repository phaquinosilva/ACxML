# funções que simulam o comportamento lógico de cada FA aproximado

def sma(a, b, c_in):
    sum = c_in & ~(a ^ b)
    c_out = b | a & c_in
    return (sum & 1, c_out & 1)

def ama1(a, b, c_in):
    c_out = b | a & c_in
    return (~c_out & 1, c_out & 1)

def ama2(a, b, c_in):
    sum = c_in & (~a | b)
    return (sum & 1, a & 1)

def axa2(a, b, c_in):
    sum = ~(a ^ b)
    c_out = a & b | (a ^ b) & c_in
    return (sum & 1, c_out & 1)

def axa3(a, b, c_in):
    sum = c_in & ~(a ^ b)
    c_out = a & b | (a ^ b) & c_in
    return (sum & 1, c_out & 1)

# usado como prova de conceito
def exact(a, b, c_in):
    sum = a ^ b ^ c_in
    c_out = a & b | (a ^ b) & c_in
    return (sum & 1, c_out & 1)
