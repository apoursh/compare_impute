"""
split_vcf_info.py
author: Gerard Tse (gerardtse@gmail.com)

This file defines logic to deal with chunked VCF files by loading the
metadata file generated by chunking. Designed to work with genotypes
split using splitVcfRef.jar, described here.
http://www.unc.edu/~yunmli/MaCH-Admix/tutorial.php#split
"""
import os

# This class reads data from info csv files generated by splitVcfRef.jar
class SplitVcfInfo(object):

    def __init__(self, base):
        self.base_ = base
        self.core_boundaries_ = []
        self.buffered_boundaries_ = []
        self.filenames_ = []
        self.valid_ = self.load()

    def valid(self):
        return self.valid_

    def load(self):
        metadata_fn = self.base_ + ".splitlog.csv"
        if not os.path.exists(metadata_fn):
            return False
        f = open(metadata_fn, 'r')
        f.readline()   # Skip header
        for line in f:
            _, core_starts, core_ends, buffer_starts, buffer_ends, filename = line.split(",")
            self.core_boundaries_.append([core_starts, core_ends])
            self.buffered_boundaries_.append([buffer_starts, buffer_ends])
            self.filenames_.append(filename.strip())
        f.close()
        return True

    def num_regions(self):
        return len(self.core_boundaries_)

    def core_boundaries(self, i):
        return self.core_boundaries_[i]

    def buffered_boundaries(self, i):
        return self.buffered_boundaries_[i]
            
    def filename(self, i):
        return self.filenames_[i]