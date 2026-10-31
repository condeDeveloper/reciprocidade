"""Os tres caminhos do simbolo, conferidos um contra o outro."""

import unittest

from reciprocidade.legendre import (
    menor_nao_residuo,
    por_contagem,
    por_euler,
    por_jacobi,
    residuos,
)

PRIMOS = [p for p in range(2, 200) if all(p % d for d in range(2, int(p ** 0.5) + 1))]


class TestContagem(unittest.TestCase):
    def test_residuos_de_sete(self):
        self.assertEqual(residuos(7), [1, 2, 4])

    def test_residuos_de_treze(self):
        self.assertEqual(residuos(13), [1, 3, 4, 9, 10, 12])

    def test_sao_sempre_metade(self):
        for p in PRIMOS:
            if p == 2:
                continue
            self.assertEqual(len(residuos(p)), (p - 1) // 2, "p=%d" % p)

    def test_zero_da_zero(self):
        for p in PRIMOS:
            self.assertEqual(por_contagem(0, p), 0, "p=%d" % p)
            self.assertEqual(por_contagem(p, p), 0, "p=%d" % p)

    def test_um_e_sempre_quadrado(self):
        for p in PRIMOS:
            self.assertEqual(por_contagem(1, p), 1, "p=%d" % p)

    def test_recusa_modulo_invalido(self):
        with self.assertRaises(ValueError):
            por_contagem(1, 1)


class TestOsTresConcordam(unittest.TestCase):
    def test_contagem_contra_euler(self):
        for p in PRIMOS:
            if p == 2:
                continue
            for a in range(p):
                self.assertEqual(por_contagem(a, p), por_euler(a, p), "a=%d p=%d" % (a, p))

    def test_euler_contra_jacobi(self):
        for p in PRIMOS:
            if p == 2:
                continue
            for a in range(1, p):
                self.assertEqual(por_euler(a, p), por_jacobi(a, p), "a=%d p=%d" % (a, p))

    def test_jacobi_de_multiplo_da_zero(self):
        for p in PRIMOS:
            if p == 2:
                continue
            self.assertEqual(por_jacobi(p, p), 0, "p=%d" % p)

    def test_jacobi_recusa_par(self):
        for n in (2, 4, 100, 0, -3):
            with self.assertRaises(ValueError):
                por_jacobi(1, n)

    def test_euler_recusa_composto(self):
        # com modulo composto a potencia nao cai em 1 nem em p-1
        with self.assertRaises(ValueError):
            por_euler(2, 15)

    def test_e_multiplicativo(self):
        for p in PRIMOS[1:20]:
            for a in range(1, p):
                for b in range(1, p):
                    self.assertEqual(
                        por_euler(a * b, p),
                        por_euler(a, p) * por_euler(b, p),
                        "a=%d b=%d p=%d" % (a, b, p),
                    )


class TestMenorNaoResiduo(unittest.TestCase):
    def test_os_primeiros(self):
        esperado = {3: 2, 5: 2, 7: 3, 11: 2, 13: 2, 17: 3, 19: 2, 23: 5, 29: 2, 31: 3}
        for p, a in esperado.items():
            self.assertEqual(menor_nao_residuo(p), a, "p=%d" % p)

    def test_ele_nao_e_quadrado_mesmo(self):
        for p in PRIMOS:
            if p == 2:
                continue
            a = menor_nao_residuo(p)
            self.assertEqual(por_contagem(a, p), -1, "p=%d" % p)

    def test_tudo_antes_dele_e_quadrado(self):
        for p in PRIMOS:
            if p == 2:
                continue
            a = menor_nao_residuo(p)
            for menor in range(1, a):
                self.assertEqual(por_contagem(menor, p), 1, "p=%d a=%d" % (p, menor))

    def test_ele_e_sempre_primo(self):
        # se fosse composto, um dos fatores dele ja seria nao-residuo
        for p in PRIMOS:
            if p == 2:
                continue
            a = menor_nao_residuo(p)
            self.assertTrue(
                all(a % d for d in range(2, int(a ** 0.5) + 1)), "p=%d a=%d" % (p, a)
            )
