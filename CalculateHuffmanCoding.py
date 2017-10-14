#!/usr/bin/env python3

import sys
from collections import defaultdict
from heapq import heappop, heappush
import time

def load_data(file_name):
    #Read in the frequency data.
    
    #f_heap is a heap of frequencies of the associated symbols
    #f_dict is a dictionary with frequencies for keys and symbols for values
    
    f_heap = []
    f_dict = defaultdict(set)
    fn = open(file_name,'r')
    nr_syms = int(fn.readline().strip())
    sym_id = 0
    
    for line in fn:
        f = int(line.strip())
        f_dict[f].add(sym_id)
        heappush(f_heap,f)
        sym_id += 1
    fn.close()
    
    assert len(f_heap) == len(set(f_heap)) #we will assume all weights are distinct
    return f_heap, f_dict

def generate_coding(f_heap,f_dict):
    #Generate Huffman coding by continuously popping the two smallest frequencies and merging their associated branches.
    
    f1 = heappop(f_heap)
    f2 = heappop(f_heap)
    if not f_heap:
        Huffman_coding = dict()
        Huffman_coding[max(f1,f2)]='0'
        Huffman_coding[min(f1,f2)]='1'
        return Huffman_coding
    else:
        fn = f1 + f2
        if fn in f_dict:
            raise FatalError('frequency collision during Huffman coding')
        f_dict[fn] = f_dict[fn] | f_dict.pop(f1) | f_dict.pop(f2)
        heappush(f_heap,fn)
        Huffman_coding = generate_coding(f_heap,f_dict)
        bifur_code = Huffman_coding[fn]
        Huffman_coding[max(f1,f2)] = bifur_code + '0'
        Huffman_coding[min(f1,f2)] = bifur_code + '1'
        del Huffman_coding[fn]
    return Huffman_coding

if __name__ == "__main__":
    file_name = 'huffmaneasytest.txt'
    sys.setrecursionlimit(1002) #for N pieces of data the recursion limit must be set at N+2
    
    start = time.time()

    f_heap, f_dict = load_data(file_name)
    Huffman_coding = generate_coding(f_heap,f_dict)

    print('Huffman coding:')
    print(Huffman_coding)
    
    end = time.time()
    print(end - start)