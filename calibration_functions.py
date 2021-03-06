import numpy as np
from file_handler import get_header
from astropy.io import fits

def make_master_bias(path, bias_frames):
	return np.nanmedian(bias_frames)
		
def make_master_dark(path, dark_frames, mb, scale=False):
	exptimes={}
	for frame in dark_frames:
		exptimes[frame] = get_header(path, frame)["EXPTIME"]
	frames_sorted_by_exptime = sorted(exptimes.items(), key = lambda x: x[1])
	if not scale:
		darks_grouped_by_exptime=[]
		for exp_time in np.unique(frames_sorted_by_exptime[:][1]):
			darks_grouped_by_exptime.append(frames_sorted_by_exptime[np.where(frames_sorted_by_exptime[:][1]==exp_time)])
		master_dark=[]
		for exptime_group in darks_grouped_by_exptime:
			data = [fits.open(path+"/"+frame)[0].data for frame in exptime_group]
			data_bias_sub = [frame - mb for frame in data]
			master_dark.append(np.nanmedian(data_bias_sub))
	else:
		scaled_data = [fits.open(path+"/"+frame)[0].data/get_header(path,frame)["EXPTIME"] for frame in dark_frames]
		scaled_bias_sub = [frame - mb for frame in scaled_data]
		master_dark = np.nanmedian(scaled_bias_sub)
	return master_dark
	
def make_master_white(path, flat_frames):
	all_img=[]
	exptimes=[]
	for frame in flat_frames:
		all_img.append(fits.open(frame)[0].data)
		exptimes.append(get_header(path,frame)["EXPTIME"])
	exptimes_scaled_to_median = np.array(exptimes) / np.median(exptimes)
	scaled_img = np.array(all_img) / exptimes_scaled_to_median.reshape(len(all_img), 1, 1)
	median_img = np.median(scaled_img, axis=0)
	mean_stderr = np.std(scaled_img, axis=0)/np.sqrt(len(all_img)) #-1 here in gh code?
	median_stderr = 1.253*(mean_stderr/np.sqrt(len(all_img)))
	
	return median_img, median_stderr