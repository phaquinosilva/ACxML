## gera grupos de soma para cada par de primos
import math
import sys

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
        # soma pode não ser comutativa
        if (approx):
            for j in primes:
                groups.append((i, j, i+j))
        else:
            for j in range(primes.index(i), len(primes)):
                groups.append((i, primes[j], i + primes[j]))
    # NÃO PRECISO MAIS ESCREVER EM UM ARQUIVO
    # for i in groups: print(groups.index(i))
    # file = open('sums_decimal.txt', 'w')
    # for i in groups:
    #     file.write(str(i[0]) + '+' + str(i[1]) + '=' + str(i[2]) + '\n')
    # file.close()
    return groups

# assumindo que Cin = '0' em todos os casos
def generate_format(approx, num):
    dec_sums = generate_sums(approx, num)
    bin_sums = []
    for i in dec_sums:
        print(i)
        bin_sums.append((format(i[0],'#08b'), format(i[1],'#08b'), format(i[2],'#08b')))
    return bin_sums

# gera arquivos de estímulos para HSPICE
def gen_files(approx, num):
    sums = generate_format(approx, num)
    # index for measure definitions
    change = 0
    # write input sources in a file
    for i in sums:
        with open("sources/sources_sum" + "{:0>2d}".format(sums.index(i)) + ".cir",'w+') as file:
            file.write("** sources file for sum " + "{:0>2d}".format(sums.index(i))+ '\n\n')
            # writes all input sources for A
            file.write("*8-bit input A\n")
            it = 0
            for bit in i[0][ : :-1]:
                if (bit == '0'):
                    file.write("Va" + str(it) + " a" + str(it) +"_in gnd PWL(0n 0)\n")
                else:
                    change = it
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
            for bit in i[2][::-1]:
                if (approx):
                    file.write(".measure tran tplh_s" + str(it) + " trig v(a" + str(change) + ") val='0.5*0.7' rise=1 targ v(s" + str(it) + "_in) val='0.5*0.7' rise=1\n")
                else:
                    if (bit == '1'):
                        file.write(".measure tran tplh_s" + str(it) + " trig v(a" + str(change) + ") val='0.5*0.7' rise=1 targ v(s" + str(it) + "_in) val='0.5*0.7' rise=1\n")
                it += 1

gen_files(True, 5)
################### COISAS QUE QUERO TESTAR ###############
# → se os parametros do HSPICE estiverem funcionando com arquivos separados,
# fazer a redução de tensão fica mais fácil, aí altero os 0.7 aqui por vdd
# e os tempos por 't*n'
