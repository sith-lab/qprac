import pickle
import sys
import matplotlib.pyplot as plt
figx = pickle.load(open(sys.argv[1], 'rb'))

plt.show()