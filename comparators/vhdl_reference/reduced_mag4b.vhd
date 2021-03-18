library ieee;
use ieee.std_logic_1164.all;

-- comparador de magnitude 4bit, reduzido
entity reduced_mag4b is
    port (
        a, b: in std_logic_vector(3 downto 0);
        greater: out std_logic
        -- greater = 1 => a > b
        -- greater = 0 => a <= b
    );
end entity;

architecture structural_xnor of reduced_mag4b is
    signal eq: std_logic_vector(3 downto 0);
begin
    eq <= a xnor b;
    greater <=   (a(3) and (not b(3))) or
                (eq(3) and a(2) and (not b(2))) or
                (eq(3) and eq(2) and a(1) and (not b(1))) or
                (eq(3) and eq(2) and eq(1) and a(0) and (not b(0)));
end structural_xnor;

architecture structural_nand of reduced_mag4b is
    signal eq: std_logic_vector(3 downto 0);
begin
    eq <= a xnor b;
    greater <=   not(
                (not (a(3) and (not b(3)))) and
                (not (eq(3) and a(2) and (not b(2)))) and
                (not (eq(3) and eq(2) and a(1) and (not b(1)))) and
                (not (eq(3) and eq(2) and eq(1) and a(0) and (not b(0))))
                );
end structural_nand;