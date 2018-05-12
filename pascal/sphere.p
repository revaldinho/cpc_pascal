(* Sphere or Woolball demo after Acornsoft BBC BASIC original *)
(* C-, A-, I-, O- *)
program sphere;
const
  xo = 300;
  yo = 200;
  sc = 200;
var
  n, x, y: integer;
  i      : real;

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

begin
  scrsetmode(0);
  graclearwindow;
  gramoveabs(xo, yo);
  i:=0;
  for n := 0 to 504 do
    begin
      x := xo+round(sc * sin(i));
      y := yo+round(sc * cos(i) * sin(i*0.95));
      gralineabs(x,y);
      i := i + 0.25;       
    end;
end.
