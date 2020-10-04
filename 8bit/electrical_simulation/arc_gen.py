## gera grupos de soma para cada par de primos
import math
import sys

########################### COISAS QUE QUERO TESTAR ###########################
# -> se os parametros do HSPICE estiverem funcionando com arquivos separados, #
# fazer a redução de tensão fica mais fácil, aí altero os 0.7 aqui por vdd    #
# e os tempos por 't*n'                                                       #
###############################################################################

def sieve(n):
    A = [True]*n
    for i in range(2, int(math.sqrt(n))):
        if A[i]:
            for j in range(i*i, n, i):
                if (j < n):
                    A[j] = False
    primes = [1]
    for i in range(2,n):
        if A[i] == True:
            primes.append(i)
    return primes

def generate_sums(approx, num):
    primes = sieve(num)
    groups = []
    for i in primes:
        # soma pode nao ser comutativa
        if (approx):
            for j in primes:
                groups.append((i, j, i+j))
        else:
            for j in range(primes.index(i), len(primes)):
                groups.append((i, primes[j], i + primes[j]))
    # ja nao preciso escrever num arquivo, mas fica aqui caso precise
    # for i in groups: print(groups.index(i))
    # file = open('sums_decimal.txt', 'w')
    # for i in groups:
    #     file.write("sum"+ "{:0>2d}".format(groups.index(i)) + ": " + str(i[0]) + '+' + str(i[1]) + '=' + str(i[2]) + '\n')
    # file.close()
    return groups

# assumindo que Cin = '0' em todos os casos
def generate_format(approx, num):
    dec_sums = generate_sums(approx, num)
    bin_sums = []
    for i in dec_sums:
        bin_sums.append((format(i[0],'#010b')[2:], format(i[1],'#010b')[2:], format(i[2],'#010b')[2:]))
    return bin_sums

# gera arquivos de estimulos para HSPICE
def gen_files(approx, num):
    sums = generate_format(approx, num)
    # index for measure definitions
    # write input sources in a file
    for i in sums:
        with open("sources/sources_sum" + str(sums.index(i)) + ".cir",'w+') as file:
            file.write("** sources file for sum " + str(sums.index(i))+ '\n\n')
            # writes all input sources for A
            file.write("*8-bit input A\n")
            it = 0
            for bit in i[0][ : :-1]:
                if (bit == '0'):
                    file.write("Va" + str(it) + " a" + str(it) +"_in gnd PWL(0n 0)\n")
                else:
                    file.write("Va" + str(it) + " a" + str(it) + "_in gnd PWL(0n 0 1n 0 1.1n 0.7)\n")
                it += 1
            # writes all input sources for A
            file.write("*8-bit input B\n")
            it = 0
            for bit in i[1][ : :-1]:
                if (bit == '0'):
                    file.write("Vb" + str(it) + " b" + str(it) +"_in gnd PWL(0n 0)\n")
                else:
                    file.write("Vb" + str(it) + " b" + str(it) + "_in gnd PWL(0n 0 1n 0 1.1n 0.7)\n")
                it += 1
            # writes all measures for outputs
            file.write("\n*measures\n")
            it = 0
            for bit in i[2][ : :-1]:
                if (approx):
                    # low-high
                    file.write(".measure tran tplh_s" + str(it) + " trig v(tr) val='0.5*0.7' rise=1 targ v(s" + str(it) + "_in) val='0.5*0.7' rise=1\n")
                    # high-low
                    file.write(".measure tran tphl_s" + str(it) + " trig v(tr) val='0.5*0.7' rise=1 targ v(s" + str(it) + "_in) val='0.5*0.7' fall=1\n")
                else:
                    if (bit == '1'):
                        file.write(".measure tran tplh_s" + str(it) + " trig v(tr) val='0.5*0.7' rise=1 targ v(s" + str(it) + "_in) val='0.5*0.7' rise=1\n")
                it += 1
    return len(sums)
gen_files(True, 5)

