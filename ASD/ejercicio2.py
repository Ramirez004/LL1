#   S -> B uno
#   S -> dos C
#   S -> epsilon
#   A -> S tres B C
#   A -> cuatro
#   A -> epsilon
#   B -> A cinco C seis
#   B -> epsilon
#   C -> siete B
#   C -> epsilon

tokens = []
pos = 0

def token_actual():
    if pos < len(tokens):
        return tokens[pos]
    return '$'

def consumir(esperado):
    global pos
    if token_actual() == esperado:
        print(f"  consumiendo: {esperado}")
        pos += 1
    else:
        raise SyntaxError(f"Error: se esperaba '{esperado}' pero se encontro '{token_actual()}'")

# PRIMEROS:
#   PRIMEROS(S) = { cinco (via B->A cinco..., A->epsilon), dos, epsilon, uno (via B->epsilon) }
#   En la practica: PRIMEROS(S) = { cuatro, cinco, dos, epsilon }
#   PRIMEROS(A) = { cuatro, cinco, epsilon, dos }
#   PRIMEROS(B) = { cuatro, cinco, epsilon, dos }
#   PRIMEROS(C) = { siete, epsilon }

# SIGUIENTES:
#   SIGUIENTES(S) = { tres, $, uno, dos, cuatro, cinco, siete }
#   SIGUIENTES(A) = { cinco }
#   SIGUIENTES(B) = { uno, seis, siete, $ }
#   SIGUIENTES(C) = { seis, $ }

def parse_S():
    print("S ->", end=" ")
    t = token_actual()

    # S -> B uno  (prediccion: PRIMEROS(B uno) = PRIMEROS(B) - {eps} U {uno} U ...)
    # S -> dos C  (prediccion: { dos })
    # S -> epsilon (prediccion: SIGUIENTES(S))

    if t == 'dos':
        print("dos C")
        consumir('dos')
        parse_C()
    elif t in ('cuatro', 'cinco', 'dos'):
        # B puede derivar en esas cosas, pero 'dos' ya fue tomado arriba
        # este caso no ocurre aqui realmente
        print("B uno")
        parse_B()
        consumir('uno')
    elif t in ('tres', '$', 'uno', 'seis', 'siete'):
        # S -> epsilon: token en SIGUIENTES(S)
        print("epsilon")
    else:
        # intentar S -> B uno
        print("B uno")
        parse_B()
        consumir('uno')

def parse_A():
    print("A ->", end=" ")
    t = token_actual()

    if t == 'cuatro':
        print("cuatro")
        consumir('cuatro')
    elif t == 'cinco':
        # A -> epsilon no corresponde, pero cinco pertenece a PRIMEROS(B->A cinco...)
        # Si estamos en A y viene 'cinco', es epsilon (cinco pertenece a SIGUIENTES(A))
        print("epsilon")
    elif t in ('dos', 'siete', 'tres', '$'):
        # A -> S tres B C: PRIMEROS incluye dos, epsilon de S
        # Si t in PRIMEROS(S) o PRIMEROS(S) contiene eps y t == 'tres'
        if t in ('dos',):
            print("S tres B C")
            parse_S()
            consumir('tres')
            parse_B()
            parse_C()
        else:
            print("epsilon")
    else:
        print("epsilon")

def parse_B():
    print("B ->", end=" ")
    t = token_actual()

    # B -> A cinco C seis  prediccion: PRIMEROS(A cinco C seis)
    # PRIMEROS(A) incluye epsilon, por lo que si A->eps, el primero util es 'cinco'
    # Tokens de prediccion: { cuatro, cinco, dos }  (cuatro y dos de PRIMEROS(A)-{eps}, cinco directo)
    # B -> epsilon  prediccion: SIGUIENTES(B) = { uno, seis, siete, $ }

    if t in ('cuatro', 'cinco', 'dos'):
        print("A cinco C seis")
        parse_A()
        consumir('cinco')
        parse_C()
        consumir('seis')
    elif t in ('uno', 'seis', 'siete', '$'):
        print("epsilon")
    else:
        print("epsilon")

def parse_C():
    print("C ->", end=" ")
    t = token_actual()

    # C -> siete B  prediccion: { siete }
    # C -> epsilon  prediccion: SIGUIENTES(C) = { seis, $ }

    if t == 'siete':
        print("siete B")
        consumir('siete')
        parse_B()
    elif t in ('seis', '$', 'tres', 'uno'):
        print("epsilon")
    else:
        print("epsilon")

def analizar(entrada):
    global tokens, pos
    tokens = entrada.split()
    pos = 0
    print(f"\nAnalizando: {entrada}")
    print("-" * 40)
    try:
        parse_S()
        if token_actual() == '$':
            print("-" * 40)
            print("Cadena ACEPTADA")
        else:
            print(f"Error: tokens restantes desde '{token_actual()}'")
    except SyntaxError as e:
        print(e)
        print("Cadena RECHAZADA")

# Pruebas
if __name__ == "__main__":
    print("=" * 50)
    print("ASDR - Ejercicio 2")
    print("=" * 50)

    # cadena vacia (S -> epsilon)
    analizar("$")

    # S -> dos C, C -> epsilon
    analizar("dos $")

    # S -> dos C, C -> siete B, B -> epsilon
    analizar("dos siete $")

    # S -> B uno, B -> A cinco C seis, A -> cuatro, C -> epsilon
    analizar("cuatro cinco seis uno $")

    # S -> B uno, B -> A cinco C seis, A -> epsilon, C -> siete B, B -> epsilon
    analizar("cinco siete seis uno $")
