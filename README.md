# Reciprocidade quadrática

Quais números são quadrados perfeitos **módulo um primo**? O símbolo de Legendre
`(a/p)` responde com 1, −1 ou 0, e a lei de reciprocidade de Gauss diz que os
símbolos `(p/q)` e `(q/p)` são iguais — **exceto** quando os dois primos deixam
resto 3 na divisão por 4, e aí são opostos. Gauss chamou isso de *theorema
aureum* e provou de oito jeitos diferentes.

Aqui o símbolo sai por **três caminhos que não compartilham código**: elevar ao
quadrado todo mundo e procurar na lista, o critério de Euler de 1748, e o
símbolo de Jacobi, que não sabe fatorar nem exponenciar e só aplica a própria
lei de reciprocidade. Python puro, sem dependência nenhuma.

## Os quatro achados

1. **Os três caminhos concordam nos 4.225 pares `(a, p)` conferidos**, e a lei
   de Gauss não falha uma vez em **2.926 pares de primos**. O caso raro da lei —
   os dois símbolos opostos — acontece em **26,7%** dos pares, que é a fatia dos
   dois primos deixarem resto 3 ao mesmo tempo.
2. **O menor não-resíduo é quase sempre minúsculo: 42 dos 77 primos param no
   2.** A média é **3,08**, e o maior em toda a faixa até 400 é **11**, no primo
   311. Nenhum primo precisou passar do 11 para achar um não-quadrado.
3. **O símbolo de Jacobi nunca mente em 27 e em 125, e mente em metade dos casos
   em 9, 25, 49, 81 e 121.** A diferença é a paridade do expoente: com `p³` o
   símbolo é `(a/p)` e continua dizendo a verdade; com `p²` ele é sempre 1, e aí
   metade das respostas é mentira.
4. **Fora das potências de primo, a mentira segue o número de fatores.** Dois
   primos distintos dão exatamente **25%**; três primos distintos, **37,5%** —
   medido em 105, 165 e 195. Em 54 compostos ímpares conferidos aparecem só
   quatro fatias: 0%, 25%, 37,5% e 50%.

## As tabelas

Tudo abaixo sai de `python -m ferramentas.medidor`. Nenhum número foi digitado à
mão, e todos estão presos em `testes/test_medidas.py`.

### Os três caminhos do símbolo

| pares (a, p) conferidos | primos usados | divergências |
|---|---|---|
| 4.225 | 45 | 0 |

### A lei de reciprocidade de Gauss

| pares de primos ímpares | falhas | pares com símbolos opostos | fatia |
|---|---|---|---|
| 2.926 | 0 | 780 | 26,7% |

### Os dois suplementos

| suplemento | primos conferidos | falhas |
|---|---|---|
| (−1/p) = 1 quando p ≡ 1 (mod 4) | 77 | 0 |
| (2/p) = 1 quando p ≡ 1 ou 7 (mod 8) | 77 | 0 |

### Metade é sempre metade

Em 45 primos conferidos, o número de resíduos quadráticos não nulos é
**exatamente `(p−1)/2`** em todos. Módulo 13 eles são `1, 3, 4, 9, 10, 12`.

### O menor não-resíduo

| primos conferidos | maior menor-não-resíduo | em que primo | média |
|---|---|---|---|
| 77 | 11 | 311 | 3,08 |

| menor não-resíduo | quantos primos |
|---|---|
| 2 | 42 |
| 3 | 19 |
| 5 | 10 |
| 7 | 5 |
| 11 | 1 |

Ele é sempre primo, e isso está em teste: se fosse composto, um dos fatores já
seria não-resíduo antes dele.

### Onde o símbolo de Jacobi mente

| composto | mentiras | conferidos | fatia |
|---|---|---|---|
| 9 | 3 | 6 | 50% |
| 15 | 2 | 8 | 25% |
| 21 | 3 | 12 | 25% |
| 25 | 10 | 20 | 50% |
| 27 | 0 | 18 | 0% |
| 33 | 5 | 20 | 25% |
| 35 | 6 | 24 | 25% |
| 45 | 6 | 24 | 25% |
| 49 | 21 | 42 | 50% |
| 81 | 27 | 54 | 50% |
| 121 | 55 | 110 | 50% |
| 125 | 0 | 100 | 0% |

Em 54 compostos ímpares até 200, as fatias que aparecem são **0%, 25%, 37,5% e
50%** — nenhuma outra. E quando o símbolo diz **−1** ele nunca erra, nem em
composto: isso é conferido em todos os pares `(a, n)` da faixa.

## O que as medidas me corrigiram

- **Achei que o símbolo de Jacobi mentisse mais em número composto "mais
  composto".** Mente conforme a **estrutura**, não conforme o tamanho: 125, que
  é 5³, nunca mente, enquanto 9, que é bem menor, mente em metade dos casos. O
  que manda é a paridade dos expoentes e a quantidade de primos distintos.
- **Esperava que o caso raro da lei de Gauss fosse mesmo raro.** Ele acontece em
  26,7% dos pares, perto de um quarto — que é a chance de dois primos ímpares
  caírem os dois na classe 3 módulo 4. "Exceto quando" soa excepcional e não é.
- **Esperava que o menor não-resíduo crescesse junto com o primo.** Em 77
  primos até 400 ele nunca passa de 11, e mais da metade para no 2. O recorde,
  11, acontece **uma vez só**, no 311.
- **Deixei o critério de Euler devolver qualquer coisa para módulo composto, e
  depois voltei atrás.** A potência `a^((p-1)/2)` só cai em 1 ou em `p-1` quando
  `p` é primo; fora disso ela devolve um número qualquer, que seria lido como
  símbolo sem ninguém perceber. Agora ela levanta erro — e isso também está em
  teste, com módulo 15.

## Como está organizado

```
reciprocidade/legendre.py  o símbolo pelos três caminhos, e o menor não-resíduo
reciprocidade/lei.py       a lei de Gauss e os dois suplementos, conferidos
reciprocidade/mentira.py   onde o símbolo de Jacobi mente, e quanto
ferramentas/medidor.py     roda tudo e imprime as tabelas acima
testes/                    33 testes
```

## Rodar

```bash
python -m unittest discover -s testes -t . -v   # a bateria inteira
python -m ferramentas.medidor                   # recalcula as tabelas deste README
python -m ferramentas.medidor --completo        # primos até 1.000
```

Sem `pip install`: não há dependência. Precisa de Python 3.11 ou mais novo.

## Licença

MIT.
