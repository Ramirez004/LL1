# Gramatica sin recursividad por izquierda
# S  -> A B C | D E
# A  -> dos B tres | e
# B  -> B'
# B' -> cuatro C cinco B' | e
# C  -> seis A B | e
# D  -> uno A E | B
# E  -> tres

tokens = []
pos = 0

def ver():
    if pos < len(tokens):
        return tokens[pos]
    return "$"

def consumir(esperado):
    global pos
    if ver() == esperado:
        pos += 1
    else:
        raise SyntaxError(f"Esperaba '{esperado}' pero encontre '{ver()}' en pos {pos}")

def S():
    if ver() in ["uno", "tres"]:
        D(); E()
    else:
        A(); B(); C()

def A():
    if ver() == "dos":
        consumir("dos"); B(); consumir("tres")
    # si no, A -> vacio

def B():
    Bp()

def Bp():
    if ver() == "cuatro":
        consumir("cuatro"); C(); consumir("cinco"); Bp()
    # si no, B' -> vacio

def C():
    if ver() == "seis":
        consumir("seis"); A(); B()
    # si no, C -> vacio

def D():
    if ver() == "uno":
        consumir("uno"); A(); E()
    else:
        B()

def E():
    consumir("tres")

def analizar(cadena):
    global tokens, pos
    tokens = cadena.strip().split()
    pos = 0
    print(f"Analizando: {tokens if tokens else ['(vacia)']}")
    try:
        S()
        if ver() == "$":
            print("ACEPTADA\n")
        else:
            print(f"ERROR: sobran tokens desde '{ver()}'\n")
    except SyntaxError as e:
        print(f"RECHAZADA: {e}\n")

# Pruebas
analizar("")                      # vacia -> ACEPTADA
analizar("dos tres")              # A -> dos B tres
analizar("cuatro cinco")          # B' -> cuatro C cinco B'
analizar("seis")                  # C -> seis A B
analizar("cuatro cinco tres")     # S -> D E
analizar("seis uno")              # invalida -> RECHAZADA
