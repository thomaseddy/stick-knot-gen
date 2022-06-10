# Superbridge index data
This folder contains the data referred to in the papers

- Clayton Shonkwiler. [New computations of the superbridge index](https://doi.org/10.1142/S0218216520500960). _Journal of Knot Theory and Its Ramifications_ **29** (2020), no. 14, 2050096. [arXiv:2009.13648 [math.GT]](https://arxiv.org/abs/2009.13648)

- Clayton Shonkwiler. New superbridge index calculations from non-minimal realizations. Preprint, 2022.

As well as results on superbridge index from the papers

- Ryan Blair, Thomas D. Eddy, Nathaniel Morrison, and Clayton Shonkwiler. [Knots with exactly 10 sticks](https://doi.org/10.1142/S021821652050011X). _Journal of Knot Theory and Its Ramifications_ **29** (2020), no. 3, 2050011. [arXiv:1909.06947 [math.GT]](https://arxiv.org/abs/1909.06947)

- Clayton Shonkwiler. [All prime knots through 10 crossings have superbridge index ≤ 5](https://arxiv.org/abs/2112.10902). _Journal of Knot Theory and Its Ramifications_, to appear. [arXiv:2112.10902 [math.GT]](https://arxiv.org/abs/2112.10902).

## Table of superbridge indices
A table of exact values of the superbridge index—or, when the exact value is not known, the possible values it might be—for each knot with crossing number 10 or less is given in `superbridge_values.csv`. This table reflects the current state of the art and the intent is to keep it up to date.

Ranges of possible values are indicated as intervals. So for example the superbridge index of the 5_2 knot is either 3 or 4, and this is indicated in the table with `[3,4]`.

Also, all knots up to 16 crossings for which the exact value of superbridge index is known are given in `exact_values.csv`. For example, to our knowledge the only 16-crossing knot for which the exact superbridge index is known is K16n783154, better known as the (8,3)-torus knot, which has superbridge index equal to 6. Again, the plan is to keep this table current.

## Knot coordinates
The `knots` folder contains vertex coordinates for each of the 33 knots mentioned in the “New computations of the superbridge index” paper and each of the 22 knots mentioned in the “New superbridge index calculations from non-minimal realizations” paper, as well as the 12-stick 10_37 with superbridge number 5 given in Appendix C of the “All prime knots…” paper. Each set of coordinates is stored in a tab-separated ASCII text file, which can be conveniently read into KnotPlot or easily reformatted for other software.

The coordinates given here are double-precision floats; in the papers it was convenient to round these coordinates to three significant figures and scale them to be integers. Hence, the coordinates given in the papers can be reconstructed using the Python expression `round(1000*coord)` or an analogous operation in any other language.

This same information is also stored in a SQLite database `knots.db` along with some basic metadata. In particular, the following code demonstrates how to extract the vertex coordinates from the database into Python.
```
import sqlite3
conn = sqlite3.connect('superbridge_index/knots.db')
c = conn.cursor()
c.execute("SELECT identifier, vertices FROM knots;")
identifier, vertices_string = c.fetchone()
vertices = eval(vertices_string)
```
