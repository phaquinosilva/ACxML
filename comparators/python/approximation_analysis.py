import pandas as pd
# from bitstring import BitArray
from adders import *
from ac_operations import *

##################### ANALISE DE ERRO EM COMPARADORES 4bit ###################### 
# -> O que este programa faz é avaliar exaustivamente o erro gerado pela        #
#    aproximação em todos os valores possíveis da tabela verdade para cada      #
#    somador                                                                    #
# -> Temos 8 bits de entrada e 1 bit de saída, logo 2**8 entradas               #
#    na tabela verdade                                                          #
#################################################################################

# comparação aproximada com somadores
def sim_add(op_a, op_b, adders):
    results = {
        "default" : 1 if int(op_a,2) <= int(op_b,2) else 0
        }
    error = {}
    for i in adders:
        comp = leq(i, op_a, op_b, 4)
        results[i.__name__] = comp
        error[i.__name__] = comp ^ results['default']
    return results, error

def sim_dedicated(op_a, op_b, comparators):
    results = {
        "default" : 1 if int(op_a,2) <= int(op_b,2) else 0
        }
    error = {}
    for i in comparators:
        comp = i(op_a, op_b)
        results[i.__name__] = comp
        error[i.__name__] = comp ^ results['default']
    return results, error

def run_simulation():
    # compare approx adders and comparators with their exact counterparts on all possible outputs
    inputs = [(format(a,'#06b')[2:], format(b,'#06b')[2:]) for a in range(16) for b in range(16)]
    adders = [exact, sma, ama1, ama2, axa2, axa3]
    add_list = [i.__name__ for i in adders]
    comparators = [comp_exact, comp_approx1, comp_approx2, \
                    comp_approx3, comp_approx4, comp_approx5, comp_approx6]
    comp_names = [i.__name__ for i in comparators]
    # result lists
    r_add = []
    r_ded = []
    # error lists
    e_add = []
    e_ded = []
    for in_ in inputs:
        # adders
        tmp = sim_add(in_[0], in_[1], adders)
        r_add.append(tmp[0])
        e_add.append(tmp[1])
        # dedicated
        tmp = sim_dedicated(in_[0], in_[1], comparators)
        r_ded.append(tmp[0])
        e_ded.append(tmp[1])
    #results_adders = pd.DataFrame(r_add)
    error_adders = error_analysis(pd.DataFrame(e_add), add_list)
    #results_adders.to_csv('results_adders.csv')
    #error_adders.to_csv('error_adders.csv')
    #results_dedicated = pd.DataFrame(r_ded)
    error_dedicated = error_analysis(pd.DataFrame(e_ded), comp_names)
    #results_dedicated.to_csv('results_dedicated.csv')
    #error_dedicated.to_csv('error_dedicated.csv')

# erro bit a bit
def error_analysis(errors, names):
    ed = errors.sum()
    er = errors.mean()
    error = pd.DataFrame({'ED': ed, 'ER': er})
    error = error.transpose()
    print(error)
    return error

run_simulation()