# Exemplos de Interação com o Agente - Empório da Música

Este documento reúne 5 conversas reais demonstrando o comportamento do agente inteligente desenvolvido com **LangChain**, aplicando **RAG nas Políticas da Loja**, **Function Calling / Consultas no Catálogo e Pedidos** e **Guardrails de Escopo**.

---

## Conversa 1: Consulta de Catálogo com Filtro de Preço (Situação Real)
> **Cenário**: Cliente busca instrumentos específicos respeitando um limite de orçamento.
> **Ferramenta executada**: `search_products(category_name='Violões', max_price=1000.0)`

* **Cliente**: "Olá, tudo bem? Quais opções de violões disponíveis vocês têm custando até R$1000?"
* **Assistente**:
  > "Fala, beleza! Tudo ótimo por aqui! 🎸
  >
  > Temos excelentes opções de violões para você fazer um som de qualidade dentro desse orçamento. Olha só o que temos disponível agora no estoque:
  >
  > 1. **Yamaha C40 Nylon Natural**
  >    * **Categoria**: Violões (Nylon)
  >    * **Preço de Tabela**: R$ 599,90
  >    * **À vista no PIX (5% OFF)**: R$ 569,91
  >    * **Parcelamento**: até 12x de R$ 49,99 sem juros
  >    * **Estoque**: 12 unidades disponíveis
  >    * *Destaque*: Tampo em Spruce, excelente projeção sonora e ergonomia ideal para iniciantes e estudantes.
  >
  > 2. **Tagima Dallas Aço Eletroacústico**
  >    * **Categoria**: Violões (Aço)
  >    * **Preço de Tabela**: R$ 899,00
  >    * **À vista no PIX (5% OFF)**: R$ 854,05
  >    * **Parcelamento**: até 12x de R$ 74,92 sem juros
  >    * **Estoque**: 8 unidades disponíveis
  >    * *Destaque*: Pré-amplificador ativo com afinador digital integrado e corte cutaway.
  >
  > Lembrando que para pedidos acima de R$ 500,00 aqui na região metropolitana de Campo Grande o frete é **grátis** via motoboy próprio! 
  >
  > Você prefere cordas de nylon para um som mais suave ou de aço para uma pegada mais brilhante?"

---

## Conversa 2: Consulta Específica de Instrumento e Regras de Pagamento
> **Cenário**: Consulta sobre modelo específico (Takamine GD20), cálculo do desconto PIX e parcelamento no cartão.
> **Ferramentas executadas**: `get_product_details(name_or_id='Takamine GD20')` e `get_store_policies(topic_or_query='pagamento pix parcelamento')`

* **Cliente**: "Quanto custa o Takamine GD20? Como funciona o pagamento parcelado e no PIX?"
* **Assistente**:
  > "O **Takamine GD20** é uma verdadeira máquina! É um modelo Dreadnought folk com tampo sólido em cedro, que entrega um grave encorpado e sustain incrível.
  >
  > Ele está saindo por **R$ 2.199,00**.
  >
  > Nossas condições de pagamento para ele:
  > * **No PIX à vista**: Você ganha **5% de desconto** sobre o preço de tabela, saindo por **R$ 2.089,05** (economia de R$ 109,95).
  > * **No Cartão de Crédito**: Pode ser parcelado em **até 12x de R$ 183,25 sem juros** (respeitando nossa parcela mínima de R$ 100,00).
  > * **Formas Combinadas**: Como o valor ultrapassa R$ 2.000,00, você também pode combinar formas de pagamento (ex.: entrada no PIX + saldo no cartão em 12x).
  >
  > Temos 5 unidades a pronta entrega no estoque! Posso separar um para você?"

---

## Conversa 3: Aplicação de Políticas de Devolução e Arrependimento (CDC)
> **Cenário Não Trivial**: Cliente comprou online e quer exercer o direito de arrependimento.
> **Ferramenta executada**: `get_store_policies(topic_or_query='arrependi devolução compra')`

* **Cliente**: "Comprei um teclado pelo site mas me arrependi da minha compra, chegou ontem. Posso devolver meu pedido e pegar meu dinheiro de volta?"
* **Assistente**:
  > "Pode sim, fique tranquilo! A Empório da Música cumpre rigorosamente o Código de Defesa do Consumidor (Art. 49).
  >
  > Como a sua compra foi online e você recebeu o produto ontem, você tem direito de solicitar a devolução por **arrependimento em até 7 (sete) dias corridos** após o recebimento, sem necessidade de justificativa.
  >
  > **Como funciona o procedimento:**
  > 1. O produto deve estar na embalagem original, sem sinais de uso, acompanhado de todos os manuais, fontes e acessórios originais.
  > 2. O **frete de devolução é por conta da loja** (nós geramos uma autorização de postagem reversa dos Correios ou coleta sem custo para você).
  > 3. Assim que o item chega à loja e passa pela conferência, o estorno/reembolso é efetuado na mesma forma de pagamento original em até **10 dias úteis**.
  >
  > Para darmos entrada, você só precisa nos passar o **número do seu pedido** ou seu e-mail cadastrado!"

---

## Conversa 4: Guardrail de Escopo e Política de Acessórios (Regra Rígida de Negócio)
> **Cenário**: Cliente solicita itens que a loja NÃO comercializa (cordas avulsas, palhetas e amplificadores).
> **Ação**: Ativação do Guardrail de Escopo sem gasto inútil de tokens, recusa cordial e redirecionamento.

* **Cliente**: "Vocês vendem encordoamento de guitarra 0.10, palhetas Fender e amplificador de 50W?"
* **Assistente**:
  > "Olá! Aqui na Empório da Música nós trabalhamos **exclusivamente com a venda de instrumentos musicais completos** (guitarras, baixos, violões, baterias, teclados, pianos, sopros e orquestrais). 
  >
  > Nós **não comercializamos acessórios avulsos** como encordoamentos, palhetas, cabos, pedais ou amplificadores.
  >
  > Para esses itens, recomendamos lojas parceiras especializadas em áudio e acessórios no centro de Campo Grande! 
  >
  > Se você estiver buscando um instrumento musical para o seu setup, fico à total disposição para te apresentar nossos modelos disponíveis!"

---

## Conversa 5: Rastreamento de Pedido em Tempo Real com Dados do Banco
> **Cenário**: Cliente quer saber onde está sua compra realizada.
> **Ferramenta executada**: `check_order_status(order_id=1)`

* **Cliente**: "Boa tarde! Gostaria de saber o status do meu pedido 1. Quando chega?"
* **Assistente**:
  > "Boa tarde! Consultei aqui no nosso sistema:
  >
  > * **Pedido**: #1
  > * **Cliente**: Lucas Mendes da Silva
  > * **Data da Compra**: 15/10/2025
  > * **Status Atual**: **Entregue ao destinatário** ✅
  > * **Itens**: 1x Roland FP-30X Piano Digital Preto
  > * **Forma de Pagamento**: PIX (R$ 11.499,00)
  > * **Código de Rastreamento**: `BRAB1234567BR`
  > * **Data de Entrega Registrada**: 25/10/2025
  >
  > Consta em nosso sistema que o pacote foi entregue com sucesso! Caso tenha ocorrido qualquer problema com a entrega ou precise de suporte técnico sobre o instrumento, me avise que aciono a equipe de pós-venda imediatamente."
