# 📌 Análise Crítica de Elitismo e Convergência em Algoritmos Genéticos

## 📖 Descrição
Este projeto consiste na implementação de um **Algoritmo Genético (AG) binário** focado na minimização de uma função quadrática. O objetivo central é realizar um estudo comparativo sobre como o **elitismo** influencia a convergência, a manutenção da diversidade populacional e a qualidade das soluções encontradas.

### Função Objetivo
O algoritmo busca minimizar:
$$f(x) = 2x^2 + 5x$$
No intervalo: $x \in [-10, 10]$

---

## 🧠 Fundamentação Teórica

Um **Algoritmo Genético** é uma meta-heurística de otimização inspirada na teoria da evolução natural de Charles Darwin. O processo evolutivo ocorre através de ciclos de seleção, recombinação e mutação.



### Prós e Contras
| ✅ Vantagens | ❌ Desvantagens |
| :--- | :--- |
| Capacidade de busca global | Risco de convergência prematura |
| Não exige cálculo de derivadas | Sensibilidade extrema aos parâmetros |
| Robusto em problemas não lineares | Alto custo computacional em funções complexas |

### Conceitos-Chave
* **Exploração (Diversificação):** Capacidade de varrer novas áreas do espaço de busca.
* **Exploração Local (Intensificação):** Refinamento de soluções promissoras já encontradas.
* **Elitismo:** Mecanismo que garante a sobrevivência dos melhores indivíduos para a próxima geração.
* **Paralelismo Implícito:** Capacidade de processar múltiplas regiões do espaço de busca simultaneamente.

---

## ⚙️ Especificações da Implementação

Abaixo, os detalhes técnicos da modelagem do AG:

* **Codificação:** Binária (10 bits por indivíduo).
* **Seleção:** Torneio.
* **Crossover:** Um ponto (Single-point crossover).
* **Mutação:** Bit a bit.
* **Elitismo:** Parametrizável por experimento.
* **Critério de Parada:** Número fixo de gerações.

### Métricas Monitoradas
Para cada geração, o sistema registra:
1.  **Melhor Fitness:** Valor da melhor solução atual.
2.  **Fitness Médio:** Desempenho geral da população.
3.  **Diversidade:** Calculada via **Distância Média de Hamming**.

---

## 🧪 Experimentos e Resultados

Foram realizados testes comparativos com três configurações de elitismo, cada uma executada 5 vezes para garantir consistência estatística:

| Experimento | Taxa de Elitismo | Comportamento Observado |
| :---: | :---: | :--- |
| **A** | 0% | Alta diversidade, porém convergência muito lenta. |
| **B** | 2% | **Melhor equilíbrio** entre exploração e refinamento. |
| **C** | 20% | Convergência rápida, mas com perda severa de diversidade. |

### Análise de Performance
* O **elitismo alto (20%)** aumentou significativamente o risco de estagnação em ótimos locais (convergência prematura).
* A **melhor solução** encontrada aproximou-se do mínimo analítico:
    * $x \approx -1.25$
    * $f(x) \approx -3.125$

> [!TIP]
> **Estratégia de Mitigação:** Para os casos de elitismo alto, foi implementada uma **mutação adaptativa**. Quando a diversidade caía abaixo de um limiar, a taxa de mutação subia automaticamente para evitar a estagnação.

---

## 🏁 Conclusão
O estudo demonstrou que o elitismo é uma ferramenta poderosa para acelerar a convergência, mas deve ser usado com cautela. Um elitismo moderado (~2%) provou ser a configuração mais robusta, garantindo que o algoritmo não "vicie" em soluções medianas e continue explorando o espaço de busca de forma eficiente.