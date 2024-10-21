import classLabs
import hashlib

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
    print("Verify with [Gx, Gy] :", monSousGroup.verify(G))

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

    b = int.from_bytes(ecdhkeyBob[7:39], byteorder = 'big') # cle prive bob
    Bb = int.from_bytes(ecdhkeyBob[57:], byteorder = 'big') # cle pub bob
    xB = int.from_bytes(ecdhkeyBob[57:89], byteorder = 'big') # cle pub bob
    yB = int.from_bytes(ecdhkeyBob[89:], byteorder = 'big') # cle pub bob
    pointB = [xB, yB]

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

    print("\n ===== PART 4 =====")

    m = "Example of ECDSA with P-256"
    h = 0xa41a41a12a799548211c410c65d8133afde34d28bdd542e4b680cf2899c8a8c4
    sk = 0xc477f9f65c22cce20657faa5b2d1d8122336f851a508a1ed04e479c34985bf96
    k = 0x7a1a7e52797fc8caaa435d2a4dace39158504bf204fbe19f14dbb427faee50ae
    t = 0x2b42f576d07f4165ff65d1f3b1500f81e44c316f1f0b3ef57325b69aca46104f
    s = 0xdc42c2122d6392cd3e3a993a89502a8198c1886fe69d262c4b329bdb6b63faf1
    
    hashed_obj = hashlib.sha256()
    hashed_m = m.encode('utf8')
    hashed_obj.update(hashed_m)
    hashed_m_str = hashed_obj.hexdigest()
    hm = int(hashed_m_str, 16)
    print("Verification hash : ", h == hm)
    print("Signature ECDSA :", [t, s] == monSousGroupeDH.ecdsa_sign(hm, sk, k))

    t1 = h * pow(s, -1, N) % N
    t2 = t * pow(s, -1, N) % N
    Q1 = monSousGroupeDH.exp(G,t1)
    pk = monSousGroupeDH.exp(G, sk)
    Q2 = monSousGroupeDH.exp(pk, t2)
    print("Verification signature ECDSA :", monSousGroupeDH.ecdsa_verif(hm, s, t, pk))

    print("\n ===== PART 6 =====")
    
    B = 2982236234343851336267446656627785008148015875581
    Gx = 5759917430716753942228907521556834309477856722486
    Gy = 1216722771297916786238928618659324865903148082417
    N = 0x40000000000000000000292fe77e70c12a4234c33
    G = [Gx, Gy]
    poly = (1<<163)^(1<<7)^(1<<6)^(1<<3)^1
    courbePart6 = classLabs.SubGroup("ECC_F2^n", idElement, N, p, G, poly, 1, B)
    print("Verify with [0, 0] :", courbePart6.verify(idElement))
    print("Verify with [Gx, Gy] :", courbePart6.verify(G))
    print("testDiffieHellman using B-163 :", courbePart6.testDiffieHellman())

    m = "Example of ECDSA with B-163"
    h = 0x728d59bbe028509dd5d2ce480f458e2925232ac3 
    d = 0x348d138c2de9447bd288feed177222ee377fb7bea 
    Qx = 0x66b015c0b72b0f81b1ecba6f58e7545d94744644c
    Qy = 0xba6d4d62419155b186a29784f4aa4b8e8e1e7f76 
    k = 0x8ed0f93f7d492bb3991847d0e96f9cc3947259aa
    Kx = 0x760938a97d88b30fdfb2cce1a4c59783ad0ed8fde
    inv_Kx = 0x36dc66491684211373aaa8bd16024dd0a12a8ff11
    t = 0x360938a97d88b30fdfb2a3b1bd4726c282cca43ab
    s = 0x19a7b5043d93a13d714b4717fc0698e6791cf7f7c
    inv_s = 0x35417609847921e6d0e2691d924335adf62c1b6b2 % N
    inv_hs = 0x3c4099db241a80c807e02d81be10955b2eb2e5d8c % N
    inv_ts = 0x160ccedabb7e3e767a604d8b042a65751708cc262 % N
    Rx = 0x760938a97d88b30fdfb2cce1a4c59783ad0ed8fde
    
    hashed_obj = hashlib.sha1()
    hashed = m.encode('utf-8')
    hashed_obj.update(hashed)
    hashed_m_str = hashed_obj.hexdigest()
    hm = int(hashed_m_str, 16)
    print("Verification hash : ", h == hm)
    print("Signature ECDSA :", [t, s] == monSousGroupeDH.ecdsa_sign(hm, d, k))
    
    t1 = h * pow(s, -1, N) % N
    t2 = t * pow(s, -1, N) % N
    Q1 = monSousGroupeDH.exp(G,t1)
    pk = monSousGroupeDH.exp(G, d)
    Q2 = monSousGroupeDH.exp(pk, t2)
    print("Verification signature ECDSA :", monSousGroupeDH.ecdsa_verif(hm, s, t, pk))



testLabs1_part2()