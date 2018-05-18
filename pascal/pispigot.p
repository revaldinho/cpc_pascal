(* Compute digits of pi using Rabinowitz & Wagon spigot correcting up to 2 pre-digits *)
(* https://www.maa.org/sites/default/files/pdf/pubs/amm_supplements/Monthly_Reference_12.pdf *)
(*$C-,A-,I-,O-*)

program pispigot;

const
   digits  = 256;
   cols    = 854; (* use 1+ (digits*10 DIV 3) *)

var
   rem                        : array [0..cols] of integer; 
   predigits                  : array [0..1] of integer;
   carry, npd, quo, i, result : integer;
   d, denom                   : integer;

begin   
   for i:=0 to cols do
      rem[i] := 2;
   
   npd := 2;
   predigits[0]:=0;
   predigits[1]:=0;
   carry :=0;
   
   for d :=0 to digits-1 do
   begin      
      i := cols;
      quo := 0;
      repeat
         quo := quo + (rem[i]*10);
         denom := (2*i) -1 ;
         rem[i] := quo MOD denom;
         quo := quo DIV denom;
         i := i-1;
         if i > 0 then quo := quo * i;
      until i=0 ;
      result := carry + (quo DIV 10);

      if result = 10 then
      begin
         predigits[1] := predigits[1]+1;
         result := 0;
         if predigits[1] = 10 then
         begin
            predigits[1] := 0;
            predigits[0] := predigits[1]+1;
         end;      
      end;
   
      if d >= 2 then
      begin      
         write(predigits[0]:1);
         if d=2 then write('.':1);
      end;
      predigits[0] := predigits[1];
      predigits[1] := result;
      carry := quo MOD 10;
   end;
   
   write(predigits[0]:1);
   write(predigits[1]:1);
   writeln;   
end.
