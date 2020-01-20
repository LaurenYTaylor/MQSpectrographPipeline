import glob
from astropy.io import fits
import numpy as np

def get_file_types(path):
	bias_frames=[]
	dark_frames=[]
	flat_frames=[]
	cal_frames=[]
	science_frames=[]
	
	filenames = glob.glob(path+'/*')
	
	for fn in filenames:
		if 'bias' in fn:
			bias_frames.append(fn)
		elif 'dark' in fn:
			dark_frames.append(fn)
		elif 'flat' in fn:
			flat_frames.append(fn)
		elif 'thar' in fn:
			cal_frames.append(fn)
		else:
			science_frames.append(fn)
	
	return bias_frames, dark_frames, flat_frames, cal_frames, science_frames

def get_header(path, filename):
	hdu = fits.open(filename)
	return hdu[0].header

def get_fibre_frames(path, frames):
	fiber1_frames=[]
	fiber2_frames=[]
	fiber3_frames=[]
	for frame in frames:
		header = get_header(path, frame)
		header_keys=list(header.keys())
		if sum('FIBER' in key for key in header_keys)==1:
			if 'FIBER_1' in header_keys:
				fiber1_frames.append(frame)
			if 'FIBER_2' in header_keys:
				fiber2_frames.append(frame)
			if 'FIBER_3' in header_keys:
				fiber3_frames.append(frame)
	return fiber1_frames, fiber2_frames, fiber3_frames