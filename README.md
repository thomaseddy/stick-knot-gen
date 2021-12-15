# stick-knot-gen
Welcome to **stick-knot-gen**, a collection of scripts which efficiently generate and classify random stick knots in confinement. This code was developed by Thomas Eddy in collaboration with Clayton Shonkwiler for use in improving upper bounds of the stick number knot invariant. That work is summarized and used in the following texts:
- Thomas D. Eddy. [Improved Stick Number Upper Bounds](https://mountainscholar.org/handle/10217/195411). Master’s thesis, Colorado State University, 2019.
- Thomas D. Eddy and Clayton Shonkwiler. [New stick number bounds from random sampling of confined polygons](https://doi.org/10.1080/10586458.2021.1926000). _Experimental Mathematics_ (2021), DOI: 10.1080/10586458.2021.1926000. [arXiv:1909.00917 [math.GT]](https://arxiv.org/abs/1909.00917)
- Ryan Blair, Thomas D. Eddy, Nathaniel Morrison, and Clayton Shonkwiler. [Knots with exactly 10 sticks](https://doi.org/10.1142/S021821652050011X). _Journal of Knot Theory and Its Ramifications_ **29** (2020), no. 3, 2050011. [arXiv:1909.06947 [math.GT]](https://arxiv.org/abs/1909.06947)
- Clayton Shonkwiler. [New computations of the superbridge index](https://doi.org/10.1142/S0218216520500960). _Journal of Knot Theory and Its Ramifications_ **29** (2020), no. 14, 2050096. [arXiv:2009.13648 [math.GT]](https://arxiv.org/abs/2009.13648)
- Clayton Shonkwiler. All prime knots through 10 crossings have superbridge index ≤ 5. Preprint, 2021.

This repository contains supplementary data referenced in the above works as well as the code used to generate the stated results. For an explanation of what is contained in the `stick_number/` and `superbridge_index/` directories, please see the enclosed README files. A table giving the current best stick number upper bounds for all knots with crossing number 10 or fewer is given in [`stick_number/stick_number_upper_bounds.csv`](stick_number/stick_number_upper_bounds.csv), and a current table of superbridge indices for knots up to 10 crossings is in [`superbridge_index/superbridge_values.csv`](superbridge/superbridge_values.csv).

## Basic usage

### Generate and classify stick knots
To generate stick knots, simply invoke `generate_random_stick_knots.py`. This script generates a specified number of random equilateral unit-edge stick knots, classifies their knot type, and writes out the results. The user is able to specify a rooted confinement radius which restricts the space in which the knots may form. An example usage is:
```
$ python generate_random_stick_knots.py -cr 1.01 -ne 10 -mi 100000 -csv blah.csv -kc blah.pkl -rs 1003189127625852959 -v 2
PARAMETERS:
	Confinement radius: 1.010000
	Number of edges: 10
	Maximum steps: 100000
	Maximum seconds: 86400
	Random seed: 1003189127625852959


Knot Frequency Counts:
0_1	93106
3_1	5893
4_1	679
5_2	162
5_1	103
6_2	17
6_1	14
6_3	10
3_1 # 3_1	5
8_20	4
8_21	2
8_19	2
7_6	1
7_4	1
8_7	1
```
The above command generates 100000 stick knots (`-mi` flag), each with 10 edges (`-ne` flag), in a tight confinement radius of 1.01 (`-cr` flag).

The results are written out to a csv file, `blah.csv`, which contains information on individual knots that were generated, including vertex coordinates. At the present verbosity (the `-v` flag), the only knots which are recorded in the csv file are those where the number of edges (specified by the `-ne` flag) are less than or equal to the best-known stick number upper bound for that knot. In this case, the only knot written to the csv file is the 8_7 knot. To record every knot, use verbosity `-v 3`.

The knot frequency counts are also recorded and written out as a pickled dictionary object in the location specified by the `-kc` flag. A summary of the frequency counts are printed to the command line, as above.

The `-rs`flag allows the user to specified a random seed, for reproducibility.

### Batch generation
To generate larger numbers of stick knots, it is useful to do so in batches. The script `generate_stick_knots_batch.py` implements this functionality, including some basic parallelism. Example usage:
```
$ python generate_stick_knots_batch.py -cr 1.01 -ne 10 -t 1000000 -b 100000 -c 10stick_knots_csv/ -k 10stick_knots_pkl/ -p 4
```
This command generates a total (`-t` flag) of one million 10-stick knots in batches of 100000 (`-b` flag). The flags for confinement radius and number of edges are the same as described above.

This script also generates csv and pickled dictionary files, as described above, but in this case generating one file for each batch. The command takes directory arguments `-c` and `-k` where all csv and knot frequency counts, respectively, will be written.

The `-p` flag allows the user to specify the maximum number of concurrent processes. Each process will run one batch at a time.

### Identify knot type
These scripts use the `pyknotid` module to classify stick knots by their type. The `identify_knot.py` script can be used to identify text files representing stick knots whose vertices are specified as tab separated values (the format commonly accepted by KnotPlot). All the stick knots in `data/mseq_knots/` are in this format. To identify the knot type, simply point to the file:
```
$ python identify_knot.py -kf stick_number/mseq_knots/K14n17306.txt
K14n17306
```
The command will print the identifier of the knot, as above. If `pyknotid` cannot make a definitive determination, then this command will return as list of identifiers, as below:
```
$ python identify_knot.py -kf stick_number/mseq_knots/K11n34.txt
['K11n34', 'K11n42']
```
Identifications are determined primarily based on HOMFLY-PT polynomial and hyperbolic volume. Consequently, mutant knot pairs will require additional invariants to make a definitive determination.

The `identify_knot.py` file also contains handy functions which can be imported into the python interpreter or used in custom scripts.

## Dependencies
All code in this repository should be run using Python 2.7. Running the code depends on installing:
- [plCurve](http://www.jasoncantarella.com/wordpress/software/plcurve/) version at least 8.0.6. Installing this software requires building from source so makes sure you have the appropriate command line tools like `autoconf`, etc.
- [pyknotid](https://github.com/spocknots/pyknotid). Should be as easy as `pip install pyknotid`.
- The scripts also require the common python libraries: `numpy`, `pandas`, and `sympy`. Each should be able to be installed using `pip`.

## How to cite
If you find this project useful, please consider citing the project itself and/or the paper explaining what it does:

Thomas D. Eddy. stick-knot-gen, efficiently generate and classify random stick knots in confinement. [https://github.com/thomaseddy/stick-knot-gen](https://github.com/thomaseddy/stick-knot-gen)

Thomas D. Eddy and Clayton Shonkwiler. New stick number bounds from random sampling of confined polygons. _Experimental Mathematics_ (2021), DOI: 10.1080/10586458.2021.1926000.
