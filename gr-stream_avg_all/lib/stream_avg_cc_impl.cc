/* -*- c++ -*- */
/* 
 * Copyright 2014 <+YOU OR YOUR COMPANY+>.
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
#include "stream_avg_cc_impl.h"

namespace gr {
  namespace stream_avg_all {

    stream_avg_cc::sptr
    stream_avg_cc::make(
			const unsigned int num_v, 
			const unsigned int Nfft)
    {
      return gnuradio::get_initial_sptr
        (new stream_avg_cc_impl(num_v,Nfft));
    }

    /*
     * The private constructor
     */
    stream_avg_cc_impl::stream_avg_cc_impl(
			const unsigned int num_v, 
			const unsigned int Nfft)
      : gr::sync_decimator("stream_avg_cc",
              gr::io_signature::make(1, 1, Nfft*sizeof(gr_complex)),
              gr::io_signature::make(1, 1, Nfft*sizeof(float)), num_v),
		d_num_v(num_v),
		d_Nfft(Nfft)
    {}

    /*
     * Our virtual destructor.
     */
    stream_avg_cc_impl::~stream_avg_cc_impl()
    {
    }

    int
    stream_avg_cc_impl::work(int noutput_items,
			  gr_vector_const_void_star &input_items,
			  gr_vector_void_star &output_items)
    {
        const gr_complex *in = (const gr_complex *) input_items[0];
        float *out = (float *) output_items[0];
		
		memset(out, 0x00, noutput_items*sizeof(float));
		unsigned int i,j,k,index;
		float answer;
		
		//Processing Periodogram Estimator across FFT bins
		for(i=0;i<noutput_items;i++){
			for(j=0;j<d_num_v;j++){
				for(k=0;k<d_Nfft;k++){
					//Index
					index = i*d_num_v*d_Nfft + j*d_Nfft + k; 

					//Power Calculation
					answer = in[index].real()*in[index].real() +
								in[index].imag()*in[index].imag();

					//Output
					out[i*d_Nfft + k] += answer/(float) d_num_v;
				}
			}
		}

        // Tell runtime system how many output items we produced.
        return noutput_items;
    }

  } /* namespace stream_avg_all */
} /* namespace gr */

