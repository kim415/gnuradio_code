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
#include "stream_avg_ff_impl.h"

namespace gr {
  namespace stream_avg_all {

    stream_avg_ff::sptr
    stream_avg_ff::make(const unsigned int fft_len, const unsigned int nstreams)
    {
      return gnuradio::get_initial_sptr
        (new stream_avg_ff_impl(fft_len,  nstreams));
    }

    /*
     * The private constructor
     */
    stream_avg_ff_impl::stream_avg_ff_impl(const unsigned int fft_len, const unsigned int nstreams)
      : gr::sync_block("stream_avg_ff",
              gr::io_signature::make(1, 1, sizeof(float)*fft_len*nstreams),
              gr::io_signature::make(2, 2, sizeof(float)*fft_len))
    {
	this->fft_len = fft_len;	
	this->nstreams = nstreams;	

    }

    /*
     * Our virtual destructor.
     */
    stream_avg_ff_impl::~stream_avg_ff_impl()
    {
    }

    int
    stream_avg_ff_impl::work(int noutput_items,
			  gr_vector_const_void_star &input_items,
			  gr_vector_void_star &output_items)
    {
        const float  *in = (const float *) input_items[0];
        float *out = (float *) output_items[0];
        float *out1 = (float *) output_items[1];

        // Do <+signal processing+>

        unsigned int i,j,k;

	unsigned int nstreams,len_size;
	nstreams = this->nstreams;
	len_size= this->fft_len;
	for(i=0;i<nstreams;i++){
		for(j=0;j<len_size;j++){
			for(k=0;k<noutput_items;k++){
				if(i ==0){
					out[noutput_items*j + k]= in[noutput_items*j + k];	
				}else{
					out[noutput_items*j + k] += in[len_size*noutput_items*i + noutput_items*j + k];	
				}
			}
		}		
	}
	
	for(j=0;j<len_size;j++){
		for(k=0;k < noutput_items;k++){
			out[noutput_items*j + k] = out[noutput_items*j + k]/nstreams; 
			out[noutput_items*j + k] = out[noutput_items*j + k]/len_size; 
			out1[noutput_items*j + k] = 0; 
			
		}
	}

	for(i=0;i<nstreams;i++){
		for(j=0;j<len_size;j++){
			for(k=0;k<noutput_items;k++){
				out1[noutput_items*j + k] += 
					(out[noutput_items*j + k] - in[len_size*noutput_items*i + noutput_items*j + k])
					*(out[noutput_items*j + k] - in[len_size*noutput_items*i + noutput_items*j + k]);	
			}
		}	
	}
	
	for(j=0;j<len_size;j++){
		for(k=0;k < noutput_items;k++){
			out1[noutput_items*j + k] = out1[noutput_items*j + k]/nstreams; 
			out1[noutput_items*j + k] = out1[noutput_items*j + k]/len_size; 
		}
	}
        // Tell runtime system how many output items we produced.
        return noutput_items;
    }

  } /* namespace stream_avg_all */
} /* namespace gr */

