# from bitstring import BitArray
import adders as add
import arc_gen as primes
import pandas as pd


# RCA nbit
def approx_sum(op_a, op_b, n_bits):

    # bem, não pensei em outro jeito melhor de iterar sobre essas funções, então cá estamos
    adder = [add.sma, add.ama1, add.ama2, add.axa2, add.axa3]

    # passo operandos para binário de n_bits
    form = '#0' + str(n_bits + 2) + 'b'
    in_a = format(op_a, form)[2:]
    in_b = format(op_b, form)[2:]
    # para organizar o DF
    results = {
        "a" : op_a,
        "b" : op_b,
        "exact" : op_a + op_b
    }
    for a in adder:
        cin = 0
        final = ''
        for i in range(len(in_a)-1, -1, -1):
            fa = a(int(in_a[i]), int(in_b[i]), cin)
            final += str(fa[0])
            cin = fa[1]
        # já que se adiciona iterativamente do LSB até o MSB, invertemos a bistring do resultado
        # converte para binário, para permitir comparação mais fácil com o exato
        final_bin = final[::-1]             # esse método não considera complemento de dois, mas tudo bem para essa aplicação
        #final_dec = int(final_bin, 2)
        # b = BitArray(bin=final[::-1])
        # final = b.int                    # já esse b.int considera
        # adiciona resultados a um dict para criar o DF
        results[a.__name__] = final_bin
    return results

# executa cada soma e organiza resultados em um df que sera escrito em
def sum_primes(num, bit_len):
    sums = primes.generate_sums(True, num)
    s_list = []
    for s in sums:
        s_list.append(approx_sum(s[0], s[1], bit_len))
    results = pd.DataFrame(s_list)
    results.to_csv('prime_sums.csv')
    return results

# calcula a error distance para cada somador
# def calc_ed():

# testes:
print(sum_primes(5, 8))
