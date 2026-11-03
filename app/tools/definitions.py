"""Standardized Function Calling / Tool Definitions for LLM Agents."""

TOOL_DEFINITIONS = [
    {
        "name": "search_products",
        "description": "Busca instrumentos musicais no catálogo da loja por palavras-chave, categoria ou faixa de preço.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Termo de busca (ex: 'violão', 'Takamine', 'Yamaha', 'piano', 'bateria')"
                },
                "category_name": {
                    "type": "string",
                    "description": "Categoria do instrumento: 'Guitarras', 'Baixos', 'Violões', 'Baterias e Percussão', 'Teclados e Pianos', 'Instrumentos de Sopro (Madeiras)', 'Instrumentos de Sopro (Metais)', 'Cordas Orquestrais', 'Ukuleles'"
                },
                "max_price": {
                    "type": "number",
                    "description": "Preço máximo em Reais (ex: 1000.00)"
                },
                "min_price": {
                    "type": "number",
                    "description": "Preço mínimo em Reais"
                },
                "in_stock_only": {
                    "type": "boolean",
                    "description": "Filtrar apenas itens disponíveis em estoque (padrão true)"
                }
            }
        }
    },
    {
        "name": "get_product_details",
        "description": "Obtém detalhes completos, preço, desconto PIX, opções de parcelamento e estoque de um instrumento específico.",
        "parameters": {
            "type": "object",
            "properties": {
                "name_or_id": {
                    "type": "string",
                    "description": "Nome do modelo (ex: 'Takamine GD20', 'Yamaha C40') ou ID numérico do produto."
                }
            },
            "required": ["name_or_id"]
        }
    },
    {
        "name": "check_order_status",
        "description": "Consulta o status atual, rastreamento e itens de um pedido de cliente.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "integer",
                    "description": "Número de identificação do pedido (ex: 1, 2, 3)"
                },
                "tracking_code": {
                    "type": "string",
                    "description": "Código de rastreamento do envio (ex: 'BRAB1234567BR')"
                },
                "customer_phone_or_email": {
                    "type": "string",
                    "description": "E-mail ou telefone do cliente cadastrado"
                }
            }
        }
    },
    {
        "name": "list_promotions",
        "description": "Consulta promoções e campanhas com descontos ativos na loja.",
        "parameters": {
            "type": "object",
            "properties": {
                "active_only": {
                    "type": "boolean",
                    "description": "Se verdadeiro, lista apenas promoções ativas e válidas atualmente (padrão true)"
                }
            }
        }
    },
    {
        "name": "get_store_policies",
        "description": "Consulta as políticas internas da loja: horários de funcionamento, endereço, prazos de entrega e fretes, formas de pagamento (PIX 5%, parcelamento), regras de trocas e devoluções (7 dias arrependimento CDC), garantia (90 dias CDC) e escopo de atendimento.",
        "parameters": {
            "type": "object",
            "properties": {
                "topic_or_query": {
                    "type": "string",
                    "description": "Assunto ou dúvida a ser consultada no manual (ex: 'horário de funcionamento', 'endereço', 'política de devolução', 'prazo de entrega campo grande', 'formas de pagamento')"
                }
            },
            "required": ["topic_or_query"]
        }
    }
]

