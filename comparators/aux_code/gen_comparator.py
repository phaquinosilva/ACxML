# usado para gerar measures
from ac_operations import greater
from adders import *

def differ_test(cs, ns, f, n):
    # cs, ns: current state and next state, respectively (strings of bits)
    # f: boolean function to be evaluated (can be described with logic operators or look-up tables), should be 1bit only
    # apply function to both states
    form = '#0' + str(2*n + 2) + 'b'
    cs, ns = format(cs, form)[2:], format(ns, form)[2:]
    cf, nf = f(cs), f(ns)
    if cf == nf:  # if result changes
        return False
    # if only one input changes
    dif_bit = -1
    for i in range(len(cs)):
        if dif_bit != -1 and cs[i] != ns[i]:
            return False
        elif dif_bit == -1 and cs[i] != ns[i]:
            dif_bit = i
    if dif_bit == -1: return False
    return True

def find_diffs(cs, ns, f, n):
    form = '#0' + str(2*n + 2) + 'b'
    cs, ns = format(cs, form)[2:], format(ns, form)[2:]
    cf, nf = f(cs), f(ns)
    dif_bit = -1
    k = 0
    rof_s = ''
    rof_f = ''
    rise = lambda a, b: "fall" if a > b else "rise"
    for i in range(len(cs)-1, -1, -1):
        if dif_bit == -1 and cs[i] != ns[i]:
            dif_bit = k
            rof_s = rise(cs[i],ns[i])
            rof_f = rise(cf, nf)
        k += 1
    if dif_bit >= n:
        return ("a"+str(dif_bit-n), rof_s, rof_f) 
    return ("b"+str(dif_bit), rof_s, rof_s)

def inputs_of_interest(f, n):
    # f: function to be evaluated
    # n: number of input bitsinp
    inputs = [(i,j) for i in range(2**(2*n)) for j in range(2**(2*n)) if i != j]
    inputs = filter(lambda tup: differ_test(tup[0], tup[1], f, n), inputs)
    return list(inputs)

def delay_arcs_per_comparator(adders, names):
    k = 0
    infos = {}
    interest = {}
    for adder in adders:
        interest[names[k]] = inputs_of_interest((lambda g: greater(adder, g[0:4], g[4:], 4)), 4)
        get_infos = lambda tup: find_diffs(tup[0], tup[1], (lambda g: greater(adder, g[0:4], g[4:], 4)), 4)
        infos[names[k]] = list(map(get_infos, interest[names[k]]))
        k += 1
    return interest, infos

def create_files_comparators():
    adders = [ama2]
    names = [str(i.__name__) for i in adders]
    interest, infos = delay_arcs_per_comparator(adders, names)

    for add in names:
        k = 0
        for tup in interest[add]:
            gen_files(tup[0]>>4, tup[0]&15, tup[1]>>4, tup[1]&15, 4, add+"_"+str(k), infos[add][k])
            k += 1

# recebe a mudanca no valor de 'a' e 'b' -> gera arquivos de estimulos para HSPICE
# obs: no momento, usar somente com naturais
def gen_files(a0, b0, a1, b1, n, file_name, infos):
    ## a0, b0: valores de 'a' e 'b' antes
    ## a1, b1: valores de 'a' e 'b' depois
    ## n: numero de bits
    form = '#0' + str(n + 2) + 'b'
    tups = []  # lista com tuplas (a0, a1, b0, b1)
    tups.append((format(a0, form)[2:][::-1], format(a1,form)[2:][::-1], format(b0,form)[2:][::-1], format(b1,form)[2:][::-1]))
    # index for measure definitions
    # write input sources in a file

    with open("sources/source_" + file_name + ".cir",'w+') as file:
        file.write("** sources and measures for comparator type: "+file_name+"\n\n")
        for k in range(len(tups)):
            tup = tups[k]
            # writes all input sources for A
            file.write("*"+str(n)+"-bit input A\n")
            for i in range(n):
                if (tup[0][i] == '0'):
                    if (tup[1][i] == '0'):
                        file.write("Va" + str(i) + " a" + str(i) +"_in gnd PWL(0n 0)\n")
                    else:
                        file.write("Va" + str(i) + " a" + str(i) +"_in gnd PWL(0n 0 1n 0 1.1n vdd)\n")
                else:
                    if (tup[1][i] == '0'):
                        file.write("Va" + str(i) + " a" + str(i) +"_in gnd PWL(0n vdd 1n vdd 1.1n 0)\n")
                    else:
                        file.write("Va" + str(i) + " a" + str(i) +"_in gnd PWL(0n vdd)\n")
            # writes all input sources for A
            file.write("*"+str(n)+"-bit input B\n")
            for i in range(n):
                if (tup[2][i] == '0'):
                    if (tup[3][i] == '0'):
                        file.write("Vb" + str(i) + " b" + str(i) +"_in gnd PWL(0n 0)\n")
                    else:
                        file.write("Vb" + str(i) + " b" + str(i) +"_in gnd PWL(0n 0 1n 0 1.1n vdd)\n")
                else:
                    if (tup[3][i] == '0'):
                        file.write("Vb" + str(i) + " b" + str(i) +"_in gnd PWL(0n vdd 1n vdd 1.1n 0)\n")
                    else:
                        file.write("Vb" + str(i) + " b" + str(i) +"_in gnd PWL(0n vdd)\n")
            
        # write measures
        (bit, in_rof, out_rof) = infos
        file.write("\n*measures\n")
        type = "hl" if out_rof == "fall" else "lh"
        file.write(".measure tran tp"+type+" trig v("+bit+") val='0.5*vdd' "+ \
                    in_rof+"=1 targ v(greater) val='0.5*vdd' "+ out_rof +"=1\n")


#adders = [exact, sma, ama1, ama2, axa2, axa3, bxfa]
#names = [str(i.__name__) for i in adders]
#interest, infos = delay_arcs_per_comparator(adders, names)

create_files_comparators()

### TODOs RELEVANTES:
# gerar os arquivos de fontes e measures para o greater no modo: exato, sma, ama1, ama2, axa2, 
#       axa3, dedicado, dedicados com aproximacoes

## Comentarios para um eu do futuro que va mexer nisso aqui:
# 1. As estruturas das funcoes ficaram meio confusas porque eu estava tratando como operacoes e nao como funcoes logicas.
#    Se, por exemplo, eu tratasse dos inputs_of_interest como uma funcao booleana generica, nao seria preciso usar duas comprehensions
#    e ainda ha o beneficio de ser mais modular. Eh uma troca a ser feita no futuro.
# 2. O tanto de lambda que apareceu so pra interfacear com funcoes antigos so grita o tanto que eu preciso refatorar esse codigo todo D:

### To-dos pra quando eu tiver tempo: 
# generalizar gen_files para arcos de transicao maiores
# generalizar differ para, dadas duas linhas de uma tabela verdade, avaliar se sao de interesse para medicao de atraso
# encontrar todas as transicoes de interesse em uma determinada tabela
# automatizar o fluxo para: dada uma funcao logica ou tabela verdade, gerar todos os arcos de atraso e seus
#       arquivos de simulacao usar algum algoritmo de grafos (caminho euleriano, por ex) para definir todos 
#       os arcos de transicao para uma determinada tabela, removendo arestas ja utilizadas e iterando ate 
#       encontrar todos os arcos possiveis, e concatena-los junto de arestas que tenham eventualmente sobrado

