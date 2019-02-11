#f(x) = 20*log10(1/(sqrt(1+(1/(6.875*(10**-5)*2*pi*x)**2))))
#g(x) = (atan(1/(6.875*(10**-5)*2*pi*x)))*360/(2*pi)
#filename=ARG1
set terminal png
set output 'Teorica.png'
set style data linespoints
set y2label 'Time (s)'
set ylabel 'accurance'
set y2tics border nomirror
set datafile separator ";"
set grid
set xlabel 'n - deph level'
set xrange[-0.5:3.5]
set yrange[0:0.1]
plot filename using 1:3 title 'Time' axis x1y2, filename using 1:5 title "Accurance" axis x1y1 #with impulses
#plot f(x) title 'Ganancia teorica' axis x1y1, g(x) title 'Fase teorica' axis x1y2#, 'ganancia.txt' using 1:(20*log10($2)) title 'Ganancia experimental' axis x1y1, 'fase.txt' title 'Fase experimental' axis x1y2
