import os
import numpy as np
from astropy.io import fits
from file_handler import get_file_types, get_header, get_fibre_frames
from calibration_functions import make_master_bias, make_master_dark, make_master_white
from order_tracing import trace_orders
from order_extraction import extract_stripes
from scipy import sparse
from fit_profiles import fit_profiles

data_file="New Simulated Spectra"

#Open Files#
path = os.getcwd()+"/"+data_file
bias_frames, dark_frames, flat_frames, cal_frames, science_frames = get_file_types(path)

x_dim = 4096
y_dim = 4096

#Bias Frames#
if bias_frames:
	master_bias = make_master_bias(path, bias_frames)
else:
	master_bias = np.zeros((x_dim, y_dim))

#Dark Frames#
if dark_frames:
	dark_frame_data = [fits.open(path+"/"+frame)[0].data for frame in dark_frames]
	dark_frame_data = dark_frame_data - master_bias
	master_dark = make_master_dark(path, dark_frame_data)
else:
	master_dark = np.zeros((x_dim, y_dim))

#Flat Frames#
fiber1_flat, fiber2_flat, fiber3_flat = get_fibre_frames(path, flat_frames)
fiber1_white_master, fiber1_err = make_master_white(path, fiber1_flat)
#fiber2_white_master, fiber2_err = make_master_white(path, fiber2_flat)
#fiber3_white_master, fiber3_err = make_master_white(path, fiber3_flat)
#fibre_white_master, white_err = make_master_white(path, flat_frames) #include all frames or only triple flat?

#Order Tracing#
poly_fits, mask = trace_orders(fiber1_white_master, debug_level=0, simu=True, maskthresh=20)
ids = list(range(1, len(poly_fits)+1))
P_id = dict(zip(ids, poly_fits))

#Order Extraction#
stripes, stripe_indices = extract_stripes(fiber1_white_master, P_id, slit_height=3)
err_stripes = extract_stripes(fiber1_err, P_id, slit_height=3, return_indices=False)
profiles = fit_profiles(stripes, err_stripes, P_id)
