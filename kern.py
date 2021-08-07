import math

print("****** Method De Kern ********")
#####lES CONSTANTS######
#Les Constants de coté chaud
Tce = 71.0
Tcs = 49.0
cpc = 2.38
kc = 0.129
viscoc = 0.0002
Rdc = 0.000025
Sgc = 0.685
mvc = 685.0

#Les Constants de cote froid
Tfe = 24.0
Tfs = 49.0
mf = 67500.0
cpf = 2.0
kf = 0.143
Rdf = 0.000049
Sgf = 0.8

#constants general
R = 0.88
P = 0.529

#============================================================================================================
#energy balance
Q = mf*cpf*(Tfs-Tfe)
mc= Q/(cpc*(Tce-Tcs))
print("[+]La puissance = ",Q) #W
print("[+]Le débit de fluid chaud = ",mc)#Kg/h

#facteur de correction
S1 = math.sqrt((math.pow(R,2) + 1 ))* math.log((1-P)/(1-R*P))
S2 = (R-1)*math.log((2-P*(R+1-(math.sqrt(math.pow(R,2)+1))))/(2-P*(R+1+math.sqrt(math.pow(R,2)+1))))
Ft = S1/S2
print("[+]Le facteur de correction = ",Ft)

#DTLM
DTa=Tce-Tfs                                                                                                 
DTb=Tcs-Tfe
DTLM =(DTa-DTb)/(math.log(DTa/DTb))
print("[+]DTLM = ",DTLM) # degree celcuis 

#la surface d'echange 
while True:
    Uass = float(input("Entrer le coef d'échange consideré >> "))
    A = ((Q/3600)/(Uass*Ft*DTLM))*(10**3)
    print("[+]La surface d'echange = ",A) #meter carre

    #le nombre des tubes 
    do = float(input("Entrer le diametre exterieur des tubes >> "))
    Lt = float(input("Entrer La Longueur des tubes >> ")) 
    nt = (A) /(math.pi*do*10**(-3)*Lt)
    print("[+]nombre du tubes",nt) 

    #la vitesse de fluide
    np = float(input("Entrer le nombre des passes >> ")) 
    di = float(input("Entrer le diametre interieur des tubes >>"))    

    visco = 0.0016   
    mv = 800.0

    nta = float(input("Entrer le nombre des tubes assume >> ")) 
    Re = (4*(mf/3600)*(np/nta))/(math.pi*di*10**(-3)*visco)
    print("[+]Le nombre de RYNOLDS cote tubes = ",Re)
    V = (Re*visco)/(di*10**(-3)*mv)
    print("[+]La vitesse de fluide cote tubes = ",V) #m/s

    if Re < 10**4:
        print("[+]Le nombre de Rynolds est inferieur a 10^4 essayer avec des nouveaux parametres !")
    else:
        print("[+]le nombre de Rynolds est grand que 10**4")
        break

#le coef d'echange cote tubes
jH = float(input("Entrer le coeficient de transfert cote tubes jH >>")) #has no unit
cpt = cpf
kt = kf
viscot = visco

pr3 = ((viscot*cpt*10**3)/kt)**(0.3333333)
h = (kt*jH*(pr3))/(di*10**(-3))
print("[+]le coeficient d'echange cote tubes h= ",h) #W/m2 . C

#le diametre interieur de calandre
st = str(input("Carre 'c' ou triangelaire 't' disposition ? >> "))
Pt = float(input("Entre la distance entre les centres des tubes >> "))

if st == 'c':
    De= (4*((Pt**2)-(((math.pi)*(do**2))/4)))/(math.pi*do)
    print("[+]Le diametre equivalent De = ",De) #mm

elif st == 't':
    De = (4*((0.5*Pt*0.86*Pt)-(0.5*(math.pi*do**2)/4)))/(0.5*math.pi*do)
    print("[+]Le diametre equivalent De = ",De)#mm

#le coefcient d'echange cote calandre
clr = float(input("Entrer clearence >> ")) #mm
spacing = float(input("Entrer l'espace entre les chicanes >> ")) #mm
Ds = float(input("Entrer le diametre exterieur de la calandre >> "))  #mm  

a = ((clr*10**(-3))*(spacing*10**(-3))*(Ds*10**(-3)))/(Pt*10**(-3))
print("[+]Shell side cross flow area = ",a)

Gs = (mc/3600)/a
print("[+]Gs = ",Gs) #Kg/m2 . s 

Vc = Gs/mvc
print("[+]La vitesse de fluide cote calandre = ",Vc) #m/s

Re2 = (De*10**(-3)*Gs)/viscoc
print("[+]Le nombre de Rynolds cote calandre Re = ",Re2)

cpt = cpc
kt = kc
viscot = viscoc

jH2 = float(input("Entrer le coeficient de transfert cote calandre jH >> "))
jH=jH2
pr3 = ((viscot*cpt*10**3)/kt)**(0.3333333)
h2 = (kt*jH*(pr3))/(De*10**(-3))
print("[+]Coef d'echange cote calandre = ",h2) #W/m2 . C

#le coeficient d'echange globale
km = float(input("Entrer la conductivite de materiaux des tubes >> "))    
A0 = float(math.pi * (do**2))
Ai = float(math.pi * (di**2))

Ucal = 1/((1/h2)+(Rdc)+(A0/Ai)*((do-di)*10**(-3))/((2*km))+((A0/Ai)*(1/h))+((A0/Ai)*Rdf))  #W/m2 . C

print("[+]Ucal = ",Ucal)
print("[+]Uass = ",Uass)

#error
error = (Ucal - Uass)/(Uass)
print("[!]error = ",error)

#les petes de charges 
print("********* LES PERTES DE CHARGES *********")

f = float(input("Entrer le facteur de friction cote tubes >> ")) #factor has no unit        

DPt = np*(((8*f)*(Lt/(di*10**(-3))))+2.5)*((mv*(V**2))/2)
print("[+]Les pertes de charges cote tube DPt = ", DPt*10**(-5)) #Bar

#les pertes de charges cote calandre
fs = float(input("Entrer facteur de friction cote calandre >> "))  #factor has no unit    
DPs = 8*(fs)*(Ds/De)*(Lt/(spacing*10**(-3)))*(((mvc*Vc**2))/2) 
print("[+]les pertes de charges cote calandre = ",DPs*10**(-5))#Bar 

#Over Surface
hio = h*(di/do)
Uc = (h2*hio)/(h2+hio)
osc = (Uc - Ucal)/Uc

#over design
print("\n \n \n*********** LA SUR-CONCEPTION ***********")
Asup = math.pi*do*10**(-3)*Lt*nta
ovd = (Asup - A)/A
print("[+]La surconception = ",ovd)
print("[+]10% est accepté")
