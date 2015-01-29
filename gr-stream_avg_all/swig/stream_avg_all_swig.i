/* -*- c++ -*- */

#define STREAM_AVG_ALL_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "stream_avg_all_swig_doc.i"

%{
#include "stream_avg_all/stream_avg_ff.h"
#include "stream_avg_all/spectrum_detect_ff.h"
#include "stream_avg_all/stream_avg_cc.h"
%}


%include "stream_avg_all/stream_avg_ff.h"
GR_SWIG_BLOCK_MAGIC2(stream_avg_all, stream_avg_ff);
%include "stream_avg_all/spectrum_detect_ff.h"
GR_SWIG_BLOCK_MAGIC2(stream_avg_all, spectrum_detect_ff);
%include "stream_avg_all/stream_avg_cc.h"
GR_SWIG_BLOCK_MAGIC2(stream_avg_all, stream_avg_cc);
