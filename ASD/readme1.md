# Ejercicio 1 - Analizador Sintactico Descendente Recursivo (ASDR)

Lenguajes de Programacion - Procesadores de Lenguaje

---

## Gramatica original

```
S  -> A B C
S  -> D E
A  -> dos B tres
A  -> ε
B  -> B cuatro C cinco   (recursiva por la izquierda!)
B  -> ε
C  -> seis A B
C  -> ε
D  -> uno A E
D  -> B
E  -> tres
```

---

## a) Eliminar recursividad por la izquierda

Solo **B** tiene recursividad por la izquierda.

Se aplica la formula:
> Si `X -> X α | β`  entonces:  `X -> β X'`  y  `X' -> α X' | ε`

Resultado:

```
B  -> B'
B' -> cuatro C cinco B'
B' -> ε
```

**Gramatica sin recursividad:**

```
S  -> A B C
S  -> D E
A  -> dos B tres
A  -> ε
B  -> B'
B' -> cuatro C cinco B'
B' -> ε
C  -> seis A B
C  -> ε
D  -> uno A E
D  -> B
E  -> tres
```

---

## b) Conjuntos PRIMEROS

| No terminal | PRIMEROS |
|-------------|----------|
| E           | { tres } |
| B'          | { cuatro, ε } |
| B           | { cuatro, ε } |
| A           | { dos, ε } |
| C           | { seis, ε } |
| D           | { uno, cuatro, ε } |
| S           | { dos, cuatro, seis, uno, tres, ε } |

---

## b) Conjuntos SIGUIENTES

| No terminal | SIGUIENTES |
|-------------|------------|
| S           | { $ } |
| A           | { cuatro, cinco, seis, tres, $ } |
| B           | { seis, cinco, tres, $ } |
| B'          | { seis, cinco, tres, $ } |
| C           | { cinco, $ } |
| D           | { tres } |
| E           | { $ } |

---

## b) Conjuntos de Prediccion

| Produccion | Prediccion |
|------------|------------|
| S -> A B C | { dos, cuatro, seis, uno, tres, $ } |
| S -> D E   | { uno, cuatro, tres } |
| A -> dos B tres | { dos } |
| A -> ε     | { cuatro, cinco, seis, tres, $ } |
| B -> B'    | { cuatro, seis, cinco, tres, $ } |
| B' -> cuatro C cinco B' | { cuatro } |
| B' -> ε    | { seis, cinco, tres, $ } |
| C -> seis A B | { seis } |
| C -> ε     | { cinco, $ } |
| D -> uno A E | { uno } |
| D -> B     | { cuatro, tres } |
| E -> tres  | { tres } |

---

## Es LL(1)?

**NO**, la gramatica no es LL(1).

El problema esta en **S**: los conjuntos de prediccion de sus dos producciones se intersecan.

```
S -> A B C  =>  { dos, cuatro, seis, uno, tres, $ }
S -> D E    =>  { uno, cuatro, tres }

Interseccion: { uno, cuatro, tres }  ← CONFLICTO
```

Con entrada `uno`, `cuatro` o `tres` el analizador no sabe que produccion elegir.

---

## Como ejecutar

```bash
python parser.py
```

Salida esperada para `analizar("uno tres")`:

```
Analizando: ['uno', 'tres']
Entrando a S
Entrando a D
Entrando a A
  A -> vacio
Entrando a E
  [match] 'tres' OK
>>> CADENA ACEPTADA <<<
```

---

## Estructura del codigo

```
parser.py
│
├── lookahead()   # mira el token actual
├── match()       # consume un token
│
├── S()           # no terminal S
├── A()           # no terminal A
├── B()           # no terminal B (llama a Bp)
├── Bp()          # no terminal B'
├── C()           # no terminal C
├── D()           # no terminal D
├── E()           # no terminal E
│
└── analizar()    # funcion principal para probar cadenas
```
