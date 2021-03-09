#include <stdlib.h>
#include "defns.i"


/* DEFINICOES FA*/

void sma(int a, int b, int cin, int output[]) {
    int sum = cin & !(a ^ b);
    int c_out = b | a & cin;
    output[0] = sum & 1;
    output[1] = c_out & 1;
}

void ama1(int a, int b, int cin, int output[]) {
    int c_out = b | a & cin;
    output[0] = !c_out & 1;
    output[1] = c_out & 1;
}

void ama2(int a, int b, int cin, int output[]) {
    int sum = cin & (!a | b);
    output[0] = sum & 1;
    output[1] = a & 1;
}

void axa2(int a, int b, int cin, int output[]) {
    int sum = !(a ^ b);
    int c_out = a & b | (a ^ b) & cin;
    output[0] = sum & 1;
    output[1] = c_out & 1;
}

void axa3(int a, int b, int cin, int output[]) {
    int sum = cin & !(a ^ b);
    int c_out = a & b | (a ^ b) & cin;
    output[0] = sum & 1;
    output[1] = c_out & 1;
}

void buf(int a, int b, int cin, int output[]) {
    output[0] = a & 1;
    output[1] = b & 1;
}

void exact(int a, int b, int cin, int output[]) {
    output[0] = a ^ b ^ cin;
    output[1] = (a & b) | (cin & (a ^ b));
}


/* HELPERS */

void print_bin(int* bin, int n) {
    for(int i = n; i > -1; i--)
        printf("%d", bin[i]);
    printf("\n");
}

void to_binary (int input, int n, int* bin) {
    int pow2 = 1;
    for (int i = 0; i < n; i++) {
        if (input & pow2) {
            bin[i] = 1;
        } else {
            bin[i] = 0;
        }
        pow2 *= 2;
    }
}

int to_int (int* bin, int n) {
    int pow2 = 1;
    int value = 0;
    // int largest = bin[n-1];
    for (int i = 0; i < n; i++) {
        if (bin[i] == 1) {
            value += pow2;
        }
        pow2 *= 2;
    }
    // calcula C2
    // largest *= pow2;
    // value -= largest;
    
    return value;
}


/* DEFINICOES OPERACOES */

// valores discretos: int
// valores continuos: double
int add(int a, int b, void (*f) (int, int, int, int *), int n) {
    // a, b: operandos (a + b)
    // (*f): nome do FA a ser simulado
    // n: numero de bits
    
    // conversao inteiro binario
    int bin_a[n];
    int bin_b[n];
    to_binary(a, n, bin_a);
    to_binary(b, n, bin_b);

    int bin_out[n];
    int int_out[2];
    int cin = 0;

    for (int i = 0; i < n; i++) {
        (*f) (bin_a[i], bin_b[i], cin, int_out);   
        bin_out[i] = int_out[0];
        cin = int_out[1];
    }

    // retorna resultado em int
    int result = to_int(bin_out, n);
    
    return result;
}

int sub(int a, int b, void (*f) (int, int, int, int *), int n) {
    // a, b: operandos (a - b)
    // (*f): nome do FA a ser simulado
    // n: numero de bits
    
    // conversao inteiro binario
    int bin_a[n];
    int bin_b[n];
    to_binary(a, n, bin_a);
    to_binary(~b, n, bin_b); // bitwise not para subtracao

    int bin_out[n];
    int int_out[2];
    int cin = 1;

    for (int i = 0; i < n; i++) {
        (*f) (bin_a[i], bin_b[i], cin, int_out);    
        bin_out[i] = int_out[0];
        cin = int_out[1];
    }

    // retorna resultado em int
    int result = to_int(bin_out, n);
    
    return result;
}

int geq(int a, int b, void (*f) (int, int, int, int *), int n) {
    // a, b: operandos (a > b)
    // (*f): nome do FA a ser simulado
    // n: numero de bits
    
    // conversao inteiro binario
    int bin_a[n];
    int bin_b[n];
    to_binary(a, n, bin_a);
    to_binary(~b, n, bin_b); // bitwise not para subtracao

    int bin_out[n];
    int int_out[2];
    int cin = 1;

    // a - b >= 0 : a >= b -> ultimo bit = 0
    // a - b < 0 : a < b -> ultimo bit = 1
    for (int i = 0; i < n; i++) {
        (*f) (bin_a[i], bin_b[i], cin, int_out);
        bin_out[i] = int_out[0];
        cin = int_out[1];
    }    

    // retorna resultado em int
    int result = !bin_out[n-1]; // '!' por causa do true e false ser !0 e 0 em C -- so pra me lembrar mesmo
    
    return result;
}

int leq(int a, int b, void (*f) (int, int, int, int *), int n) {
    return geq(b, a, f, n);
}