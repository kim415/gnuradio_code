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


#ifndef INCLUDED_STREAM_AVG_ALL_STREAM_AVG_CC_H
#define INCLUDED_STREAM_AVG_ALL_STREAM_AVG_CC_H

#include <stream_avg_all/api.h>
#include <gnuradio/sync_decimator.h>

namespace gr {
  namespace stream_avg_all {

    /*!
     * \brief <+description of block+>
     * \ingroup stream_avg_all
     *
     */
    class STREAM_AVG_ALL_API stream_avg_cc : virtual public gr::sync_decimator
    {
     public:
      typedef boost::shared_ptr<stream_avg_cc> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of stream_avg_all::stream_avg_cc.
       *
       * To avoid accidental use of raw pointers, stream_avg_all::stream_avg_cc's
       * constructor is in a private implementation
       * class. stream_avg_all::stream_avg_cc::make is the public interface for
       * creating new instances.
       */
      static sptr make(
			const unsigned int num_v, 
			const unsigned int Nfft);
    };

  } // namespace stream_avg_all
} // namespace gr

#endif /* INCLUDED_STREAM_AVG_ALL_STREAM_AVG_CC_H */

