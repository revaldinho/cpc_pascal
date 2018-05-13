(* Sphere or Woolball demo after Acornsoft BBC BASIC original *)
(*$C-,A-,I-,O-*)
program sphere;
const
  sc = 160; (* scale to 80% of screen height to match BBC original *)
var
  n, x, y: integer;
  i      : real;

procedure scrsetmode(mode : integer);
begin
   ra:=chr(mode);
   user(#bc0e)
end;

procedure grasetorigin(x,y : integer);
begin
   rde:=x; rhl:=y;
   user(#bbc9)
end;

procedure gramoveabs(x,y : integer );
begin
   rde:=x; rhl:=y;
   user(#bbc0)
end;

procedure gralineabs(x,y :integer );
begin
   rde:=x; rhl:=y;
   user(#bbf6)
end;

procedure graclearwindow;
begin
   user(#bbdb)
end;

begin
  scrsetmode(1);
  graclearwindow;
  grasetorigin(300,200);
  gramoveabs(0, 0);
  i:=0;
  for n := 0 to 504 do
    begin
      x := round(sc * sin(i));
      y := round(sc * cos(i) * sin(i*0.95));
      gralineabs(x,y);
      i := i + 0.25;       
    end;
end.
