#   S  -> A B C
#   S  -> S uno   (recursividad izquierda)
#   A  -> dos B C
#   A  -> epsilon
#   B  -> C tres
#   B  -> epsilon
#   C  -> cuatro B
#   C  -> epsilon
#
# Despues de eliminar recursividad izquierda en S:
#   S  -> A B C S'
#   S' -> uno S' | epsilon
#   A  -> dos B C | epsilon
#   B  -> C tres  | epsilon
#   C  -> cuatro B | epsilon
#
# PRIMEROS:
#   PRIMEROS(C)  = { cuatro, epsilon }
#   PRIMEROS(B)  = { cuatro, tres(no), epsilon }  -> PRIMEROS(C)-{eps} U {epsilon} = { cuatro, epsilon }
#   PRIMEROS(A)  = { dos, epsilon }
#   PRIMEROS(S') = { uno, epsilon }
#   PRIMEROS(S)  = PRIMEROS(A B C S')
#               -> PRIMEROS(A)-{eps} U (si A->eps) PRIMEROS(B)-{eps} U ... = { dos, cuatro, epsilon }
#
# SIGUIENTES:
#   SIGUIENTES(S)  = { $ }
#   SIGUIENTES(S') = { $ }   (S' al final de S, SIGUIENTES(S) propagado)
#   SIGUIENTES(A)  = PRIMEROS(B C S') - {eps} U (si BCS'->eps) SIGUIENTES(S)
#                 = { cuatro, $ }
#   SIGUIENTES(B)  = PRIMEROS(C S') - {eps} U ... = { cuatro, uno, $ }
#                   + { tres } desde B -> C tres (SIGUIENTES(B) en C tres: tras C viene tres)
#                   Realmente SIGUIENTES(B) se calcula mirando donde aparece B:
#                     S -> A B C S': tras B viene C S', PRIMEROS(C)-{eps}={cuatro}, si C->eps sigue S' -> PRIMEROS(S')-{eps}={uno}, si S'->eps -> SIGUIENTES(S)={$}
#                     A -> dos B C:  tras B viene C, PRIMEROS(C)-{eps}={cuatro}, si C->eps -> SIGUIENTES(A)={cuatro,$}
#                   = { cuatro, uno, $ }
#   SIGUIENTES(C)  = { tres } (de B -> C tres) U PRIMEROS(S')-{eps} (de S -> ABC S', tras C viene S') U si S'->eps SIGUIENTES(S)
#                   + SIGUIENTES(A) si C al final de A -> dos B C
#                 = { tres, uno, $, cuatro }

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

def parse_S():
    print("S -> A B C S'")
    parse_A()
    parse_B()
    parse_C()
    parse_Sp()

def parse_Sp():
    t = token_actual()
    if t == 'uno':
        print("S' -> uno S'")
        consumir('uno')
        parse_Sp()
    else:
        print("S' -> epsilon")

def parse_A():
    t = token_actual()
    if t == 'dos':
        print("A -> dos B C")
        consumir('dos')
        parse_B()
        parse_C()
    else:
        print("A -> epsilon")

def parse_B():
    t = token_actual()
    if t == 'cuatro':
        print("B -> C tres")
        parse_C()
        consumir('tres')
    else:
        print("B -> epsilon")

def parse_C():
    t = token_actual()
    if t == 'cuatro':
        print("C -> cuatro B")
        consumir('cuatro')
        parse_B()
    else:
        print("C -> epsilon")

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
            print(f"Error: tokens sobrantes desde '{token_actual()}'")
            print("Cadena RECHAZADA")
    except SyntaxError as e:
        print(e)
        print("Cadena RECHAZADA")

if __name__ == "__main__":
    print("=" * 50)
    print("ASDR - Ejercicio 3")
    print("=" * 50)

    # S -> A B C S', todos epsilon
    analizar("$")

    # S -> A B C S', S' -> uno S' -> epsilon
    analizar("uno $")

    # S -> A(dos B C) B C S'
    # A -> dos B(epsilon) C(epsilon), luego B(epsilon) C(epsilon) S'(epsilon)
    analizar("dos $")

    # C -> cuatro B(epsilon), B -> C tres -> cuatro B(epsilon) tres
    analizar("cuatro tres $")

    # dos + cuatro tres + uno
    analizar("dos cuatro tres uno $")
