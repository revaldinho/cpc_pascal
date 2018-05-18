(* Compute digits of e using Rabinowitz & Wagon spigot algorithm *)
(* https://www.maa.org/sites/default/files/pdf/pubs/amm_supplements/Monthly_Reference_12.pdf *)
(*$C-,A-,I-,O-*)
program espigot;

const
   digits = 256;
   cols   = 258;           

var
   i, j      : integer;
   n, q      : integer;
   current   : integer;
   remainder : array [0..cols] of integer;

begin
   remainder[0]:= 0;
   for i:= 1 to cols do
      remainder[i]:=1;
   
   write('2.');
   
   for j:=0 to digits-1 do
   begin
      q := 0;
      for i := cols downto 0 do
      begin
         n := q + remainder[i] * 10;
         q := n DIV (i+1);
         remainder[i] := n MOD (i+1)
      end;
      write(q:1);
   end;
   writeln;
end.
