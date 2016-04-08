import os
import numpy as np
import pandas as pd
import pylab
import sys
from scipy import ndimage
import matplotlib.pyplot as plt
import cv2
	# OpenCV installation guides:
	# Mac: https://jjyap.wordpress.com/2014/05/24/installing-opencv-2-4-9-on-mac-osx-with-python-support/
	# Ubuntu: http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/
import mahotas as mh
# import theano				
# import theano.tensor as T 	
# import lasagne

# choose type of training data to generate (uncompensated or compensated)
uncompensated = True
compensated = False

# read-in files and set directories
results_dir = 'HRR_data/'
video_dir = 'flow_meter_videos/All/'
info_file = 'test_info_manual_HRR.csv'
info = pd.read_csv(info_file, index_col='Test')

HRR_df_headers = ['Time (s)', 'V_flow (ft^3)', 'V_flow (m^3)', 'mdot (kg/s)', 'HRR']
ft3_to_m3 = 0.3048**3
density_C3H8 = 2.423 # [kg/m^3]
delH_C3H8 = 46.0 	# [MJ/kg]
# density_C3H8 = 582 	# [kg/m^3]
# delH_C3H8 = 0.42531 	# [MJ/kg]

def new_row_for_df(old_time, current_time, Vold, Vnew):
	current_time_s = current_time/1000
	Vdot_ft3 = float(Vnew-Vold)/(current_time_s-old_time)
	Vdot_m3 = Vdot_ft3*ft3_to_m3
	mdot = Vdot_m3*density_C3H8
	HRR = mdot*delH_C3H8
	new_row = pd.Series([current_time_s, Vdot_ft3, Vdot_m3, 
		mdot, HRR], index=HRR_df_headers)
	print 'Saved Dataframe with new row'
	return new_row, current_time_s, Vnew

# Note: Time = 0 corresponds to video start
for f in os.listdir(video_dir):	# actually generating training data
	if f.endswith('.mp4'):

		test_name = f[:-24]
		if test_name[-1] == '_':
			test_name = test_name[:-1]

		print '-----' + test_name + '-----'
		old_img_value = info['Initial Reading'][test_name]
		current_HRR_df = pd.DataFrame(columns=HRR_df_headers)
		video = cv2.VideoCapture(video_dir + f)

		if test_name != 'Test_22':
			continue


		if test_name != 'Test_2' and test_name != 'Test_3':
			uncompensated = True
			compensated = False
			data_file_name = results_dir+test_name+'_uncompensated.csv'
		else:
			uncompensated = False
			compensated = True
			dial_spinning = True
			find_spin_start = False
			data_file_name = results_dir+test_name+'_compensated.csv'
			continue
			# spin_start = float(old_img_value)

		# get coordinates of current dial
		x1, x2 = info['X Bounds'][test_name].split(', ')
		y1, y2 = info['Y Bounds'][test_name].split(', ')

		# set video at start/end times (convert start time to ms)
		gas_on = info['Gas on'][test_name].split(':')
		gas_off = info['Gas off'][test_name].split(':')
		test_duration = [int(gas_off[0])-int(gas_on[0]), int(gas_off[1])-int(gas_on[1])]
		if np.sign(test_duration[1])==-1:
			test_duration[0] = test_duration[0]-1
			test_duration[1] = test_duration[1]+60
		video_start = info['Video Start'][test_name].split(':')
		video_end = [int(video_start[0])+test_duration[0], int(video_start[1])+test_duration[1]]
		video_start_ms = (int(video_start[0])*60+int(video_start[1]))*1000
		video_end_ms = (video_end[0]*60+video_end[1])*1000

		current_time = int(video_start_ms)
		old_time = video_start_ms/1000
		cant_read = False
		Vold = float(old_img_value)
		while(current_time<video_end_ms):
			# read entire frame as image
			video.set(0, current_time)
			ret, image = video.read()
			dial_img = image[int(y1)-50:int(y2)+50, int(x1)-100:int(x2)+50]
			dial_img_visible = cv2.cvtColor(dial_img, cv2.COLOR_BGR2RGB)
			plt.imshow(dial_img_visible)
			plt.show(block=False)
		
			loop = True
			while(loop):
				try:
					img_value = raw_input('Enter dial reading. ' +
						'(if unable to read, type "more" to see surrounding frames): ')
					print
					img_value = float(img_value)
					loop = False
				except ValueError:
					if img_value == 'more' or img_value == 'less':
						multiplier = 1
						if img_value == 'less':
							multiplier = -1
						current_time = current_time+1000*multiplier
						plt.close()
						video.set(0, current_time)
						ret, image = video.read()
						dial_img = image[int(y1)-50:int(y2)+50, int(x1)-100:int(x2)+50]
						dial_img_visible = cv2.cvtColor(dial_img, cv2.COLOR_BGR2RGB)
						plt.imshow(dial_img_visible)
						plt.show(block=False)
						print
					else:
						print ('Invalid Entry -- ' +
							'input should be a single digit or float of format X.X')
			plt.close()

			if uncompensated:
				if img_value != old_img_value:
					if current_time>video_start_ms:	
						new_row, old_time, Vold = new_row_for_df(old_time, current_time, Vold, img_value)
						current_HRR_df = current_HRR_df.append(new_row, ignore_index=True)
				# jump to next frame 5 seconds ahead
				current_time += 10000
			else:
				if float(img_value) == float(old_img_value):
						if dial_spinning:
							dial_spinning = False
						current_time += 5000
				else:
					if(dial_spinning):
						if current_time>video_start_ms:
							new_row, old_time, Vold = new_row_for_df(old_time, current_time, Vold, img_value)
							current_HRR_df = current_HRR_df.append(new_row, ignore_index=True)
						current_time += 5000
					else:
						print 'move backward to find point at which it find changes'
						spin_start = float(old_img_value)
						current_time -= 1000
						dial_spinning = True
				
			old_img_value = img_value

			# save after analysis of every frame
			current_HRR_df.to_csv(data_file_name)