# Representative Agent Interactions - Empório da Música

This document details five representative interaction scenarios demonstrating the conversational agent's architecture, including LangChain ReAct orchestration, RAG policy retrieval, relational database function calling, and deterministic pre-LLM scope guardrails.

---

## Scenario 1: Catalog Search with Price Ceiling

* **Context**: Customer is searching for available acoustic guitars within a strict budget ceiling of R$ 1,000.00.
* **Execution Path**: Agent processes the query, identifies category and budget constraints, and calls `search_products`.
* **Invoked Tool**: `search_products(category_name='Violões', max_price=1000.0)`
* **Customer Input (PT-BR)**:
  > "Olá, tudo bem? Quais opções de violões disponíveis vocês têm custando até R$1000?"
* **Agent Response**:
  > Temos ótimas opções de violões disponíveis em estoque por até R$ 1.000,00!
  >
  > * **Tagima Memphis AC-39 Nylon Natural**
  >   * **Preço:** R$ 429,90 *(ou R$ 408,40 à vista no PIX com 5% de desconto)*
  >   * **Estoque:** 15 unidades disponíveis
  >   * **Perfil:** Violão clássico de estudo com cordas de nylon, alta tocabilidade para iniciantes.
  >
  > * **Rozini RC-104 Nylon Estudante**
  >   * **Preço:** R$ 459,90 *(ou R$ 436,90 à vista no PIX)*
  >   * **Estoque:** 10 unidades disponíveis
  >   * **Perfil:** Acabamento primoroso e acústica equilibrada para aprendizado.
  >
  > * **Shelby SN-100 Folk Aço Preto**
  >   * **Preço:** R$ 549,00 *(ou R$ 521,55 à vista no PIX)*
  >   * **Estoque:** 5 unidades disponíveis
  >   * **Perfil:** Modelo Folk com cordas de aço e sonoridade encorpada.
  >
  > * **Yamaha C40 Nylon Natural**
  >   * **Preço:** R$ 599,90 *(ou R$ 569,91 à vista no PIX)*
  >   * **Estoque:** 12 unidades disponíveis
  >   * **Perfil:** Referência pedagógica global com tampo em Spruce e afinação estável.
  >
  > Todos os modelos contam com parcelamento em até **12x sem juros** no cartão de crédito (observada a parcela mínima de R$ 100,00) ou 5% de desconto no PIX. Para pedidos acima de R$ 500,00 na região de Campo Grande, a entrega expressa é gratuita via frota própria.
* **Technical Notes**:
  * Tool correctly extracted the price boundary (`max_price=1000.0`) and category filter (`category_name='Violões'`).
  * Only in-stock models (`stock_quantity > 0`) were returned.
  * Pricing includes precise 5% PIX discount calculations and store installment policies.

---

## Scenario 2: Specific Instrument Details & Payment Terms

* **Context**: Customer asks about a high-value instrument (Takamine GD20), installment conditions, and cash discounts.
* **Execution Path**: Multi-tool sequential execution. The agent retrieves exact product specs from SQLite and cross-references payment policies from the policy manual (RAG).
* **Invoked Tools**:
  1. `get_product_details(name_or_id='Takamine GD20')`
  2. `get_store_policies(topic_or_query='pagamento pix parcelamento')`
* **Customer Input (PT-BR)**:
  > "Quanto custa o Takamine GD20? Como funciona o pagamento parcelado e no PIX?"
* **Agent Response**:
  > O **Takamine GD20** (modelo Folk Dreadnought com tampo sólido em Cedar e escala em Ovangkol) está disponível em nosso estoque por **R$ 2.199,00** (temos 5 unidades em estoque).
  >
  > Condições de pagamento disponíveis:
  > * **À vista no PIX**: 5% de desconto direto sobre o valor de tabela, saindo por **R$ 2.089,05** (economia de R$ 109,95).
  > * **Cartão de Crédito**: Parcelamento em até **12x de R$ 183,25 sem juros** (respeitando a parcela mínima de R$ 100,00 da loja).
  > * **Condição Especial de Alto Valor**: Por se tratar de um instrumento com valor superior a R$ 2.000,00, é permitida a divisão de pagamento entre duas modalidades (por exemplo, entrada no PIX com abatimento do saldo em até 12x no cartão).
* **Technical Notes**:
  * The ReAct loop recognized that pricing came from the database while rules governing split payments and installment floors came from the policy manual.
  * Both pieces of knowledge were synthesized deterministically without prompt drift.

---

## Scenario 3: Store Return Policy & Consumer Rights (CDC)

* **Context**: Customer purchased an electronic keyboard online, received it recently, and wishes to initiate a return under the statutory right of withdrawal.
* **Execution Path**: Agent queries internal customer service policies to retrieve statutory and operational return guidelines.
* **Invoked Tool**: `get_store_policies(topic_or_query='devolucao arrependimento compra')`
* **Customer Input (PT-BR)**:
  > "Comprei um teclado pelo site mas me arrependi da minha compra, chegou ontem. Posso devolver meu pedido?"
* **Agent Response**:
  > Sim, a devolução é perfeitamente assegurada pelo Código de Defesa do Consumidor (Artigo 49) e pelas políticas internas da Empório da Música.
  >
  > Para compras realizadas em nossos canais digitais, você tem até **7 (sete) dias corridos**, contados a partir da data de entrega, para solicitar a devolução por direito de arrependimento com reembolso integral.
  >
  > Diretrizes operacionais para a devolução:
  > 1. O instrumento deve ser devolvido em sua embalagem original, acompanhado de todos os manuais, cabos e fontes de alimentação, sem sinais de mau uso ou avarias.
  > 2. O custo do frete de logística reversa é integralmente assumido pela loja por meio de autorização de postagem dos Correios.
  > 3. O estorno financeiro é processado na mesma forma de pagamento original em até 10 dias úteis após a conferência técnica do item em nosso centro de distribuição.
  >
  > Por favor, informe o número do seu pedido ou o e-mail cadastrado na compra para gerarmos o código de postagem reversa.
* **Technical Notes**:
  * Correctly prioritized policy knowledge over order status search.
  * Verified 7-day statutory deadline, complete packaging requirement, free reverse logistics, and refund SLA.

---

## Scenario 4: Scope Guardrail Activation (Accessory Rejection)

* **Context**: Customer asks to purchase accessories (guitar strings, picks, amplifier) that are explicitly excluded from the store catalog.
* **Execution Path**: Deterministic pre-LLM Guardrail intercepts the prompt before tool dispatch or external model invocation.
* **Invoked Tool**: None (intercepted at `app/agent/guardrails.py`).
* **Customer Input (PT-BR)**:
  > "Vocês vendem encordoamento de guitarra 0.10, palhetas Fender e amplificador de 50W?"
* **Agent Response**:
  > A Empório da Música é especializada exclusivamente na venda de instrumentos musicais completos (violões, guitarras, contrabaixos, baterias, teclados, pianos e instrumentos de sopro).
  >
  > Não comercializamos acessórios avulsos, peças avulsas, encordoamentos, palhetas, cabos, pedais de efeito, amplificadores ou cases avulsos.
  >
  > Recomendamos que você procure lojas especializadas em áudio e acessórios na região central de Campo Grande. Estamos à disposição para auxiliá-lo na escolha de instrumentos musicais completos de nosso catálogo.
* **Technical Notes**:
  * Evaluated in 0 ms API latency with zero token consumption.
  * Rejection is firm, polite, and preserves store branding by suggesting partner channels.

---

## Scenario 5: Relational Order Status Tracking

* **Context**: Customer provides an order ID to check current shipment progress and delivery confirmation.
* **Execution Path**: Agent parses the integer identifier and executes a relational query against `orders`, `order_items`, and `customers`.
* **Invoked Tool**: `check_order_status(order_id=1)`
* **Customer Input (PT-BR)**:
  > "Gostaria de saber o status do meu pedido 1. Quando chega?"
* **Agent Response**:
  > Seguem os dados atualizados do pedido consultado em nosso sistema operacional:
  >
  > * **Pedido**: #1
  > * **Cliente**: Lucas Mendes da Silva
  > * **Data da Compra**: 15/10/2025
  > * **Status Atual**: Entregue ao destinatário
  > * **Item Adquirido**: 1x Roland FP-30X Piano Digital Preto
  > * **Valor Total**: R$ 11.499,00 (Pagamento à vista via PIX)
  > * **Código de Rastreamento**: BRAB1234567BR
  > * **Data de Entrega**: 25/10/2025
  >
  > O pedido consta como entregue no endereço cadastrado. Caso tenha ocorrido qualquer inconsistência no recebimento ou precise de suporte técnico coberto pela garantia legal de 90 dias, estamos à disposição para atendê-lo.
* **Technical Notes**:
  * Relational join successfully linked customer details, item quantities, tracking identifier, and delivery timestamp.
  * The agent accurately stated delivery completion rather than speculating about future delivery dates.
