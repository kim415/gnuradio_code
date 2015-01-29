#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2013 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr, gr_unittest, blocks
import stream_avg_all_swig as stream_avg_all

class qa_spectrum_detect_ff (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        # set up fg
	test_input  =  (1,1,0,0,2,2,3,3,4,4,-1,-1,5,5);
	test_threshold=(2,2,1,1,1,1,1,1,5,5,0,0,3,3);
	test_output =  (0,0,0,0,1,1,1,1,0,0,0,0,1,1);

	vector_input=blocks.vector_source_f(test_input);
	s_to_v = blocks.stream_to_vector(gr.sizeof_float,14);
	detection = stream_avg_all.spectrum_detect_ff(14,test_threshold);
	v_to_s = blocks.vector_to_stream(gr.sizeof_float,14);
	dest = blocks.vector_sink_f();


	self.tb.connect(vector_input,s_to_v);
	self.tb.connect(s_to_v,detection);
	self.tb.connect(detection,v_to_s);
	self.tb.connect(v_to_s,dest);

        self.tb.run()
	self.assertEqual(test_output,dest.data());
        # check data


if __name__ == '__main__':
    gr_unittest.run(qa_spectrum_detect_ff, "qa_spectrum_detect_ff.xml")
