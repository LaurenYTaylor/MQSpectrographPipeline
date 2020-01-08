import os
import numpy as np
from astropy.io import fits
from file_handler import get_file_types, get_header, get_fibre_frames
from calibration_functions import make_master_bias, make_master_dark, make_master_white

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
fiber2_white_master, fiber2_err = make_master_white(path, fiber2_flat)
fiber3_white_master, fiber3_err = make_master_white(path, fiber3_flat)
fibre_white_master, white_err = make_master_white(path, flat_frames) #include all frames or only triple flat?
print(fibre_white_master)

#Order Tracing#
poly_fits, mask = trace_orders(fibre1_white_master, debug_level=2, simu=True, maskthresh=20))

