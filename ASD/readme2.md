# Ejercicio 2 - ASDR

## Gramática
```
S → B uno | dos C | ε
A → S tres B C | cuatro | ε
B → A cinco C seis | ε
C → siete B | ε
```

## a) PRIMEROS

| No Terminal | PRIMEROS |
|-------------|----------|
| S | { dos, cuatro, cinco, ε } |
| A | { dos, cuatro, cinco, ε } |
| B | { dos, cuatro, cinco, ε } |
| C | { siete, ε } |

## b) SIGUIENTES

| No Terminal | SIGUIENTES |
|-------------|------------|
| S | { tres, uno, seis, siete, $ } |
| A | { cinco } |
| B | { uno, seis, siete, $ } |
| C | { seis, $ } |

## c) Conjuntos de Predicción

| Regla | Predicción |
|-------|-----------|
| S → B uno | { dos, cuatro, cinco, uno } |
| S → dos C | { dos } |
| S → ε | { tres, uno, seis, siete, $ } |
| A → S tres B C | { dos, cuatro, cinco, tres } |
| A → cuatro | { cuatro } |
| A → ε | { cinco } |
| B → A cinco C seis | { dos, cuatro, cinco } |
| B → ε | { uno, seis, siete, $ } |
| C → siete B | { siete } |
| C → ε | { seis, $ } |

## d) ¿Es LL(1)?

**No.** El token `dos` aparece en los conjuntos de predicción de `S → B uno` y `S → dos C` al mismo tiempo. Eso es un conflicto y la gramática no puede ser LL(1).

## e) Cómo ejecutar

```bash
python asdr.py
```
