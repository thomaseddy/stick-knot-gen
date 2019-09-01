# Supplementary data
This folder contains the supplementary data referred to in the paper [New Stick Number Bounds from Random Sampling of Confined Polygons](https://arxiv.org/).

Of primary interest are minimal equilateral (unit length edges) stick coordinates for each of the 2415 different knot types we observed while generating the data for the paper. Also included are frequency counts of how many times each knot type was observed while randomly generating stick knots with various numbers of edges and at various confinements.

## Minimal stick equilateral knots
The `mseq_knots` folder contains minimal stick vertex coordinates for every knot type we observed while working on the paper. Importantly, this folder contains minimal stick knots for every knot with 10 crossings or fewer, representing the current best-known minimal stick representations of these knots. Each set of coordinates is stored as tab separated ASCII text files, which can be conveniently read into KnotPlot or easily reformatted for other software.

For further convenience, this same information is stored is a SQLite database `mseq_knots.db` along with some basic metadata. In particular, the following code demonstrates how easily it is to extract the vertex coordinates from the database into Python.
```
import sqlite3
conn = sqlite3.connect('data/mseq_knots.db')
c = conn.cursor()
c.execute("SELECT identifier, vertices FROM mseq_knots;")
identifier, vertices_string = c.fetchone()
vertices = eval(vertices_string)
```

## Knot frequency counts
Over the course of this project we randomly generated and classified 220 billion stick knots. We generated 70 billion knots each for 9-, 10-, and 11-stick knots. For each of these 70 billion: 50 billion were generated at a confinement radius of 1.01; 10 billion at confinement 1.1; and 10 billion at confinement 1.5. Additionally, we generated 10 billion 12-stick knots, all at a confinement radius of 1.01.

The distribution of knot types for these generated knots may be of interest to some users. The `frequency_counts` folder includes four tables containing this information. Each table gives the count of stick knots identified to be of a particular type, broken down by confinement radius. The method of generation and identification are described in the paper referenced above.

### Caveats
We believe that the knot identifications presented in this supplementary data are quite accurate on the whole. Each of the 2415 minimal stick knots in the `mseq_knots` folder has been double-checked through an alternative identification pipeline, verifying the identified label in each case.

For the frequency counts, however, there is some uncertainty on the labels due to the limitations of our identification effort. All identifications were done through a combination of the classification functions of plCurve and pyknotid. There is a particular blind spot when it comes to knots with crossing number 16 or higher. Neither of these tools was able to identify knots with more than 15 crossings. In fact, if the HOMFLY-PT polynomial uniquely matched one knot in this set of smaller (<=15) crossing knots, it would have been labeled as such. As seen in the data, we were able to identify some 16-crossing knots through post-processing with Mathematica, but it is possible that some other 16-crossing knots slipped through the cracks and were mislabeled in the tables. Based on the frequency of 15-crossing knots, whose labels are definitive, we believe that the number of mislabeled 16-crossing knots could only possibly be a handful of the billions of knots we generated.

#### Rows with asterisks
One of the rows in the 9-stick table is labeled with an asterisk; three of the rows in the 10-stick table are; 18 rows are asterisked in the 11-stick table; and 33 rows have asterisks in the 12-crossing table.

This labeling is to denote potential identification errors in these rows due to a programming bug which was discovered after the fact. We believe that the large majority of knots counted in these rows are accurate, however, it is possible that some other knot types were lumped into the asterisked rows. Specifically:
- Some asterisked knots counted as 6_2 might actually have been K12n25
- Some asterisked knots counted as 7_1 might actually have been K12n749
- Some asterisked knots counted as 7_3 might actually have been K12n523
- Some asterisked knots counted as 8_2 might actually have been K12n340
- Some asterisked knots counted as 8_4 might actually have been K13n2067
- Some asterisked knots counted as 8_5 might actually have been K13n789
- Some asterisked knots counted as 8_8 might actually have been 10_129 or K13n1836 or K15n42042
- Some asterisked knots counted as 8_14 might actually have been K15n51379
- Some asterisked knots counted as 9_7 might actually have been K15n142497
- Some asterisked knots counted as 9_11 might actually have been K13n3125
- Some asterisked knots counted as 9_14 might actually have been K14n15687
- Some asterisked knots counted as 9_19 might actually have been K13n2328
- Some asterisked knots counted as 9_20 might actually have been K14n7097 or K14n17441
- Some asterisked knots counted as 9_28 might actually have been K13n1698
- Some asterisked knots counted as 9_31 might actually have been K13n1855
- Some asterisked knots counted as 10_2 might actually have been K14n23999
- Some asterisked knots counted as 10_9 might actually have been K15n22039
- Some asterisked knots counted as 10_18 might actually have been K12n561 or K13n2625
- Some asterisked knots counted as 10_23 might actually have been K12n607 or K15n78892
- Some asterisked knots counted as 10_32 might actually have been K13n3568
- Some asterisked knots counted as 10_50 might actually have been K15n80251
- Some asterisked knots counted as 10_59 might actually have been K14n11989 or K15n40303
- Some asterisked knots counted as 10_85 might actually have been K14n18136 or K15n54491 or K15n76296
- Some asterisked knots counted as 10_86 might actually have been 10_83 or K12n317 or K12n511 or K12n588 or K15n49256 or K15n79945
- Some asterisked knots counted as 10_95 might actually have been K12n595 or K15n88440
- Some asterisked knots counted as 10_96 might actually have been K14n8289
- Some asterisked knots counted as 10_107 might actually have been K14n10911
- Some asterisked knots counted as 10_112 might actually have been K15n86484 or K15n137516
- Some asterisked knots counted as 10_119 might actually have been K15n45480 or K15n54332
- Some asterisked knots counted as 10_122 might actually have been K15n43312
- Some asterisked knots counted as 10_141 might actually have been K12n438
- Some asterisked knots counted as 10_155 might actually have been K11n37
- Some asterisked knots counted as 10_162 might actually have been K14n9408 or K15n73961

As can be seen above, the knots which were potentially mislabeled should occur randomly with far less frequency (since they have higher crossing number) than the knots they may have been labeled as. However, some cases, especially a confusion between 8_8 and 10_129, likely were a problem.

To clarify, any rows which do not have an asterisk can be considered fully accurate and any that do have an asterisk could only have been miscounted in the manner listed above.  
