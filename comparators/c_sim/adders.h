#include <stdio.h>


/* OPERACOES */

/* FUNCOES: soma, subtracao e comparacao (a > b)
*  Args:
*    - operandos inteiros 'a' e 'b' de n bits (unsigned, por enquanto)
*    - 'f' nome da funcao do FA que se deseja simular
*/

// a + b
int add(int a, int b, void (*f) (int, int, int, int *), int n);
// a - b
int sub(int a, int b, void (*f) (int, int, int, int *), int n);
// a > b
int gt(int a, int b, void (*f) (int, int, int, int *), int n);


/* FAs */

// decidir se escrevo os FAs como funcoes booleanas ou maps (PLA)
/* EXATOS */
// int exa(int a, int b);
// int ema(int a, int b);
/* APROXIMADOS */
void sma(int a, int b, int cin, int output[]);
void ama1(int a, int b, int cin, int output[]);
void ama2(int a, int b, int cin, int output[]);
void axa2(int a, int b, int cin, int output[]);
void axa3(int a, int b, int cin, int output[]);
void buf(int a, int b, int cin, int output[]);
void exact(int a, int b, int cin, int output[]);


/* HELPERS */

void to_binary(int input, int n, int* bin);
int to_int (int* bin, int n);
void print_bin(int* bin, int n);