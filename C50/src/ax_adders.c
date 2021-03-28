#include <stdlib.h>
#include "defns.i"


/* DEFINICOES FA*/

void sma(int a, int b, int cin, int output[]) {
    int sum[8] = {0,1,0,0,0,0,0,1};
    int cout[8] = {0,0,1,1,0,1,1,1};
    int pos = ((a<<2) + (b<<1) + cin);
    output[0] = sum[pos];
    output[1] = cout[pos];
}

void ama1(int a, int b, int cin, int output[]) {
    int sum[8] = {1,1,0,0,1,0,0,0};
    int cout[8] = {0,0,1,1,0,1,1,1};
    int pos = ((a<<2) + (b<<1) + cin);
    output[0] = sum[pos];
    output[1] = cout[pos];
}

void ama2(int a, int b, int cin, int output[]) {
    int sum[8] = {0,1,0,1,0,0,0,1};
    int cout[8] = {0,0,0,0,1,1,1,1};
    int pos = ((a<<2) + (b<<1) + cin);
    output[0] = sum[pos];
    output[1] = cout[pos];
}

void axa2(int a, int b, int cin, int output[]) {
    int sum[8] = {1,1,0,0,0,0,1,1};
    int cout[8] = {0,0,0,1,0,1,1,1};
    int pos = ((a<<2) + (b<<1) + cin);
    output[0] = sum[pos];
    output[1] = cout[pos];
}

void axa3(int a, int b, int cin, int output[]) {
    int sum[8] = {0,1,0,0,0,0,0,1};
    int cout[8] = {0,0,0,1,0,1,1,1};
    int pos = ((a<<2) + (b<<1) + cin);
    output[0] = sum[pos];
    output[1] = cout[pos];
}

void buf(int a, int b, int cin, int output[]) {
    output[0] = a & 1;
    output[1] = b & 1;
}

void exact(int a, int b, int cin, int output[]) {
    int sum[8] = {0,1,1,0,1,0,0,1};
    int cout[8] = {0,0,0,1,0,1,1,1};
    int pos = ((a<<2) + (b<<1) + cin);
    output[0] = sum[pos];
    output[1] = cout[pos];
}


/* HELPERS */

void to_binary (int input, int n, int* bin) {
    int pow2 = 1;
    for (int i = 0; i < n; i++) {
        if (input & pow2) {
            bin[i] = 1;
        } else {
            bin[i] = 0;
        }
        pow2 = pow2 << 1;
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

int leq(int a, int b, void (*f) (int, int, int, int *), int n) {
    // a, b: operandos (a <= b)
    // (*f): nome do FA a ser simulado
    // n: numero de bits
    
    // conversao inteiro binario
    int bin_a[n];
    int bin_b[n];
    to_binary(~a, n, bin_a);
    to_binary(b, n, bin_b); // bitwise not para subtracao

    int bin_out[n];
    int int_out[2];
    int cin = 1;

    // a - b >= 0 : a >= b -> ultimo bit = 0
    // a - b < 0 : a < b -> ultimo bit = 1
    for (int i = 0; i < n; i++) {
        (*f) (bin_b[i], bin_a[i], cin, int_out);
        bin_out[i] = int_out[0];
        cin = int_out[1];
    }

    // retorna resultado em int
    int result = cin; 
    return result;
}

int leq_exact(int a, int b) {
    int bin_a[4];
    int bin_b[4];
    to_binary(~a, 4, bin_a);
    to_binary(b, 4, bin_b);
    int eq1 = ~(bin_a[1] ^ bin_b[1]);
    int eq2 = ~(bin_a[2] ^ bin_b[2]);
    int eq3 = ~(bin_a[3] ^ bin_b[3]);
    int n3 = ~(bin_a[3] & ~bin_b[3]);
    int n2 = ~(bin_a[2] & ~bin_b[2] & eq3);
    int n1 = ~(bin_a[1] & ~bin_b[1] & eq3 & eq2);
    int n0 = ~(bin_a[0] & ~bin_b[0] & eq3 & eq2 & eq1);
    return (n0 & n1 & n2 & n3) & 1;
}

int leq_a1(int a, int b) {
    int bin_a[4];
    int bin_b[4];
    to_binary(~a, 4, bin_a);
    to_binary(b, 4, bin_b);
    int eq1 = ~(bin_a[1] ^ bin_b[1]);
    int eq2 = ~(bin_a[2] ^ bin_b[2]);
    int eq3 = ~(bin_a[3] ^ bin_b[3]);
    int n3 = ~(bin_a[3] & ~bin_b[3]);
    int n2 = ~(bin_a[2] & ~bin_b[2] & eq3);
    int n1 = ~(bin_a[1] & ~bin_b[1] & eq3 & eq2);
    int n0 = ~(eq3 & eq2 & eq1);
    return (n0 & n1 & n2 & n3) & 1;
}

int leq_a2(int a, int b) {
    int bin_a[4];
    int bin_b[4];
    to_binary(~a, 4, bin_a);
    to_binary(b, 4, bin_b);
    // int eq1 = ~(bin_a[1] ^ bin_b[1]);
    int eq2 = ~(bin_a[2] ^ bin_b[2]);
    int eq3 = ~(bin_a[3] ^ bin_b[3]);
    int n3 = ~(bin_a[3] & ~bin_b[3]);
    int n2 = ~(bin_a[2] & ~bin_b[2] & eq3);
    int n1 = ~(bin_a[1] & ~bin_b[1] & eq3 & eq2);
    // int n0 = ~(bin_a[0] & ~bin_b[0] & eq3 & eq2 & eq1);
    return (n1 & n2 & n3) & 1;
}

int leq_a3(int a, int b) {
    int bin_a[4];
    int bin_b[4];
    to_binary(~a, 4, bin_a);
    to_binary(b, 4, bin_b);
    // int eq1 = ~(bin_a[1] ^ bin_b[1]);
    int eq2 = ~(bin_a[2] ^ bin_b[2]);
    int eq3 = ~(bin_a[3] ^ bin_b[3]);
    int n3 = ~(bin_a[3] & ~bin_b[3]);
    int n2 = ~(bin_a[2] & ~bin_b[2] & eq3);
    int n1 = ~(bin_a[1] & ~bin_b[1] & eq3 & eq2);
    // int n0 = ~(bin_a[0] & ~bin_b[0] & eq3 & eq2 & eq1);
    return (bin_a[0] & n1 & n2 & n3) & 1;
}

int leq_a4(int a, int b) {
    int bin_a[4];
    int bin_b[4];
    to_binary(~a, 4, bin_a);
    to_binary(b, 4, bin_b);
    // int eq1 = ~(bin_a[1] ^ bin_b[1]);
    int eq2 = ~(bin_a[2] ^ bin_b[2]);
    int eq3 = ~(bin_a[3] ^ bin_b[3]);
    int n3 = ~(bin_a[3] & ~bin_b[3]);
    int n2 = ~(bin_a[2] & ~bin_b[2] & eq3);
    // int n1 = ~(bin_a[1] & ~bin_b[1] & eq3 & eq2);
    int n0 = ~(bin_a[0] & ~bin_b[0] & eq3 & eq2 & bin_a[1]);
    return (n0 & bin_a[1] & n2 & n3) & 1;
}

int leq_a5(int a, int b) {
    int bin_a[4];
    int bin_b[4];
    to_binary(~a, 4, bin_a);
    to_binary(b, 4, bin_b);
    // int eq1 = ~(bin_a[1] ^ bin_b[1]);
    // int eq2 = ~(bin_a[2] ^ bin_b[2]);
    int eq3 = ~(bin_a[3] ^ bin_b[3]);
    int n3 = ~(bin_a[3] & ~bin_b[3]);
    int n2 = ~(bin_a[2] & ~bin_b[2] & eq3);
    // int n1 = ~(bin_a[1] & ~bin_b[1] & eq3 & eq2);
    // int n0 = ~(bin_a[0] & ~bin_b[0] & eq3 & eq2 & eq1);
    return (bin_a[0] & bin_a[1] & n2 & n3) & 1;
}

int leq_a6(int a, int b) {
    int bin_a[4];
    int bin_b[4];
    to_binary(~a, 4, bin_a);
    to_binary(b, 4, bin_b);
    // int eq1 = ~(bin_a[1] ^ bin_b[1]);
    // int eq2 = ~(bin_a[2] ^ bin_b[2]);
    int eq3 = ~(bin_a[3] ^ bin_b[3]);
    int n3 = ~(bin_a[3] & ~bin_b[3]);
    int n2 = ~(bin_a[2] & ~bin_b[2] & eq3);
    // int n1 = ~(bin_a[1] & ~bin_b[1] & eq3 & eq2);
    // int n0 = ~(bin_a[0] & ~bin_b[0] & eq3 & eq2 & eq1);
    return (bin_a[1] & n2 & n3) & 1;
}
