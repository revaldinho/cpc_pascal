(* Sphere or Woolball demo after Acornsoft BASIC original *)

program sphere;
const
  xo = 300;
  yo = 200;
  sc = 200;
var
  n, x, y : integer;
  i : real;


procedure scrsetmode(mode : integer);
begin
   ra:=chr(mode);
   user(#bc0e)
end;

                            
procedure gramoveabs(x,y :integer );
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

procedure klsettime;
begin
   rde:=0; rhl:=0;
   user(#bd10)
end;

begin
  scrsetmode(0);
  graclearwindow;
  gramoveabs(xo, yo);
  for n := 0 to 504 do
    begin
      i := n * 0.25;
      x := round(sc * sin(i));
      y := round(sc * cos(i) * sin(i*0.95));
      gralineabs(x+xo,y+yo);
    end
end.
