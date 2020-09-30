# Superbridge index data
This folder contains the data referred to in the paper 

* Clayton Shonkwiler. [New Computations of the Superbridge Index](https://arxiv.org/abs/2009.13648). Preprint, 2020. [arXiv:2009.13648 [math.GT]](https://arxiv.org/abs/2009.13648)


## Table of superbridge indices
A table of exact values of the superbridge index—or, when the exact value is not known, the possible values it might be—for each knot with crossing number 10 or less is given in `superbridge_values.csv`. This table reflects the current state of the art and the intent is to keep it up to date.

Ranges of possible values are indicated as intervals. So for example the superbridge index of the 5_2 knot is either 3 or 4, and this is indicated in the table with `[3,4]`. Likewise, the superbridge index of 10_55 is 4, 5, or 6, and this is indicated with `[4,6]`.

## Knot coordinates
The `knots` folder contains vertex coordinates for each of the 33 knots mentioned in the paper. Each set of coordinates is stored in a tab-separated ASCII text file, which can be conveniently read into KnotPlot or easily reformatted for other software.

The coordinates given here are double-precision floats; in the paper it was convenient to round these coordinates to three significant figures and scale them to be integers. Hence, the coordinates given in the paper can be reconstructed using the Python expression `round(1000*coord)` or an analogous operation in any other language.

This same information is also stored in a SQLite database `knots.db` along with some basic metadata. In particular, the following code demonstrates how to extract the vertex coordinates from the database into Python.
```
import sqlite3
conn = sqlite3.connect('superbridge_index/knots.db')
c = conn.cursor()
c.execute("SELECT identifier, vertices FROM knots;")
identifier, vertices_string = c.fetchone()
vertices = eval(vertices_string)
```
