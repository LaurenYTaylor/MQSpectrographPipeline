from astropy.io import fits
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage, signal
import warnings
from numpy import RankWarning
import sys 

def trace_orders(flat, deg_polynomial=2, gauss_filter_sigma=3., min_peak=0.05, maskthresh=100., weighted_fits=True, slowmask=False, simu=False, timit=False, debug_level=0):
	"""
	Based on Christoph Bergmann's Veloce pipeline, which is based on Julian 
	Stuermer's Maroon_X pipeline.
	
	Locates and fits stripes (ie orders) in a flat field echelle spectrum.
	"""
	
	#np.set_printoptions(threshold=sys.maxsize)
	warnings.filterwarnings("error", category=RankWarning)
	
	if timit:
		start_time = time.time()
	
	#Simulated data for MQ is the wrong way around
	flat = np.rot90(flat)

	print("Finding stripes...")
	ny, nx = flat.shape
	# smooth image slightly for noise reduction
	filtered_flat = ndimage.gaussian_filter(flat.astype(np.float), gauss_filter_sigma)
	# find peaks in center column
	data = filtered_flat[:, int(nx / 2)]
	
	peaks = np.zeros(data.shape, dtype=bool)
	#peak_idxs = signal.find_peaks(data, height=min_peak*np.max(data))[0]
	peak_idxs = signal.find_peaks(data)[0]
	#trough_idxs = signal.find_peaks(-data, height=min_peak*np.max(data))[0]
	peaks[peak_idxs]=True
	maxima = np.arange(ny)[peak_idxs]
	# filter out maxima too close to the boundary to avoid problems
	maxima = maxima[maxima > 3]
	maxima = maxima[maxima < ny - 3]
	
	n_order = len(maxima)
	print('Number of stripes found: %d' % n_order)
	
	if debug_level > 1:
		plt.title(f"Peaks of {len(peak_idxs)} Orders")
		plt.plot(data)
		plt.scatter(np.arange(ny)[peaks], np.sqrt(data[peaks]),s=25, c='red')
		plt.show()
		plt.close()
		plt.imshow(filtered_flat, cmap='gray')
		plt.scatter([int(nx/2)]*n_order, maxima, s=1)
		plt.title("Flat image with location of peaks indicated")
		plt.gca().invert_yaxis()
		plt.show()
		plt.close()

	orders = np.zeros((n_order, nx))
	# because we only want to use good pixels in the fit later on
	mask = np.ones((n_order, nx), dtype=bool)

	# walk through to the left and right along the maximum of the order
	# loop over all orders:
	print("Tracing orders...")
	for m, row in enumerate(maxima):
		column = int(nx / 2)
		orders[m, column] = row
		start_row = row
		# walk right
		i=0
		while (column + 1 < nx):
			prev_row=start_row
			column += 1
			#args is current column plus the column to the left and right
			args = np.array(np.linspace(max(1, start_row - 1), min(start_row + 1, ny - 1), 3), dtype=int)
			args = args[np.logical_and(args < ny, args > 0)]	 #deal with potential edge effects
			p = filtered_flat[args, column]
			# new maximum (apply only when there are actually flux values in p, ie not when eg p=[0,0,0]), otherwise leave start_row unchanged
			if ~(p[0]==p[1] and p[0]==p[2]):
				start_row = args[np.argmax(p)]
			orders[m, column] = start_row
			
			#build mask - exclude pixels at upper/lower end of chip; also exclude peaks that do not lie at least 5 sigmas above rms of 3-sigma clipped background (+/- cliprange pixels from peak location)
			if slowmask:
				cliprange = 25
				bg = filtered_flat[start_row-cliprange:start_row+cliprange+1, column]
				clipped = sigma_clip(bg,3.)
				if (filtered_flat[start_row,column] - np.median(clipped) < 5.*np.std(clipped)) or (start_row in (0,nx-1)):
					mask[m,column] = False
			else:
				if ((p < maskthresh).all()) or (start_row in (0,ny-1)):
					mask[m,column] = False
			if debug_level > 1 and m==n_order-2 and i<40:
				plt.cla()
				plt.imshow(filtered_flat, cmap='gray')
				plt.text(int(nx/2)+10, row+10,f"Order {m} peak is at row {start_row}", 
						fontsize=12,bbox=dict(facecolor='white', alpha=0.5))
				plt.ylim(row-15, row+15)
				plt.xlim(int(nx/2),int(nx/2)+40)
				plt.title(f"Peak tracing demonstration")
				if prev_row==start_row:
					plt.scatter([column]*3, args, s=3)
					plt.pause(0.2)
				else:
					plt.scatter([column]*3, [start_row-1, start_row, start_row+1], s=3, c="red")
					plt.pause(0.8)					
				i+=1
				
		# walk left
		plt.close()
		column = int(nx / 2)
		start_row = row
		while (column > 0):
			column -= 1
			args = np.array(np.linspace(max(1, start_row - 1), min(start_row + 1, ny - 1), 3), dtype=int)
			args = args[np.logical_and(args < ny, args > 0)]	 #deal with potential edge effects
			p = filtered_flat[args, column]
			# new maximum (apply only when there are actually flux values in p, ie not when eg p=[0,0,0]), otherwise leave start_row unchanged
			if ~(p[0]==p[1] and p[0]==p[2]):
				start_row = args[np.argmax(p)]
			orders[m, column] = start_row

			if slowmask:
				cliprange = 25
				bg = filtered_flat[start_row-cliprange:start_row+cliprange+1, column]
				clipped = sigma_clip(bg,3.)
				if (filtered_flat[start_row,column] - np.median(clipped) < 5.*np.std(clipped)) or (start_row in (0,nx-1)):
					mask[m,column] = False
			else:
				if ((p < maskthresh).all()):
					mask[m,column] = False
				elif (start_row in (0,ny-1)):
					mask[m,column] = False
				elif (simu==True and m==0 and column < 1300):
					mask[m,column] = False
				elif (simu==False and m==0 and column < 900):
					mask[m,column] = False

	# do Polynomial fit for each order, using the points traced out above
	print('Fit polynomial of order %d to each stripe...' % deg_polynomial)
	P = []
	xx = np.arange(nx)
	for i in range(len(orders)):
		if not weighted_fits:
			#unweighted
			try:
				fit = np.polyfit(xx[mask[i,:]], orders[i,mask[i,:]], deg_polynomial)
				p = np.poly1d(fit) #returns coeffs of polynomial
			except RankWarning:
				print(f"Not enough points in order {i} to fit. Try using a smaller value for maskthresh.")
				p = np.poly1d([0,0,0])
		else:
			#weighted by flux level
			filtered_flux_along_order = np.zeros(nx)
			for j in range(nx):
				filtered_flux_along_order[j] = filtered_flat[orders[i,j].astype(int),j]
			filtered_flux_along_order[filtered_flux_along_order < 1] = 1   
			w = np.sqrt(filtered_flux_along_order)
			
			try:
				fit = np.polyfit(xx[mask[i,:]], orders[i,mask[i,:]], deg_polynomial, w=w[mask[i,:]])
				p = np.poly1d(fit) #returns coeffs of polynomial
			except RankWarning:
				print(f"Not enough points in order {i} to fit. Try using a smaller value for maskthresh.")
				p = np.poly1d([0,0,0])
		P.append(p)

	if debug_level > -1:
		plt.figure()
		plt.imshow(filtered_flat, interpolation='none', vmin=np.min(flat), vmax=0.9 * np.max(flat), cmap=plt.get_cmap('gray'))
		for p in P:
			plt.plot(xx, p(xx), 'g', alpha=1)
		plt.ylim((0, ny))
		plt.xlim((0, nx))
		plt.show()	  
		plt.savefig('orders.png')
		
	if timit:
		print('Elapsed time: '+str(time.time() - start_time)+' seconds')

	return P,mask