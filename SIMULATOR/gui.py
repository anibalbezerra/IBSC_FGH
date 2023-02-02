#importa a biblioteca de criação de gráfica
from matplotlib.pyplot import close, tight_layout, subplots_adjust
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from PySimpleGUI import read_all_windows, theme , Frame,RELIEF_SUNKEN
from PySimpleGUI import Button, HSeparator, Text, Slider, Window, Canvas, Column, VSeparator, WIN_CLOSED, popup_auto_close
from webbrowser import open as op

from numpy import linspace, sign, genfromtxt, zeros, argwhere, eye, dot, exp, pi, arange, cos, reshape, array,where
from numpy.linalg import eig

from screeninfo import get_monitors

from numba import njit

tema = "DarkBlue13"
colorButton = "slate blue"
bkgd = "slate blue"

def pix_pol(x):
    return x * 0.01042

def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)
    
    return figure_canvas_agg

        
class Toolbar(NavigationToolbar2Tk):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar2Tk.toolitems if
                 t[0] in ('Home', 'Back', 'Forward', 'Pan','Save', 'Zoom')]

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side = 'top', fill = 'both', expand = 1, padx = 6, pady = 10)
    return figure_canvas_agg

def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    close('all')


def Janela_lin():
    #theme('SystemDefault')
    theme(tema)
    layout1 = [[Button('Welcome to the IBSC simulator. Click here to use the english version.', size = (50, 4), key = 'EN', button_color = colorButton,
                   pad = ((10,10),(10,10)))], 
              [HSeparator(pad = (5,5))],
              [Button('Bem-vindo ao simulador de CSBI. Clique aqui para usar a versão em português.', size = (50, 4), key = 'PT', button_color = colorButton)]]
    return Window('Idioma/Language', layout = layout1, finalize = True)

        
def Janela_sim(idioma):
    states = arange(1, 21)
    theme(tema)

    Layout_Parametros = [

            [Button(idioma[0], size = (35, 2), key = 'het', button_color = colorButton, pad = ((10,10),(10,10))),
                          Button(idioma[1], size = (35, 2), key = 'par', button_color = colorButton)],

            [HSeparator(pad = (5,5))],

            [Text(idioma[2], size = (15,3)), 
             Slider(range = (0, 1), size = (20, 10), resolution = 0.01, orientation = 'h', key = 'x',
                                                 enable_events = True, disabled = True),
             Text(idioma[3], size = (15, 3)), 
             Slider(range = (0, 1), size = (20, 10),resolution = 0.01, orientation = 'h', key = 'y',
                                                     enable_events = True, disabled = True)],

            [Text(idioma[4], size = (15, 3)), 
             Slider(range = (-200, 200), size = (20, 10), resolution = 10, orientation = 'h',
                          default_value = 0, key = 'EL', enable_events = True, disabled = True), 
             Text(idioma[5], size = (15, 3)), 
             Slider(range = (10, 700), size = (20, 10), resolution = 10, orientation = 'h', key = 'ELX',
                       enable_events = True, default_value = 10, disabled = True)],

            [Text(idioma[6], size = (15, 3)), 
             Slider(range = (0, 200), size = (20, 10), resolution = 5, orientation = 'h', key = 'LQW',
                                                      enable_events = True, disabled = True),
             Button(idioma[7], size = (35, 1), pad = ((15,0),(12,0)), key = 'SP', 
                       enable_events = True, button_color = colorButton, disabled = True)],

            [Text(idioma[8], pad = ((20, 0),(5,0)), size = (20, 2)), 
             Text(idioma[9], pad = ((20, 0),(5,0)), size = (20, 2)), 
             Text(idioma[10], pad = ((20, 0),(5,0)), size = (20, 2))],

            [Text(key = 'BV', size = (13, 2), background_color = bkgd, pad = ((30, 15),(2,5)), justification = 'center'),  
             Text(key = 'BC', size = (13, 2), background_color = bkgd, pad = ((70, 0),(2,5)), justification = 'center'), 
             Text(key = 'EG', size = (13, 2), background_color = bkgd, pad = ((75, 0),(2,5)), justification = 'center')], 

            [HSeparator()],

            [Button(idioma[11], size = (20, 2), key = 'PQ', pad = ((35, 40),(20,0)),
                       button_color = colorButton, disabled = True), 
             Button(idioma[12], size = (20, 2), key = 'ES', pad = ((10, 10),(20,0)),
                       button_color = colorButton, disabled = True), 
             Button('+', size = (3, 2), enable_events = True, pad = ((0, 5),(20, 0)), key = '+',
                       button_color = colorButton, disabled = True), 
             Button('-', size = (3, 2), enable_events = True, pad = ((0, 0),(20,0)), key = '-',
                       button_color = colorButton, disabled = True)],

            [Text(idioma[13], pad = ((50, 0),(25,0))), Text(key = 'E_BV', size = (13, 2), pad = ((5, 0),(25,0)),
                                                             background_color = bkgd),  
             Text(idioma[14], pad = ((30, 0),(25,0))), Text(key = 'E_BC', size = (13, 2), pad = ((5, 0),(25,0)),
                     background_color = bkgd),
             Text(r'DE', pad = ((30, 0),(25,0)), font = ('Symbol')), 
             Text(key = 'E_TR', size = (13, 2), pad = ((5, 0),(25,0)), background_color = bkgd)], 

            [HSeparator(pad = (5,5))],

            [Button(idioma[15], size = (70, 2), button_color = colorButton, key = 'AB', pad = ((10, 10),(5,20)), 
                       enable_events = True, disabled = True)],

            [Text(idioma[16], size = (55, 2), justification = 'center', 
                     font=("Arial", 12))],

            [HSeparator(pad = (5,5))],


            [Text(idioma[17]), Slider(range = (1e2, 1e4), resolution = 50, size = (30, 10), 
                                               orientation = 'h', key = 'T',enable_events = True), 
             Button(idioma[18], key = 'SOL', enable_events = True, pad = ((0, 0),(10,0)),
                                                                button_color = colorButton)],

            [Button(idioma[19], size = (70, 2), key = 'CN', 
                       pad = ((10,10),(10,10)),button_color = colorButton)],

            [HSeparator(pad = (5,5))],

            [Button(idioma[20], enable_events = True, key = 'help', size = (15,2), pad = ((10,10), (10,10)),
                       button_color = colorButton), 
             Button(idioma[21], enable_events = True, key = 'RE', size = (15,2), pad = ((10,10), (10,10)),
                       button_color = colorButton),
             Button(idioma[22], enable_events = True, key = 'VO', size = (15,2), pad = ((10,10), (10,10)),
                       button_color = colorButton),
             Button(idioma[23], key = 'sair', size = (15,2), pad = ((10,10), (10,10)),button_color = colorButton)]

        ]

    w, h = Window.get_screen_size()
    
    for monitor in get_monitors():
        w = monitor.width
        h = monitor.height
        #print(str(width) + 'x' + str(height))

    Layout_Graficos = [

            [Canvas(key = 'controls_cv', size=((0.48*w), 0.1))],
            [Canvas(size=((0.48*w), 0.4*h), background_color = 'white', key = 'CanvaPotencial', tooltip='Heteroestrutura')],
            [HSeparator(pad = (1,1))],
            [Canvas(key = 'controls_cv1', size=((0.48*w), 0.1))],
            [Canvas(size = ((0.48*w), 0.4*h), background_color = 'white', key = 'CanvaAbsorcao', tooltip='Absorção')],
            [HSeparator(pad = (1,1))],
            [Canvas(key = 'controls_cv2', size=((0.48*w), 0.1))],
            [Canvas(size = ((0.48*w), 0.4*h), background_color = 'white', key = 'CanvaCorpoNegro', tooltip='Radiação de corpo negro')],
            [HSeparator(pad = (1,1))],
            [Canvas(key = 'controls_cv3', size=((0.48*w), 0.1))],
            [Canvas(size = ((0.48*w), 0.5*h), background_color = 'white', key = 'CanvaJsv', tooltip='Densidade de Corrente')]

        ]

    Layout = [
             [Column(Layout_Parametros, scrollable = True, size = (0.45 * w, h)), VSeparator(),
              Column(Layout_Graficos, scrollable = True, size = (0.5* w, 2*h))]
        ]

    wd = Window('IBSC - Ga(x)In(1-x)As/Al(y)Ga(1-y)As', Layout, finalize = True, resizable = True)#, icon = r'./IBSC.ico')
    wd.set_icon("./IBSC.png")
    return wd
