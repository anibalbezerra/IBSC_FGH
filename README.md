# IBSC_FGH
Using the Fourier Grid Hamiltonian Method to describe the optical properties of Intermediate band solar cells composed of quantum wells.

The algorithm was written using Python3 and presented within the file "IntermediateBandSolarCell.ipynb". It is intended to generate the potential profile of an Intermediate Band Solar Cell, composed of an p-i-n semicondutor junction with a quantum in the intrinsec (i) region. Changing the quantum well's properties we can change the optical response and analyse its dependence in comparison to the solar cell emission spectrum.

The code is divided into some parts, that are described next.

1) Importing required libraries.
2) Defining the system’s properties.
3) Defining useful functions and matrices.
4) Semiconductor properties.
5) Defining the square well potential.
6) Defining electric field Stark Effect.
7) Diagonalization.
8) Evaluating Absorption.
9) Black body radiation for Sunlight.
10) Plotting results.

**Running the code as it is will produce the graph as in the paper**.

*1) Importing required libraries.*

   The **numpy** library is used for almost all mathematical operations. It is employed to deal with the arrays (Vectors and matrices). To plot the results the **matplotlib** library is used.
   
 *2) Defining the system’s properties.*
 
The properties of the system are defined in the second cell. 
      
**N** is the number of points of the position grid. It also defines the size of the Hamiltonian matrix (N times N). The way it is implemented, it should be an odd number.

**L** defines the size of the p-i-n cell.

**Lqw** defines the quantum well half width. As known from Quantum Mechanics, the larger the well the more states will be within the quantum well. Controlling the quantum well's width allows for increasing or decreasing the number of localized states that will serve as the intermediate band to the solar cell. It also changes the separation between the valence and conduction band states, direct reflecting in the absorption edges.

**elf** and **elfx** are the variables responsible for controlling the simulated built-in electric field due to the heavily doped p and n contacts. **elf** defines the field intensity while **elfx** defines the intrinsic (non-doped) layer size. Changing the doping direct affects the response of the solar cell, it is responsible for drifting electrons and holes from the active region (where the absorption occurs) to the contacts, generating a net current.
      
To evaluate the absorption the energy grid was also discretized and has a total of **Ne** points. The variable **hw** defines the array to store the energy points.

*3) Defining useful functions and matrices.*

The evaluation of the oscillator strength, used with the absorption, requires a Heaviside step function. Such a function is defined inline as **Heaviside**, using the *lambda* syntax. 

To define the kinetic energy operator we need a matrix of indexes to be used with the cosine function. Such a matrix depends only of the number of point in the grid and can be reused for several potentials, if the grid doesn't change. Two inline neested for loops are used to construct the indexes matrix **MM**.

The inline **Tl** function together with the **hh** function define the piecewise kinect operator. The sum over all the cosines is given by the **HH** matrix. As in the case of the index matrix, the **HH** can be resused if the number of points of the grid doesn't change.


*4) Semiconductor properties.*

Since the solar cell is defined by the semiconductors that form it, the next cell defines the semiconductros properties. We used the juntion of AlGaAs and GaInAs as the hosts, but they can be exchanged to explore other regions of response for the cell. The quantum well itself is comprised by the GaInAs layer, surrounded by the AlGaAs layer. The quantum well height is defined by the bad gap discontinuity amongst the semiconductors. The band gap of the AgGaAs layer is controlled by the aluminum concentration, defined by the variable **cy**, while the band gap of the GaInAs is controlled by the indium concentration give by the variable **cx**.

*5) Defining the square well potential.*

The potential profile is defined using the numpy's **argwhere** function. Since the grid is centered around the origin, the absolute value of the quantum well's width is enought to define the whole quantum well. We define the valence and conduction bands potential profiles separately by the arrays **VBV** and **VBC**.


    




