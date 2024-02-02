import glob
import numpy
import argparse

# Set up the command line argument parser
parser = argparse.ArgumentParser(description='Find trigger files in a given directory')
parser.add_argument('--gps-start-time', type=int,
                    help='Start time of the collection of trigger files.')
parser.add_argument('--gps-end-time', type=int,
                    help='End time of the collection of trigger files.')
parser.add_argument('--trigger-file-loc', type=str,
                    help='Directory containing the trigger files.'
                    'Trigger files are expected to be in subdirectories.')
parser.add_argument('--output-file', type=str,
                    help='Name of the output file.')
parser.add_argument('--output-location', type=str,
                    help='Directory to save the output file.')
args = parser.parse_args()

trigger_files = [
    l for l in glob.glob(args.trigger_file_loc + '/*/H1L1-Live-*.hdf', recursive=True)
    if float(l.split('/')[-1][10:27]) > args.gps_start_time and float(l.split('/')[-1][10:27]) < args.gps_end_time
]

numpy.savetxt(args.output_location + args.output_file, trigger_files,
              delimiter=',', fmt='%s')







