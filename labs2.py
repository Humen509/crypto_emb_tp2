import classLabs

B = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5

G = [Gx, Gy]
idElement = [0, 0]

def testLabs1_part2():
    N = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
    p = (1<<256) - (1<<224) + (1<<192) + (1<<96) - 1
    B = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
    A = -3
    Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
    Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
    G = [Gx, Gy]
    idElement = [0, 0]

    print("\n ===== PART 1 =====")
    monSousGroup = classLabs.SubGroup("ECConZp", idElement, N, p, G, None, A, B)
    print("Test 0 infiny :", monSousGroup.verify([0, 0]))
    googlePublicKey = open("google-fr.der", 'rb')
    PK = googlePublicKey.read()[0xb0 + 15 : 0xf0 + 15]
    Pkx = int.from_bytes(PK[:len(PK) // 2], byteorder='big')
    Pky = int.from_bytes(PK[len(PK) // 2:], byteorder='big')
    googlePublicKey.close()
    print("Pk :", PK)
    print("Pkx :", hex(Pkx))
    print("Pky :", hex(Pky))
    print("Test Google :", monSousGroup.verify([Pkx, Pky]))

    print("\n ===== PART 2 =====")

    print("Test DiffieHellman dans Courbe Elli : ", monSousGroup.testDiffieHellman())

    #A = 1
    #B = 2
    #P = [4, 9]
    #monGroup = classLabs.Group("ECConZp", idElement, 16, 11, None, A, B)
    #print("Test courbe (1, 1) et (1, 1) :", monGroup.law(P, [0,0]))
    #print("Test courbe (1, 1) et (1, 1) :", monGroup.law(P, P))
    #print("Test courbe (1, 1) et (1, 1) :", monGroup.law(2*P, P))
    #print("Test courbe (1, 1) et (1, 1) :", monGroup.law(3*P, P))
    #print("Test courbe (1, 1) et (1, 1) :", monGroup.law(4*P, P))
    #print("Test courbe (1, 1) et (1, 1) :", monGroup.law(5*P, P))
    #print("Test courbe (1, 1) et (1, 1) :", monGroup.law(6*P, P))
    #print("Test courbe (1, 1) et (1, 1) :", monGroup.law(7*P, P))


testLabs1_part2()