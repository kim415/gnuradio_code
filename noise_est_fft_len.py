#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Wed Jun 19 12:40:09 2013
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio import fft
from gnuradio import analog
from gnuradio import filter
from gnuradio.eng_option import eng_option
from optparse import OptionParser
import time
import math
import sys
import stream_avg_all
import struct
import os

class top_block(gr.top_block):  
	def __init__(self,options,usrp):
		gr.top_block.__init__(self)

		##################################################
		# Variables
		##################################################
		
		self.sigFreq = options.sigf
		self.sampRate = options.samp
		self.rxGain = options.gain
		self.carrierFreq = options.carf
		self.fft_length =options.fft_len
		self.usrp_source = usrp
		self.nstream = options.nstream
		
		##################################################
		# Blocks
		##################################################
		
		#Serial to Parallel
		self.s_to_p =\
			 blocks.stream_to_vector(gr.sizeof_gr_complex,self.fft_length)
		
		#Window Process for FFT process
		self.windows_tap \
			=filter.firdes.window(filter.firdes.WIN_BLACKMAN_HARRIS,self.fft_length,1)
        	power=0;
		
		for tap in self.windows_tap:
            		power += tap*tap

		#FFT process
		self.fft_process =fft.fft_vcc(self.fft_length,True,self.windows_tap,True,1)
		
		#Power process
		self.complex_to_mag_sq =\
			 blocks.complex_to_mag_squared(self.fft_length)
		
		#Parallel to Serial
		self.p_to_s=\
			 blocks.vector_to_stream(gr.sizeof_float,self.fft_length)
		

		#Serial to Parallel with a different size
		self.s_to_p2=\
		blocks.stream_to_vector(gr.sizeof_float, self.fft_length*self.nstream)

		#Average Periodogram Estimator process
		self.avg_best =\
			 stream_avg_all.stream_avg_ff(self.fft_length,self.nstream)
		
		#Parallel to Serial for Average Peridogream Estimator
		self.p_to_s2=\
			 blocks.vector_to_stream(gr.sizeof_float,self.fft_length)


		#Parallel to Serial for the variance of Peridogream Estimator
		self.p_to_s3=\
			 blocks.vector_to_stream(gr.sizeof_float,self.fft_length)

		
		#self.log_ff= blocks.nlog10_ff(20,self.fft_length,\
		#		 -10*math.log10(self.fft_length)\
		#		 -10*math.log10(power/self.fft_length))
		

		

		self.blocks_time=blocks.file_sink(gr.sizeof_gr_complex,'time_domain')
		self.blocks_mean=blocks.file_sink(gr.sizeof_float,'fft_average')
		self.blocks_var=blocks.file_sink(gr.sizeof_float,'fft_variance')
		
		##################################################
		# Connections
		##################################################
		
		self.connect((self.usrp_source,0), (self.s_to_p,0))
		#self.connect((self.usrp_source,0), (self.blocks_time,0))
		self.connect((self.s_to_p,0), (self.fft_process,0))
		self.connect((self.fft_process, 0), (self.complex_to_mag_sq, 0))
		self.connect((self.complex_to_mag_sq, 0),(self.p_to_s,0))
		self.connect((self.p_to_s,0), (self.s_to_p2,0))
		self.connect((self.s_to_p2, 0),(self.avg_best, 0))

		self.connect((self.avg_best, 0),(self.p_to_s2, 0))
		self.connect((self.avg_best, 1),(self.p_to_s3, 0))
		self.connect((self.p_to_s2, 0),(self.blocks_mean,0))
		self.connect((self.p_to_s3, 0),(self.blocks_var,0))
	
		
if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	
	parser.add_option("-f","--sigf",type="eng_float",\
			default=10000,help="Set signal frequency.")
	parser.add_option("-g","--gain",type="eng_float",\
			default=0,help="Set receiver gain.")
	parser.add_option("-c","--carf",type="eng_float",\
			default=600E6,help="Set carrier frequency.")
	parser.add_option("-s","--samp",type="eng_float",\
			default=5E6,help="Set carrier frequency.")
	parser.add_option("-t","--time",type="eng_float",\
			default=1,help="Set carrier frequency.")
	parser.add_option("-n","--nstream",type="eng_float",\
			default=50,help="Set carrier frequency.")
	parser.add_option("-x","--fft_len",type="eng_float",\
			default=8192,help="Set carrier frequency.")
	parser.add_option("-m","--name",type="string",\
			default="fft_average",help="Set carrier frequency.")

	(options, args) = parser.parse_args()
	

	## USRP Setup
	usrp_source = uhd.usrp_source(
		device_addr="",
		stream_args=uhd.stream_args(
			cpu_format="fc32",
			channels=range(1),
		),
	)

        usrp.set_center_freq(uhd.tune_request(options.carf, 0, \                   
               dsp_freq_policy = uhd.tune_request.POLICY_MANUAL,\               
               rf_freq_policy = uhd.tune_request.POLICY_MANUAL), 0) 

	usrp_source.set_samp_rate(options.samp)
	#usrp_source.set_center_freq(options.carf, 0)
	usrp_source.set_gain(options.gain, 0)
		
	
	
	tb = top_block(options,usrp_source)

	#List of Parameter printout
	print "Signal Freq = " + str(options.sigf) + " Hz"
	print "RX gain = " + str(options.gain) + " dB"
	print "Carrier Freq = " + str(options.carf) + " Hz"
	print "Sample Rate = " + str(options.samp) + " sps"

	#Set Count/CountMax
	count = 0
	countMax = 1
	fft_len_decrement = 2
	print "Printing out the noise estimation at " + str(options.carf) + "MHz"	
	while True:
		
		#Start USRP
		print usrp_source.get_sensor("lo_locked")
		while not usrp_source.get_sensor("lo_locked"):
			    print usrp_source.get_sensor("lo_locked")
			
		tb.start()
		time.sleep(3)
		tb.stop()
		tb.wait()
		
		count = count + 1
		
		print "Trial "+ str(count) + " is recorded."
		
		os.rename("fft_average",\
			"fft_average"+str(int(options.fft_len))+"_"+ str(count))
		os.rename("fft_variance",\
			"fft_variance"+str(int(options.fft_len))+"_"+ str(count))
		os.rename("time_domain",\
			"time_domain"+str(int(options.fft_len))+"_"+ str(count))
		tb = top_block(options, usrp_source)
		#time.sleep(5)
		if count > countMax-1:
			count = 0
			print "Complete! Good job."
			options.fft_len = options.fft_len/fft_len_decrement
			tb = top_block(options, usrp_source)
			print "Printing out the noise estimation at " \
				+ str(options.fft_len) + "block length"	
			if options.fft_len < 8:
				sys.exit(1)
