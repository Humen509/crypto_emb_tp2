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

    print("\n ===== PART 3 =====")
    
    aliceKey = open("ecdhkeyAlice.der", 'rb')
    alicePub = open("ecdhpubAlice.der", 'rb')
    ecdhkeyAlice = aliceKey.read() # pour a
    ecdhpubAlice = alicePub.read() # pour A
    aliceKey.close()
    alicePub.close()

    bobKey = open("ecdhkeyBob.der", 'rb')
    bobPub = open("ecdhpubBob.der", 'rb')
    ecdhkeyBob = bobKey.read() # pour b
    ecdhpubBob = bobPub.read() # pour B
    bobKey.close()
    bobPub.close()

    a = int.from_bytes(ecdhkeyAlice[7:39], byteorder = 'big') # cle prive alice
    Aa = int.from_bytes(ecdhkeyAlice[57:], byteorder = 'big') # cle pub alice
    xA = int.from_bytes(ecdhkeyAlice[57:89], byteorder = 'big') # cle pub alice
    yA = int.from_bytes(ecdhkeyAlice[89:], byteorder = 'big') # cle pub alice
    pointA = [xA, yA]

    #print("a =", hex(a))
    #print("Aa =", hex(Aa))
    #print("xA =", hex(xA))
    #print("yA =", hex(yA))

    b = int.from_bytes(ecdhkeyBob[7:39], byteorder = 'big') # cle prive bob
    Bb = int.from_bytes(ecdhkeyBob[57:], byteorder = 'big') # cle pub bob
    xB = int.from_bytes(ecdhkeyBob[57:89], byteorder = 'big') # cle pub bob
    yB = int.from_bytes(ecdhkeyBob[89:], byteorder = 'big') # cle pub bob
    pointB = [xB, yB]

    #print("b =", hex(b))
    #print("Bb =", hex(Bb))
    #print("xB =", hex(xB))
    #print("yB =", hex(yB))

    key1 = open("ecdhkey1.bin", 'rb')
    ecdhkey1 = key1.read()
    key1.close()
    K1 = int.from_bytes(ecdhkey1, byteorder = 'big')

    key2 = open("ecdhkey2.bin", 'rb')
    ecdhkey2 = key2.read()
    key2.close()
    K2 = int.from_bytes(ecdhkey2, byteorder = 'big')
    
    N = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
    p = (1<<256) - (1<<224) + (1<<192) + (1<<96) - 1
    B = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
    A = -3
    Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
    Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
    G = [Gx, Gy]
    idElement = [0, 0]
    monSousGroupeDH = classLabs.SubGroup("ECConZp", idElement, N, p, G, None, A, B)

    print("DiffieHellman sur fichier dh avec K1: ", monSousGroupeDH.DiffieHellman(a, b, pointA, pointB, K1))
    print("DiffieHellman sur fichier dh avec K2: ", monSousGroupeDH.DiffieHellman(a, b, pointA, pointB, K2))

testLabs1_part2()