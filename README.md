# IBSC_FGH
Using the Fourier Grid Hamiltonian Method to describe the optical properties of Intermediate band solar cells composed of quantum wells.

The algorithm was written using Python3 and presented within the file "IntermediateBandSolarCell.ipynb". It is intended to generate the potential profile of an Intermediate Band Solar Cell, composed of an p-i-n semicondutor junction with a quantum in the intrinsic (i) region. Changing the quantum well's properties we can change the optical response and analyse its dependence in comparison to the solar cell emission spectrum.

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

To define the kinetic energy operator we need a matrix of indexes to be used with the cosine function. Such a matrix depends only on the number of points in the grid and can be reused for several potentials if the grid doesn't change. Two inline nested for loops are used to construct the indexes matrix **MM**.

The inline **Tl** function together with the **hh** function defines the piecewise Kinect operator. The sum over all the cosines is given by the **HH** matrix. As in the case of the index matrix, the **HH** can be reused if the number of points of the grid doesn't change.


*4) Semiconductor properties.*

Since the solar cell is defined by the semiconductors that form it, the next cell defines the properties of the semiconductors. We used the junction of AlGaAs and GaInAs as the hosts, but they can be exchanged to explore other regions of response for the cell. The quantum well itself is comprised of the GaInAs layer, surrounded by the AlGaAs layer. The quantum well height is defined by the bandgap discontinuity amongst the semiconductors. The bandgap of the AgGaAs layer is controlled by the aluminum concentration, defined by the variable **cy**, while the bandgap of the GaInAs is controlled by the indium concentration given by the variable **cx**.

*5) Defining the square well potential.*

The potential profile is defined using the numpy's **argwhere** function. Since the grid is centered around the origin, the absolute value of the quantum well's width is enough to define the whole quantum well. We define the valence and conduction band potential profiles separately by the arrays **VBV** and **VBC**.

    
*6) Defining electric field Stark Effect.*

The doped layers define an intrinsic electric field that bends the intrinsic layer due to the so-called Stark Effect. Such a bend is responsible for the drift dynamics of the carriers. To mimic such an effect we employed a constant electric field and summed its contributions to the potential profile.

*7) Diagonalization.*

After properly defining the potential profile, we add it to the diagonal of the Hamiltonian matrix and perform the diagonalization. Such a procedure is done separately for the valence and conduction bands. Since the valence band has an inverted profile in comparison to the conduction one, the code interprets it as a barrier instead of a quantum well. To solve it we changed its signal and added the quantum well bandgap. After performing the diagonalization we revert the changes.

The diagonalization is done using the linear algebra library of numpy, through the function *linalg.eig*. It returns both the eigenvalues and the eigenvectors.

*8) Evaluating Absorption.*

To evaluate the absorption spectra we employed the Fermi golden rule, taking the scalar product between the valence and conduction band states - as the oscillator strength. We start by creating a matrix with the energy difference between the states **Ev**. Together with the oscillator strength **f** times the Heaviside function the absorption **alpha** is summed over the states.

*9) Black body radiation for Sunlight.*

To compare the absorption spectra of the solar cell, we also evaluated the black-body radiation spectra to simulate the solar irradiance **I**. We use the Fermi-Dirac distribution with a temperature of 5775K.

*10) Plotting results.*

Finally, we plotted all the results, starting with the potential profiles together with the square modulus of the eigenfunctions, shifted according to the eigenergies. After we plotted the absorption and the solar irradiance.
