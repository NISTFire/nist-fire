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
if uncompensated: 
	info_file = 'test_info_raw.csv'
	image_dir = 'initial_images/Raw/'			# used to troubleshoot code
	video_dir = 'flow_meter_videos/Raw/'		# used in actual implementation
elif compensated: 
	info_file = 'test_info_compensated.csv'
	image_dir = 'initial_images/Compensated/'		# used to troubleshoot code
	video_dir = 'flow_meter_videos/Compensated/'	# used in actual implementation

info = pd.read_csv(info_file, index_col='Test')
# create dfs to store the dial's value and pixel data from each image
# final image size and pixel names for integer/fractional dials 
if uncompensated:
	int_dial_width = 15
	int_dial_height = 30
elif compensated:
	frac_dial_width = 55
	frac_dial_height = 75
	frac_df_headers = ['label']
	for pixID in range(0, frac_dial_width*frac_dial_height): 
		frac_df_headers.append('pixel'+str(pixID))
	frac_img_df = pd.DataFrame(columns=frac_df_headers)
	int_dial_width = 15
	int_dial_height = 31

int_df_headers = ['label']
for pixID in range(0, int_dial_width*int_dial_height): 
	int_df_headers.append('pixel'+str(pixID))
int_img_df = pd.DataFrame(columns=int_df_headers)

img_values_ls = []

# for f in os.listdir(image_dir):	# testing out code with captured screenshots
# 	if f.endswith('.png'):
for f in os.listdir(video_dir):	# actually generating training data
	if f.endswith('.mp4'):
		
		# to keep things simple initially, only consider videos of same flow meter angle 
		# i.e., Test_6 and Test_22--Test_25
		# if  f[5]=='6' or len(f)==11:
		# 	test_name = f[:-4]
		# else:
		# 	continue

		test_name = f[:-24]
		if test_name != 'Test_6':
			continue
		print '-----' + test_name + '-----'

		video = cv2.VideoCapture(video_dir + f)

		# get x,y coordinates of each dial for current test video frames
		x_bound_pairs = info['X Bounds'][test_name].split('|')
		y_bound_pairs = info['Y Bounds'][test_name].split('|')
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

		while(True):
			# read entire frame as image
			video.set(0, video_start_ms)
			ret, image = video.read()
			# video.get(5)
			# sys.exit()
			# cv2.imshow('frame', image)
			# sys.exit()
		# # # for each frame in video:
		# # # 	image = cv2.imread(current frame)

			dial_ID = 0
			while dial_ID < len(x_bound_pairs):
				# get coordinates of current dial
				x1, x2 = x_bound_pairs[dial_ID].split(', ')
				y1, y2 = y_bound_pairs[dial_ID].split(', ')

				# dial corresponding to coordinates is cropped (row values, column values) = (y_range, x_range)
				dial_img = image[int(y1):int(y2), int(x1):int(x2)]
				# cv2.imshow('cropped', dial_img)
				# cv2.waitKey(0)
				# pylab.imshow(dial_img)
				# plt.show()

				if compensated:
					# resize image of dial (if necessary)
					h,w = dial_img.shape[:2]
					if dial_ID == 0:
						min_width = frac_dial_width
						min_height = frac_dial_height
					else:
						min_width = int_dial_width
						min_height = int_dial_height

					resize_loop_iter = 0
					while (w != min_width) or (h != min_height):
						# preserve aspect ratio
						if w != min_width:
							h_scale = (float(min_width)/w)*h
							if h_scale < min_height:
								print 'Consider reassigning min_height due to aspect ratio'
								print h, ' scaled to ', h_scale
								sys.exit()
							# resize image
							dial_img = cv2.resize(dial_img, (min_width,int(h_scale)), 
								interpolation = cv2.INTER_AREA)
						else:
							diff = h-min_height
							if diff % 2 == 0:
								reduce_px = diff/2
								dial_img = dial_img[reduce_px:h-reduce_px, :]
							else:
								reduce_px = (diff+1)/2
								dial_img = dial_img[(reduce_px-1):h-reduce_px, :]

						h,w = dial_img.shape[:2]
						
						# ensure code doesn't get stuck in while loop
						resize_loop_iter+=1
						if resize_loop_iter > 5:
							print '[ERROR] resize exceeded 5 iterations'
							sys.exit()

					print w,'x', h


				# convert image to ls of RGB values for each pixel and store in df

				# rotate image (if compensated picture and display
				if uncompensated:
					dial_img_visible = dial_img
				else:
					center = (w/2, h/2)
					M = cv2.getRotationMatrix2D(center, rotation_angle, 1.0) # (1.0 = scaling factor)
					dial_img_visible = cv2.warpAffine(dial_img, M, (w,h))
				cv2.imshow('figure',dial_img_visible)
				plt.show(block=False)

				# Read value from user's input, add to list 
				i = 0 	# i and j count for while loops, may write an exception 
						# so the while loop exits after so many iterations
				loop = True
				while(loop):
					try:
						img_value = raw_input('Enter the number shown in current image. ' +
						'Input value as a single digit or a float to one decimal place. ' +
						'(Note: if last value was entered incorrectly, input "redo"): ')
						print
						i += 1
						float(img_value)
						if dial_ID == 0 and (compensated):
							while (len(img_value)!=3):
								img_value = raw_input('Invalid Entry -- image of dial displays ' +
									'floats. Enter value in the format X.X: ')
								i+=1
						else:
							while (len(img_value) != 1):
								img_value = raw_input('Invalid Entry -- dial displays integers. ' +
									'Enter value as a single digit: ')
								i+=1
						
						float(img_value)
						img_values_ls.append(img_value)
						loop = False

					except ValueError:
						if img_value == 'redo':
							i = 0
							j = 0
							redo_loop = True
							while(redo_loop):
								try:
									corrected_value = raw_input('Enter correct value of ' +
										'previous image: ')
									j += 1
									float(corrected_value)
									if dial_ID == 1 and (compensated):
										while (len(corrected_value)!=3): 
											corrected_value = raw_input('Invalid Entry -- ' +
												'image of last dial displayed floats. ' +
												'Enter value in format X.X: ')
											j+=1
									else:
										while (len(corrected_value) != 1):
											corrected_value = raw_input('Invalid Entry -- ' +
												'image of last dial displayed integers. ' +
												'Enter value as single digit: ')
											j+=1

									float(corrected_value)
									try:
										img_values_ls[-1] = corrected_value
									except IndexError:
										print 'No previous image exists'

									redo_loop = False

								except ValueError:
									print ('Invalid Entry -- ' +
										'input should be a single digit or float of format X.X')
						else:
							print ('Invalid Entry -- ' +
								'input should be a single digit or float of format X.X')
				plt.close()
				dial_ID += 1
			print img_values_ls
			sys.exit()
# save training data files for int/frac dial images 
print img_values_ls
# group_results.to_csv(results_dir + test_name + '_' + group.replace(' ', '_')  + '_averages.csv')
# 				print ('   Saving result file for ' + group)

# # next step will be to add fully test command line functionality and write code
# # such that for the 4 different videos, various frames are studied and
# # training_data.csv is created and stores resized, cropped values. Rotated image is strictly for viewing.
# # flip image for viewing, but store upside down since that is how the original video is

# # multiple threads?
 
# 			# # rotate image

# 			# cv2.imshow("dial", dial_img)

# 			# print '	IMG SIZE: ' + str(abs(int(x1)-int(x2))) + 'X' + str(abs(int(y1)-int(y2)))
# 			# plt.show()
# 			# print w,'X',h
# 			# print '---'
			

# 		# x_bound_pairs = info['x_bounds'][test_name].split('|')
# 		# y_bound_pairs = info['y_bounds'][test_name].split('|')

# 		# image = mh.imread(image_dir + f)
# 		# if info['Rotate?'][test_name] == 'Y':
# 		# 	image = ndimage.rotate(image, -19)

# 		# # x,y coordinates for meter, starting at top left & rotating CW
# 		# # [600, 400]; [1900, 400]; [1900, 1000]; [600, 1000]

# 		# dial_ID = 0
# 		# while dial_ID < len(x_bound_pairs):
# 		# 	x1, x2 = x_bound_pairs[dial_ID].split(', ')
# 		# 	y1, y2 = y_bound_pairs[dial_ID].split(', ')

# 		# 	pylab.imshow(image)
# 		# 	plt.xlim(int(x1), int(x2))
# 		# 	plt.ylim(int(y1), int(y2))
# 		# 	print '	IMG SIZE: ' + str(abs(int(x1)-int(x2))) + 'X' + str(abs(int(y1)-int(y2)))
# 		# 	plt.show()
# 		# 	dial_ID += 1
