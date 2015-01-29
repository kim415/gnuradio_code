/* -*- c++ -*- */
/* 
 * Copyright 2013 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "spectrum_detect_ff_impl.h"

namespace gr {
  namespace stream_avg_all {

    spectrum_detect_ff::sptr
    spectrum_detect_ff::make(const unsigned int fft_len, const std::vector<float> &window)
    {
      return gnuradio::get_initial_sptr
        (new spectrum_detect_ff_impl(fft_len,window));
    }

    /*
     * The private constructor
     */
    spectrum_detect_ff_impl::spectrum_detect_ff_impl(const unsigned int fft_len, const std::vector<float> &window)
      : gr::sync_block("spectrum_detect_ff",
              gr::io_signature::make(1, 1, fft_len*sizeof(float)),
              gr::io_signature::make(1, 1, fft_len*sizeof(float)))
    {	
	this->fft_len=fft_len;
	this->window=window;
    }

    /*
     * Our virtual destructor.
     */
    spectrum_detect_ff_impl::~spectrum_detect_ff_impl()
    {
    }

    int
    spectrum_detect_ff_impl::work(int noutput_items,
			  gr_vector_const_void_star &input_items,
			  gr_vector_void_star &output_items)
    {
        const float *in = (const float *) input_items[0];
        float *out = (float *) output_items[0];
	std::vector<float> threshold;
	int i,j;	


	fft_len = this->fft_len;
	threshold = this->window;

	for(i=0;i<fft_len;i++){
		for(j=0;j<noutput_items;j++){
			if(in[i*noutput_items + j] > threshold[i*noutput_items + j]){
				out[i*noutput_items + j]=1;
			}else{
				out[i*noutput_items + j]=0;
			}			

		}

	}
	
        // Do <+signal processing+>

        // Tell runtime system how many output items we produced.
        return noutput_items;
    }

  } /* namespace stream_avg_all */
} /* namespace gr */

