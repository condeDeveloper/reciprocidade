"""A lei de reciprocidade quadratica, e os dois suplementos.

Gauss chamou de *theorema aureum* e provou de oito jeitos diferentes. Para p e q
primos impares distintos:

    (p/q) * (q/p) = (-1)^((p-1)/2 * (q-1)/2)

ou seja: os dois simbolos sao iguais, EXCETO quando p e q deixam os dois resto 3
na divisao por 4, e nesse caso sao opostos. Os suplementos cuidam dos casos que
a lei nao cobre:

    (-1/p) = 1 se p == 1 (mod 4)
    ( 2/p) = 1 se p == 1 ou 7 (mod 8)

Nada disso e usado como atalho em lugar nenhum: tudo e conferido contra o
criterio de Euler, par a par.
"""

from .legendre import por_euler


def sinal_da_lei(p, q):
    """O lado direito da lei: 1 se os simbolos batem, -1 se sao opostos."""
    return -1 if p % 4 == 3 and q % 4 == 3 else 1


def conferir_lei(primos):
    """Confere a lei em todo par de primos impares distintos da lista.

    Devolve (conferidos, falhas, opostos), com `opostos` contando os pares em
    que os dois simbolos sao diferentes - que e o caso raro da lei.
    """
    impares = [p for p in primos if p > 2]
    conferidos = 0
    falhas = []
    opostos = 0
    for i, p in enumerate(impares):
        for q in impares[i + 1 :]:
            conferidos += 1
            esquerda = por_euler(p, q) * por_euler(q, p)
            direita = sinal_da_lei(p, q)
            if esquerda != direita:
                falhas.append((p, q))
            if direita == -1:
                opostos += 1
    return conferidos, falhas, opostos


def conferir_suplemento_menos_um(primos):
    """(-1/p) = 1 exatamente quando p deixa resto 1 na divisao por 4."""
    falhas = []
    for p in primos:
        if p == 2:
            continue
        esperado = 1 if p % 4 == 1 else -1
        if por_euler(-1, p) != esperado:
            falhas.append(p)
    return falhas


def conferir_suplemento_dois(primos):
    """(2/p) = 1 exatamente quando p deixa resto 1 ou 7 na divisao por 8."""
    falhas = []
    for p in primos:
        if p == 2:
            continue
        esperado = 1 if p % 8 in (1, 7) else -1
        if por_euler(2, p) != esperado:
            falhas.append(p)
    return falhas


def quantos_residuos(p):
    """Quantos residuos quadraticos nao nulos existem modulo p."""
    from .legendre import residuos

    return len(residuos(p))
