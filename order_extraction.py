from astropy.io import fits
import numpy as np
from matplotlib import pyplot as plt
from scipy import sparse
import sys
np.set_printoptions(threshold=sys.maxsize)
def extract_single_stripe(img, p, slit_height=3, debug_level=0):
	img = np.rot90(img)
	
	ny, nx = img.shape
	xx = np.arange(nx, dtype='f8')
	yy = np.arange(ny, dtype='f8')

	y = np.poly1d(p)(xx)
	x_grid, y_grid = np.meshgrid(xx, yy, copy=False)
	t=y.repeat(ny).reshape((nx, ny)).T
	distance = y_grid - t
	
	if debug_level>1:
		plt.imshow(abs(distance)/np.amax(abs(distance)), origin='lower', cmap='binary')
		plt.colorbar()
		plt.plot(xx,y)
		plt.show()
	indices = abs(distance) <= slit_height
	
	if debug_level > 1:
		plt.figure()
		plt.imshow(img, cmap='gray', origin='lower')
		plt.imshow(indices, origin='lower', alpha=0.1)
		plt.show()
	
	mat = sparse.coo_matrix((img[indices], (y_grid[indices], x_grid[indices])), shape=(ny, nx))

	return mat.tocsr()
			
def extract_stripes(img, P_id, slit_height, indonly=False, debug_level=0):
	stripes={}
	for id, p in sorted(P_id.items()):
		#The following if-statement is just for testing, 
		#if you don't want to go through every order..
		if id>5:
			break
		if debug_level>0 and (id-1)%5==0:
			print(f"Extracting stripes {id}-{id+4}...")
		stripe_ind = extract_single_stripe(img, p, slit_height=3, debug_level=0)
		stripes[id] = stripe_ind
	return stripes
		
