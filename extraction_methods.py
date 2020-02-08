import numpy as np
from fit_profiles import flatten_stripe
from matplotlib import pyplot as plt
from numpy import poly1d

def tramline_extraction(P_id, stripes, slit_height=3, debug_level=0):
	ord_flux={}
	ord_flux_err={}
	print("Extracting flux (tramline)...")
	xx=range(4096)
	for id, stripe in stripes.items():
		mid_tramline = P_id[id].c
		bot_tramline = P_id[id].c.copy()
		bot_tramline[2] = bot_tramline[2]-slit_height
		top_tramline = P_id[id].c.copy()
		top_tramline[2] = top_tramline[2]+slit_height
		if debug_level>0:
			plt.title(f"Tramlines for order {id}")
			plt.plot(xx, np.poly1d(mid_tramline)(xx), label='mid')
			plt.plot(xx, np.poly1d(bot_tramline)(xx), label='bot')
			plt.plot(xx, np.poly1d(top_tramline)(xx), label='top')
			plt.legend()
			plt.show()

		flat_stripe_flux, flat_stripe_rows = flatten_stripe(stripe)
		#err_flat_stripe_flux, err_flat_stripe_rows = flatten_stripe(err_stripes[id])
		flux_by_col = np.sum(flat_stripe_flux, axis=0)
		#err_by_col = np.sqrt(np.sum(err_flat_stripe_flux, axis=0))
		ord_flux[id] = flux_by_col
		#ord_flux_err[id] = err_by_col
		#col = stripe.get_col(id-1) #id starts from 1
		#ord_flux[id] = np.sum(col.toarray())
		
	return ord_flux