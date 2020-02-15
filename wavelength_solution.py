import numpy as np
from scipy import ndimage
from scipy.signal import argrelmax
from matplotlib import pyplot as plt

def find_good_peaks(data, max_thresh=None, min_thresh=0.2, slope=1e-4, gauss_filter_size=None, debug_level=0):
	xx = np.arange(len(data))
	#The slope is added slope*xx to ensure peaks are found even when consecutive pixels 
	#have the same value, I'm not convinced this is necessary yet but we'll see
	print("Finding peaks...")
	#peaks = filtered_data[peak_locs][1:-1] 
	if gauss_filter_size:
		order = ndimage.gaussian_filter1d(data, gauss_filter_size) + xx*slope
	else:
		order=data
	if debug_level>1:
		plt.subplot(2,1,1)
		plt.plot(xx, data)
		plt.subplot(2,1,2)
		plt.plot(xx, order)
		plt.title(f"Unfiltered vs. filtered data")
		plt.xlabel("Pixels")
		plt.ylabel("Flux")
		plt.show()
		plt.close()
	peak_locs = argrelmax(np.array(order))[0]
	max_mask = np.ones(len(peak_locs), dtype='bool')
	#This is to remove saturated lines (like cosmic rays I guess)
	if max_thresh:
		max_mask[order[peak_locs] > max_thresh] = False
	unsat_peaks = peak_locs[max_mask]
	min_mask = np.ones(len(unsat_peaks), dtype='bool')
	min_mask[order[unsat_peaks] < min_thresh] = False
	final_peaks = unsat_peaks[min_mask]
	if debug_level>0:
		print(f"Number of peaks found: {len(final_peaks)}")
		print(f"Peak locations: {final_peaks}")
		plt.plot(xx, order)
		plt.scatter(final_peaks, order[final_peaks], c='red')
		plt.xlabel("Pixels")
		plt.ylabel("Flux")
		plt.title("Real peaks")
		plt.show()
		plt.close()

	return final_peaks
	
def spectra_to_actual_peaks(data, all_peaks_locs, debug_level=0):
	actual_peaks = np.zeros(len(data))
	actual_peaks[all_peaks_locs] = data[all_peaks_locs]
	return actual_peaks

def overlay_reference_peaks(arc2d, order_id, startwave, stepwave, refwav, refflux, show_plot=True):
	# Top of 2D frame = red, left side of 2D frame = red

	# Create the rough linear wavelength vector via a linear function. This
	# function is what was tweaked in order to get the extracted spectrum
	# to line up with the reference list
	StartWav = startwave
	StepWav = stepwave
	lam = StepWav * np.arange(0,arc2d[order_id].size) + StartWav
	# Make plot of extracted spectrum
	fig, ax1 = plt.subplots()
	ax1.set_xlabel('Wavelength (Ang)')
	ax1.set_ylabel('Flux')
	ax1.set_title('Order '+str(order_id))
	ax1.tick_params(axis='y')
	ax1.set_xlim(np.amin(lam),np.amax(lam))
	ax1.plot(lam,arc2d[order_id])

	# Overplot the reference lines. Note that it looks like a saw-tooth
	# in places because it is not an evenly sampled spectrum, but rather
	# a list of lines and their flux. This list was used to make the simulated
	# arc exposure, so the fluxes in the peaks should be reasonably consistent.
	ax1.plot(refwav,refflux)
	plt.show()

def find_wavelength_slice(refwav, lam):
	diff_min = np.abs(refwav-lam[0])
	diff_max = np.abs(refwav-lam[-1])
	i_min = np.argmin(diff_min)
	i_max = np.argmin(diff_max)
	print(f"Min wavelength is {np.round(refwav[i_min],2)} at index {i_min}.")
	print(f"Max wavelength is {np.round(refwav[i_max],2)} at index {i_max}.")
	return i_min, i_max

def pixel_wavelength_map(peak_pixels, peak_wavelengths, deg=2, plot=False):
	coeffs, residuals,_,_,_ = np.polyfit(peak_pixels, peak_wavelengths, deg=deg, full=True)
	if plot:
		plt.scatter(peak_pixels, poly(peak_pixels), c='red', label='peaks')
		xx=np.arange(np.min(peak_pixels), np.max(peak_pixels))
		poly = np.poly1d(coeffs)
		plt.plot(xx, poly(xx), label='poly fit')
		plt.xlabel("Pixel")
		plt.ylabel("Wavelength (Ang)")
		plt.title("Wavelength vs. pixel fit")
		plt.legend()
		plt.show()
	return residuals, coeffs