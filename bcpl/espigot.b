// Compute digits of e using Rabinowitz & Wagon spigot algorithm 
// https://www.maa.org/sites/default/files/pdf/pubs/amm_supplements/Monthly_Reference_12.pdf 

STATIC $( digits = 256 ; cols = 258 $)

LET start() = VALOF
$( LET i,j,n,q,current  = 1,1,1,1,1
   AND remainder = VEC 1026
   AND t = 0

   t := starttest(2)
   
   remainder!0 := 0
   FOR i = 1 TO cols-1 DO remainder!i := 1

   writes("*n2.")
   
   FOR j = 0 TO digits-1 DO $(
       q := 0
       FOR i = cols-1 TO 0 BY -1 DO $(
           n := q + (remainder!i) *10
           q := n / (i+1)
           remainder!i := n REM (i+1)           
       $)
       wrch(q+'0')
   $)
   newline()

   endtest(t)
   RESULTIS 0
$)
