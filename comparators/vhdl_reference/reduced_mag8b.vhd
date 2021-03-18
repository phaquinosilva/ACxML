library ieee;
use ieee.std_logic_1164.all;

-- comparador de magnitude 4bit, reduzido
entity reduced_mag8b is
    port (
        a, b: in std_logic_vector(7 downto 0);
        lesser: out std_logic
        -- lesser = 1 => a > b
        -- lesser = 0 => a <= b
    );
end entity;

architecture structural_xnor of reduced_mag8b is
    signal eq, alb: std_logic_vector(7 downto 0);
begin
    eq <= a xnor b;  -- equals
    alb <= b and (not a);  -- a less than b
    lesser <=   alb(7) or
                (eq(7) and alb(6)) or
                (eq(7) and eq(6) and alb(5)) or
                (eq(7) and eq(6) and eq(5) and alb(4)) or
                (eq(7) and eq(6) and eq(5) and eq(4) and alb(3)) or
                (eq(7) and eq(6) and eq(5) and eq(4) and eq(3) and alb(2)) or
                (eq(7) and eq(6) and eq(5) and eq(4) and eq(3) and eq(2) and alb(1)) or
                (eq(7) and eq(6) and eq(5) and eq(4) and eq(3) and eq(2) and eq(1) and alb(0));
end structural_xnor;

architecture structural_nand of reduced_mag8b is
    signal eq: std_logic_vector(7 downto 0);
begin
    eq <= a xnor b;  -- equals
    lesser <=   not (
                (not (b(7) and not a(7))) and
                (not (eq(7) and b(6) and not a(6))) and
                (not (eq(7) and eq(6) and b(5) and not a(5))) and
                (not (eq(7) and eq(6) and eq(5) and b(4) and not a(4))) and
                (not (eq(7) and eq(6) and eq(5) and eq(4) and b(3) and not a(3))) and
                (not (eq(7) and eq(6) and eq(5) and eq(4) and eq(3) and b(2) and not a(2))) and
                (not (eq(7) and eq(6) and eq(5) and eq(4) and eq(3) and eq(2) and b(1) and not a(1))) and
                (not (eq(7) and eq(6) and eq(5) and eq(4) and eq(3) and eq(2) and eq(1) and b(0) and not a(0)))
                );
end structural_nand;