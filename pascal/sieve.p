(* Sieve - find first 10000 prime numbers *)
(*$C-,A-,I-,O-*)

program sieve;

const
   maxnum = 10000;
   memtop =  5000; (* should be half of maxnum *)
var
   mem  : array [0..memtop] of boolean;
   i, j : integer;
   
begin
   for i:=0 to memtop do
      mem[i] := false ;
      
   i:=3;
   repeat
      if not mem[i DIV 2] then
      begin
         j:=i+i; 
         while j<maxnum do
         begin
            if odd(j) then
               mem[j DIV 2] := true;
            j :=j+i;
         end;
      end;
      i := i+2;
   until i> maxnum;

   i:=3;
   repeat
      if not mem[i DIV 2] then write(i);
      i := i+2;
   until i> maxnum;
   writeln;   
end.
