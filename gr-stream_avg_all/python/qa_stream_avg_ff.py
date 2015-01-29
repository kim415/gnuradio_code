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

class qa_stream_avg_ff (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        # set up fg
	test_input = (1,2,3,4,2,3,4,5,3,4,5,6,4,5,6,7,5,6,7,8);
	test_output = (3, 4, 5, 6);
	test_output1 = (2, 2, 2, 2);
        # set up fg
	vector_input = blocks.vector_source_f(test_input);
	s_to_v = blocks.stream_to_vector(gr.sizeof_float,20);
	#s_to_v_1 = blocks.stream_to_vector(gr.sizeof_float,9);
	
	summing = stream_avg_all.stream_avg_ff(4,5)
	v_to_s = blocks.vector_to_stream(gr.sizeof_float,4);
	v_to_s_1 = blocks.vector_to_stream(gr.sizeof_float,4);
	dest = blocks.vector_sink_f();
	dest_1 = blocks.vector_sink_f();
	
	self.tb.connect(vector_input,s_to_v);
	#self.tb.connect(s_to_v,s_to_v_1);
	self.tb.connect(s_to_v,summing);
	self.tb.connect((summing,0),v_to_s);
	self.tb.connect((summing,1),v_to_s_1);
	#self.tb.connect(v_to_s_1,v_to_s);
	self.tb.connect(v_to_s,dest);
	self.tb.connect(v_to_s_1,dest_1);
	self.tb.run();
	#print dest.data();
	#print dest_1.data();
	
	self.assertEqual(test_output,dest.data())
	self.assertEqual(test_output1,dest_1.data())
        # check data


if __name__ == '__main__':
    gr_unittest.run(qa_stream_avg_ff, "qa_stream_avg_ff.xml")
