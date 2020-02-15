import numpy as np
from wavelength_solution import overlay_reference_peaks, find_good_peaks, find_wavelength_slice, spectra_to_actual_peaks, pixel_wavelength_map
import pandas 
from astropy.io import fits
from matplotlib import pyplot as plt
from df_handling import add_row
from scipy import ndimage

#Get the ThAr simulated data and the reference peaks
data = fits.getdata("extraction_data/thar_f1_all_orders_quick.fits", ext=0)
df = pandas.read_csv('New Simulated Spectra/ThAr.csv')
refwav = pandas.to_numeric(df.loc[:]['Wavelength']) * 10000.
refflux = pandas.to_numeric(df.loc[:]['Flux'])

#Choose the starting/step wavelength and an order, using the spec_plot_arc jupyter 
#notebook to find a good starting/step wvth is probably easiest
num_orders = len(data)
order=0
start_wav = 8644.6
step_wav = 0.034

#Create the wavelength vector
lam = step_wav * np.arange(len(data[order])) + start_wav

#Find the slice of fluxes in refflux corresponding to the wavelengths, 
#find_wavelength_slice is needed because you need to find the closest wavelength in
#the actual refwav list to the starting wavelength you chose
i_min, i_max = find_wavelength_slice(refwav, lam)
ref_data=refflux[i_min:i_max].values

#Find the index of the peaks in both the list of pixel positions and the list of wavelengths
good_peaks_locs = find_good_peaks(data[order], min_thresh=117, gauss_filter_size=6, slope=0, debug_level=debug)
ref_good_peaks_locs = find_good_peaks(ref_data, min_thresh=560, slope=0, debug_level=debug)

#The following plots helps you to see if/which peaks need to be removed from
#the spectra before fitting is attempted
print(f"Arc number of peaks found: {len(good_peaks_locs)}")
print(f"Arc peak locations: {good_peaks_locs}")
print(f"Ref number of peaks found: {len(ref_good_peaks_locs)}")
print(f"Ref peak locations: {ref_good_peaks_locs}")
plt.subplot(2,1,1)
plt.title("Real peaks Arc")
data[order] = ndimage.gaussian_filter1d(data[order], 12)
plt.plot(np.arange(len(data[order])), data[order])
plt.scatter(good_peaks_locs, data[order][good_peaks_locs], c='red')
plt.subplot(2,1,2)
plt.title("Real peaks Ref")
plt.plot(np.arange(len(ref_data)), ref_data)
plt.scatter(ref_good_peaks_locs, ref_data[ref_good_peaks_locs], c='red')
plt.xlabel("Pixels")
plt.ylabel("Flux")
plt.show()
plt.close()

#Actual wavelength and pixel positions for peaks
peak_wavelengths = refwav[i_min:i_max].values[ref_good_peaks_locs]
peak_pixels = np.arange(4096)[good_peaks_locs]

#If you need to remove some peaks, here is an example to remove items at 7,9,11
#peak_pixels = np.delete(np.arange(4096)[good_peaks_locs], [7,9,11])

print(len(peak_pixels))
print(len(peak_wavelengths))

#Fit the wavelength vs. pixel positions
residuals, coeffs = pixel_wavelength_map(peak_pixels, peak_wavelengths, deg=2, plot=True)
print(residuals)

#The following creates a csv file if it doesn't exist yet, or loads the existing file and adds a row
add_row("order_coeffs.csv", num_orders, [order, start_wav, step_wav, np.min(peak_pixels), np.max(peak_pixels), coeffs])