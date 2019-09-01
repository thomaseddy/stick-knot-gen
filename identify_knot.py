from pyknotid.catalogue.getdb import find_database, download_database
from pyknotid.representations.dtnotation import DTNotation
from pyknotid.catalogue.identify import from_invariants
from pyknotid.spacecurves import Knot
import subprocess
import os
import sys
import numpy as np
from contextlib import contextmanager
from libpl import plcurve
from libpl.pdcode import plctopology
import random
import sympy as sym
import argparse

#get the pyknotid knot database if not already available
try:
    find_database()
except IOError:
    download_database()


def knot_tuple_to_string(knot_tuple):
    out_string = []
    if knot_tuple == None:
        return None
    for component in sorted(knot_tuple):
        if len(component) == 2:
            #component of the form "5_2"
            out_string.append('_'.join(map(str,component)))
        elif len(component) == 3:
            #component of the form "K11n169"
            out_string.append('K' + ''.join(map(str,component)))
        else:
            #badly formatted knot tuple
            return None
    #
    return ' # '.join(out_string)


def knot_string_to_tuple(knot_string):
    out_tuple = []
    if knot_string == None:
        return None
    if isinstance(knot_string, list):
        return None
    for component in knot_string.split(" # "):
        if component.startswith("K"):
            #>=11 crossings
            if "a" in component:
                #alternating
                crossings, index = map(int, component.lstrip("K").split("a"))
                out_tuple.append((crossings, "a", index))
            elif "n" in component:
                #non-alternating
                crossings, index = map(int, component.lstrip("K").split("n"))
                out_tuple.append((crossings, "n", index))
            else:
                #badly formatted knot string
                return None
        else:
            #component of the form "5_2"
            try:
                out_tuple.append(tuple(map(int, component.split("_"))))
            except ValueError:
                return None
    #
    return tuple(sorted(out_tuple))


@contextmanager
def silence_stdout():
    new_target = open(os.devnull, "w")
    old_target, sys.stdout = sys.stdout, new_target
    try:
        yield new_target
    finally:
        sys.stdout = old_target


@contextmanager
def silence_stderr():
    new_target = open(os.devnull, "w")
    old_target, sys.stderr = sys.stderr, new_target
    try:
        yield new_target
    finally:
        sys.stderr = old_target


def write_vertices_tsv(vertices, f_obj):
    f_obj.seek(0)
    f_obj.truncate()
    f_obj.writelines(map(lambda v: '\t'.join(map(str, v)) + '\n', vertices))
    f_obj.flush()


def get_vertices_from_file(file_path, sep=' '):
    #filepath in KnotPlot vertex format
    lines = []
    with open(file_path, 'r') as fin:
        lines = fin.readlines()
    return map(lambda x: tuple(map(float, x.rstrip().split(sep))), lines)


def get_homfly_plcurve(vertices, random_seed=None):
    #takes list of 3-tuples which represent vertices
    plc = plcurve.PlCurve()
    plc.add_component(vertices)

    rng = plcurve.RandomGenerator()
    if not random_seed:
        random_seed = int(random.getrandbits(64))
    rng.set(random_seed)

    homfly_string = plctopology.plc_knot_homfly(rng, plc)

    if homfly_string == None:
        return None

    homfly_string = homfly_string.replace('^','**').replace('{','(').replace('}',')')
    homfly_string = homfly_string.replace(')a',')*a').replace(')z',')*z')
    for var_char in ['a','z']:
        for num_char in map(str, range(0,10)):
            homfly_string = homfly_string.replace('%s%s' % (num_char, var_char),
                                                  '%s*%s' % (num_char, var_char))

    z = sym.var('z')
    a = sym.var('a')
    homfly = eval(homfly_string)
    if isinstance(homfly, int):
        #this should only happen when homfly = 1 (i.e. the knot is trivial)
        return homfly
    else:
        return homfly.subs(a,a*sym.I).subs(z,z*sym.I)


def pyknotid_classify(vertices):
    id_list = []
    identify_kwargs = {}
    knot = None

    #annoyingly, pyknotid stuff prints to command line excessively
    with silence_stdout():
        knot = Knot(np.array(vertices))
        sym_homfly = get_homfly_plcurve(vertices)
        if sym_homfly is not None:
            identify_kwargs['homfly'] = sym_homfly
        else:
            #if HOMFLY fails, we can try some roots of the alexander poly
            for root in (2,3,4):
                identify_kwargs['alex_imag_{}'.format(root)] = knot.alexander_at_root(root)
        identify_kwargs['v2'] = knot.vassiliev_degree_2()
        identify_kwargs['v3'] = knot.vassiliev_degree_3()
        if len(knot.gauss_code()) < 16:
            identify_kwargs['max_crossings'] = len(knot.gauss_code())
        hyp_vol, sig_figs, note = knot.hyperbolic_volume()
        #sometimes very small values come back, which should be assumed to be zero
        #the smallest conjectured knot hyperbolic volume is around 2
        if hyp_vol < 0.1:
            #not hyperbolic
            identify_kwargs['hyperbolic_volume'] = 'Not hyperbolic'
        elif note == 'contains degenerate tetrahedra':
            #may be a bad result, let's not inlcude this in our check
            pass
        else:
            #pyknotid wants hyperbolic volume as a text string with
            #a maximum of 6 digits
            volume_string = '%.6g' % hyp_vol
            if "." not in volume_string:
                #if the above formatting rounds to a whole number, it will not
                #include the decimal point which is required for the naive
                #string compare that pyknotid does. For example, see 9_27
                volume_string += "."
            identify_kwargs['hyperbolic_volume'] = volume_string

        #pyknotid defaults to only searching prime knots
        id_list = from_invariants(**identify_kwargs)

        if len(id_list) == 1:
            #Great! We've got an identification
            return str(id_list[0].identifier)

        elif ( (len(id_list) == 0) and
               (identify_kwargs['hyperbolic_volume'] == 'Not hyperbolic') ):
            #If it's not hyperbolic, maybe the knot is composite, let's check.
            #pyknotid support for composite knots isn't great however
            identify_kwargs['composite'] = True
            composite_check = from_invariants(**identify_kwargs)
            if len(composite_check) == 1:
                #Great! We've got a composite identification
                return str(composite_check[0].identifier).replace("#"," # ")
        else:
            #Otherwise, return list of candidates
            return map(lambda x:str(x.identifier), id_list)


def plcurve_classify(vertices, random_seed=None):
    #takes list of 3-tuples which represent vertices
    plc = plcurve.PlCurve()
    plc.add_component(vertices)

    rng = plcurve.RandomGenerator()
    if not random_seed:
        random_seed = int(random.getrandbits(64))
    rng.set(random_seed)

    num_factors, crossing_num, ind, num_poss = plctopology.plc_classify_knot(rng, plc)

    knot_tuple = None
    try:
        knot_tuple = tuple(sorted(zip(crossing_num[:num_factors],ind[:num_factors])))
    except TypeError:
        #plc_classify_knot did not classify this knot
        return None

    return knot_tuple_to_string(knot_tuple)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-kf', '--KNOT_FILE', type=str, required=True, dest='KNOT_FILE',
                        help="Path to KnotPlot formatted knot file")

    args = parser.parse_args()

    print(pyknotid_classify(get_vertices_from_file(args.KNOT_FILE, sep='\t')))
