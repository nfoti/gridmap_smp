from __future__ import print_function

import numpy as np
import os.path as op

from gridmap import Job, process_jobs


def worker(n):
	X = np.random.randn(n, n)
	np.linalg.svd(X)
	return n


def main(njobs, nslots):
	
	jobs = [Job(worker, [2500], num_slots=nslots, par_env='smp') for _ in range(njobs)]
	process_jobs(jobs, temp_dir=op.expanduser("~/gridmap_scratch"))


if __name__ == '__main__':
	import sys
	njobs = int(sys.argv[1])
	nslots = int(sys.argv[2])
	main(njobs, nslots)
