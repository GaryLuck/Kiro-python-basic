10 PRINT "Prime Number Checker"
20 LET N = 29
30 PRINT "Checking if", N, "is prime..."
40 IF N < 2 GOTO 200
50 LET I = 2
60 IF I * I > N GOTO 180
70 LET R = N / I
80 LET T = R * I
90 IF T = N GOTO 200
100 LET I = I + 1
110 GOTO 60
180 PRINT N, "is PRIME"
190 GOTO 210
200 PRINT N, "is NOT prime"
210 END
