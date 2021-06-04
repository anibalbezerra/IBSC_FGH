# IBSC_FGH
Using the Fourier Grid Hamiltonian Method to describe the optical properties of Intermediate band solar cells composed of quantum wells.

The algorithm was written using Python3 and presented within the file "IntermediateBandSolarCell.ipynb". It is intended to generate the potential profile of an Intermediate Band Solar Cell, composed of an p-i-n semicondutor junction with a quantum in the intrinsec (i) region. Changing the quantum well's properties we can change the optical response and analyse its dependence in comparison to the solar cell emission spectrum.

The code is divided in some parts, that are discribed next.

1) Importing required libraries.
2) Defining system’s properties.
3) Defining useful functions and matrices.
4) Semiconductor properties.
5) Defining the square well potential.
6) Defining electric field Stark Effect.
7) Diagonalization.
8) Evaluating Absorption.
9) Black body radiation for Sunlight.
10) Ploting results.

**Running the code as ot is will produce the graph as in the paper**.

*1) Importing required libraries.*

   The **numpy** library is used to almost all mathematical operations. It is employed to deal with the arrays (Vectors and matrices). To plot the results the **matplotlib** library is used.
   
 *2) Defining system’s properties.*
 
The properties of the system are defined in the second cell. 
      
**N** is the number of points of the position grid. It also defines the size of the Hamiltonian matrix (N times N). The way it is implemented, it should be an odd number.

**L** defines the size of the p-i-n cell.

**Lqw** defines the quantum well width. As known from Quantum Mechanics, the larger the well the more states will be within the quantum well. Controling the quantum well's width allow for increasing or decrasing the number os localized states that will seve as intermediate band to the solar cell. It also changes the separation between the valence and conduction band states, direct reflecting in the absorption edges.

**elf** and **elfx** are the variables responsible for controlling the simulated built-in electric field due to the heavily doped p an n contacts. **elf** defines the filed intensity while **elfx** defines the intrinsic (non-doped) layer size. Changing the doping direct affects the solar cells response, it is responsible to driftting electron and hole from the acitive region (where the absorption occurs) to the contacts, generating a net current.
      
    
    




