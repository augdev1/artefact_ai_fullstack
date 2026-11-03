# Exemplos de Interacao com o Agente - Emporio da Musica

Este documento reune 5 conversas representativas demonstrando o comportamento do agente inteligente desenvolvido com LangChain, aplicando RAG nas Politicas da Loja, Function Calling em catalogo e pedidos relacionais, e Guardrails de Escopo.

---

## Conversa 1: Consulta de Catalogo com Filtro de Preco (Situacao Real)
* **Cenario**: Cliente busca instrumentos especificos respeitando um teto orcamentario de R$ 1.000,00.
* **Ferramenta Executada**: `search_products(category_name='Violões', max_price=1000.0)`
* **Entrada do Cliente**: "Ola, tudo bem? Quais opcoes de violoes disponiveis voces tem custando ate R$1000?"
* **Resposta do Agente**:
  > "Ola! Temos excelentes opcoes de violoes em estoque dentro do seu orcamento:
  >
  > 1. **Tagima Memphis AC-39 Nylon Natural**
  >    * Preco de Tabela: R$ 429,90
  >    * A vista no PIX (5% de desconto): R$ 408,40
  >    * Parcelamento: ate 12x de R$ 35,82 sem juros
  >    * Estoque: 15 unidades disponiveis
  >    * Perfil: Classico de estudo com cordas de nylon.
  >
  > 2. **Yamaha C40 Nylon Natural**
  >    * Preco de Tabela: R$ 599,90
  >    * A vista no PIX (5% de desconto): R$ 569,91
  >    * Parcelamento: ate 12x de R$ 49,99 sem juros
  >    * Estoque: 12 unidades disponiveis
  >    * Perfil: Tampo em Spruce, acabamento tradicional e referencia para estudantes.
  >
  > 3. **Shelby SN-100 Folk Aco Preto**
  >    * Preco de Tabela: R$ 549,00
  >    * A vista no PIX (5% de desconto): R$ 521,55
  >    * Parcelamento: ate 12x de R$ 45,75 sem juros
  >    * Estoque: 5 unidades disponiveis
  >    * Perfil: Estilo Folk com cordas de aco.
  >
  > Para entregas na regiao metropolitana de Campo Grande acima de R$ 500,00 o frete e gratuito via motoboy proprio. Gostaria de mais detalhes sobre algum desses modelos?"

---

## Conversa 2: Consulta Especifica de Instrumento e Regras de Pagamento
* **Cenario**: Consulta sobre modelo especifico (Takamine GD20), calculo de desconto a vista no PIX e regras de parcelamento sem juros.
* **Ferramentas Executadas**: `get_product_details(name_or_id='Takamine GD20')` e `get_store_policies(topic_or_query='pagamento pix parcelamento')`
* **Entrada do Cliente**: "Quanto custa o Takamine GD20? Como funciona o pagamento parcelado e no PIX?"
* **Resposta do Agente**:
  > "O Takamine GD20 (modelo Folk Dreadnought com tampo solido em cedro) esta disponivel em nosso estoque pelo valor de tabela de **R$ 2.199,00** (temos 5 unidades disponiveis).
  >
  > Nossas condicoes de pagamento:
  > * **A vista no PIX**: 5% de desconto sobre o preco de tabela, totalizando **R$ 2.089,05** (economia de R$ 109,95).
  > * **Cartao de Credito**: Parcelamento em ate **12x de R$ 183,25 sem juros**, em conformidade com a parcela minima de R$ 100,00 da loja.
  > * **Condicoes Especiais**: Por se tratar de uma compra acima de R$ 2.000,00, e permitida a combinacao de formas de pagamento (ex.: entrada no PIX com abatimento de saldo em cartao de credito)."

---

## Conversa 3: Aplicacao de Politicas de Devolucao e Arrependimento (CDC)
* **Cenario**: Cliente adquiriu produto pelo canal online e manifesta arrependimento de compra dentro do prazo legal.
* **Ferramenta Executada**: `get_store_policies(topic_or_query='arrependi devolucao compra')`
* **Entrada do Cliente**: "Comprei um teclado pelo site mas me arrependi da minha compra, chegou ontem. Posso devolver meu pedido e receber o reembolso?"
* **Resposta do Agente**:
  > "Sim, a devolucao e garantida conforme o Codigo de Defesa do Consumidor (Artigo 49).
  >
  > Para compras realizadas em nossos canais online, voce possui ate **7 (sete) dias corridos** apos a data de recebimento para solicitar a devolucao por direito de arrependimento, sem necessidade de justificativa.
  >
  > Procedimentos operacionais:
  > 1. O instrumento deve ser devolvido em sua embalagem original, sem sinais de utilizacao ou avarias, acompanhado de manuais, cabos e acessorios de fabrica.
  > 2. O custo do frete de devolucao e integralmente coberto pela Emporio da Musica atraves de autorizacao de postagem reversa.
  > 3. O estorno/reembolso financeiro e realizado na mesma modalidade de pagamento original em ate 10 dias uteis apos a conferencia fisica do item em nossa central.
  >
  > Por favor, informe o numero do pedido ou o e-mail cadastrado para que possamos iniciar o procedimento de devolucao."

---

## Conversa 4: Guardrail de Escopo e Politica de Acessorios
* **Cenario**: Cliente solicita itens nao comercializados pela loja (cordas avulsas, palhetas e amplificadores).
* **Acao**: Bloqueio deterministico imediato na camada de Guardrail de escopo antes do envio da requisicao ao modelo.
* **Entrada do Cliente**: "Voces vendem encordoamento de guitarra 0.10, palhetas Fender e amplificador de 50W?"
* **Resposta do Agente**:
  > "A Emporio da Musica atua com especializacao exclusiva na comercializacao de instrumentos musicais completos (violões, guitarras, contrabaixos, baterias, teclados, pianos, instrumentos de sopro e orquestrais).
  >
  > A loja nao comercializa acessorios avulsos, tais como encordoamentos avulsos, palhetas, cabos, pedais de efeito, amplificadores ou cases.
  >
  > Recomendamos a busca desses insumos em lojas especializadas em audio e acessorios localizadas na regiao central de Campo Grande. Estamos a disposicao para atende-lo na selecao e compra de instrumentos musicais de nosso catalogo."

---

## Conversa 5: Rastreamento de Pedido em Tempo Real com Dados do Banco
* **Cenario**: Cliente consulta o status logistico de uma compra utilizando o identificador de pedido.
* **Ferramenta Executada**: `check_order_status(order_id=1)`
* **Entrada do Cliente**: "Boa tarde, gostaria de verificar o status do meu pedido 1. Quando chega?"
* **Resposta do Agente**:
  > "Boa tarde. Seguem os dados atualizados do pedido consultado em nosso sistema operacional:
  >
  > * **Pedido**: #1
  > * **Cliente**: Lucas Mendes da Silva
  > * **Data do Pedido**: 15/10/2025
  > * **Status Atual**: Entregue ao destinatario
  > * **Item**: 1x Roland FP-30X Piano Digital Preto
  > * **Valor Total**: R$ 11.499,00 (Pagamento via PIX)
  > * **Codigo de Rastreamento**: BRAB1234567BR
  > * **Data de Entrega Registrada**: 25/10/2025
  >
  > O pedido consta como entregue no endereco cadastrado. Caso tenha ocorrido qualquer inconsistencia na entrega ou necessite de assistencia referente a garantia de 90 dias, favor nos contatar."
