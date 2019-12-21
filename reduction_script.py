import os
import numpy as np
from astropy.io import fits
from file_handler import get_file_types, get_header, get_fibre_frames

data_file="New Simulated Spectra"

#Open Files#
path = os.getcwd()+"/"+data_file
bias_frames, dark_frames, flat_frames, cal_frames, science_frames = get_file_types(path)

#Bias Frames#
fiber1_bias, fiber2_bias, fiber3_bias = get_fibre_frames(path, flat_frames)
fiber1_bias_median = np.nanmedian([fits.open(frame)[0].data for frame in fiber1_bias])
fiber2_bias_median = np.nanmedian([fits.open(frame)[0].data for frame in fiber2_bias])
fiber3_bias_median = np.nanmedian([fits.open(frame)[0].data for frame in fiber3_bias])
		
print(fiber1_bias_median)
	
