import numpy as np
from matplotlib import pyplot as plt
from numpy import poly1d
from scipy import sparse

def flatten_stripe(img, stripe, slit_height=3, debug_level=0): 
	ny, nx = stripe.todense().shape
	row_ind = sparse.find(stripe)[0]
	col_ind = sparse.find(stripe)[1]
	flux_vals = sparse.find(stripe)[2]

	stripe_flux = np.zeros((2*slit_height, nx))
	
	col_flux = {}
	col_rows = {}
	for i, col in enumerate(col_ind):
		if col in col_flux.keys():
			col_flux[col].append(flux_vals[i])
			col_rows[col].append(row_ind[i])
		else:
			col_flux[col] = [flux_vals[i]]	
			col_rows[col] = [row_ind[i]]			
			
	for k, v in col_flux.items():
		n=len(v)
		if n == slit_height*2:
			stripe_flux.T[k]=v
		else:
			v.extend([0]*(2*slit_height-n))
			stripe_flux.T[k]=v
			
	if debug_level>0:
		plt.imshow(stripe_flux, cmap='gray',origin='lower')
		plt.title("Section of flattened stripe")
		plt.xlim(nx-100,nx-1)
		plt.show()

	return stripe_flux, col_rows

def quick_extraction(img, P_id, stripes, slit_height=3, debug_level=2):
	ord_flux={}
	ord_flux_err={}
	print("Extracting flux (quick)...")
	for id, stripe in stripes.items():
		flat_stripe_flux, flat_stripe_rows = flatten_stripe(img, stripe)
		#err_flat_stripe_flux, err_flat_stripe_rows = flatten_stripe(err_stripes[id])
		flux_by_col = np.sum(flat_stripe_flux, axis=0)
		#err_by_col = np.sqrt(np.sum(err_flat_stripe_flux, axis=0))
		ord_flux[id] = flux_by_col
		#ord_flux_err[id] = err_by_col
		#col = stripe.get_col(id-1) #id starts from 1
		#ord_flux[id] = np.sum(col.toarray())
	return ord_flux

#This is nowhere close to finished.. needs to be implemented properly, 
#use quick instead		
def tramline_extraction(img, P_id, stripes, slit_height=3, debug_level=2):
	ord_flux={}
	ord_flux_err={}
	print("Extracting flux (tramline)...")
	xx=range(4096)
	img = np.rot90(img)
	for id, stripe in stripes.items():
		mid_tramline = P_id[id].c
		bot_tramline = P_id[id].c.copy()
		bot_tramline[2] = bot_tramline[2]-slit_height
		top_tramline = P_id[id].c.copy()
		top_tramline[2] = top_tramline[2]+slit_height
		
		middle_col = 1843
		middle_row = P_id[id](middle_col)
		middle_row = int(np.round(middle_row))
		print(middle_col)
		print(middle_row)
		middle_int = img[middle_row][middle_col]
		
		print(type(img))
		print(middle_int)
		if debug_level>0:
			print(img.shape)
			plt.imshow(img, origin='lower', cmap='gray')
			plt.title(f"Tramlines for order {id}")
			#plt.plot(xx, np.poly1d(mid_tramline)(xx), label='mid')
			#plt.plot(xx, np.poly1d(bot_tramline)(xx), label='bot')
			#plt.plot(xx, np.poly1d(top_tramline)(xx), label='top')
			plt.plot(middle_col,middle_row, c='red', marker='X', markersize=5)
			plt.legend()
			plt.show()
			

		flat_stripe_flux, flat_stripe_rows = flatten_stripe(img, stripe)
		#err_flat_stripe_flux, err_flat_stripe_rows = flatten_stripe(err_stripes[id])
		flux_by_col = np.sum(flat_stripe_flux, axis=0)
		#err_by_col = np.sqrt(np.sum(err_flat_stripe_flux, axis=0))
		ord_flux[id] = flux_by_col
		#ord_flux_err[id] = err_by_col
		#col = stripe.get_col(id-1) #id starts from 1
		#ord_flux[id] = np.sum(col.toarray())
		
	return ord_flux