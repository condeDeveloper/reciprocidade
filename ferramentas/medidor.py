"""Roda as varreduras e imprime as tabelas do README.

    python -m ferramentas.medidor
    python -m ferramentas.medidor --completo   # primos ate 1.000

Nenhum numero do README foi digitado a mao, e todos estao presos em
testes/test_medidas.py.
"""

import sys
import time

from reciprocidade.legendre import (
    menor_nao_residuo,
    por_contagem,
    por_euler,
    por_jacobi,
    residuos,
)
from reciprocidade.lei import (
    conferir_lei,
    conferir_suplemento_dois,
    conferir_suplemento_menos_um,
    quantos_residuos,
)
from reciprocidade.mentira import varrer_compostos

COMPLETO = "--completo" in sys.argv
LIMITE_DOS_PRIMOS = 1000 if COMPLETO else 400
LIMITE_DOS_TRES = 200
LIMITE_DOS_COMPOSTOS = 200


def crivar(limite):
    marca = bytearray([1]) * (limite + 1)
    marca[0:2] = b"\x00\x00"
    p = 2
    while p * p <= limite:
        if marca[p]:
            marca[p * p :: p] = bytearray(len(marca[p * p :: p]))
        p += 1
    return [n for n in range(limite + 1) if marca[n]]


def milhar(n):
    return "{:,}".format(n).replace(",", ".")


def main():
    comeco = time.time()
    primos = crivar(LIMITE_DOS_PRIMOS)

    print("## Os tres caminhos do simbolo\n")
    pequenos = [p for p in primos if 2 < p <= LIMITE_DOS_TRES]
    conferidos = 0
    divergencias = 0
    for p in pequenos:
        for a in range(p):
            conferidos += 1
            valores = {por_contagem(a, p), por_euler(a, p)}
            if a:
                valores.add(por_jacobi(a, p))
            if len(valores) > 1:
                divergencias += 1
    print("| pares (a, p) conferidos | primos usados | divergencias |")
    print("|---|---|---|")
    print("| %s | %d | %d |" % (milhar(conferidos), len(pequenos), divergencias))

    print("\n## A lei de reciprocidade de Gauss\n")
    c, falhas, opostos = conferir_lei(primos)
    print("| pares de primos impares | falhas | pares com simbolos opostos | fatia |")
    print("|---|---|---|---|")
    print("| %s | %d | %s | %.1f%% |" % (milhar(c), len(falhas), milhar(opostos), 100.0 * opostos / c))

    print("\n## Os dois suplementos\n")
    print("| suplemento | primos conferidos | falhas |")
    print("|---|---|---|")
    print("| (-1/p) = 1 se p = 1 (mod 4) | %s | %d |" % (milhar(len(primos) - 1), len(conferir_suplemento_menos_um(primos))))
    print("| (2/p) = 1 se p = 1 ou 7 (mod 8) | %s | %d |" % (milhar(len(primos) - 1), len(conferir_suplemento_dois(primos))))

    print("\n## Metade e sempre metade\n")
    erradas = [p for p in primos if p > 2 and quantos_residuos(p) != (p - 1) // 2]
    print("primos conferidos: %s" % milhar(len([p for p in primos if p > 2 and p <= LIMITE_DOS_TRES])))
    print("primos em que o numero de residuos nao e (p-1)/2: %d" % len([p for p in erradas if p <= LIMITE_DOS_TRES]))
    print("residuos modulo 13: %s" % residuos(13))

    print("\n## O menor nao-residuo\n")
    pares = [(menor_nao_residuo(p), p) for p in primos if p > 2]
    maior, onde = max(pares)
    print("| primos conferidos | maior menor-nao-residuo | em que primo | media |")
    print("|---|---|---|---|")
    print(
        "| %s | %d | %d | %.2f |"
        % (milhar(len(pares)), maior, onde, sum(a for a, _ in pares) / len(pares))
    )
    print()
    distribuicao = {}
    for a, _ in pares:
        distribuicao[a] = distribuicao.get(a, 0) + 1
    print("| menor nao-residuo | quantos primos |")
    print("|---|---|")
    for a in sorted(distribuicao):
        print("| %d | %s |" % (a, milhar(distribuicao[a])))

    print("\n## Onde o simbolo de Jacobi mente\n")
    compostos = [
        n
        for n in range(9, LIMITE_DOS_COMPOSTOS + 1, 2)
        if any(n % d == 0 for d in range(3, n))
    ]
    medidas = varrer_compostos(compostos)
    print("compostos impares conferidos: %d" % len(medidas))
    nunca = [n for n, (m, _, _) in medidas.items() if m == 0]
    print("compostos em que o simbolo NUNCA mente: %s" % ", ".join(str(n) for n in nunca))
    print()
    print("| composto | mentiras | conferidos | fatia |")
    print("|---|---|---|---|")
    for n in (9, 15, 21, 25, 27, 33, 35, 45, 49, 81, 121, 125):
        if n not in medidas:
            continue
        m, c2, r = medidas[n]
        print("| %d | %d | %d | %.0f%% |" % (n, m, c2, 100 * r))
    print()
    fatias = sorted({round(r, 4) for _, _, r in medidas.values()})
    print("fatias distintas em todos os compostos conferidos: %s"
          % ", ".join("%.0f%%" % (100 * f) for f in fatias))

    print("\n(medido em %.1f s)" % (time.time() - comeco))


if __name__ == "__main__":
    main()
