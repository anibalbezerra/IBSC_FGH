from numba import njit
from numpy import linspace, sign, genfromtxt, zeros, argwhere, eye, dot, exp, pi, arange, cos, reshape, array,where
from numpy.linalg import eig

@njit
def heaviside_calc(t):
    return 0.5 * (sign(t) + 1)
    
@njit    
def absorption(Nv, N, Ne, EBC, EBV, eigBV, eigBC, hw):
    """Evaluating Absorption
    It may take some time to perform the absorption calculation
    """
    HS = [ ]
    
    for e in range(Ne):
        aux = 0
        for i in range(N):
            for j in range(Nv):
                Ev = EBC[i] - EBV[j]
                f = dot(eigBV[:,j], eigBC[:,i])**2
                
                aux += heaviside_calc(hw[e] - Ev)*f / hw[e]
            
            
        HS.append(aux)

    return HS; # Double sum over BV and BC states
    
def massa_efetiva(cx):
    return 0.023 + 0.037 * cx + 0.003 * cx**2


def gap_bar(cy):
    if cy < 0.45:
        gap_bar = 1.424 + 1.247 * cy
    else: 
        gap_bar = 1.9 + 0.125 * cy + 0.143 * cy**2
        
    return gap_bar


def GaInAs_AlGaAs(cx, cy, m):
    """Concentration - dependent 
    Ga(cx)In(1-cx)As / Al(cy)Ga(1-cy)As properties
    """
    
    Ry = 0.381 / m 
    dEgg = 1.247 * cy + 1.5 * (1 - cx ) - 0.41*(1 - cx )**2
    if cy >= 0.45:
        dEg = 0.476 + 0.125* cy + 0.143* cy**2 + 1.5*(1 - cx ) - 0.4*(1 - cx )**2
        Eg_AlGaAs = (1.9 + 0.125* cy + 0.143 * cy**2) * 1e3
    else:
        dEg = dEgg
        Eg_AlGaAs = (1.424 + 1.247 * cy ) * 1e3

    BVOff_set = 0.44 * dEgg * 1e3 / Ry                    # BV band offset
    BCOff_set = (dEg * 1e3 - BVOff_set) / Ry              # BC band offset
    Eg_GaInAs = (0.36 + 0.63* cx + 0.43 * cx**2) * 1e3    # Band Gap
    Eg = Eg_GaInAs / Ry                                   # Admensional band gap

    return BVOff_set, BCOff_set, Eg


def blackBody(T, Ne):
    """Black body radiation for Sunlight
    Inputs:
    T --> Black body temperature (K)
    """
    h = 6.626e-34                                           # Constante de Planck [ h ] = Js
    c = 3e8                                                 # Velocidade da Luz [ c ] = m / s
    K = 1.38e-23                                            # Constante de Boltzmann [ kb ] = J / K
    hwBlack = linspace(1e-5, 4, Ne) * 1.60218e-19     # J
    w = hwBlack / h
    hwnm = w * 1e-12 * 0.00414
    I = 2 * pi * w**3 / (exp(hwBlack / (K * T)) - 1) / (c**2); # Irradiance
    
    return (I * 1.60218e-19 / 100**4), hwnm

def potential(BV, BC, Eg, N, x, m, elf, Elfx, LQW):
    """Defines the square well potential
       Defaut --> True - Uses the GaInAs_AlGaAs properties as parameters
    """ 
    Ry = 0.381 / m 
    elfx = Elfx / 100
    Lqw = LQW / 100
    
    VBV = zeros(N) - (Eg + BV);
    VBV[argwhere(abs(x) < Lqw)] = -Eg ;        # BV

    VBC = zeros(N) + BC;
    VBC[argwhere(abs(x) < Lqw)]  = 0;          # BC
      
    # Defining electric field Stark Effect
    elfvec = zeros(N);
    ind = argwhere(abs(x) < elfx)                       # indexes
    elfvec[ind] = (x[ind] + x[ind[-1]]) * elf / 2;
    elfvec[ind[-1][0]:] = x[ind[-1][0]] * elf ;
    VBV = VBV + elfvec ;                                # Add to BV
    VBC = VBC + elfvec ;                                # Add to BC
        
    return VBV, VBC

def bulk(BV, BC, Eg, N, x, m, elf, Elfx, LQW):
    Ry = 0.381 / m 
    elfx = Elfx / 100
    Lqw = LQW / 100
    
    VBV = zeros(N) - (Eg + BV);
    
    VBC = zeros(N) + BC;
          
    # Defining electric field Stark Effect
    elfvec = zeros(N);
    ind = argwhere(abs(x) < elfx)                       # indexes
    elfvec[ind] = (x[ind] + x[ind[-1]]) * elf / 2;
    elfvec[ind[-1][0]:] = x[ind[-1][0]] * elf ;
    VBV = VBV + elfvec ;                                # Add to BV
    VBC = VBC + elfvec ;                                # Add to BC
        
    return VBV, VBC

def HH(s, N, dx):
    MM = reshape([(i-j) for i in range(N) for j in range(N)], (N, N))
    Tl = lambda l: (2 * pi * l / dx / N)**2
    hh = lambda nv: (2 / N) * cos(nv * 2*pi * MM / N) * Tl(nv);
    
    return sum([hh(i) for i in range(int(s + 1))]); # Operator


def diagonalize(VBV, VBC, Eg, N, m, HH):
    """Sums the potential to the Hamiltonian and performs the diagonalization"""     
    
    Ry = 0.381 / m
    
    VBV_calc = -(VBV + Eg);                           # Re - leveling BV for calculation purposes
    HBV = (HH + VBV_calc * eye(N, N)) * Ry ;          # BV Hamiltonian
    EBV_calc, eigBV = eig(HBV);                       # BV Hamiltonian diagonalization
    EBV = -(EBV_calc + Eg * Ry);                      # Reverting leveling

    HBC = (HH + VBC * eye(N, N)) * Ry ;               # BC Hamiltonian
    EBC, eigBC = eig(HBC);                            # BC Hamiltonian diagonalization

    idx = EBC.argsort()[::-1]   
    EBC = EBC[idx]
    eigBC = eigBC[:,idx]

    idx = EBV.argsort()[::-1]   
    EBV = EBV[idx]
    eigBV = eigBV[:,idx]
    
    return eigBV, eigBC, EBV, EBC



def current_density(absp, alpha_bulk, black_body,gap_bar, evec):

    Jsc = [a * b for a,b in zip(absp, black_body)]
    Jsc_bulk = [a * b for a,b in zip(alpha_bulk, black_body)]

    Jsc_dif = [abs(a - b) for a,b in zip(Jsc_bulk, Jsc)] 

    return Jsc,Jsc_bulk,Jsc_dif 