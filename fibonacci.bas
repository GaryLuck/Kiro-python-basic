10 PRINT "Fibonacci Sequence Generator"
20 PRINT "How many terms? (max 20)"
30 LET N = 15
40 DIM F[20]
50 LET F[0] = 0
60 LET F[1] = 1
70 LET I = 2
80 IF I >= N GOTO 120
90 LET F[I] = F[I-1] + F[I-2]
100 LET I = I + 1
110 GOTO 80
120 PRINT "First", N, "Fibonacci numbers:"
130 LET I = 0
140 IF I >= N GOTO 180
150 PRINT F[I]
160 LET I = I + 1
170 GOTO 140
180 END
