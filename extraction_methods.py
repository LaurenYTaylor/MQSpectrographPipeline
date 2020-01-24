import numpy as np
from fit_profiles import flatten_stripe
from matplotlib import pyplot as plt

def tramline_extraction(stripes, err_stripes):
	ord_flux={}
	ord_flux_err={}
	print("Extracting flux (tramline)...")
	for id, stripe in stripes.items():
		flat_stripe_flux, flat_stripe_rows = flatten_stripe(stripe)
		#err_flat_stripe_flux, err_flat_stripe_rows = flatten_stripe(err_stripes[id])
		flux_by_col = np.sum(flat_stripe_flux, axis=0)
		#err_by_col = np.sqrt(np.sum(err_flat_stripe_flux, axis=0))
		ord_flux[id] = flux_by_col
		#ord_flux_err[id] = err_by_col
		#col = stripe.get_col(id-1) #id starts from 1
		#ord_flux[id] = np.sum(col.toarray())
		
	return ord_flux, ord_flux_err