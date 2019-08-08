import math
import cmath

from tabulate import tabulate
import os

pi = math.pi
c = 3*10**8 #m/s
f=50 #MHZ
landa = c/(f*10**6) #m
B=(2*pi)/landa

Er = 15
sig = 5*10**-3
I = 1 #amp

d = 3 #miles


#heights 

h1 = 100 #ft
h2 = 30 #ft

x = 18*10**3*sig/f

y = math.atan((h1+h2)/(3*5280))

def correct_angle(Rvh, Rvhpol):

	if (Rvh.real < 0 and Rvh.imag > 0):

		return 180 - Rvhpol[1]

	elif (Rvh.real < 0 and Rvh.imag < 0) :

		return Rvhpol[1] - 180

	elif (Rvh.real > 0 and Rvh.imag < 0) :

		return 360 - Rvhpol[1]

	else:
		return Rvhpol[1]




r =complex( Er*(math.sin(y)), -(x*(math.sin(y)))) 
comp = complex(Er - (math.cos(y)**2), -x)

Rv1 = ((r) - (cmath.sqrt(comp)))
Rv2 = ((r) + (cmath.sqrt(comp)))
Rv = (Rv1/Rv2)

Rvpol = cmath.polar(Rv) 

ang = correct_angle(Rv, Rvpol)

rad = Rvpol[0]

R1 = math.sqrt((d*5280)**2 + (h1 - h2)**2)*0.3048
R2 = math.sqrt((d*5280)**2 + (h1 + h2)**2)*0.3048
R2_R1 = (R2 - R1)

angR = (360/landa)*R2_R1

new_ang = ang - angR

new_ang = math.radians(new_ang)


complejo = complex((Rvpol[0]*math.cos(new_ang)), Rvpol[0]*math.sin(new_ang))

Esp = (60/(d*1609))*math.sqrt(((1 + complejo.real)**2) + ((complejo.imag)**2))


#fase constante
b = math.atan((Er+1)/x)

# P distancia numerica

#R distancia desde el dipolo hasta el punto donde el campo esta siendo considerado R>>landa

R = d*1609
p = (pi*R*math.cos(b))/(landa*x)


Esu = (60/(d*1609*2*p))*(cmath.polar((1 - Rv))[0])

#print(Esu)


#---------------Horizontal--------------

Rh1 = (math.sin(y) - (cmath.sqrt(comp)))
Rh2 = (math.sin(y) + (cmath.sqrt(comp)))

Rh = Rh1/Rh2

Rhpol = cmath.polar(Rh)

angh = math.radians(correct_angle(Rh, Rhpol) - (B*R2_R1*180/pi))

complejoh = complex((Rhpol[0]*math.cos(angh)), Rhpol[0]*math.sin(angh))


Esph = (60/(d*1609))*math.sqrt(((1 + complejoh.real)**2) + ((complejoh.imag)**2))

#print(Esph)

#-------campo superficial Horizontal

bh = math.atan((Er-1)/x)
ph = (pi*R*x)/(landa*math.cos(bh))

Esuh = (60/(d*1609*2*ph))*(cmath.polar((1 - Rh))[0])

print(Esuh)

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

                'Lab1 de Sistel': [],


                         }

if __name__ == "__main__":

	os.system ("clear")

	print(tabulate(presentacion, headers = 'keys'))







