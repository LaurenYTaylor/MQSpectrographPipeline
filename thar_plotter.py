import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('New Simulated Spectra/ThAr.csv', sep=';', names=['lambda', 'int'])
plt.plot(df['lambda'], df['int'])
plt.show()
