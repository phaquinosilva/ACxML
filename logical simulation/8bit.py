# from bistring import BitArray
import adders

# vou começar escrevendo um RCA 4bit
def approx_sum(op_a, op_b, adder_type, n_bits):
    # passo operandos para binário para operar bit a bit
    # formatação para decidirmos número bits
    form = '#0' + str(n_bits + 2) + 'b'
    op_a = format(op_a, form)[2:]
    op_b = format(op_b, form)[2:]

    cin = 0
    result = ''

    for i in range(len(op_a)-1, -1, -1):
        fa = adder_type(int(op_a[i]), int(op_b[i]), cin)
        print("In: " + str((int(op_a[i]), int(op_b[i]), cin)))
        print("Out: " + str(fa))
        result += str(fa[0])
        cin = fa[1]

    # já que se adiciona iterativamente do LSB até o MSB, invertemos a bistring do resultado
    result = result[::-1]

    # converte para binário, para permitir comparação mais fácil com o exato
    result = int(result, 2)             # esse método não considera complemento de dois
    # b = BitArray(bin=result)
    # result = b.int                    # já esse int considerou C2
    return result

# teste:
# print(approx_sum(14, 6, adders.axa3, 6))

## algumas ideias:
# → posso inverter os dois operandos e fazer o 'for' crescente, mas ainda precisaria reverter o result
# → gostaria de conseguir iterar sobre as funções de cada topologia, pra extrair todos os resultados de uma vez para cada soma
