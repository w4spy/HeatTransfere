from math import exp, log

class Exchanger:

    def __init__(self):
        #parameters entry
        print("[!] enter fluid 1 parameters")
        self.m1 = float(input("Qm1 (kg/h)> "))/3600
        self.t1 = float(input("T1 (c°)> "))
        self.cp1 = float(input("cp1 (kj/kg.c°)> "))
        print("\n[!] enter fluid 2 parameters")
        self.m2 = float(input("Qm2 (kg/h)> "))/3600
        self.t2 = float(input("T1 (c°)> "))
        self.cp2 = float(input("cp2 (kj/kg.c°)> "))
        self.s = float(input("\n[!] enter la surface d'échange (m²)> "))
        self.k = float(input("[!] enter cof globale (w/m².c°)> "))/1000

    #calcul nut
    def nute(self):
        self.c1 = self.m1 * self.cp1
        self.c2 = self.m2 * self.cp2

        if self.c1 > self.c2:
            self.Cmin = self.c2
        else:
            self.Cmin = self.c1
        self.nut = (self.k * self.s) / self.Cmin
        return self.nut

    #calcul de efficacité
    def effi(self):
        self.z = self.c1 / self.c2 
        x = exp(-(1 - self.z) * self.nut)
        self.E = 1 - x / 1 - (self.z * x)
        return self.E
    
    #calcule de temp
    def temp(self):
        self.Tmm = self.t1 - self.t2
        T1s = self.t1 - self.E * self.Tmm
        T2s = self.z * (self.t1 - T1s) + self.t2
        Te = self.t1 - T2s
        Ts = T1s - self.t2 
        Tme = (Te - Ts) / log(Te/Ts)
        return T1s,T2s,Tme 

    #calcule de Q
    def Qu(self):
        Q = self.k * self.s * self.Tmm
        return Q

def main():
    run = Exchanger()
    print("\n__résultat__\n")
    print("Nut = ",run.nute())
    print("Efficacité = ",run.effi())
    r = run.temp()
    print(f"T1s = {r[0]} C°\nT2s = {r[1]} C°\n∆Tme = {r[2]} C°")
    print("Q = ",run.Qu(),"KW")

if __name__== "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        print("\nI accept only numbers")

input("\ncontinue.")
