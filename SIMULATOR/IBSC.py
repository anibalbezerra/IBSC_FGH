from physics import *
from gui import *

from PySimpleGUI import read_all_windows, theme, Button, HSeparator, Text, Slider, Window, Canvas, Column, VSeparator, WIN_CLOSED, popup_auto_close
from webbrowser import open as op


#importa a biblioteca de manipulação materica de arrays
from numpy import linspace, sign, genfromtxt, zeros, argwhere, eye, dot, exp, pi, arange, cos, reshape, array,where
from numpy.linalg import eig

from numba import njit

#importa a biblioteca de criação de gráfica
from matplotlib.pyplot import close, tight_layout, subplots_adjust
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from screeninfo import get_monitors

# Defining system ’ s properties
n = 1
N = 351;                    # number of grid points ( must be odd )
s = (N -1) / 2;             # upper limit to FGH sum
a0 = 100;                   # length scaling [ angstroms ]
L = 1000 / a0 ;             # structure ’ s length
Lqw = 50;                   # QW width
        
x = linspace(-L, L, N);     # position vector        
dx = x[2] - x[1];           # grid spacing

elf = 10;                             # electric field
elfx = 500 ;                          # electric field intervall
Ne = 1000;                            # number of points for absorption energy vector
hw = linspace(1e-5, 4000, Ne);        # absorption energy vector


EN = ['Ga(0.47)In(0.53)As/Al(0.6)Ga(0.4)As', 'Custom Parameters', 'Gallium Concentration ', 'Aluminum Concentration ', 
      'Electric Field (kV/cm)', 'Intrinsic Region Width (Ang)','Quantum Well-Width (Ang)','Generate Heterostructure','VB Discontinuity',
      'CB Discontinuity', 'QW Gap', 'Draw Potential','Evaluate States', 'E_VB(n)','E_CB(1)','Absorption',
      'This simulation may take a few seconds...','Temperature (K)', 'Sun', 'Show Black-Body Radiation', 'Help', 'Reset', 'Language', 'Exit', 'QW gap', 'Barrier gap']

PT = ['Ga(0.47)In(0.53)As/Al(0.6)Ga(0.4)As', 'Parâmetros Customizados', 'Concentração de Gálio ', 'Concentração de Alumínio ', 
      'Campo Elétrico (kV/cm)', 'Largura Região Inrínseca (Ang)','Largura do Poço (Ang)','Gerar Heteroestrutura','Descontinuidade da BV',
      'Descontinuidade da BC', 'Gap de energia no poço', 'Plotar Potencial','Calcular Estados', 'E_BV(n)','E_BC(1)','Absorção',
      'Essa simulação pode levar alguns segundos...','Temperatura (K)', 'Sol', 'Mostrar Espectro de Corpo Negro', 'Ajuda','Reset', 
      'Idioma', 'Sair', 'Gap poço', 'Gap barreira']

colorButton = 'slate blue'
clickButton = 'orange'

janela_lin, janela_sim = Janela_lin(), None

ver0, ver1, ver2 = False, False, False
figure_agg1, figure_agg2, figure_agg3 = None, None, None
try:
    while True:
        window, event, values = read_all_windows()

        if window in (janela_lin, janela_sim) and event in (WIN_CLOSED, 'sair'):
            break

        if window == janela_lin and event == 'PT':
            janela_lin.hide()
            janela_sim = Janela_sim(PT)
            idioma = PT
        elif window == janela_lin and event == 'EN':
            janela_lin.hide()
            janela_sim = Janela_sim(EN)
            idioma = EN
        if window == janela_sim and event == 'VO':
            janela_sim.hide()
            janela_lin.un_hide()

        for monitor in get_monitors():
            w = monitor.width
            h = monitor.height
        #    print(str(width) + 'x' + str(height))
        #w, h = Window.get_screen_size()
        X, Y = pix_pol(0.43*w), pix_pol(0.4*h)
        
        if  event == 'het':
            window.Element('x').Update(0.47)
            window.Element('y').Update(0.6)
            window.Element('EL').Update(10)
            window.Element('ELX').Update(500)
            window.Element('LQW').Update(150)
            window.Element('PQ').Update(disabled = True)
            window.Element('ES').Update(disabled = True)
            window.Element('SP').Update(disabled = False)
            window.Element('het').Update(button_color = clickButton)
            window.Element('par').Update(button_color = colorButton)
            window.Element('SP').Update(button_color = colorButton)
        elif event == 'par':
            window.Element('SP').Update(disabled = True)
            window.Element('ES').Update(button_color = colorButton)
            window.Element('PQ').Update(button_color = colorButton)
            window.Element('het').Update(button_color = colorButton)
            window.Element('par').Update(button_color = clickButton)
            window.Element('SP').Update(button_color = colorButton)
            window.Element('AB').Update(button_color = colorButton)            
            window.Element('x').Update(disabled = False)
            window.Element('y').Update(disabled = False)
            window.Element('EL').Update(disabled =  False)
            window.Element('ELX').Update(disabled = False)
            window.Element('LQW').Update(disabled = False)
            window.Element('PQ').Update(disabled = True)
            window.Element('ES').Update(disabled = True)
            window.Element('BV').Update(' ')
            window.Element('BC').Update(' ')
            window.Element('EG').Update(' ')
            window.Element('E_BV').Update(' ')
            window.Element('E_BC').Update(' ')
            window.Element('EG').Update(' ')
            window.Element('E_TR').Update(' ')
            n = 1        
        elif event in ('x', 'y', 'EL', 'ELX', 'LQW'): 
            window.Element('SP').Update(disabled = False)
            window.Element('PQ').Update(disabled = True)
            window.Element('ES').Update(disabled = True)
            window.Element('SP').Update(button_color = colorButton)

    ############################################################################################################

        if  event == 'SP':

            Ry = 0.381 / massa_efetiva(values['x'])
            BV, BC, EG = GaInAs_AlGaAs(values['x'], values['y'], massa_efetiva(values['x']))

            BVV = ' ' + str(round(BV * Ry, 2)) + ' meV'
            BCC = ' ' + str(round(((BC * Ry)), 2)) + ' meV'
            EGG = ' ' + str(round(EG * Ry, 2)) + ' meV'
            window.Element('BV').Update(BVV)
            window.Element('BC').Update(BCC)
            window.Element('EG').Update(EGG)
            window.Element('PQ').Update(disabled = False)
            window.Element('ES').Update(disabled = False)
            window.Element('SP').Update(button_color = clickButton)
            ver0 = True
            ver1 = True
        
    ############################################################################################################   
        #plota o potencial
        if  event == 'PQ' and ver0 == True:
            ver0 = False
            if figure_agg1 != None:
                delete_figure_agg(figure_agg1)  
                
            BV, BC, EG = GaInAs_AlGaAs(values['x'], values['y'], massa_efetiva(values['x']))
            VBV, VBC = potential(BV, BC, EG, N, x, massa_efetiva(values['x']),  values['EL'], values['ELX'], values['LQW'])
            VBV_bulk, VBC_bulk = bulk(BV, BC, EG, N, x, massa_efetiva(values['x']),  values['EL'], values['ELX'], values['LQW'])
            
            fig = Figure(figsize = (X, 0.8*Y))
            ax = fig.add_subplot(111)
            ax.plot(x * a0, (VBV * Ry) * 1e-3, lw = 1.5 , color = 'black')
            ax.plot(x * a0, (VBC * Ry) * 1e-3, lw = 1.5 , color = 'black')
            
            ax.plot(x * a0, (VBV_bulk * Ry) * 1e-3, lw = 1.5 , color = 'black', marker="x")
            ax.plot(x * a0, (VBC_bulk * Ry) * 1e-3, lw = 1.5 , color = 'black', marker="x")
            
            ax.set_ylabel(r'$\hbar\omega$(eV)')
            ax.set_xlabel(r'Z($\AA)$')

            subplots_adjust(bottom=0.5)
            figure_agg1 = draw_figure_w_toolbar(window['CanvaPotencial'].TKCanvas, fig, window['controls_cv'].TKCanvas)
            window.Element('PQ').Update(button_color = clickButton)
            
        #plota os Estados
        elif event == 'ES' and ver1 == True: 
            ver1 = False
            ver2 = True
            if figure_agg1 != None:
                delete_figure_agg(figure_agg1)

            fig = Figure(figsize = (X, 0.8*Y))
            ax = fig.add_subplot(111)

            #Calcula os estados
            BV, BC, EG = GaInAs_AlGaAs(values['x'], values['y'], massa_efetiva(values['x']))
            VBV, VBC = potential(BV, BC, EG, N, x, massa_efetiva(values['x']),  values['EL'], values['ELX'], values['LQW'])
            eigBV, eigBC, EBV, EBC = diagonalize(VBV, VBC, EG, N, massa_efetiva(values['x']), HH(s, N, dx))
            
            #Calcula os estados bulk
            VBV_bulk, VBC_bulk = bulk(BV, BC, EG, N, x, massa_efetiva(values['x']),  values['EL'], values['ELX'], values['LQW'])
            eigBV_bulk, eigBC_bulk, EBV_bulk, EBC_bulk = diagonalize(VBV_bulk, VBC_bulk, EG, N, massa_efetiva(values['x']), HH(s, N, dx))

            #Plota estados e estados
            for i in range(n):
                ax.plot(x * a0, (-1500 * eigBV[:,i]**2 + EBV[i]) * 1e-3,
                        x * a0, (1500 * eigBC[:,-1-i]**2 + EBC[-1-i]) * 1e-3)

            ax.plot(x * a0, (VBV * Ry) * 1e-3, lw = 1.5 , color = 'black')
            ax.plot(x * a0, (VBC * Ry) * 1e-3, lw = 1.5 , color = 'black')
            ax.set_ylabel(r'$\hbar\omega$(eV)')
            ax.set_xlabel(r'Z($\AA)$')

            subplots_adjust(bottom=0.5)
            figure_agg1 = draw_figure_w_toolbar(window['CanvaPotencial'].TKCanvas, fig, window['controls_cv'].TKCanvas)


            E_BV = ' ' + str(round(EBV[0], 2)) + ' meV'
            E_BC = ' ' + str(round(EBC[-1], 2)) + ' meV'
            E_tra = ' ' + str(round(abs(EBC[-1] - EBV[0]), 2)) + ' meV'
            window.Element('PQ').Update(button_color = clickButton)
            window.Element('ES').Update(button_color = clickButton)
            window.Element('AB').Update(disabled = False)
            window.Element('+').Update(disabled = False)
            window.Element('-').Update(disabled = False)
            window.Element('E_BC').Update(E_BC)
            window.Element('E_BV').Update(E_BV)
            window.Element('E_TR').Update(E_tra)

        elif event == '+':
            if figure_agg1 != None:
                delete_figure_agg(figure_agg1)
            elif n > N:
                pass

            n = n + 1 

            fig = Figure(figsize = (X, 0.8*Y))
            ax = fig.add_subplot(111)

            for i in range(n):
                ax.plot(x * a0, (-1500 * eigBV[:,i]**2 + EBV[i]) * 1e-3,
                            x * a0, (1500 * eigBC[:,-1-i]**2 + EBC[-1-i]) * 1e-3)

            ax.plot(x * a0, (VBV * Ry) * 1e-3, lw = 1.5 , color = 'black')
            ax.plot(x * a0, (VBC * Ry) * 1e-3, lw = 1.5 , color = 'black')
            ax.set_ylabel(r'$\hbar\omega$(eV)')
            ax.set_xlabel(r'Z($\AA)$')
            figure_agg1 = draw_figure_w_toolbar(window['CanvaPotencial'].TKCanvas, fig, window['controls_cv'].TKCanvas)

        elif event == '-':
            if figure_agg1 != None:
                delete_figure_agg(figure_agg1)

            
            if n <= 0:
                pass
            else:
                n = n - 1

            fig = Figure(figsize = (X, 0.8*Y))
            ax = fig.add_subplot(111)

            for i in range(n):
                ax.plot(x * a0, (-1500 * eigBV[:,i]**2 + EBV[i]) * 1e-3,
                        x * a0, (1500 * eigBC[:,-1-i]**2 + EBC[-1-i]) * 1e-3)

            ax.plot(x * a0, (VBV * Ry) * 1e-3, lw = 1.5 , color = 'black')
            ax.plot(x * a0, (VBC * Ry) * 1e-3, lw = 1.5 , color = 'black')
            ax.set_ylabel(r'$\hbar\omega$(eV)')
            ax.set_xlabel(r'Z($\AA)$')
            figure_agg1 = draw_figure_w_toolbar(window['CanvaPotencial'].TKCanvas, fig, window['controls_cv'].TKCanvas)

    ############################################################################################################

        if  event == 'AB' and ver2 == True:
            if figure_agg2 != None:
                delete_figure_agg(figure_agg2)
                

            #BV, BC, EG = GaInAs_AlGaAs(values['x'], values['y'], massa_efetiva(values['x']))
            #VBV, VBC = potential(BV, BC, EG, N, x, massa_efetiva(values['x']),  values['EL'], values['ELX'], values['LQW'])
            #eigBV, eigBC, EBV, EBC = diagonalize(VBV, VBC, EG, N, massa_efetiva(values['x']), HH(s, N, dx))
            alpha = absorption(100, N, Ne, EBC, EBV, eigBV, eigBC, hw)
            alpha_bulk = absorption(100,  N, Ne, EBC_bulk, EBV_bulk, eigBV_bulk, eigBC_bulk, hw)
            g = gap_bar(values['y'])

            fig = Figure(figsize = (X, 0.8*Y))
            ax = fig.add_subplot(111)
            ax.plot(hw[20:]*1e-3, alpha[20:], lw = 2 , color = 'red',label='IBSC') 
            ax.plot(hw[20:]*1e-3, alpha_bulk[20:], lw = 2 , color = 'black', ls='--',label='p-i-n')
            ax.axvline(EG*1e-3* Ry, color = 'green')
            ax.text(3, 0.0025, idioma[-2], color = 'green', size = 'large')
            ax.axvline(g, color = 'blue')
            ax.text(3, 0.001, idioma[-1], color = 'blue', size = 'large')
            ax.set_ylabel(r'$\alpha~$(a.u.)')
            ax.set_xlabel(r'$\hbar\omega~$(eV)')
            ax.legend()

            subplots_adjust(bottom=0.8)
            tight_layout(pad=100)
            figure_agg2 = draw_figure_w_toolbar(window['CanvaAbsorcao'].TKCanvas, fig, window['controls_cv1'].TKCanvas)
            #figure_agg2 = draw_figure(window['CanvaAbsorcao'].TKCanvas, fig)
            window.Element('AB').Update(button_color = clickButton)
            window.Element('AB').Update(disabled = False)
            
            ver2 = False
            
    ############################################################################################################
        if  event == 'SOL':
            window.Element('T').Update(5775)
            window.Element('SOL').Update(button_color = clickButton)
            window.Element('CN').Update(button_color = colorButton)
        elif  event == 'T':
            window.Element('SOL').Update(button_color = colorButton)
            window.Element('CN').Update(button_color = colorButton)

        if  event == 'CN':
            if figure_agg3 != None:
                delete_figure_agg(figure_agg3)
            else:
                window.Element('CN').Update(button_color = colorButton)

            B, v = blackBody(values['T'], Ne)
            fig = Figure(figsize = (X, 0.8*Y))
            ax = fig.add_subplot(111)
            ax.plot(v, B)   
            ax.set_ylabel(r'I ~($10^{2}~$ W / m$ ^2$ eV )')
            ax.set_xlabel(r'$\hbar\omega~$(eV)')
            #fig.tight_layout()
            figure_agg3 = draw_figure_w_toolbar(window['CanvaCorpoNegro'].TKCanvas, fig, window['controls_cv2'].TKCanvas)
            #figure_agg3 = draw_figure(window['CanvaCorpoNegro'].TKCanvas, fig)
            window.Element('CN').Update(button_color = clickButton)

            ######### current density
            g = gap_bar(values['y'])           
            
            Jsv, Jsv_barr, Jsv_dif = current_density(alpha,alpha_bulk, B,g,v)
            fig = Figure(figsize = (X, 0.8*Y))
            ax = fig.add_subplot(111)
            ax.plot(v,Jsv, label='IBSC')

            ax.plot(v,Jsv_barr,'--', label='p-i-n') 

            ax.plot(v,Jsv_dif,'-*', label='difference')
             
            ax.set_ylabel(r'Current Density (a.u.)')
            ax.set_xlabel(r'$\hbar\omega~$(eV)')
            ax.legend()
            
            figure_agg4 = draw_figure_w_toolbar(window['CanvaJsv'].TKCanvas, fig, window['controls_cv3'].TKCanvas)
            #figure_agg4 = draw_figure(window['CanvaJsv'].TKCanvas, fig)

    ############################################################################################################
        if event == 'RE':
            window.Element('x').Update(0)
            window.Element('y').Update(0)
            window.Element('EL').Update(0)
            window.Element('ELX').Update(0)
            window.Element('LQW').Update(0)
            window.Element('T').Update(1e2)
            window.Element('AB').Update(button_color = colorButton)
            window.Element('CN').Update(button_color = colorButton)
            window.Element('par').Update(button_color = colorButton)
            window.Element('het').Update(button_color = colorButton)
            window.Element('SOL').Update(button_color = colorButton)
            window.Element('ES').Update(button_color = colorButton)
            window.Element('SP').Update(button_color = colorButton)
            window.Element('PQ').Update(button_color = colorButton)
            window.Element('BV').Update(' ')
            window.Element('BC').Update(' ')
            window.Element('EG').Update(' ')
            window.Element('E_BV').Update(' ')
            window.Element('E_BC').Update(' ')
            window.Element('EG').Update(' ')
            window.Element('E_TR').Update(' ')
            window.Element('AB').Update(disabled = True)
            window.Element('PQ').Update(disabled = True)
            window.Element('ES').Update(disabled = True)
            window.Element('SP').Update(disabled = True)
            window.Element('+').Update(disabled = True)
            window.Element('-').Update(disabled = True)
            n = 1

            ver0, ver1, ver2 = False, False, False        

            if figure_agg1 != None:
                delete_figure_agg(figure_agg1)
            if figure_agg2 != None:
                delete_figure_agg(figure_agg2)
            if figure_agg3 != None:
                delete_figure_agg(figure_agg3)
                
        if event == 'help':
            op('https://www.unifal-mg.edu.br/ldft/IBSC_GUI') 
                  
    window.close()
    
except ValueError:
    popup_auto_close('Erro inesperado', auto_close_duration = 5, font = ('Arial', 15))
    window.close()
