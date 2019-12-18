import glob
import astropy.io.fits as pyfits
import numpy as np

def get_file_type(path):
	bias_frames=[]
	dark_frames=[]
	flat_frames=[]
	cal_frames=[]
	science_frames=[]
	
	filetypes=['bias', 'dark', 'flat', 'thar']
	filenames = glob.glob(path)
	
	for fn in filenames:
		if 'bias' in fn:
			bias_frames.append(fn)
		else if 'dark' in fn:
			dark_frames.append(fn)
		else if 'flat' in fn:
			flat_frames.append(fn)
		else if 'thar' in fn:
			cal_frames.append(fn)
		else:
			science_frames.append(fn)
			