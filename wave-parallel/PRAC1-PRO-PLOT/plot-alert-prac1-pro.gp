# Set terminal to PDF with enhanced font, size, and format
set terminal pdfcairo enhanced font 'Times,12' size 4in, 2.5in
set output 'plot-alert-prac1-pro.pdf'

# Set labels for axes
set xlabel 'Row Pool Size (PRAC-PROACTIVE-1)' font 'Times,14'
set ylabel 'Alerts Issued' font 'Times,14'

# Set x-axis limit
set xrange [0:65536]

# Enable grid lines
set grid

# Set key outside the plot
set key outside top

# Define custom labels for each file
labels = "NBO1 NBO2 NBO4 NBO8 NBO16 NBO32 NBO64 NBO128 NBO256"

# Function to find the highest point in a data file
highest_point(file) = sprintf('< awk ''{if ($1 != "GroupSize" && ($5 > max || ($5 == max && $1 > x))) {max=$5; x=$1}} END {print x, max}'' %s', file)

# List of files to plot
files = "~/PRAC/NBO1/NBO1-prac1-pro.txt ~/PRAC/NBO2/NBO2-prac1-pro.txt ~/PRAC/NBO4/NBO4-prac1-pro.txt ~/PRAC/NBO8/NBO8-prac1-pro.txt ~/PRAC/NBO16/NBO16-prac1-pro.txt ~/PRAC/NBO32/NBO32-prac1-pro.txt ~/PRAC/NBO64/NBO64-prac1-pro.txt ~/PRAC/NBO128/NBO128-prac1-pro.txt ~/PRAC/NBO256/NBO256-prac1-pro.txt"

# Colors for the plots
colors = "blue red green magenta cyan orange brown violet pink yellow"

# Plot commands with custom labels, colors, line styles, and markers
plot for [i=1:words(files)] word(files, i) using 1:5 with lines lw 2 lc rgb word(colors, i) title word(labels, i), \
     for [i=1:words(files)] highest_point(word(files, i)) using 1:2 with points pointtype 7 pointsize 0.5 lc rgb "black" notitle, \
     for [i=1:words(files)] highest_point(word(files, i)) using 1:2:(sprintf("%.0f", $2)) with labels offset char 1, char 1 font 'Times,10' notitle
