"""Onde o simbolo de Jacobi mente, e quanto.

O simbolo de Jacobi (a/n) e definido para todo `n` impar, primo ou nao, e e
calculado exatamente pela mesma regra da reciprocidade. Quando `n` e primo ele e
o simbolo de Legendre e diz a verdade. Quando `n` e composto ele continua
devolvendo 1 ou -1, mas o significado se perde:

* se (a/n) = -1, entao `a` realmente NAO e quadrado modulo n;
* se (a/n) = 1, `a` pode ser quadrado ou nao. E aqui que mora a mentira.

Este arquivo mede o tamanho da mentira em vez de descreve-la.
"""

from .legendre import por_jacobi


def e_quadrado(a, n):
    """A definicao, sem simbolo nenhum: existe x com x^2 = a modulo n?"""
    a %= n
    return any(x * x % n == a for x in range(n))


def medir_mentira(n):
    """Para um `n` impar, compara o simbolo de Jacobi com a verdade.

    Devolve (conferidos, mentiras, acertos_negativos), contando so os `a`
    coprimos com `n`, que sao os unicos em que o simbolo nao e zero.
    """
    from math import gcd

    conferidos = 0
    mentiras = 0
    negativos_corretos = 0
    for a in range(1, n):
        if gcd(a, n) != 1:
            continue
        conferidos += 1
        simbolo = por_jacobi(a, n)
        verdade = e_quadrado(a, n)
        if simbolo == 1 and not verdade:
            mentiras += 1
        if simbolo == -1:
            # quando o simbolo diz -1 ele nunca erra, nem em composto
            if verdade:
                raise AssertionError("Jacobi disse -1 para um quadrado: a=%d n=%d" % (a, n))
            negativos_corretos += 1
    return conferidos, mentiras, negativos_corretos


def varrer_compostos(impares):
    """A fatia de mentiras de cada composto impar da lista."""
    saida = {}
    for n in impares:
        conferidos, mentiras, _ = medir_mentira(n)
        saida[n] = (mentiras, conferidos, mentiras / conferidos if conferidos else 0.0)
    return saida
