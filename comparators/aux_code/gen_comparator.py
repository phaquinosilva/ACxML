

# inserir numeros em binario "0bXXXX" ajuda, se for colocar na mao
def generate_format(a0: int, b0: int, a1: int, b1: int):
    dec_sums = generate_sums(approx, num)
    bin_sums = []
    for i in dec_sums:
        bin_sums.append((format(i[0],'#010b')[2:], format(i[1],'#010b')[2:], format(i[2],'#010b')[2:]))
    return bin_sums


# recebe a mudanca no valor de 'a' e 'b' -> gera arquivos de estimulos para HSPICE
def gen_files(a0, b0, a1, b1, n):
    ## a0, b0: valores de 'a' e 'b' antes
    ## a1, b1: valores de 'a' e 'b' depois
    ## n: numero de bits

    voltage_arc = generate_format(a0, b0, a1, b1)
    # index for measure definitions
    # write input sources in a file
    
    with open("sources/sources_sum" + str(sums.index(i)) + ".cir",'w+') as file:
        file.write("** sources file for sum " + str(sums.index(i))+ '\n\n')
        # writes all input sources for A
        file.write("*n-bit input A\n")
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
