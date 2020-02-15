from astropy.io import fits
from matplotlib import pyplot as plt

data = fits.getdata("New Simulated Spectra/mqlts_thar_f1_quick_extracted.fits", ext=0)
print(len(data))
plt.plot(range(len(data[-1])), data[-1])
plt.show()