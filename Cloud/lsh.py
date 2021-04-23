#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 21:09:34 2020

@author: sourav
"""

from itertools import combinations
import numpy as np
from pandas import DataFrame
from sklearn.metrics.pairwise import pairwise_distances

class LSH:
    def __init__(self, data, model):
        self.data = data
        self.model = model

    def __search_nearby_bins(self, query_bin_bits, table, search_radius=10, candidate_set=None):
        if candidate_set is None:
            candidate_set = set()

        n_vectors = query_bin_bits.shape[0]
        powers_of_two = 1 << np.arange(n_vectors - 1, -1, step=-1)

        for different_bits in combinations(range(n_vectors), search_radius):
            # flip the bits (n_1, n_2, ..., n_r) of the query bin to produce a new bit vector
            index = list(different_bits)
            alternate_bits = query_bin_bits.copy()
            alternate_bits[index] = np.logical_not(alternate_bits[index])

            # convert the new bit vector to an integer index
            nearby_bin = alternate_bits.dot(powers_of_two)

            # fetch the list of documents belonging to
            # the bin indexed by the new bit vector,
            # then add those documents to candidate_set;
            # make sure that the bin exists in the table
            if nearby_bin in table:
                candidate_set.update(table[nearby_bin])

        return candidate_set

    def query(self, query_vec, k, max_search_radius, initial_candidates=set()):

        if not self.model:
            print('Model not yet build. Exiting!')
            exit(-1)

        data = self.data
        print(data)
        table = self.model['table']
        table = {int(k):v for k,v in table.items()}
        print(table)
        random_vectors = np.array(self.model['random_vectors'])
        print(query_vec)
        print(random_vectors)
        bin_index_bits = (query_vec.dot(random_vectors) >= 0).flatten()

        candidate_set = set()
        # Search nearby bins and collect candidates
        for search_radius in range(max_search_radius + 1):
            candidate_set = self.__search_nearby_bins(bin_index_bits, table, search_radius, candidate_set)
        # Sort candidates by their true distances from the query
        nearest_neighbors = DataFrame({'id': list(candidate_set)})
        print(list(candidate_set))
        candidates = data[np.array(list(candidate_set)), :]
        
        nearest_neighbors['distance'] = pairwise_distances(candidates, query_vec, metric='euclidean').flatten()
        res_id = list(nearest_neighbors.nsmallest(k, 'distance')['id'])
        print(res_id)
        return nearest_neighbors.nsmallest(k, 'distance'), res_id
