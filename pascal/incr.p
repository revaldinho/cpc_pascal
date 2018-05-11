program incr;
var i, j : real;
   n  : integer;
begin
   i := 0.0;
   j := 0.0;
   for n := 1 to 10 do
      begin
         writeln(i, j);
         i := i+0.25 ;
         j := n*0.25 ;
      end   
end.

