
Gridmap with SMP on Grid Engine
===============================

## Disclaimer

This is in a rough form right now and may be cleaned up over time. PRs welcome
if you find anything wrong with the instructions.

## python environment
  - numpy
  - nomkl
  - gridmap (master branch with pip)
 
## setting up sge parallel environment and queue

- I have updated my [fork](https://github.com/nfoti/StarCluster) of starcluster
  to create an `smp` parallel environment oncluster startup.

#### manual sge setup

- Make a new parallel env: `qconf -ap smp`
  * this will pop up an editor, then you need to:
  * Set the number of slots to the number of cores times the number of instances
  * Make sure that `allocation_rule` is set to `$pe_slots`
- Tell SGE queue to use the new `smp` parallel environment:
  * First, list the queues you have `qconf -sql` and find the one you want to
    associate the `smp` pe with.
  * Run `qconf -mq <queue_name>` which will open an editor
  * add `smp` to the `pe_list` entry

## running

I ran experiments on 2 `c4.2xlarge` instances, each with 8 vCPUs (4 threads).

run the test script like: `python gridmap_smp.py num_jobs num_slots`

`num_jobs` is the number of parallel jobs we need to run
`num_slots` is the number of slots each job takes up

Note the setting of `temp_dir` in the `process_jobs` function. This is
necessary, `gridmap` will silently freeze if you don't have write access to the
directory specified here (`/scratch` by default).

OpenBLAS will parallelize over all threads (inluding hyperthreads) by default,
so also try the following:

`OMP_NUM_THREADS=4; python gridmap_smp.py 8 4`

On the `c4.2xlarge` instances I specified this will run 4 jobs at a time, each using 4 threads.

Alternatively, `OMP_NUM_THREADS=4; python gridmap_smp.py 8 8`
will again run 8 jobs, but only 2 will run at a time (one per instance)
because each grabs 8 slots but each will only use 4 threads.
