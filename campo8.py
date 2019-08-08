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

x = (18*10**3)*sig/f

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


def compx(fm=0.5, dk= 5):

	f = fm
	d = dk

	x = (18*10**3*sig)/f

	y = math.atan((h1 + h2)/(d*1000))

	#r =complex( Er*(math.sin(y)), -(x*(math.sin(y)))) 
	r = (complex(Er, -x)*math.sin(y))
	#comp = complex(Er - (math.cos(y)**2), -x)
	comp = (complex(Er, -x) - (math.cos(y)**2))

	return r, comp

def calcl_RV(fm=0.5, dk= 5):
	f = fm
	d = dk

	r, comp = compx(f, d)

	Rv1 = ((r) - (cmath.sqrt(comp)))
	Rv2 = ((r) + (cmath.sqrt(comp)))
	Rv = (Rv1/Rv2)

	return Rv

def calcl_Rh(fm=0.5, dk= 5):
	f = fm
	d = dk

	y = math.atan((h1+h2)/(d*1000))

	r, comp= compx(f, d)
	Rh1 = (math.sin(y) - (cmath.sqrt(comp)))
	Rh2 = (math.sin(y) + (cmath.sqrt(comp)))
	Rh = Rh1/Rh2

	return Rh



#--------------------calculos de ejercicio------------------

def calcular_Espv(fm=0.5, dk=5):
	f = fm
	d = dk

	landa = c / (f*10**6)

	Rv = calcl_RV(f, d)

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

	Espv = (60/(d*1000))*math.sqrt(((1 + complejo.real)**2) + ((complejo.imag)**2))

	return Espv


#fase constante
# P distancia numerica
#R distancia desde el dipolo hasta el punto donde el campo esta siendo considerado R>>landa
#--------sperficial Vertical----------

def calcular_Esuv(fm=0.5, dk=5):

	f = fm
	d = dk
	x = (18*10**3*sig)/f

	landa =c/(f*10**6)

	Rv = calcl_RV(f, d)

	R = d
	b = math.atan((Er+1)/x)
	p = ((pi*R)/(landa*x))*math.cos(b)

	Esuv = (60/d*1000)*((cmath.polar(1 - Rv)[0])/(2*p))
	
	return Esuv

#---------------espacial Horizontal--------------

def calcular_Esph(fm=0.5, dk=5):

	f = fm
	d= dk
	landa = c/(f*10**6)
	B = (2*pi)/landa

	R1 = math.sqrt((d*1000)**2 + (h1 - h2)**2)
	R2 = math.sqrt((d*1000)**2 + (h1 + h2)**2)
	R2_R1 = (R2 - R1)

	Rh = calcl_Rh(f, d)

	Rhpol = cmath.polar(Rh)

	##Corregir angulo
	
	ang_h = correct_angle(Rh, Rhpol)

	angh = math.radians(ang_h - ((360/landa)*R2_R1))
	
	complejoh = complex((Rhpol[0]*math.cos(angh)), Rhpol[0]*math.sin(angh))

	
	Esph = (60/(d*1000))*math.sqrt((((1 + complejoh.real)**2) + ((complejoh.imag)**2)))

	return Esph

#-------campo superficial Horizontal

def calcular_Esuh(fm=0.5, dk=5):

	f = fm
	d = dk
	x = (18*10**3)*sig/f

	landa = c/(f*10**6)

	Rh = calcl_Rh(f, d)

	R = d
	bh = math.atan((Er-1)/x)

	ph = (pi*R*x)/(landa*math.cos(bh))

	Esuh = (60/(d*1000*2*ph))*(cmath.polar((1 - Rh))[0])

	return Esuh


#--------------------------------Datos Generales Aplicaciòn-----------------------------------
Rvn = calcl_RV()
angn = correct_angle(Rvn, cmath.polar(Rvn))

Rhn = calcl_Rh()
angnh = correct_angle(Rvn, cmath.polar(Rhn))


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
coef_ReflexRv= '%.3E'% Decimal(abs(Rvn.real))
angRv= '%.3E'% Decimal(angn)
coef_ReflexRh= '%.3E'% Decimal(abs(Rhn.real))
angRh='%.3E'% Decimal(angnh)
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
                 'E espacial Vertical      = ', 
                 'E Superficial Vertical   = ', 
                 'E espacial Horizontal    = ', 
                 'E Superficial Horizontal = ', 
                 
                           ],

                 'Value':[str('%.3E' % Decimal(Eev)),
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
    tab1 = tabulate(tab1Distancia1,  tablefmt='simple',stralign='left')
    tab2 = tabulate(tab2Distancia1,  tablefmt='simple',stralign='left')
    Ajust={'data1':[tab1], 'date2':[tab2],}
    #print(type(tab1))
    print(tabulate(Ajust, tablefmt='fancy_grid',stralign='left',floatfmt='.4f'))

#Calculos intermedios



def CalculosIntermedios(jfa=1, jda=5, landaa= 300, da =5 , R1a=1.000001, R2a=1.000002, h1a=30.4878, h2a=9.146341, Xia=0.001891795, f=0.5, era=15 , sigmaa =5*10**-3, xa= 90, Aa =0.9231):
    
    jf=jfa
    jd=jda
    d=da
    R1=R1a
    R2= R2a
    h1=h1a
    h2=h2a
    R12=R1-R2
    Xi= Xia
    frec= f
    Er = era
    sigma = sigmaa
    x= xa
    landa = landaa
    A = Aa
    #Aqui van los otros valores Aldaircho 
    
    
    tabCalculosIntermedios= {'TypeWave2': [
                'jf , jd         =  ', 
                'Long. de Onda   =   ', 
                'd               = ', 
                'R1, R2          =',
                'h1 , h2         =',
                'R1-R2           =',
                'Xi              =',
                'frec.           =',
                'er,sigma, x     =',
                'Rhm, rhag, rhar =',
                'Rvm, rvag, rvar =',
                'pv , ph         =',
                'bv , bpv, bsv  =',
                'bh , bph, bsh   =',
                'A               =',
                'pa              =',           
                                       ],

                        'Value2':[
                         str('%.3E'% Decimal(jf)),
                         str('%.3E'% Decimal(landa)),
                            
                         str('%.3E'% Decimal(d)),
                         str('%.3E'% Decimal(R1)),
                            
                         str('%.3E'% Decimal(h1)),
                         str('%.3E'% Decimal(R12)),
                            
                         str('%.3E'% Decimal(Xi)),
                         str('%.3E'% Decimal(frec)),
                            
                         str('%.3E'% Decimal(Er)),
                         str('%.3E'% Decimal(0)),
                            
                         str('%.3E'% Decimal(0)),
                         str('%.3E'% Decimal(0)),
                            
                         str('%.3E'% Decimal(0)),
                         str('%.3E'% Decimal(0)),
                         str('%.3E'% Decimal(A)),
                         str('%.3E'% Decimal(0)),
                           ],
                        'Value3':
                         [
                         str('%.3E' % Decimal(jd) ),
                         str('%.3E'% Decimal(0)),
                         
                         str('%.3E'% Decimal(0)),
                         str('%.3E'% Decimal(R2)),
                             
                         str('%.3E'% Decimal(h2)),     
                         str('%.3E'% Decimal(0)),
                             
                         str('%.3E'% Decimal(0)),
                         str('%.3E'% Decimal(0)),
                             
                         str('%.3E'% Decimal(sigma)),
                         str('%.3E'% Decimal(0)),
                             
                         str('%.3E'% Decimal(0)),
                         str('%.3E'% Decimal(0)),
                             
                         str('%.3E'% Decimal(0)),
                         str('%.3E'% Decimal(0)),
                         str('%.3E'% Decimal(0)),
                         str('%.3E'% Decimal(0)),
                          
                        
                           ], 
                         
                         'Value4':[
                         str('%.3E' % Decimal(0) ),
                         str('%.3E'% Decimal(0)),
                             
                         str('%.3E'% Decimal(0)),
                         str('%.3E'% Decimal(0)),
                             
                         str('%.3E'% Decimal(0)),
                         str('%.3E'% Decimal(0)),
                             
                         str('%.3E'% Decimal(0)),
                         str('%.3E'% Decimal(0)),
                             
                         str('%.3E'% Decimal(x)),    
                         str('%.3E'% Decimal(0)),
                         
                        str('%.3E'% Decimal(0)), 
                        str('%.3E'% Decimal(0)),   
                             
                        str('%.3E'% Decimal(0)),
                        str('%.3E'% Decimal(0)),
                        str('%.3E'% Decimal(0)), 
                        str('%.3E'% Decimal(0)),

                                   
                           ], 
                        }
    saveTabCalculosIntermedios = tabulate(tabCalculosIntermedios,  tablefmt='simple', stralign='left',floatfmt='.4f')
    print(saveTabCalculosIntermedios)

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

if __name__ == "__main__":

    os.system ("clear")

    print("            CAMPOS DE UNA ANTENA PROXIMA AL SUELO ")   

print(tabulate(presentacion, headers = 'keys', tablefmt='fancy_grid',stralign='center'))

validation = input("Precione c para visualizar ejemplo de prueba ")

if (validation):

	os.system ("clear")
	mostrarDatosGenerales(Directividad,Cte,Potencia,Frec,Distancia,h1,h2,Epsilon,Sigma,Ang_aproxRad,Ang_aproxgrd,coef_ReflexRv,angRv,coef_ReflexRh,angRh)

	val1 = input("Digite c para continuar")

	os.system ("clear")    

	Resultados_campos = []

	#variacion Frecuencia
	Var_Fre = 2
	var_dis = 2
	for i in range(0, Var_Fre):

		encabezado = {'Univ. del Cauca': [],
                'Fac. Ing. Electrónica': [],
                'Frec. = {} MHz'.format(f):[]
                         }

		print(tabulate(encabezado, headers='keys'))


		for j in range(0, var_dis):

			Espv = calcular_Espv(f, d)
			Esuv = calcular_Esuv(f, d)
			Esph = calcular_Esph(f, d)
			Esuh = calcular_Esuh(f, d)

			Rh = calcl_Rh(f, d)
			Rv = calcl_RV(f, d)

			presentarCalculos(Espv, Esuv, Esph, Esuh, Rh.real, Rv.real,0.9936, d)

			Resultados_campos.append([[d], [Espv], [Esuv], [Esph], [Esuh]])

			d += 5

		f += 0.5
		

		instruction = None
		instruction2 = None

		while  not instruction:
			instruction = input('Precione c para continuar ')

		os.system('clear')

		print('----------calculos intermedios-----------')
		CalculosIntermedios(da=d-5)

		while  not instruction2:
			instruction2 = input('Precione c para continuar ')

		os.system('clear')
		d = 5

	#for x in Resultados_campos:
		
	print(tabulate({'distancia': Resultados_campos}, headers = 'keys'))