#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 18:32:07 2020

@author: sourav
"""

import numpy as np

class LSH():
    def __generate_random_vectors(self, num_vector, dim):
        return np.random.randn(dim, num_vector)
    
    def generate_indices(self, data, num_vector, seed=None):
        dim = data.shape[1]
        if seed is not None:
            np.random.seed(seed)

        random_vectors = self.__generate_random_vectors(num_vector, dim)
        powers_of_two = 1 << np.arange(num_vector - 1, -1, -1)

        table = {}
        # Partition data points into bins
        bin_index_bits = (data.dot(random_vectors) >= 0)

        # Encode bin index bits into integers
        bin_indices = bin_index_bits.dot(powers_of_two)

        # Update `table` so that `table[i]` is the list of document ids with bin index equal to i.
        for data_index, bin_index in enumerate(bin_indices):
            if bin_index not in table:
                # If no list yet exists for this bin, assign the bin an empty list.
                table[bin_index.tolist()] = []
            # Fetch the list of document ids associated with the bin and add the document id to the end.
            table[bin_index.tolist()].append(data_index)
        model = {'bin_indices': bin_indices.tolist(), 'table': table,
                      'random_vectors': random_vectors.tolist(), 'num_vector': num_vector}
        return model
