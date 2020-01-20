from scipy import sparse
import numpy as np
from matplotlib import pyplot as plt

def fit_profiles(stripes, err_stripes, P_id, slit_height=3):
	flat_stripe_fluxes={}
	flat_stripe_rows={}
	err_flat_stripe_fluxes={}
	err_flat_stripe_rows={}
	for id, stripe in sorted(stripes.items()):
		flat_stripe_fluxes[id], flat_stripe_rows[id] = flatten_stripe(stripe)
		err_flat_stripe_fluxes[id], err_flat_stripe_rows[id] = flatten_stripe(err_stripes[id])
	
	for id in sorted(flat_stripe_fluxes.keys()):
		profile = fit_order_profile(flat_stripe_rows[id], flat_stripe_fluxes[id], p
	
	
	return flat_stripe_fluxes, flat_stripe_rows
		



def flatten_stripe(stripe, slit_height=3): 
	ny, nx = stripe.todense().shape
	row_ind = sparse.find(stripe)[0]
	col_ind = sparse.find(stripe)[1]
	flux_vals = sparse.find(stripe)[2]
	# the individual columns correspond to the unique values of the x-indices, stored in contents[1]	
	col_values, col_indices, counts = np.unique(col_ind, return_index=True, return_counts=True)		
	stripe_flux = np.zeros((2*slit_height, nx)) - 1.	 #negative flux can be used to identify pixel-positions that fall outside the chip later
	stripe_rows = np.zeros((2*slit_height, nx))
	
	# check if whole order falls on CCD in dispersion direction
	if len(col_indices) != nx:	
		print('WARNING: Not the entire order falls on the CCD:')
	
	for i in range(len(col_indices)):
		if i == len(col_indices)-1:
			flux = flux_vals[col_indices[i]:]         #flux
			rownum = row_ind[col_indices[i]:]       #row number
		else:
			flux = flux_vals[col_indices[i]:col_indices[i+1]]         #flux
			rownum = row_ind[col_indices[i]:col_indices[i+1]]       #row number
		stripe_flux[:,i] = flux
		stripe_rows[:,i] = rownum
	return stripe_flux, stripe_rows.astype(int)