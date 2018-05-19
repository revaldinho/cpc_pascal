10 REM E-Spigot generation
15 s!=TIME
20 DEFINT a-z
30 digits=256
40 cols=258
50 DIM r(cols)
55 r(0)=0
60 FOR i=1 TO cols:r(i)=1:NEXT
90 PRINT "2.";
100 FOR j=0 TO digits-1
110 q=0
120 FOR i=cols-1 TO 0 STEP -1
130 n=q+r(i)*10
140 q =INT(n/(i+1))
150 r(i)=n MOD (i+1)
160 NEXT
170 PRINT q;
180 NEXT
190 PRINT
191 PRINT(TIME-s!)/300;"s"
200 END

