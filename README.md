# MQSpectrographPipeline
A data reduction pipeline for the future Echelle spectrograph at Macquarie University, NSW.

Any questions please contact: 

Lauren Taylor, UNSW

lauren.y.taylor96@gmail.com



The main script is reduction_script.py. The following is a description of the steps followed in the reduction process:

##### STEP 1: BIAS FRAMES

If bias frames supplied, master bias is made using the median of the bias frames. 
If not supplied (currently there is no bias simu), bias frame is an array of zeros.
`make_master_bias` is in calibration_functions.py.

##### STEP 2: DARK FRAMES

If dark frames supplied, a median can be found of all frames (if exp time is the same),
or can be scaled down to 1s of exposure.
If not supplied, (currently there is no dark simu), dark frame if an array of zeros.
`make_master_dark` is in calibration_functions.py.

##### STEP 3: WHITE FRAMES

The white frames are scaled to the median exposure time, then the median of the frames is found. The error is calculated by 1.253*mean_standard_error/sqrt(num_frames) (ref: http://davidmlane.com/hyperstat/A106993.html). 

`make_master_white` is in calibration_functions.py.

*TODO: Currently this only implemented for one fibre, needs to be expanded for three fibres at a time so orders can be traced along each fibre location.*

##### STEP 4: ORDER TRACING

The orders are traced by drawing a line through the middle of the image (in the cross-dispersion direction) and noting the location of the peaks. The peaks are then traced by starting at the centre peak location and stepping right and then left along the order. A polynomial is fit to the order using these y-values. A list of these polynomials is returned. Should be used for one fibre at a time. 

`trace_orders` is in order_tracing.py. The parameter `maskthresh` is currently set to `maskthresh=20`, as the simulated whites are quite dim. The polynomial order is set to `deg_polynomial=2`, higher orders should not be necessary.

##### STEP 5: ORDER EXTRACTION

The order extraction created a sparse matrix for each order. The sparse matrix stores a location (x,y) and the intensity value at this location only if intensity>0. Most of the image except along the current order will be black so this is quite efficient. This is also used for ThAr extraction.

`extract_stripes` is in order_extraction.py. `slit_height` is currently set as `slit_height=3`, as the height of the orders seemed to be around 6 by inspection.

##### STEP 6: EXTRACTION

This first uses `flatten_stripes` to make a rectangular array of the intensities of the order, shape = *x_dim* x *(slit_height\*2)*. The tramline then moves along the columns of the array and adds up the intensities in the cross-dispersion direction. 

*TODO: Find tramlines and include fractional intensities from the partial pixels cut through by the tramlines.*



**STEP 7: WAVELENGTH SOLUTION**

Good peaks are found using `find_good_peaks`within the extracted Arc lamp simulated data (thar_1d), and the position of the peaks (in pixels) is noted. Some manual effort is then required to find the small section of peaks within the larger wavelength reference spectrum from ThAr.csv. The position of the peaks (in wavelength) is noted for the reference spectrum, and the wavelength range for the order is found using `find_wavelength_slice`. A polynomial is then fit to the peak positions, to map the pixel positions to a wavelength, using `pixel_wavelength_map`. Not all peaks show up in both spectra, some will have to be removed for a good fit to be found. This must be done manually (np.delete is useful for removing items in a list at a specified index). 

`find_good_peaks`, `find_wavelength_slice`, and `pixel_wavelength_map` are in wavelength_solution.py. It is faster to access them in the order given in the file wavelength_solution_from_file.py once you have the ThAr extracted into a fits file.

*TODO: Find the wavlength solution for order 22-78, the first 22 orders are done, just ran out of time to process the rest of them.* 



**The file order_coeffs.csv contains the coefficients for the fits for the first 22 orders.**



General TODOs:

1. Do errors properly. A white error image is calculated in make_master_white but it needs to be propagated through the script, and same for ThAr and science images.
2. Background and cosmic ray subtraction.