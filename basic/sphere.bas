10 REM Sphere or Woolball demo after
20 REM Acornsoft BBC BASIC original
30 MODE 1
40 s%=160
50 start=TIME
60 ORIGIN 320,200
70 MOVE 0,0
80 FOR a=0 TO 126 STEP 0.25
90 DRAW s%*SIN(a),s%*(COS(a)*SIN(0.95*a))
100 NEXT a
110 PRINT "Runtime: ",(TIME-start)/300,"s"
