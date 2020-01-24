from astropy.io import fits
import numpy as np
from matplotlib import pyplot as plt
from scipy import sparse
import sys
np.set_printoptions(threshold=sys.maxsize)
def extract_single_stripe(img, p, slit_height=3, return_indices=True, debug_level=0):

	#start_time = time.time()
	img = np.rot90(img)
	ny, nx = img.shape
	#xx = np.arange(nx, dtype=img.dtype)
	xx = np.arange(nx, dtype='f8')
	#yy = np.arange(ny, dtype=img.dtype)
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
		plt.imshow(img, cmap='gray')
		plt.imshow(indices, origin='lower', alpha=0.5)
		plt.show()

	mat = sparse.coo_matrix((img[indices], (y_grid[indices], x_grid[indices])), shape=(ny, nx))

	if return_indices:
		return mat.tocsr(),indices
	else:
		return mat.tocsr()
			
def extract_stripes(img, P_id, slit_height, return_indices=True, indonly=False, debug_level=0):
	stripes={}
	if return_indices:
		stripe_indices={}
	for id, p in sorted(P_id.items()):
		if debug_level>0 and (id-1)%5==0:
			print(f"Extracting stripes {id}-{id+4}...")
		stripe_ind = extract_single_stripe(img, p, slit_height=3, 
										return_indices=return_indices, 
										debug_level=0)
		if return_indices:
			stripes[id] = stripe_ind[0]
			stripe_indices[id] = stripe_ind[1]
		else:
			stripes[id] = stripe_ind
	
	if return_indices: 
		return stripes, stripe_indices
		exit()
	else:
		return stripes
		exit()