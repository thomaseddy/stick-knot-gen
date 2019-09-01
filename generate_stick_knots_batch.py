import subprocess
import os
import random
import argparse


parser = argparse.ArgumentParser()

parser.add_argument('-cr', '--CONFINEMENT_RADIUS', type=float, default=1.01, dest='CONFINEMENT_RADIUS',
                    help="The radius in which to confine the polygons")
parser.add_argument('-ne', '--NUMBER_OF_EDGES', type=int, required=True, dest='NUMBER_OF_EDGES',
                    help="The number of edges of the polygons")
parser.add_argument('-t', '--TOTAL_TO_GENERATE', type=int, required=True, dest='TOTAL_TO_GENERATE',
                    help="The number of polygons to generate")
parser.add_argument('-b', '--BATCH_SIZE', type=int, default=1000000, dest='BATCH_SIZE',
                    help="The number to generate in each batch")
parser.add_argument('-s', '--BATCH_MAX_SECONDS', type=int, default=86400, dest='BATCH_MAX_SECONDS',
                    help="The maximum time in seconds to run each batch, by default one day")
parser.add_argument('-v', '--VERBOSITY', type=int, default=2, dest='VERBOSITY',
                    help="Verbosity level")
parser.add_argument('-c', '--CSV_DIRECTORY', type=str, dest='CSV_DIRECTORY',
                    help="The directory to output csv results")
parser.add_argument('-k', '--KNOT_COUNTS_DIRECTORY', type=str, dest='KNOT_COUNTS_DIRECTORY',
                    help="The directory to output knot frequency counts as pickled python objects")
parser.add_argument('-p', '--MAX_PROCESSES', type=int, default=4, dest='MAX_PROCESSES',
                    help="Maximum number of concurrent processes")

args = parser.parse_args()

if args.TOTAL_TO_GENERATE < args.BATCH_SIZE:
    args.BATCH_SIZE = args.TOTAL_TO_GENERATE

###################################
### RUN GENERATION SUBPROCESSES ###
###################################

processes = set()
DEVNULL = open(os.devnull, 'wb')

#generate a random seed for each batch
for random_seed in [int(random.getrandbits(64)) for i in range(args.TOTAL_TO_GENERATE / args.BATCH_SIZE)]:
    command = ['python', 'generate_random_stick_knots.py']
    command += ['-cr', str(args.CONFINEMENT_RADIUS)]
    command += ['-ne', str(args.NUMBER_OF_EDGES)]
    command += ['-mi', str(args.BATCH_SIZE)]
    command += ['-ms', str(args.BATCH_MAX_SECONDS)]
    command += ['-v', str(args.VERBOSITY)]
    command += ['-rs', str(random_seed)]
    command += ['-csv', str(args.CSV_DIRECTORY + '/' + '%d_%d.csv' % (args.NUMBER_OF_EDGES, random_seed))]
    command += ['-kc', str(args.KNOT_COUNTS_DIRECTORY + '/' + '%d_%d.pkl' % (args.NUMBER_OF_EDGES, random_seed))]

    print("Running command: \"%s\"" % ' '.join(command))

    processes.add(subprocess.Popen(command, stdout=DEVNULL, stderr=subprocess.STDOUT))
    if len(processes) >= args.MAX_PROCESSES:
        os.wait() #wait for a child process to complete, then remove non running processes
        processes.difference_update([
            p for p in processes if p.poll() is not None])

#Check if all the child processes were closed
for p in processes:
    if p.poll() is None:
        p.wait()

print("\nAll subprocesses complete! Polygons generated.")
