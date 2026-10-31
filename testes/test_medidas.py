"""Os numeros do README, presos."""

import unittest

from reciprocidade.legendre import menor_nao_residuo, por_jacobi, residuos
from reciprocidade.lei import (
    conferir_lei,
    conferir_suplemento_dois,
    conferir_suplemento_menos_um,
    quantos_residuos,
    sinal_da_lei,
)
from reciprocidade.mentira import e_quadrado, medir_mentira, varrer_compostos


def crivar(limite):
    return [n for n in range(2, limite + 1) if all(n % d for d in range(2, int(n ** 0.5) + 1))]


PRIMOS = crivar(400)
COMPOSTOS = [n for n in range(9, 201, 2) if any(n % d == 0 for d in range(3, n))]


class TestLei(unittest.TestCase):
    def test_nenhuma_falha_em_2926_pares(self):
        conferidos, falhas, opostos = conferir_lei(PRIMOS)
        self.assertEqual(conferidos, 2926)
        self.assertEqual(falhas, [])
        self.assertEqual(opostos, 780)
        self.assertAlmostEqual(100.0 * opostos / conferidos, 26.7, places=1)

    def test_os_opostos_sao_os_dois_com_resto_tres(self):
        for p in PRIMOS:
            for q in PRIMOS:
                if p <= 2 or q <= 2 or p == q:
                    continue
                esperado = -1 if (p % 4 == 3 and q % 4 == 3) else 1
                self.assertEqual(sinal_da_lei(p, q), esperado, "p=%d q=%d" % (p, q))

    def test_os_suplementos(self):
        self.assertEqual(conferir_suplemento_menos_um(PRIMOS), [])
        self.assertEqual(conferir_suplemento_dois(PRIMOS), [])
        self.assertEqual(len(PRIMOS) - 1, 77)

    def test_metade_e_sempre_metade(self):
        pequenos = [p for p in PRIMOS if 2 < p <= 200]
        self.assertEqual(len(pequenos), 45)
        for p in pequenos:
            self.assertEqual(quantos_residuos(p), (p - 1) // 2, "p=%d" % p)

    def test_residuos_de_treze(self):
        self.assertEqual(residuos(13), [1, 3, 4, 9, 10, 12])


class TestMenorNaoResiduo(unittest.TestCase):
    def test_o_maior_e_onde(self):
        pares = [(menor_nao_residuo(p), p) for p in PRIMOS if p > 2]
        self.assertEqual(len(pares), 77)
        self.assertEqual(max(pares), (11, 311))

    def test_a_media(self):
        pares = [menor_nao_residuo(p) for p in PRIMOS if p > 2]
        self.assertAlmostEqual(sum(pares) / len(pares), 3.08, places=2)

    def test_a_distribuicao(self):
        esperado = {2: 42, 3: 19, 5: 10, 7: 5, 11: 1}
        conta = {}
        for p in PRIMOS:
            if p == 2:
                continue
            a = menor_nao_residuo(p)
            conta[a] = conta.get(a, 0) + 1
        self.assertEqual(conta, esperado)

    def test_mais_da_metade_dos_primos_para_no_dois(self):
        conta = sum(1 for p in PRIMOS if p > 2 and menor_nao_residuo(p) == 2)
        self.assertEqual(conta, 42)
        self.assertGreater(conta / 77, 0.5)


class TestMentiraDeJacobi(unittest.TestCase):
    MEDIDAS = varrer_compostos(COMPOSTOS)

    def test_quantos_compostos_foram_conferidos(self):
        self.assertEqual(len(self.MEDIDAS), 54)

    def test_os_que_nunca_mentem(self):
        nunca = [n for n, (m, _, _) in self.MEDIDAS.items() if m == 0]
        self.assertEqual(nunca, [27, 125])

    def test_a_tabela_de_mentiras(self):
        esperado = {
            9: (3, 6), 15: (2, 8), 21: (3, 12), 25: (10, 20), 27: (0, 18),
            33: (5, 20), 35: (6, 24), 45: (6, 24), 49: (21, 42), 81: (27, 54),
            121: (55, 110), 125: (0, 100),
        }
        for n, (mentiras, conferidos) in esperado.items():
            m, c, _ = self.MEDIDAS[n]
            self.assertEqual((m, c), (mentiras, conferidos), "n=%d" % n)

    def test_as_quatro_fatias_possiveis(self):
        fatias = sorted({round(r, 4) for _, _, r in self.MEDIDAS.values()})
        self.assertEqual(fatias, [0.0, 0.25, 0.375, 0.5])

    def test_tres_fatores_distintos_dao_trinta_e_sete_e_meio(self):
        for n in (105, 165, 195):
            _, _, r = self.MEDIDAS[n]
            self.assertAlmostEqual(r, 0.375, places=4, msg="n=%d" % n)

    def test_potencia_impar_de_primo_nunca_mente(self):
        for n in (27, 125):
            conferidos, mentiras, _ = medir_mentira(n)
            self.assertEqual(mentiras, 0, "n=%d" % n)
            self.assertGreater(conferidos, 0)

    def test_potencia_par_de_primo_mente_na_metade(self):
        for n in (9, 25, 49, 81, 121, 169):
            conferidos, mentiras, _ = medir_mentira(n)
            self.assertAlmostEqual(mentiras / conferidos, 0.5, places=6, msg="n=%d" % n)

    def test_o_simbolo_nunca_erra_quando_diz_menos_um(self):
        for n in COMPOSTOS:
            for a in range(1, n):
                if por_jacobi(a, n) == -1:
                    self.assertFalse(e_quadrado(a, n), "a=%d n=%d" % (a, n))
