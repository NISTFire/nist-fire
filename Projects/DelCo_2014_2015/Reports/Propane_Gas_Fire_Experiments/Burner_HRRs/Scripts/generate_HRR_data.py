import os
import numpy as np
import pandas as pd
import pylab
import sys
from scipy import ndimage
import matplotlib.pyplot as plt
import cv2

# read-in files and set directories
results_dir = 'HRR_data/'
comp_video_dir = 'flow_meter_videos/Compensated/'
raw_video_dir = 'flow_meter_videos/Raw/'
info_file = 'test_info.csv'

info = pd.read_csv(info_file, index_col='Test')

# HRR_df_headers = ['Time (s)', 'V_flow (ft^3)', 'V_flow (m^3)', 'mdot (kg/s)', 'HRR']
HRR_df_headers = ['Test', '1 Burner Start', '2 Burners Start', 
'3 Burners', '2 Burners End', '1 Burner End']
HRR_df = pd.read_csv(results_dir+'calculated_HRRs.csv', index_col=0)
skip_tests = []
for test in HRR_df['Test']:
	skip_tests.append(test)

ft3_to_m3 = 0.3048**3
density_C3H8 = 2.423 # [kg/m^3]
delH_C3H8 = 46000.0 	# [kJ/kg]

def calculate_range_HRR(start_time, end_time, V_start, V_end):
	HRR = (float(V_end-V_start)/(end_time-start_time))*1000.0*ft3_to_m3*density_C3H8*delH_C3H8
	return round(HRR, 1)

if 'Compensated' not in skip_tests:
	new_row = pd.Series(['Compensated', ' ', ' ', ' ', ' ', ' '], index=HRR_df_headers)
	HRR_df = HRR_df.append(new_row, ignore_index=True)

for f in os.listdir(comp_video_dir):
	if f.endswith('.mp4'):

		test_name = f[:-24]

		if test_name[-1] == '_':
			test_name = test_name[:-1]

		if test_name in skip_tests:
			continue

		print
		print '-------------------------------'
		print '----- '+test_name+' Compensated -----'
		print '-------------------------------'
		video = cv2.VideoCapture(comp_video_dir + f)

		if info['Rotation'][test_name]:
			rotate = True
		else:
			rotate = False

		# get coordinates of current dial
		x1, x2 = info['Comp X Bounds'][test_name].split(', ')
		y1, y2 = info['Comp Y Bounds'][test_name].split(', ')

		# set video at start/end times (convert start time to ms)
		corner_on_times = info['Corner burner on'][test_name].split('|')
		middle_on_times = info['Middle burner on'][test_name].split('|')
		center_on_times = info['Center burner on'][test_name].split('|')
		corner_off_times = info['Corner burner off'][test_name].split('|')
		middle_off_times = info['Middle burner off'][test_name].split('|')
		center_off_times = info['Center burner off'][test_name].split('|')

		video_start = info['Comp Start'][test_name].split(':')
		video_start_ms = (int(video_start[0])*60+int(video_start[1]))*1000

		test_seq = 0
		while test_seq < len(corner_on_times):
			# convert times to seconds, determine ranges of video for different steps
			corner_on = corner_on_times[test_seq].split(':')
			middle_on = middle_on_times[test_seq].split(':')
			center_on = center_on_times[test_seq].split(':')
			corner_off = corner_off_times[test_seq].split(':')
			middle_off = middle_off_times[test_seq].split(':')
			center_off = center_off_times[test_seq].split(':')
			seq_steps = sorted([60*int(corner_on[0])+int(corner_on[1]), 60*int(middle_on[0])+int(middle_on[1]),
				60*int(center_on[0])+int(center_on[1]), 60*int(corner_off[0])+int(corner_off[1]), 
				60*int(middle_off[0])+int(middle_off[1]), 60*int(center_off[0])+int(center_off[1])])

			# difference between recorded times and video time
			if test_seq == 0:
				video_time_diff = video_start_ms-seq_steps[0]*1000
			
			if len(corner_on_times) > 1:
				new_row_ls = [test_name + ' - Seq. ' + str(test_seq+1)]
				print
				print '** Calculating HRRs for '+ test_name + ' - Seq. ' + str(test_seq+1)+' **'
			else:
				new_row_ls = [test_name]
				print
				print '** Calculating HRRs for '+ test_name + ' **'

			i = 0
			while i < len(seq_steps)-1:
				start_time = seq_steps[i]*1000+video_time_diff
				end_time = seq_steps[i+1]*1000+video_time_diff

				if i < 3:
					print
					print 'Start/stop for '+str(i+1)+' of 3 burners on'
				else:
					print
					print 'Start/stop for '+str(i-2)+' of 3 burners off'

				if end_time-start_time > 30000:
					# read entire frame as image
					video.set(0, start_time)
					ret, image = video.read()
					dial_img_visible = image[int(y1):int(y2), int(x1):int(x2)]
					if rotate:
						h,w = dial_img_visible.shape[:2]
						center = (w/2, h/2)
						M = cv2.getRotationMatrix2D(center, 180, 1.0) # (1.0 = scaling factor)
						dial_img_visible = cv2.warpAffine(dial_img_visible, M, (w,h))
					dial_img_visible = cv2.cvtColor(dial_img_visible, cv2.COLOR_BGR2RGB)
					plt.imshow(dial_img_visible)
					plt.show(block=False)
					
					print
					print '-Go forward to the last second of the next full dial spin.'
					while(True):
						try:
							print
							print '  Enter "++"/"--" to go forward/backward 2 seconds.'
							print '  Enter "+"/"-" to go forward/backward 1 second.'
							start_value = raw_input('  Once at the end of spin, enter the dial reading: ')
							start_value = float(start_value)
							break
						except ValueError:
							valid_entry = True
							if start_value == '+':
								multiplier = 1
							elif start_value == '-':
								multiplier = -1 
							elif start_value == '++':
								multiplier = 2
							elif start_value == '--':
								multiplier = -2
							else:
								valid_entry = False

							if valid_entry:
								start_time = start_time+1000*multiplier
								plt.close()
								video.set(0, start_time)
								ret, image = video.read()
								dial_img_visible = image[int(y1):int(y2), int(x1):int(x2)]
								if rotate:
									h,w = dial_img_visible.shape[:2]
									center = (w/2, h/2)
									M = cv2.getRotationMatrix2D(center, 180, 1.0) # (1.0 = scaling factor)
									dial_img_visible = cv2.warpAffine(dial_img_visible, M, (w,h))
								dial_img_visible = cv2.cvtColor(dial_img_visible, cv2.COLOR_BGR2RGB)
								plt.imshow(dial_img_visible)
								plt.show(block=False)
							else:
								print '  Invalid Entry -- input should be a single digit or float'
					plt.close()

					# read entire frame as image
					video.set(0, end_time)
					ret, image = video.read()
					dial_img_visible = image[int(y1):int(y2), int(x1):int(x2)]
					if rotate:
						h,w = dial_img_visible.shape[:2]
						center = (w/2, h/2)
						M = cv2.getRotationMatrix2D(center, 180, 1.0) # (1.0 = scaling factor)
						dial_img_visible = cv2.warpAffine(dial_img_visible, M, (w,h))
					dial_img_visible = cv2.cvtColor(dial_img_visible, cv2.COLOR_BGR2RGB)
					plt.imshow(dial_img_visible)
					plt.show(block=False)

					print
					print '-Go backward until the last second of last full dial spin.'
					while(True):
						try:
							print
							print '  Enter "++"/"--" to go forward/backward 2 seconds.'
							print '  Enter "+"/"-" to go forward/backward 1 second.'
							end_value = raw_input('  Once at the end of spin, enter the dial reading: ')
							end_value = float(end_value)
							break
						except ValueError:
							valid_entry = True
							if end_value == '+':
								multiplier = 1
							elif end_value == '-':
								multiplier = -1 
							elif end_value == '++':
								multiplier = 2
							elif end_value == '--':
								multiplier = -2
							else:
								valid_entry = False

							if valid_entry:
								end_time = end_time+1000*multiplier
								plt.close()
								video.set(0, end_time)
								ret, image = video.read()
								dial_img_visible = image[int(y1):int(y2), int(x1):int(x2)]
								if rotate:
									h,w = dial_img_visible.shape[:2]
									center = (w/2, h/2)
									M = cv2.getRotationMatrix2D(center, 180, 1.0) # (1.0 = scaling factor)
									dial_img_visible = cv2.warpAffine(dial_img_visible, M, (w,h))
								dial_img_visible = cv2.cvtColor(dial_img_visible, cv2.COLOR_BGR2RGB)
								plt.imshow(dial_img_visible)
								plt.show(block=False)
							else:
								print '  Invalid Entry -- input should be a single digit or float'
					plt.close()

					if end_value == start_value:
						new_row_ls.append('N/A')
						print
						print ' >> Duration too short, HRR not calculated'
					else:
						HRR = calculate_range_HRR(start_time, end_time, start_value, end_value)
						new_row_ls.append(HRR)
						print
						print ' >> HRR = '+str(HRR)+' kW'

				else:
					new_row_ls.append('N/A')
					print
					print ' >> Duration too short, HRR not calculated'
				
				i += 1

			new_row = pd.Series(new_row_ls, index=HRR_df_headers)
			HRR_df = HRR_df.append(new_row, ignore_index=True)
			HRR_df.to_csv(results_dir+'calculated_HRRs.csv')
			test_seq +=1

new_row = pd.Series(['Uncompensated', ' ', ' ', ' ', ' ', ' '], index=HRR_df_headers)
HRR_df = HRR_df.append(new_row, ignore_index=True)

for f in os.listdir(raw_video_dir):
	if f.endswith('.mp4'):

		test_name = f[:-24]

		if test_name[-1] == '_':
			test_name = test_name[:-1]

		try:
			video_start = info['Uncomp Start'][test_name].split(':')
			video_start_ms = (int(video_start[0])*60+int(video_start[1]))*1000
		except:
			continue

		print
		print '---------------------------------'
		print '----- '+test_name+' Uncompensated -----'
		print '---------------------------------'
		video = cv2.VideoCapture(raw_video_dir + f)

		# get coordinates of current dial
		x1, x2 = info['Uncomp X Bounds'][test_name].split(', ')
		y1, y2 = info['Uncomp Y Bounds'][test_name].split(', ')

		# set video at start/end times (convert start time to ms)
		corner_on_times = info['Corner burner on'][test_name].split('|')
		middle_on_times = info['Middle burner on'][test_name].split('|')
		center_on_times = info['Center burner on'][test_name].split('|')
		corner_off_times = info['Corner burner off'][test_name].split('|')
		middle_off_times = info['Middle burner off'][test_name].split('|')
		center_off_times = info['Center burner off'][test_name].split('|')

		test_seq = 0
		while test_seq < len(corner_on_times):
			# convert times to seconds, determine ranges of video for different steps
			corner_on = corner_on_times[test_seq].split(':')
			middle_on = middle_on_times[test_seq].split(':')
			center_on = center_on_times[test_seq].split(':')
			corner_off = corner_off_times[test_seq].split(':')
			middle_off = middle_off_times[test_seq].split(':')
			center_off = center_off_times[test_seq].split(':')
			seq_steps = sorted([60*int(corner_on[0])+int(corner_on[1]), 60*int(middle_on[0])+int(middle_on[1]),
				60*int(center_on[0])+int(center_on[1]), 60*int(corner_off[0])+int(corner_off[1]), 
				60*int(middle_off[0])+int(middle_off[1]), 60*int(center_off[0])+int(center_off[1])])

			# difference between recorded times and video time
			if test_seq == 0:
				video_time_diff = video_start_ms-seq_steps[0]*1000
			
			if len(corner_on_times) > 1:
				new_row_ls = [test_name + ' - Seq. ' + str(test_seq+1)]
				print
				print '** Calculating HRRs for '+test_name+' - Seq. '+str(test_seq+1)+' **'
			else:
				new_row_ls = [test_name]
				print
				print '** Calculating HRRs for '+test_name+' **'

			i = 0

			while i < len(seq_steps)-1:
				start_time = seq_steps[i]*1000+video_time_diff
				end_time = seq_steps[i+1]*1000+video_time_diff

				if i < 3:
					print
					print 'Start/stop for '+str(i+1)+' of 3 burners on'
				else:
					print
					print 'Start/stop for '+str(i-2)+' of 3 burners off'

				if start_time != end_time:
					start_time = start_time+3000
					end_time = end_time-3000

					# read entire frame as image
					video.set(0, start_time)
					ret, image = video.read()
					dial_img_visible = image[int(y1)-50:int(y2)+50, int(x1)-100:int(x2)+50]
					dial_img_visible = cv2.cvtColor(dial_img_visible, cv2.COLOR_BGR2RGB)
					plt.imshow(dial_img_visible)
					plt.show(block=False)
					
					print
					print '-Go forward to the next whole number displayed on dial.'
					while(True):
						try:
							print
							print '  Enter "++"/"--" to go forward/backward 2 seconds.'
							print '  Enter "+"/"-" to go forward/backward 1 second.'
							start_value = raw_input('  Once at the whole number, enter the dial reading: ')
							start_value = float(start_value)
							break
						except ValueError:
							valid_entry = True
							if start_value == '+':
								multiplier = 1
							elif start_value == '-':
								multiplier = -1 
							elif start_value == '++':
								multiplier = 2
							elif start_value == '--':
								multiplier = -2
							else:
								valid_entry = False

							if valid_entry:
								start_time = start_time+1000*multiplier
								plt.close()
								video.set(0, start_time)
								ret, image = video.read()
								dial_img_visible = image[int(y1)-50:int(y2)+50, int(x1)-100:int(x2)+50]
								dial_img_visible = cv2.cvtColor(dial_img_visible, cv2.COLOR_BGR2RGB)
								plt.imshow(dial_img_visible)
								plt.show(block=False)
							else:
								print ('  Invalid Entry -- input should be an integer or +/-')
					plt.close()

					# read entire frame as image
					video.set(0, end_time)
					ret, image = video.read()
					dial_img_visible = image[int(y1)-50:int(y2)+50, int(x1)-100:int(x2)+50]
					dial_img_visible = cv2.cvtColor(dial_img_visible, cv2.COLOR_BGR2RGB)
					plt.imshow(dial_img_visible)
					plt.show(block=False)

					print
					print '-Go backward until last whole number displayed on dial.'
					while(True):
						try:
							print
							print '  Enter "++"/"--" to go forward/backward 2 seconds.'
							print '  Enter "+"/"-" to go forward/backward 1 second.'
							end_value = raw_input('  Once at the whole number, enter the dial reading: ')
							end_value = float(end_value)
							break
						except ValueError:
							valid_entry = True
							if end_value == '+':
								multiplier = 1
							elif end_value == '-':
								multiplier = -1 
							elif end_value == '++':
								multiplier = 2
							elif end_value == '--':
								multiplier = -2
							else:
								valid_entry = False

							if valid_entry:
								end_time = end_time+1000*multiplier
								plt.close()
								video.set(0, end_time)
								ret, image = video.read()
								dial_img_visible = image[int(y1)-50:int(y2)+50, int(x1)-100:int(x2)+50]
								dial_img_visible = cv2.cvtColor(dial_img_visible, cv2.COLOR_BGR2RGB)
								plt.imshow(dial_img_visible)
								plt.show(block=False)
								print
							else:
								print ('  Invalid Entry -- input should be an integer or +/-')
					plt.close()

					if end_value == start_value:
						new_row_ls.append('N/A')
						print
						print ' >> Duration too short, HRR not calculated'
					else:
						HRR = calculate_range_HRR(start_time, end_time, start_value, end_value)
						new_row_ls.append(HRR)
						print
						print ' >> HRR = '+str(HRR)+' kW'

				else:
					new_row_ls.append('N/A')
					print
					print ' >> Duration too short, HRR not calculated'

				i += 1

			new_row = pd.Series(new_row_ls, index=HRR_df_headers)
			HRR_df = HRR_df.append(new_row, ignore_index=True)
			HRR_df.to_csv(results_dir+'calculated_HRRs.csv')
			test_seq +=1
