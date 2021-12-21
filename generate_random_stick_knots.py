from libpl import plcurve, tsmcmc
from libpl.pdcode import plctopology
import numpy as np
import random
import sys
from collections import Counter
import pandas as pd
import pickle
import argparse
from identify_knot import pyknotid_classify, knot_string_to_tuple, knot_tuple_to_string


##################
### PARAMETERS ###
##################

parser = argparse.ArgumentParser()

parser.add_argument('-cr', '--CONFINEMENT_RADIUS', type=float, default=1.01, dest='CONFINEMENT_RADIUS',
                    help="The radius in which to confine the polygons")
parser.add_argument('-ne', '--NUMBER_OF_EDGES', type=int, required=True, dest='NUMBER_OF_EDGES',
                    help="The number of edges of the polygons")
parser.add_argument('-mi', '--MAX_ITERATIONS', type=int, required=True, dest='MAX_ITERATIONS',
                    help="The number of polygons to generate, not including burn-in")
parser.add_argument('-ms', '--MAX_SECONDS', type=int, default=86400, dest='MAX_SECONDS',
                    help="The maximum time in seconds to run, by default one day")
parser.add_argument('-v', '--VERBOSITY', type=int, default=2, dest='VERBOSITY',
                    help="Verbosity level")
parser.add_argument('-csv', '--CSV_OUT', type=str, dest='CSV_OUT',
                    help="The path to output results as csv. If not provided will print to command line")
parser.add_argument('-kc', '--KNOT_COUNTS_OUT', type=str, dest='KNOT_COUNTS_OUT',
                    help="The path to output knot frequency counts as a pickled python object")
parser.add_argument('-rs', '--RANDOM_SEED', type=int, dest='RANDOM_SEED',
                    help="Integer seed for the random number generator")

args = parser.parse_args()

BURN_IN_ITERATIONS = 101 #appears to be default for plCurve

#############
### SETUP ###
#############

rng = plcurve.RandomGenerator()
rp = tsmcmc.RunParameters.default_confined()

if not args.RANDOM_SEED:
    args.RANDOM_SEED = int(random.getrandbits(64))
rng.set(args.RANDOM_SEED)

knot_counter = Counter()
step_counter = Counter() #this has to be a Counter object because of cython weirdness

#to log information about the generated polygons
df = pd.DataFrame(columns=['random_seed', 'is_best', 'knot', 'num_edges', 'confinement_radius', 'string_repr'])

#best-known stick numbers for minimal stick knots
#http://www.colab.sfu.ca/KnotPlot/sticknumbers/
#now updated with results from new paper
stick_numbers = {
(0, 1):[3, 3],
(3, 1):[6, 6],
(4, 1):[7, 7],
(5, 1):[8, 8],
(5, 2):[8, 8],
(6, 1):[8, 8],
(6, 2):[8, 8],
(6, 3):[8, 8],
(7, 1):[9, 9],
(7, 2):[9, 9],
(7, 3):[9, 9],
(7, 4):[9, 9],
(7, 5):[9, 9],
(7, 6):[9, 9],
(7, 7):[9, 9],
(8, 1):[10, 10],
(8, 2):[10, 10],
(8, 3):[10, 10],
(8, 4):[10, 10],
(8, 5):[10, 10],
(8, 6):[10, 10],
(8, 7):[10, 10],
(8, 8):[10, 10],
(8, 9):[10, 10],
(8, 10):[10, 10],
(8, 11):[10, 10],
(8, 12):[10, 10],
(8, 13):[10, 10],
(8, 14):[10, 10],
(8, 15):[10, 10],
(8, 16):[9, 9],
(8, 17):[9, 9],
(8, 18):[9, 9],
(8, 19):[8, 8],
(8, 20):[8, 8],
(8, 21):[9, 9],
(9, 1):[10, 10],
(9, 2):[10, 10],
(9, 3):[10, 10],
(9, 4):[10, 10],
(9, 5):[10, 10],
(9, 6):[11, 11],
(9, 7):[10, 10],
(9, 8):[10, 10],
(9, 9):[10, 10],
(9, 10):[10, 10],
(9, 11):[10, 10],
(9, 12):[10, 10],
(9, 13):[10, 10],
(9, 14):[10, 10],
(9, 15):[10, 10],
(9, 16):[10, 10],
(9, 17):[10, 10],
(9, 18):[10, 10],
(9, 19):[10, 10],
(9, 20):[10, 10],
(9, 21):[10, 10],
(9, 22):[10, 10],
(9, 23):[11, 11],
(9, 24):[10, 10],
(9, 25):[10, 10],
(9, 26):[10, 10],
(9, 27):[10, 10],
(9, 28):[10, 10],
(9, 29):[9, 10],
(9, 30):[10, 10],
(9, 31):[10, 10],
(9, 32):[10, 10],
(9, 33):[10, 10],
(9, 34):[9, 9],
(9, 35):[9, 9],
(9, 36):[11, 11],
(9, 37):[10, 10],
(9, 38):[10, 10],
(9, 39):[9, 9],
(9, 40):[9, 9],
(9, 41):[9, 9],
(9, 42):[9, 9],
(9, 43):[9, 9],
(9, 44):[9, 9],
(9, 45):[9, 9],
(9, 46):[9, 9],
(9, 47):[9, 9],
(9, 48):[9, 9],
(9, 49):[9, 9],
(10, 1):[11, 11],
(10, 2):[11, 11],
(10, 3):[11, 11],
(10, 4):[11, 11],
(10, 5):[11, 11],
(10, 6):[11, 11],
(10, 7):[11, 11],
(10, 8):[10, 10],
(10, 9):[11, 11],
(10, 10):[11, 11],
(10, 11):[11, 11],
(10, 12):[11, 11],
(10, 13):[11, 11],
(10, 14):[11, 11],
(10, 15):[11, 11],
(10, 16):[10, 10],
(10, 17):[10, 10],
(10, 18):[10, 10],
(10, 19):[11, 11],
(10, 20):[11, 11],
(10, 21):[11, 11],
(10, 22):[11, 11],
(10, 23):[11, 11],
(10, 24):[11, 11],
(10, 25):[11, 11],
(10, 26):[11, 11],
(10, 27):[11, 11],
(10, 28):[11, 11],
(10, 29):[11, 11],
(10, 30):[11, 11],
(10, 31):[11, 11],
(10, 32):[11, 11],
(10, 33):[11, 11],
(10, 34):[11, 11],
(10, 35):[11, 11],
(10, 36):[11, 11],
(10, 37):[12, 12],
(10, 38):[11, 11],
(10, 39):[11, 11],
(10, 40):[11, 11],
(10, 41):[11, 11],
(10, 42):[11, 11],
(10, 43):[11, 11],
(10, 44):[11, 11],
(10, 45):[11, 11],
(10, 46):[11, 11],
(10, 47):[11, 11],
(10, 48):[10, 10],
(10, 49):[11, 11],
(10, 50):[11, 11],
(10, 51):[11, 11],
(10, 52):[11, 11],
(10, 53):[11, 11],
(10, 54):[11, 11],
(10, 55):[11, 11],
(10, 56):[10, 10],
(10, 57):[11, 11],
(10, 58):[11, 11],
(10, 59):[11, 11],
(10, 60):[11, 11],
(10, 61):[11, 11],
(10, 62):[11, 11],
(10, 63):[11, 11],
(10, 64):[11, 11],
(10, 65):[11, 11],
(10, 66):[11, 11],
(10, 67):[11, 11],
(10, 68):[10, 10],
(10, 69):[11, 11],
(10, 70):[11, 11],
(10, 71):[11, 11],
(10, 72):[11, 11],
(10, 73):[11, 11],
(10, 74):[11, 11],
(10, 75):[11, 11],
(10, 76):[12, 12],
(10, 77):[11, 11],
(10, 78):[11, 11],
(10, 79):[11, 11],
(10, 80):[11, 11],
(10, 81):[11, 11],
(10, 82):[10, 10],
(10, 83):[11, 11],
(10, 84):[10, 10],
(10, 85):[10, 10],
(10, 86):[11, 11],
(10, 87):[11, 11],
(10, 88):[11, 11],
(10, 89):[11, 11],
(10, 90):[10, 10],
(10, 91):[10, 10],
(10, 92):[11, 11],
(10, 93):[10, 10],
(10, 94):[10, 10],
(10, 95):[11, 11],
(10, 96):[11, 11],
(10, 97):[11, 11],
(10, 98):[11, 11],
(10, 99):[11, 11],
(10, 100):[10, 10],
(10, 101):[11, 11],
(10, 102):[10, 10],
(10, 103):[10, 10],
(10, 104):[10, 10],
(10, 105):[10, 10],
(10, 106):[10, 10],
(10, 107):[10, 10],
(10, 108):[10, 10],
(10, 109):[10, 10],
(10, 110):[10, 10],
(10, 111):[10, 10],
(10, 112):[10, 10],
(10, 113):[10, 10],
(10, 114):[10, 10],
(10, 115):[10, 10],
(10, 116):[10, 10],
(10, 117):[10, 10],
(10, 118):[10, 10],
(10, 119):[10, 10],
(10, 120):[10, 10],
(10, 121):[10, 10],
(10, 122):[10, 10],
(10, 123):[11, 11],
(10, 124):[10, 10],
(10, 125):[10, 10],
(10, 126):[10, 10],
(10, 127):[10, 10],
(10, 128):[10, 10],
(10, 129):[10, 10],
(10, 130):[10, 10],
(10, 131):[10, 10],
(10, 132):[10, 10],
(10, 133):[10, 10],
(10, 134):[10, 10],
(10, 135):[10, 10],
(10, 136):[10, 10],
(10, 137):[10, 10],
(10, 138):[10, 10],
(10, 139):[10, 10],
(10, 140):[10, 10],
(10, 141):[10, 10],
(10, 142):[10, 10],
(10, 143):[10, 10],
(10, 144):[10, 10],
(10, 145):[10, 10],
(10, 146):[10, 10],
(10, 147):[10, 10],
(10, 148):[10, 10],
(10, 149):[10, 10],
(10, 150):[10, 10],
(10, 151):[10, 10],
(10, 152):[10, 10],
(10, 153):[10, 10],
(10, 154):[11, 11],
(10, 155):[10, 10],
(10, 156):[10, 10],
(10, 157):[10, 10],
(10, 158):[10, 10],
(10, 159):[10, 10],
(10, 160):[10, 10],
(10, 161):[10, 10],
(10, 162):[10, 10],
(10, 163):[10, 10],
(10, 164):[10, 10],
(10, 165):[10, 10]
}

#All the knots <= 10 crossings which are known to have non-unique HOMFLYs
#We must double-check any identified as this type through pyknotid
non_unique_homfly_knots = set(
['10_35', '10_129', '10_122', '10_127', '9_36', '9_33', '9_32', '10_96',
'10_32', '10_33', '10_30', '10_31', '10_34', '10_38', '10_39', '9_7', '10_137',
'10_132', '9_20', '9_22', '9_26', '9_27', '9_28', '10_23', '10_22', '10_25',
'9_9', '10_27', '10_29', '10_28', '9_8', '10_103', '10_102', '10_100', '10_107',
'10_106', '10_105', '10_109', '10_108', '9_14', '9_17', '9_16', '9_11', '6_2',
'8_16', '8_14', '9_19', '10_54', '10_56', '10_50', '10_51', '10_52', '8_6',
'8_7', '8_4', '8_5', '10_59', '8_9', '10_89', '10_110', '10_111', '10_112',
'10_114', '10_116', '10_117', '10_119', '8_8', '10_150', '10_49', '10_57',
'10_43', '10_42', '10_41', '10_40', '10_47', '10_46', '10_45', '10_44', '8_2',
'10_162', '5_1', '7_5', '7_1', '7_3', '10_76', '10_75', '10_72', '10_70',
'9_31', '10_69', '10_68', '10_66', '10_60', '10_90', '10_92', '10_93', '10_94',
'10_95', '10_149', '10_141', '10_82', '10_18', '10_19', '10_10', '10_14',
'10_15', '10_16', '9_18', '10_155', '10_156', '10_9', '9_41', '10_2', '10_5',
'10_87', '10_86', '10_85', '10_84', '10_83', '10_81', '10_80', '10_157',
'10_88'])



###############
### METHODS ###
###############

def make_knotplot_polygon_string(poly):
    #should change tabs to newlines before knotplot
    return '\t'.join(map(lambda x: "%s %s %s" % (x[0], x[1], x[2]), poly))


def get_numpy_coordinate_array(plc):
    return np.asarray(plc.components[0].vertices)


def is_best_known_equilateral_stick_number(crossing_number, index, edges):
    prime_knot_tuple = (crossing_number, index)
    if prime_knot_tuple in stick_numbers:
        if stick_numbers[prime_knot_tuple][1] > edges:
            return True #EUREKA!
        elif stick_numbers[prime_knot_tuple][1] == edges:
            return None #Equivalent to best known
        else:
            return False #Worse than best known, not interesting


def integrand(plc):

    step_counter['iteration'] += 1
    num_factors, crossing_num, ind, num_poss = plctopology.plc_classify_knot(rng, plc)

    knot_tuple = None
    used_pyknotid = False
    try:
        knot_tuple = tuple(sorted(zip(crossing_num[:num_factors],ind[:num_factors])))
    except TypeError:
        #Try pyknotid, maybe the knot has more than 10 crossings
        candidates = pyknotid_classify(get_numpy_coordinate_array(plc))
        #if we found a single knot candidate
        if isinstance(candidates, str):
            knot_tuple = knot_string_to_tuple(candidates)
            used_pyknotid = True
        #otherwise
        else:
            #Unable to classify this knot, maybe too singular, maybe multiple candidates
            df.loc[step_counter['iteration']] = [args.RANDOM_SEED, 'UNCL', candidates, args.NUMBER_OF_EDGES, args.CONFINEMENT_RADIUS,
                                             make_knotplot_polygon_string(get_numpy_coordinate_array(plc))]
            knot_counter["Unclassifiable"] += 1
            return 0

    #if knot is prime
    if len(knot_tuple) == 1:
        #Double-check questionable HOMFLYs through pyknotid,
        #unless we've already used pyknotid to identify this knot
        if ('_'.join(map(str, knot_tuple[0])) in non_unique_homfly_knots) and not used_pyknotid:
            candidates = pyknotid_classify(get_numpy_coordinate_array(plc))
            #if we found a single knot candidate
            if isinstance(candidates, str):
                knot_tuple = knot_string_to_tuple(candidates)
            #otherwise
            else:
                #Unable to classify this knot, maybe multiple candidates
                df.loc[step_counter['iteration']] = [args.RANDOM_SEED, 'UNCL', candidates, args.NUMBER_OF_EDGES, args.CONFINEMENT_RADIUS,
                                                 make_knotplot_polygon_string(get_numpy_coordinate_array(plc))]
                knot_counter["Unclassifiable"] += 1
                return 0

        #if it is a prime knot with <=10 crossings we want to compare stick numbers
        is_best = is_best_known_equilateral_stick_number(knot_tuple[0][0], knot_tuple[0][1], args.NUMBER_OF_EDGES)
        if is_best:
            df.loc[step_counter['iteration']] = [args.RANDOM_SEED, 'BEST', knot_tuple, args.NUMBER_OF_EDGES, args.CONFINEMENT_RADIUS,
                                                 make_knotplot_polygon_string(get_numpy_coordinate_array(plc))]

        elif (is_best == None) and (args.VERBOSITY >= 2):
            df.loc[step_counter['iteration']] = [args.RANDOM_SEED, 'EQUIV', knot_tuple, args.NUMBER_OF_EDGES, args.CONFINEMENT_RADIUS,
                                                 make_knotplot_polygon_string(get_numpy_coordinate_array(plc))]

        elif args.VERBOSITY >= 3:
            df.loc[step_counter['iteration']] = [args.RANDOM_SEED, 'WORSE', knot_tuple, args.NUMBER_OF_EDGES, args.CONFINEMENT_RADIUS,
                                                 make_knotplot_polygon_string(get_numpy_coordinate_array(plc))]

    elif (num_factors >= 2) and (args.VERBOSITY >= 3):
        df.loc[step_counter['iteration']] = [args.RANDOM_SEED, 'NONPRIME', knot_tuple, args.NUMBER_OF_EDGES, args.CONFINEMENT_RADIUS,
                                             make_knotplot_polygon_string(get_numpy_coordinate_array(plc))]

    #in any case, we want to record that this knot was seen
    knot_counter[knot_tuple] += 1

    return 0 #return value irrelevant


#########################
### GENERATE POLYGONS ###
#########################

print("PARAMETERS:")
print("\tConfinement radius: %f" % args.CONFINEMENT_RADIUS)
print("\tNumber of edges: %d" % args.NUMBER_OF_EDGES)
print("\tMaximum steps: %d" % args.MAX_ITERATIONS)
print("\tMaximum seconds: %d" % args.MAX_SECONDS)
print("\tRandom seed: %d" % args.RANDOM_SEED)
print

tsmcmc.confined_equilateral_expectation(rng, integrand,
                                        args.CONFINEMENT_RADIUS,
                                        args.NUMBER_OF_EDGES,
                                        args.MAX_ITERATIONS + BURN_IN_ITERATIONS,
                                        args.MAX_SECONDS, rp)


######################
### REPORT RESULTS ###
######################

#write out csv file, if desired
if args.CSV_OUT:
    df.to_csv(args.CSV_OUT, index_label='iteration')
else:
    print("\niteration, random_seed, is_best, knot, num_edges, confinement_radius, string_repr")
    for iteration, data in df.iterrows():
        print(', '.join([str(iteration)] + map(lambda x:str(x), data)))
    print

#write out knot counts, if desired
if args.KNOT_COUNTS_OUT:
    with open(args.KNOT_COUNTS_OUT, 'w') as outfile:
        pickle.dump(knot_counter, outfile)

print("\nKnot Frequency Counts:")
for knot_tuple, count in sorted(knot_counter.items(), key=lambda x: x[1], reverse=True):
    print("%s\t%d" % (knot_tuple_to_string(knot_tuple), count))
