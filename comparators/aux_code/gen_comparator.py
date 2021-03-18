# usado para gerar measures
from ac_operations import *

# Bem da pra alterar differ pra funcionar com qualquer funcao logica
# checks if comparison differs and if so, 
# if it is only by one bit, returns the (bit, in_rof, out_rof) else return None
def differ(a0, b0, a1, b1, adder, n):
    form = '#0' + str(n + 2) + 'b'
    a0 = format(a0, form)[2:]
    a1 = format(a1, form)[2:]
    b0 = format(b0, form)[2:]
    b1 = format(b1, form)[2:]
    # checks if comparison differs
    geq0 = geq(adder, a0, b0, n)[1]
    geq1 = geq(adder, a1, b1, n)[1]
    if geq0 == geq1:
        return None
    # checks differing bits
    ab0 = a0 + b0
    ab1 = a1 + b1
    dif_bit = -1
    for i in range(2*n):
        if dif_bit == -1:
            if ab0[i] != ab1[i]:
                dif_bit = i
        elif ab0[i] != ab1[i]:
            return None
    if dif_bit == -1: return None
    if dif_bit < n:
        banana = str(dif_bit)
        return ("a"+banana, rise(ab0[dif_bit],ab1[dif_bit]), rise(geq0, geq1)) 
    return ("b"+str(dif_bit-8), rise(ab0[dif_bit],ab1[dif_bit]), rise(geq0, geq1))

def inputs_of_interest(adder, r):
    inputs = [(i,j) for i in range(r) for j in range(r)]
    inputs = [(i,j) for i in inputs for j in inputs if i != j]
    inputs = filter((lambda x: differ(x[0][0], x[0][1], x[1][0], x[1][1], adder, 2) != None), inputs)
    return list(inputs)

def rise(a, b):
    if a > b:
        return "fall"  # high-low
    else:
        return "rise"  # low-high

# recebe a mudanca no valor de 'a' e 'b' -> gera arquivos de estimulos para HSPICE
# obs: no momento, usar somente com naturais
def gen_files(a0, b0, a1, b1, n, adder, file_name):
    ## a0, b0: valores de 'a' e 'b' antes
    ## a1, b1: valores de 'a' e 'b' depois
    ## n: numero de bits
    form = '#0' + str(n + 2) + 'b'
    bin_values = []  # lista com tuplas (a0, a1, b0, b1)
    bin_values.append((format(a0, form)[2:], format(a1,form)[2:], format(b0,form)[2:], format(b1,form)[2:]))
    # index for measure definitions
    # write input sources in a file

    with open("sources/sources_" + file_name + ".cir",'w+') as file:
        file.write("** sources and measures for comparator type: "+file_name+"\n\n")
        for tup in bin_values:
            # writes all input sources for A
            file.write("*"+str(n)+"-bit input A\n")
            it = 0
            for i in range(n-1, -1, -1):
                if (tup[0][i] == '0'):
                    if (tup[1][i] == '0'):
                        file.write("Va" + str(it) + " a" + str(it) +"_in gnd PWL(0n 0)\n")
                    else:
                        file.write("Va" + str(it) + " a" + str(it) +"_in gnd PWL(0n 0 1n 0 1.1n vdd)\n")
                else:
                    if (tup[1][i] == '0'):
                        file.write("Va" + str(it) + " a" + str(it) +"_in gnd PWL(0n vdd 1n vdd 1.1n 0)\n")
                    else:
                        file.write("Va" + str(it) + " a" + str(it) +"_in gnd PWL(0n vdd)\n")
                it += 1
            # writes all input sources for A
            file.write("*"+str(n)+"-bit input B\n")
            it = 0
            for i in range(n-1, -1, -1):
                if (tup[2][i] == '0'):
                    if (tup[3][i] == '0'):
                        file.write("Vb" + str(it) + " b" + str(it) +"_in gnd PWL(0n 0)\n")
                    else:
                        file.write("Vb" + str(it) + " b" + str(it) +"_in gnd PWL(0n 0 1n 0 1.1n vdd)\n")
                else:
                    if (tup[3][i] == '0'):
                        file.write("Vb" + str(it) + " b" + str(it) +"_in gnd PWL(0n vdd 1n vdd 1.1n 0)\n")
                    else:
                        file.write("Vb" + str(it) + " b" + str(it) +"_in gnd PWL(0n vdd)\n")
                it += 1
            
        # write measures
        (bit, in_rof, out_rof) = differ(a0, b0, a1, b1, adder, n) 
        file.write("\n*measures\n")
        type = "hl" if out_rof == "fall" else "lh"
        file.write(".measure tran tp"+type+" trig v("+bit+") val='0.5*vdd' "+ \
                    in_rof+"=1 targ v(geq) val='0.5*vdd' "+ out_rof +"=1\n")




### TODOs RELEVANTES:
# gerar os arquivos de fontes e measures para o geq no modo: exato, sma, ama1, ama2, axa2, 
#       axa3, dedicado, dedicados com aproximacoes

## Comentarios para um eu do futuro que va mexer nisso aqui:
# 1. As estruturas das funcoes ficaram meio confusas porque eu estava tratando como operacoes e nao como funcoes logicas.
#    Se, por exemplo, eu tratasse dos inputs_of_interest como uma funcao booleana generica, nao seria preciso usar duas comprehensions
#    e ainda ha o beneficio de ser mais modular. Eh uma troca a ser feita no futuro.

### To-dos pra quando eu tiver tempo: 
# generalizar gen_files para arcos de transicao maiores
# generalizar differ para, dadas duas linhas de uma tabela verdade, avaliar se sao de interesse para medicao de atraso
# encontrar todas as transicoes de interesse em uma determinada tabela
# automatizar o fluxo para: dada uma funcao logica ou tabela verdade, gerar todos os arcos de atraso e seus
#       arquivos de simulacao usar algum algoritmo de grafos (caminho euleriano, por ex) para definir todos 
#       os arcos de transicao para uma determinada tabela, removendo arestas ja utilizadas e iterando ate 
#       encontrar todos os arcos possiveis, e concatena-los junto de arestas que tenham eventualmente sobrado

