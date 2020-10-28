from bitstring import BitArray
import adders as add
from arc_gen import generate_sums
import pandas as pd

########################### COISAS QUE QUERO TESTAR ############################# 
# -> acho que é mais fácil para visualização dos dados se eu plotar em arquivos #
# diferentes as somas em binario de cada bit                                    #
#################################################################################

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
        "exact" : (op_a + op_b) & 0b11111111
        }
    error = []
    for a in adder:
        cin = 0
        final = ''
        for i in range(n_bits-1, -1, -1):
            fa = a(int(in_a[i]), int(in_b[i]), cin)
            final += str(fa[0])
            cin = fa[1]
        # já que se adiciona iterativamente do LSB até o MSB, invertemos a bistring do resultado 
        final_bin = final[::-1]
        # !!! não usa C2 !!!
        final_dec = int(final_bin, 2)
        # adiciona resultados a um dict para criar o DF
        results[a.__name__] = final_dec
        err = format(final_dec ^ results['exact'], form)[2:]
        error.append(map(int, list(err)))
    return results, error

# executa cada soma e organiza resultados em um df que sera escrito em
def sum_primes(num, bit_len):
    sums = generate_sums(True, num)
    add_list = ['sma', 'ama1', 'ama2', 'axa2', 'axa3']
    idx = pd.MultiIndex.from_product([add_list, range(len(sums))], names=['adder', 'exp'])
    s_list = []
    e_list = []
    a = []
    sum = 0
    for s in sums:
        tmp = approx_sum(s[0], s[1], bit_len)
        s_list.append(tmp[0])
        a.append((sum, tmp[1][2]))
        [e_list.append(tmp[1][i]) for i in range(5)]
        sum += 1
    ### resultados
    results = pd.DataFrame(s_list)
    results.to_csv('dec_sums.csv')
    # resultados em binario

    ### calcula erros por bit
    err = pd.DataFrame(e_list, index=idx)
    error = pd.DataFrame(err.loc['sma'].sum().rename('sma'))
    for i in add_list[1:]: 
        error = error.join(err.loc[i].sum().rename(i))
    error.to_csv('total_error_bit.csv')
    error.div(len(sums)).to_csv('error_rate_bit.csv')
    ## calcula erros por 
    calc_ed(results, add_list)

# calcula erro para cada somador
def calc_ed(results, add):
    ed = pd.DataFrame()  # erro em cada soma
    mean_ed = pd.Series(dtype='float', name='mean')  # erro médio de cada somador
    std_dev = pd.Series(dtype='float', name='std')  # desvio padrão dos resultados
    for adder in add:
        ed[adder] = abs(results['exact'].subtract(results[adder]))
        mean_ed[adder] = ed[adder].mean()
        std_dev[adder] = results[adder].std()
    err_analysis = pd.DataFrame(mean_ed).join(std_dev)
    err_analysis.to_csv('error_analysis.csv')

# testes:
sum_primes(2**7, 8)