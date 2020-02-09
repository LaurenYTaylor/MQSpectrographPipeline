import os
import numpy as np
from astropy.io import fits
from file_handler import get_file_types, get_header, get_fibre_frames
from calibration_functions import make_master_bias, make_master_dark, make_master_white
from order_tracing import trace_orders
from order_extraction import extract_stripes
from scipy import sparse
from matplotlib import pyplot as plt
from fit_profiles import fit_profiles
from extraction_methods import tramline_extraction
import warnings
data_file="New Simulated Spectra"

#Open Files#
path = os.getcwd()+"/"+data_file
bias_frames, dark_frames, flat_frames, cal_frames, science_frames = get_file_types(path)

x_dim = 4096
y_dim = 4096

#Bias Frames#
bias_frame_data = [fits.open(path+"/"+frame)[0].data for frame in bias_frames]
warnings.filterwarnings("error", category=RuntimeWarning)
try:
	master_bias = make_master_bias(path, bias_frame_data)
except RuntimeWarning:
	print("Warning: List of bias frames is empty.")
	master_bias = np.zeros((x_dim, y_dim))

#Dark Frames#
try:
	master_dark = make_master_dark(path, dark_frames, master_bias)
except IndexError:
	print("Warning: List of dark frames is empty.")
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
#stripes = extract_stripes(fiber1_white_master, P_id, slit_height=3, debug_level=0)
#err_stripes = extract_stripes(fiber1_err, P_id, slit_height=3)
#profiles = fit_profiles(stripes, err_stripes, P_id)

#Wavelength Calibration
thar_stripes = extract_stripes(fits.open(cal_frames[0])[0].data, P_id, slit_height=3, debug_level=1)
thar_1d = tramline_extraction(P_id, thar_stripes, slit_height=3)
plt.plot(range(x_dim), thar_1d[1])
plt.show()
#Science Image Processing#

#below doesn't do anything yet..
#_ = process_cal_images(cal_frames)
#_ = process_science_images(science_frames)
#flux_dict = tramline_extraction(stripes, err_stripes)
