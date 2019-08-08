import math
import cmath
from decimal import Decimal

from tabulate import tabulate
import os

#----------------Variables Generales

pi = math.pi
c = 3*10**8 #m/s
f=0.5 #MHZ
landa = c/(f*10**6) #m
B=(2*pi)/landa

Er = 15
sig = 5*10**-3
I = 1 #amp

d = 5 #km

#heights 
h1 = 30.4878 #m
h2 = 9.146341 #m

x = 18*10**3*sig/f

y = math.atan((h1+h2)/(d*1000))

#--------------------------Final definicion de funciones y metodos----------------------------------------------------------------------

def correct_angle(Rvh, Rvhpol):

    if (Rvh.real < 0 and Rvh.imag > 0):

        return 180 - Rvhpol[1]

    elif (Rvh.real < 0 and Rvh.imag < 0) :

        return Rvhpol[1] - 180

    elif (Rvh.real > 0 and Rvh.imag < 0) :

        return 360 - Rvhpol[1]

    else:
        return Rvhpol[1]

#--------------------calculos de ejercicio------------------

r =complex( Er*(math.sin(y)), -(x*(math.sin(y)))) 
comp = complex(Er - (math.cos(y)**2), -x)

Rv1 = ((r) - (cmath.sqrt(comp)))
Rv2 = ((r) + (cmath.sqrt(comp)))
Rv = (Rv1/Rv2)

Rvpol = cmath.polar(Rv) 

ang = correct_angle(Rv, Rvpol)

rad = Rvpol[0]

R1 = math.sqrt((d*1000)**2 + (h1 - h2)**2)
R2 = math.sqrt((d*1000)**2 + (h1 + h2)**2)
R2_R1 = (R2 - R1)

angR = (360/landa)*R2_R1

new_ang = ang - angR

new_ang = math.radians(new_ang)


complejo = complex((Rvpol[0]*math.cos(new_ang)), Rvpol[0]*math.sin(new_ang))

#-------Espacial Vertical-----------

Espv = (60/(d*1609))*math.sqrt(((1 + complejo.real)**2) + ((complejo.imag)**2))


#fase constante
b = math.atan((Er+1)/x)

# P distancia numerica

#R distancia desde el dipolo hasta el punto donde el campo esta siendo considerado R>>landa

#--------sperficial Vertical----------

R = d*1609
p = (pi*R*math.cos(b))/(landa*x)

Esuv = (60/(d*1609*2*p))*(cmath.polar((1 - Rv))[0])

#---------------espacial Horizontal--------------

Rh1 = (math.sin(y) - (cmath.sqrt(comp)))
Rh2 = (math.sin(y) + (cmath.sqrt(comp)))

Rh = Rh1/Rh2

Rhpol = cmath.polar(Rh)

angh = math.radians(correct_angle(Rh, Rhpol) - (B*R2_R1*180/pi))

complejoh = complex((Rhpol[0]*math.cos(angh)), Rhpol[0]*math.sin(angh))


Esph = (60/(d*1609))*math.sqrt(((1 + complejoh.real)**2) + ((complejoh.imag)**2))

#-------campo superficial Horizontal

bh = math.atan((Er-1)/x)
ph = (pi*R*x)/(landa*math.cos(bh))

Esuh = (60/(d*1609*2*ph))*(cmath.polar((1 - Rh))[0])


#--------------------------------Datos Generales Aplicaciòn-----------------------------------

Directividad= 2.150 
Cte = '%.3E'% Decimal(1e00)
Potencia ='%.3E'% Decimal(73.00)
Frec=str('%.3E'% Decimal(f))
Distancia= '%.3E'% Decimal(d)
h1p= '%.3E'% Decimal(h1)
h2p= '%.3E'% Decimal(h2)
Epsilon=  '%.3E'% Decimal(Er)
Sigma= '%.3E'% Decimal(sig)
Ang_aproxRad='%.3E'% Decimal(0.007927)
Ang_aproxgrd= '%.3E'% Decimal(0.4542)
coef_ReflexRv= '%.3E'% Decimal(abs(Rv.real))
angRv= '%.3E'% Decimal(ang)
coef_ReflexRh= '%.3E'% Decimal(abs(Rh.real))
angRh='%.3E'% Decimal(correct_angle(Rh, Rhpol))
#-----------------------------------------Final Datos Generales ----------------------------

#-------------------------------------definiendo funciones y Métodos---------------------------------------------------------------
def mostrarDatosGenerales(Directividad,Cte,Potencia,Frec,Distancia,h1,h2,Epsilon,Sigma,Ang_aproxRad,Ang_aproxgrd,coef_ReflexRv,angRv,coef_ReflexRh,angRh):
        print("DIPOLO L/2      Polarización Horizontal o Vertical     Rr= 73 Ohmios    ")
        tabEjemplo1= {'Datos Generales': [
                 'Directividad   dBi   ', 
                 'Cte            Amp.  ', 
                 ' Potencia       Vatios', 
                 'Frec.          Mhz   ',
                 'Distancia      Kms.  ',
                 'h1, h2         mts.  ',
                 'Epsilon, Sigma',
                 'Ang aprox.     rad, gra',
                 'coef. Reflex   Rv      ',
                 'coef. Reflex   Rh      ',
                           ],

                 'Valor': [str('%.3E' % Decimal(Directividad) ),
                         str('%.3E'% Decimal(Cte)),
                         str('%.3E'% Decimal(Potencia)),
                         str('%.3E'% Decimal(Frec)),str('%.3E'% Decimal(Distancia)),
                         str('%.3E'% Decimal(h1p))  + "  "+str('%.3E'% Decimal(h2p)),
                         str('%.3E'% Decimal(Epsilon))  + "  "+str('%.3E'% Decimal(Sigma)),
                         str('%.3E'% Decimal(Ang_aproxRad)) + "  "+ str('%.3E'% Decimal(Ang_aproxgrd)),
                         str('%.3E'% Decimal(coef_ReflexRv))  + " "+ str('%.3E'% Decimal(angRv)), 
                         str('%.3E'% Decimal(coef_ReflexRh))  + "  "+ str('%.3E'% Decimal(angRh)) ],    
                            }
        
        tab = tabulate(tabEjemplo1, headers = 'keys', tablefmt='simple',stralign='left',floatfmt='.4f')
        print(tab)

def presentarCalculos(Eev,Esv,Eeh,Esh,CRefH,CRefV,Aten,dist):
    
    #Aqui va la presentacion de calculos obtenidos atraves de la fuciòn que hay que crear 
    tab1Distancia1={'TypeWave': [
                 'E espacial Vertical  ', 
                 'E Superficial Vertical', 
                 'E espacial Horizontal  ', 
                 'E Superficial Horizontal', 
                 
                           ],

                 'Value':[str('%.3E' % Decimal(Eev) ),
                         str('%.3E'% Decimal(Esv)),
                         str('%.3E'% Decimal(Eeh)),
                         str('%.3E'% Decimal(Esh)),     
                           ], }
    
    tab2Distancia1= {'TypeWave2': [
                 'C.Ref. Horiz. =  ', 
                 'C.Ref Vert.   =   ', 
                 'Aten.         = ', 
                 'dist. kmts    =', 
                 
                           ],

                 'Value2':[str('%.3E' % Decimal(CRefH) ),
                         str('%.3E'% Decimal(CRefV)),
                         str('%.3E'% Decimal(Aten)),
                         str('%.3E'% Decimal(dist)),     
                           ], }
    tab1 = tabulate(tab1Distancia1,  tablefmt='simple',stralign='left',floatfmt='.4f')
    tab2 = tabulate(tab2Distancia1,  tablefmt='simple',stralign='left',floatfmt='.4f')
    Ajust={'data1':[tab1], 'date2':[tab2],}
    #print(type(tab1))
    print(tabulate(Ajust, tablefmt='fancy_grid',stralign='left',floatfmt='.4f'))    


#_-------------presentacion---------------

presentacion = {'Univ. del Cauca': ['Onda Celeste', 
                 'Onda Terrestre', 
                 'Onda Espacial', 
                 'Onda Superficial',
                 'Eesv, Eesh',
                 'Esuv, Esuh'],

                 'Fac. Ing. Electrónica': ['La que va hacia la ionosfera',
                         'Onda espacial + Onda superficial',
                         'Onda Directa + Onda Reflejada',
                         'Onda ligada a la tierra',
                         'campo espacial vertical u Horizontal',
                         'campo superficial vertical u Horizontal'],



                         }

encabezado = {'Univ. del Cauca': [],
                'Fac. Ing. Electrónica': [],
                'Frec. = {} MHz'.format(f):[]
                         }

if __name__ == "__main__":

    os.system ("clear")

    print("            CAMPOS DE UNA ANTENA PROXIMA AL SUELO ")   

    print(tabulate(presentacion, headers = 'keys', tablefmt='fancy_grid',stralign='center'))

print("Precione c para visualizar ejemplo de prueba 1")

validation=input()
if (validation):

    os.system ("clear")
    mostrarDatosGenerales(Directividad,Cte,Potencia,Frec,Distancia,h1,h2,Epsilon,Sigma,Ang_aproxRad,Ang_aproxgrd,coef_ReflexRv,angRv,coef_ReflexRh,angRh) 
    print("Digite c para continuar")

    evaluation1=input()
    print("validacion correcta")
    
    os.system ("clear")

    

    for i in range(0,4):
        print(d)
        print(tabulate(encabezado, headers='keys'))
        for i in range(0,4):
            #Aqui hay que poner a ejecutar una funcion de todos los calculos 
            #donde varaia la Distancia cuatro veces con la misma frecuencia. Para 
            #Cada iteracion se le pasa los nuevos datos a la funciòn presentarCalculos()
            #asi se puede poner una tabla dentro de otra tabla, con un pequeño ajuste
            presentarCalculos(Espv, Esuv, Esph, Esuh, Rh.real, Rv.real,0.9936, d)

        d += 0.5
        instruction = None

        while  not instruction:
            instruction = input('Precione c para continuar')

        os.system ("clear")