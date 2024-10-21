from math import ceil, floor, log2, isqrt
from random import *
from sympy.ntheory import factorint
from sympy.ntheory.modular import crt
import utils

class Group(object):
    def __init__(self, l, e, N, p, poly = None, A = None, B = None):
        self.l = l
        self.e = e
        self.N = N
        self.p = p
        self.poly = poly
        self.A = A
        self.B = B        
        if self.checkParameters() != True:
            raise Exception("Problem with parameters")
    

    def checkParameters(self):
        if self.l != "ZpAdditive" and self.l != "ZpMultiplicative" and self.l != "F2^n" and self.l != "ECConZp" and self.l != "ECC_F2^n" :
            raise Exception("l parameter is unknown")
        return (self.l == "ECConZp" and self.e == [0, 0] and ((4*self.A**3 + 27*self.B**2) % self.p != 0) ) or self.l != "ECConZp" or ((self.l == "ZpAdditive" and self.e == 0)) or (self.l == "ZpMultiplicative" and self.e == 1) or (self.l == "F2^n" and self.e == 1)


    def law(self, g1, g2):
        if self.l == "ZpMultiplicative":
            return (g1 * g2) % self.p

        if self.l == "ZpAdditive":
            return (g1 + g2) % self.p

        if self.l == "F2^n":
            p = 0
            length_poly = utils.deg(self.poly)
            while g2 != 0:
                if (g2 & 1) > 0 :
                    p = p ^ g1
                g1 = g1 << 1
                if (g1 & (1<<length_poly)) > 0 :
                    g1 = g1 ^ self.poly
                g2 = g2 >> 1
            return p
        

        if self.l == "ECConZp" or self.l == "ECC_F2^n":
            
            if g1 == self.e:
                return g2
            elif g2 == self.e:
                return g1
            elif g1[0] == g2[0] and g1[1] != g2[1]:
                return self.e
            elif g1[0] == g2[0] and g1[1] == g2[1] and g2[1] == 0:
                return self.e
            elif g1[0] == g2[0] and g1[1] == g2[1] and g2[1] != 0:
                groupMulti = Group("ZpMultiplicative", 1, self.p - 1, self.p, self.poly, self.A, self.B)
                lamda = (3*groupMulti.exp(g1[0], 2) + self.A) * groupMulti.exp(2*g1[1], -1)
                x = (groupMulti.exp(lamda, 2) - 2*g1[0]) % self.p
                y = (lamda*(g1[0] - x) - g1[1]) % self.p
                return [x, y]
            elif g1[0] != g2[0]:
                groupMulti = Group("ZpMultiplicative", 1, self.p - 1, self.p, self.poly, self.A, self.B)
                lamda = (g2[1] - g1[1])*groupMulti.exp(g2[0] - g1[0], -1)
                x = (groupMulti.exp(lamda, 2) - g1[0] - g2[0]) % self.p
                y = (lamda*(g1[0] - x) - g1[1]) % self.p
                return [x, y]

        raise Exception("ERROR")


    def exp(self, g, k):
        if k == 0 :
            return self.e
        
        h0 = self.e
        h1 = g
        
        if k == -1:
            t = floor(log2(self.N-1))
        else:            
            t = floor(log2(k))

        for i in range(t, -1, -1):    
            if k == -1:
                ki = ((self.N-1)>>i)&1
            else:            
                ki = (k>>i)&1
            if ki == 0:
                h1 = self.law(h0, h1)
                h0 = self.law(h0, h0)
            else :
                h0 = self.law(h0, h1)
                h1 = self.law(h1, h1)
        return h0 
    


class SubGroup(Group):
    def __init__(self, l, e, N, p, g, poly = None, A = None, B = None):
        Group.__init__(self, l, e, N, p, poly, A, B)
        self.g = g

    def verify(self, P):
        if P == self.e:
            return True
        return ((P[1]**2) % self.p) == ((P[0]**3 + self.A * P[0] + self.B) % self.p )

    def DLbyBabyStepGiantStep(self, h):
        w = ceil(isqrt(self.N))
        T = []
        
        for i in range(0, w+1):
            T = T + [self.exp(self.g, i*w)]
        
        for j in range(0, w+1):
            if j == 0:
                g_inverse = self.exp(self.g, 0)
            else:
                g_inverse = self.exp(self.g, -1)
                for k in range(0, j-1):
                    g_inverse = self.law(g_inverse, self.exp(self.g, -1))

            x = self.law(h, g_inverse)
            
            for i in range (0, len(T)):
                if x == T[i]:
                    return (w*i + j) % self.N
    
    def DLTrialMultiplication(self, h):
        for i in range(0, self.N):
            if self.exp(self.g, i) == h:
                return i

    def ComputeDL(self, h, tau = 1000):
        if self.N <= tau:
            return self.DLTrialMultiplication(h)
        else:
            return self.DLbyBabyStepGiantStep(h)

    def DLinPrimePowerOrderGoup(self, h, pk, ek):
        n = ceil(pow(pk, ek-1))
        y = self.exp(self.g, n)
        i = 0
        for j in range(ek):
            nj = ceil(pow(pk, ek - j - 1))
            g_inverse = self.exp(self.g, self.N-i)
            H = self.law(g_inverse, h)
            H = self.exp(H, nj)
            nouveau_sousGroupe = SubGroup(self.l, self.e, pk, self.p, y)
            t = nouveau_sousGroupe.ComputeDL(H)
            i = (i + t*self.exp(pk, j) ) % self.N
          
        return self.exp(self.g, i), i
    
    def DLbyPohligHellman(self, h):
        moduli = []
        residu = []
        for k in factorint(self.N):
            pk, ek = k, factorint(self.N)[k]
            quotient = self.N // pk**ek
            gk = self.exp(self.g, quotient)
            hk = self.exp(h, quotient)
            monSousGroupeMulti = SubGroup(self.l, self.e, pk**ek, self.p, gk)
            ik = monSousGroupeMulti.ComputeDL(hk)
            residu.append(ik)
            moduli.append(pk**ek)
            
        return crt(moduli, residu)[0]

    def testDiffieHellman(self):
        a = randint(0, self.N)
        b = randint(0, self.N)

        A = self.exp(self.g, a)
        B = self.exp(self.g, b)

        Ab = self.exp(A, b)
        Ba = self.exp(B, a)
        return Ab == Ba
    

    def DiffieHellman(self, a, b, A, B, K):
        ga = self.exp(self.g, a)
        gb = self.exp(self.g, b)
        #print("A = ", A)
        Ab = self.exp(A, b)
        Ba = self.exp(B, a)
        if self.l == "ECConZp":
            return (A == ga and B == gb and Ab == Ba)
        else:
            return (A == ga and B == gb and K == Ab and Ab == Ba)


    def ecdsa_sign(self, m, sk, testK = None):
        if(testK):
            k = testK
        else:
            k = randint(1, self.N - 1)
        #k = 0x7a1a7e52797fc8caaa435d2a4dace39158504bf204fbe19f14dbb427faee50ae
        K = self.exp(self.g, k)
        
        groupMulti = Group("ZpMultiplicative", 1, self.p - 1, self.p, self.poly, self.A, self.B)
        t = K[0] % self.N
        s = ((m + sk*t) * pow(k, -1, self.N))% self.N
        return [t,s]
    
    def ecdsa_verif(self, m, s, t, pubk):
        if (t < 1 or t > self.N-1) or (s < 1 or s > self.N-1):
            return False
        
        R = self.law(self.exp(self.g, m*pow(s, -1, self.N)), self.exp(pubk, t*pow(s, -1, self.N)))
        
        if(R[0]%self.N != t):
            return False
        
        return True