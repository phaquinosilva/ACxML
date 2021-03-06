import pandas as pd
# from bitstring import BitArray
from adders import *

# para o experimento
from arc_gen import generate_sums

########################### COISAS QUE QUERO TESTAR ############################# 
# -> acho que é mais fácil para visualização dos dados se eu plotar em arquivos #
# diferentes as somas em binario de cada bit                                    #
#################################################################################

# RCA simples nbit
def add(adder, in_a, in_b, cin, n_bits):
    final = ''
    for i in range(n_bits-1, -1, -1):
        fa = adder(int(in_a[i]), int(in_b[i]), cin)
        final += str(fa[0])
        cin = fa[1]
    return final

# calcula soma aproximada para um grupo de FAs
def approx_sum(op_a, op_b, n_bits, adder):
    # passo operandos para binario de n_bits
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
        final = add(a, in_a, in_b, 0, n_bits)
        # já que se adiciona iterativamente do LSB até o MSB, invertemos a bistring do resultado
        final_bin = final[::-1]
        final_dec = int(final_bin, 2)
        # adiciona resultados a um dict para criar o DF
        results[a.__name__] = final_dec
        err = format(final_dec ^ results['exact'], form)[2:]
        error.append(map(int, list(err)))
    return results, error

# executa a simulação de qualquer conjunto de somas para 
# qualquer conjunto de somadores definido dentro da função
def run_simulation(sums, bit_len):

    # lista de funcoes que simulam FAs aproximados
    adders = [sma, ama1, ama2, axa2, axa3, bxfa]
    add_list = [str(i.__name__) for i in adders]
    # sum list
    s_list = []
    # error list
    e_list = []

    for s in sums:
        tmp = approx_sum(s[0], s[1], bit_len, adders)
        s_list.append(tmp[0])
        [e_list.append(tmp[1][i]) for i in range(len(adders))]

    # organizacao e processamento dos resultados
    results = pd.DataFrame(s_list)
    dec_error = decimal_error_analysis(results, add_list)
    bin_error = bit_error(add_list, e_list, len(sums))
    # envia resultados para arquivos csv
    results.to_csv('sums_results.csv')
    dec_error.to_csv("error_analysis.csv")
    bin_error[0].to_csv("total_error_bit.csv")
    bin_error[1].to_csv("error_rate_bit.csv")

# erro bit a bit
def bit_error(adders, e_list, n_op):
    idx = pd.MultiIndex.from_product([adders, range(n_op)])
    e_list_df = pd.DataFrame(e_list, index=idx)
    print(e_list_df.loc[adders[0]])
    error_df = pd.DataFrame(e_list_df.loc[adders[0]].sum().rename(adders[0]))
    print(error_df)
    for i in adders[1:]: 
        error_df = error_df.join(e_list_df.loc[i].sum().rename(i))
    print(error_df)
    mean_df = error_df.div(n_op)
    print(mean_df)
    return error_df, mean_df

# erro decimal
def decimal_error_analysis(results, add):
    error = pd.DataFrame()  # erro em cada soma
    mean_ed = pd.Series(dtype='float', name='mean')  # erro médio de cada somador
    std_dev = pd.Series(dtype='float', name='std')  # desvio padrão dos resultados
    for adder in add:
        error[adder] = abs(results['exact'].subtract(results[adder]))
        mean_ed[adder] = error[adder].mean()
        std_dev[adder] = error[adder].std()
    return pd.DataFrame(mean_ed).join(std_dev)

## experimento: soma de primos
run_simulation(generate_sums(True, 2**7), 8)