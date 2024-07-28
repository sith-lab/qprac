# Set terminal to PDF with enhanced font, size, and format
set terminal pdfcairo enhanced font 'Times,12' size 4in, 2.5in

set output 'plot-alert-prac1-pro-nbo32-q.pdf'

# Set labels for axes
set xlabel 'Row Pool Size (PRAC-PROACTIVE-NBO32)' font 'Times,14'
set ylabel 'Alerts Issued' font 'Times,14'

# Set x-axis limit
set xrange [0:65536]

# Enable grid lines
set grid

# Set key outside the plot
set key outside top

# Define custom labels for each file
labels = "Q1 Q2 Q3 Q4 Q5 Q6 Q7 Q8 Q9 Q10 Q11 Q12 Q13 Q14 Q15 Q16"

# Function to find the highest point in a data file
highest_point(file) = sprintf('< awk ''{if ($1 != "GroupSize" && ($5 > max || ($5 == max && $1 > x))) {max=$5; x=$1}} END {print x, max}'' %s', file)

# List of files to plot
files = "~/PRAC/NBO32/NBO32-prac1-pro-pq-32-1.txt ~/PRAC/NBO32/NBO32-prac1-pro-pq-32-2.txt ~/PRAC/NBO32/NBO32-prac1-pro-pq-32-3.txt ~/PRAC/NBO32/NBO32-prac1-pro-pq-32-4.txt ~/PRAC/NBO32/NBO32-prac1-pro-pq-32-5.txt ~/PRAC/NBO32/NBO32-prac1-pro-pq-32-6.txt ~/PRAC/NBO32/NBO32-prac1-pro-pq-32-7.txt ~/PRAC/NBO32/NBO32-prac1-pro-pq-32-8.txt ~/PRAC/NBO32/NBO32-prac1-pro-pq-32-9.txt ~/PRAC/NBO32/NBO32-prac1-pro-pq-32-10.txt ~/PRAC/NBO32/NBO32-prac1-pro-pq-32-11.txt ~/PRAC/NBO32/NBO32-prac1-pro-pq-32-12.txt ~/PRAC/NBO32/NBO32-prac1-pro-pq-32-13.txt ~/PRAC/NBO32/NBO32-prac1-pro-pq-32-14.txt ~/PRAC/NBO32/NBO32-prac1-pro-pq-32-15.txt ~/PRAC/NBO32/NBO32-prac1-pro-pq-32-16.txt"

# Colors for the plots
colors = "blue red green magenta cyan orange brown violet pink yellow dark-blue dark-red dark-green dark-magenta dark-cyan dark-orange"

# Plot commands with custom labels, colors, line styles, and markers
plot for [i=1:words(files)] word(files, i) using 1:5 with lines lw 2 lc rgb word(colors, i) title word(labels, i), \
     for [i=1:words(files)] highest_point(word(files, i)) using 1:2 with points pointtype 7 pointsize 0.5 lc rgb "black" notitle, \
     for [i=1:words(files)] highest_point(word(files, i)) using 1:2:(sprintf("%.0f", $2)) with labels offset char 1, char 1 font 'Times,10' notitle
