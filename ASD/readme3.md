# Ejercicio 3 - ASDR

## Gramática original
```
S → A B C
S → S uno      ← recursividad por la izquierda
A → dos B C | ε
B → C tres | ε
C → cuatro B | ε
```

## a) Eliminar recursividad por la izquierda

`S → S uno` es recursiva izquierda. Se transforma así:

- Antes: `S → A B C | S uno`
- Después:
```
S  → A B C S'
S' → uno S' | ε
```

### Gramática resultante
```
S  → A B C S'
S' → uno S' | ε
A  → dos B C | ε
B  → C tres  | ε
C  → cuatro B | ε
```

## b) PRIMEROS

| No Terminal | PRIMEROS |
|-------------|----------|
| C  | { cuatro, ε } |
| B  | { cuatro, ε } |
| A  | { dos, ε } |
| S' | { uno, ε } |
| S  | { dos, cuatro, ε } |

## SIGUIENTES

| No Terminal | SIGUIENTES |
|-------------|------------|
| S  | { $ } |
| S' | { $ } |
| A  | { cuatro, uno, $ } |
| B  | { cuatro, uno, $ } |
| C  | { tres, uno, cuatro, $ } |

## Conjuntos de Predicción

| Regla | Predicción |
|-------|-----------|
| S → A B C S' | { dos, cuatro, uno, $ } |
| S' → uno S' | { uno } |
| S' → ε | { $ } |
| A → dos B C | { dos } |
| A → ε | { cuatro, uno, $ } |
| B → C tres | { cuatro } |
| B → ε | { cuatro, uno, $ } |
| C → cuatro B | { cuatro } |
| C → ε | { tres, uno, cuatro, $ } |

## ¿Es LL(1)?

**No del todo.** Hay conflicto en B y en C:

- `B → C tres` y `B → ε` comparten `cuatro` (porque C puede empezar con `cuatro`)
- `C → cuatro B` y `C → ε` comparten `cuatro`

Eso genera ambigüedad. La gramática resultante **no es LL(1)**.

## Cómo ejecutar

```bash
python asdr.py
```
