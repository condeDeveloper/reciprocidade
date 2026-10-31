"""O simbolo de Legendre por tres caminhos que nao se falam.

    (a/p) =  1 se a e quadrado modulo p
    (a/p) = -1 se nao e
    (a/p) =  0 se p divide a

Os tres:

* `por_contagem` eleva ao quadrado todo x de 0 a p-1 e procura `a` na lista. E a
  definicao, e e a mais lenta;
* `por_euler` usa o criterio de 1748: a^((p-1)/2) e 1 ou p-1 modulo p;
* `por_jacobi` nao sabe fatorar nem exponenciar: ele aplica a lei de
  reciprocidade de Gauss, virando a fracao de cabeca para baixo ate acabar.

Quando os tres concordam em milhares de pares, os numeros do README valem.
"""


def por_contagem(a, p):
    """A definicao: existe x com x^2 congruente a `a` modulo p?"""
    if p < 2:
        raise ValueError("%d nao e um modulo valido" % p)
    a %= p
    if a == 0:
        return 0
    quadrados = {x * x % p for x in range(1, p)}
    return 1 if a in quadrados else -1


def residuos(p):
    """O conjunto dos residuos quadraticos nao nulos modulo p."""
    return sorted({x * x % p for x in range(1, p)})


def por_euler(a, p):
    """O criterio de Euler, de 1748."""
    a %= p
    if a == 0:
        return 0
    valor = pow(a, (p - 1) // 2, p)
    if valor == 1:
        return 1
    if valor == p - 1:
        return -1
    raise ValueError("criterio de Euler deu %d: %d nao e primo impar" % (valor, p))


def por_jacobi(a, n):
    """O simbolo de Jacobi, calculado so com a lei de reciprocidade.

    Para `n` primo impar ele e o simbolo de Legendre. Para `n` composto impar
    ele continua dando uma resposta - e essa resposta pode MENTIR, o que esta
    medido no README.
    """
    if n <= 0 or n % 2 == 0:
        raise ValueError("%d precisa ser impar e positivo" % n)
    a %= n
    sinal = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                sinal = -sinal
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            sinal = -sinal
        a %= n
    return sinal if n == 1 else 0


def menor_nao_residuo(p):
    """O menor inteiro positivo que NAO e quadrado modulo p."""
    for a in range(2, p):
        if por_euler(a, p) == -1:
            return a
    return None
