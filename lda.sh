#!/bin/sh

mpiexec -n 4 plda/mpi_lda --num_topics 50 --alpha 0.5 --beta 0.1\
         --training_data_file wikidump/ldacorpus3.txt\
         --model_file lda_model2.txt\
         --burn_in_iterations 100 --total_iterations 200
