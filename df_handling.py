import pandas as pd
import numpy as np

def add_row(filename, num_orders, row):
	try:
		df = pd.read_csv(filename)
		if not np.isnan(df.loc[row[0], 'Start Wavelength']):
			print("Error: This order already has an entry in the file. Please delete the entry before attempting to re-enter it.")
			return
		df.loc[row[0], 'Start Wavelength'] = row[1]
		df.loc[row[0], 'Step Wavelength'] = row[2]
		df.loc[row[0], 'Min Pixel'] = row[3]
		df.loc[row[0], 'Max Pixel'] = row[4]
		#Pandas doesn't like setting cells as arrays so 
		#need to be careful and use set_value..
		df.set_value(row[0], 'Coeffs', row[5])
		df.to_csv(filename, index=False)
		print(f"Row for order {row[0]} has been added.")
	except FileNotFoundError:
		df = pd.DataFrame(columns=['Start Wavelength', 'Step Wavelength', 'Min Pixel', 'Max Pixel', 'Coeffs'], index=np.arange(num_orders))
		df.index.name='Order'
		df.iloc[row[0]] = row[1:]
		df.to_csv(filename)
		print(f"Row for order {row[0]} has been added.")