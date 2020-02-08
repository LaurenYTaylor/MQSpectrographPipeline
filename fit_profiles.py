from scipy import sparse
import numpy as np
from matplotlib import pyplot as plt
from extraction_methods import flatten_stripe

def fit_profiles(stripes, err_stripes, P_id, slit_height=3):
	flat_stripe_fluxes={}
	flat_stripe_rows={}
	err_flat_stripe_fluxes={}
	err_flat_stripe_rows={}
	for id, stripe in sorted(stripes.items()):
		flat_stripe_fluxes[id], flat_stripe_rows[id] = flatten_stripe(stripe)
		err_flat_stripe_fluxes[id], err_flat_stripe_rows[id] = flatten_stripe(err_stripes[id])
	
	for id in sorted(flat_stripe_fluxes.keys()):
		profile = fit_order_profile(flat_stripe_rows[id], flat_stripe_fluxes[id], p)
	
	return flat_stripe_fluxes, flat_stripe_rows
		



