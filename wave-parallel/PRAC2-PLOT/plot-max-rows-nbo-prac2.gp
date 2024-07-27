# Set terminal to PDF with enhanced font, size, and format
set terminal pdfcairo enhanced font 'Times,12' size 4in, 2.5in
set output 'plot-max-rows-nbo-prac2.pdf'

# Set labels for axes
set xlabel 'Row Pool Size (PRAC-2)' font 'Times,14'
set ylabel 'Rows with Activations > NBO' font 'Times,14'

# Set x-axis limit
set xrange [0:65536]

# Enable grid lines
set grid

# Set key outside the plot
set key outside top

# Define custom labels for each file
labels = "NBO1 NBO2 NBO4 NBO8 NBO16 NBO32 NBO64 NBO128 NBO256"

# Function to find the highest point in a data file
highest_point(file) = sprintf('< awk ''{if ($1 != "GroupSize" && ($6 > max || ($6 == max && $1 > x))) {max=$6; x=$1}} END {print x, max}'' %s', file)

# List of files to plot
files = "~/PRAC/NBO1/NBO1-prac2.txt ~/PRAC/NBO2/NBO2-prac2.txt ~/PRAC/NBO4/NBO4-prac2.txt ~/PRAC/NBO8/NBO8-prac2.txt ~/PRAC/NBO16/NBO16-prac2.txt ~/PRAC/NBO32/NBO32-prac2.txt ~/PRAC/NBO64/NBO64-prac2.txt ~/PRAC/NBO128/NBO128-prac2.txt ~/PRAC/NBO256/NBO256-prac2.txt"

# Colors for the plots
colors = "blue red green magenta cyan orange brown violet pink yellow"

# Plot commands with custom labels, colors, line styles, and markers
plot for [i=1:words(files)] word(files, i) using 1:6 with lines lw 2 lc rgb word(colors, i) title word(labels, i), \
     for [i=1:words(files)] highest_point(word(files, i)) using 1:2 with points pointtype 7 pointsize 0.5 lc rgb "black" notitle, \
     for [i=1:words(files)] highest_point(word(files, i)) using 1:2:(sprintf("%.0f", $2)) with labels offset char 1, char 1 font 'Times,10' notitle
