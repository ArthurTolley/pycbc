import glob
import numpy
import h5py
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--stat', type=str, required=True)
parser.add_argument('--no-inj-search-dir', type=str, required=True)
parser.add_argument('--with-inj-search-dir', type=str, required=True)
parser.add_argument('--output-location', type=str, required=True)
parser.add_argument('--joint-time-file', type=str, required=False)
args = parser.parse_args()

no_inj_search_dir = args.no_inj_search_dir
with_inj_search_dir = args.with_inj_search_dir

if args.joint_time_file:
    joint_time_file = args.joint_time_file
    joint_time = set(numpy.loadtxt(joint_time_file))

    no_injs = [
    l for l in glob.glob(f'{no_inj_search_dir}/2020_01_*/H1L1-Live-126*.hdf', recursive=True)
    if float(l.split('/')[-1][10:20]) in joint_time
    ]

    with_injs = [
        l for l in glob.glob(f'{with_inj_search_dir}/2020_01_*/H1L1-Live-126*.hdf', recursive=True)
        if float(l.split('/')[-1][10:20]) in joint_time
    ]

    numpy.savetxt(f'{args.output_location}/{args.stat}_no_injs.txt', no_injs, delimiter=',', fmt='%s')
    numpy.savetxt(f'{args.output_location}/{args.stat}_with_injs.txt', with_injs, delimiter=',', fmt='%s')

else:
    # To prevent end of week 1 injections from being seen, re-position week 2 start
    week2_start=1262995020 + 120
    week2_end=1263600000

    no_injs = [
        l for l in glob.glob(f'{no_inj_search_dir}/2020_01_*/H1L1-Live-126*.hdf', recursive=True)
        if float(l.split('/')[-1][10:20]) > week2_start and float(l.split('/')[-1][10:20]) < week2_end
    ]

    with_injs = [
        l for l in glob.glob(f'{with_inj_search_dir}/2020_01_*/H1L1-Live-126*.hdf', recursive=True)
        if float(l.split('/')[-1][10:20]) > week2_start and float(l.split('/')[-1][10:20]) < week2_end
    ]

    numpy.savetxt(f'{args.output_location}/{args.stat}_no_injs.txt', no_injs, delimiter=',', fmt='%s')
    numpy.savetxt(f'{args.output_location}/{args.stat}_with_injs.txt', with_injs, delimiter=',', fmt='%s')