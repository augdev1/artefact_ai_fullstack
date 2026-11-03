"""Store Policies Knowledge Base for Empório da Música.
Derived from data/políticas_da_loja.pdf (Versão 2.1 - Junho de 2025).
"""

from typing import Dict, Any, List

STORE_POLICIES: Dict[str, Dict[str, Any]] = {
    "general_info": {
        "title": "Sobre a Empório da Música",
        "keywords": ["endereço", "endereco", "onde fica", "localização", "localizacao", "contato", "telefone", "whatsapp", "email", "cnpj", "cidade", "história", "historia"],
        "content": (
            "Empório da Música Instrumentos Musicais Ltda (CNPJ 12.345.678/0001-90), fundada em 2008 em Campo Grande/MS.\n"
            "Endereço: Rua 14 de Maio, 3200 – Centro, Campo Grande - MS, CEP 79202-333.\n"
            "Telefone institucional: (67) 3341-4444 | WhatsApp Atendimento: (67) 3321-4500.\n"
            "E-mail: contato@emporiodamusica.com.br.\n"
            "Catálogo: Especializada exclusivamente em instrumentos musicais (mais de 300 modelos). "
            "A loja NÃO comercializa acessórios avulsos (cordas avulsas, palhetas, cabos, pedais, cases, amplificadores)."
        )
    },
    "opening_hours": {
        "title": "Horário de Funcionamento",
        "keywords": ["horário", "horario", "aberto", "fecha", "funciona", "domingo", "sabado", "sábado", "feriado", "expediente", "atendimento"],
        "content": (
            "Horário de Atendimento presencial e via WhatsApp:\n"
            "- Segunda a Sexta-feira: 09:00 às 18:00\n"
            "- Sábado: 09:00 às 13:00\n"
            "- Domingos e Feriados: Fechado.\n"
            "Fora do horário de expediente, o atendimento automático acolhe o cliente e informa o retorno no próximo dia útil."
        )
    },
    "payment_methods": {
        "title": "Formas de Pagamento e Condições",
        "keywords": ["pagamento", "pagar", "pix", "cartão", "cartao", "credito", "crédito", "debito", "débito", "boleto", "parcelamento", "parcelas", "juros", "desconto pix"],
        "content": (
            "Formas de pagamento aceitas (presencial e online):\n"
            "1. PIX: À vista com 5% de desconto sobre o preço de tabela (ATENÇÃO: não cumulativo com preços já promocionais).\n"
            "2. Cartão de Débito: À vista, todas as bandeiras aceitas.\n"
            "3. Boleto Bancário: À vista, compensação em até 3 dias úteis.\n"
            "4. Cartão de Crédito: Até 12x SEM JUROS.\n"
            "   - Até 3x: sem juros, sem valor mínimo de parcela (exceto abaixo de R$ 50,00).\n"
            "   - 4x a 6x: sem juros, parcela mínima de R$ 80,00.\n"
            "   - 7x a 12x: sem juros, parcela mínima de R$ 100,00.\n"
            "Combinação de formas (PIX + Cartão): permitida para compras acima de R$ 2.000,00."
        )
    },
    "returns_and_exchanges": {
        "title": "Política de Trocas e Devoluções",
        "keywords": ["troca", "trocar", "devolução", "devolucao", "devolver", "arrependimento", "arrependi", "defeito", "estorno", "reembolso", "cdc"],
        "content": (
            "Diretrizes conforme Código de Defesa do Consumidor (CDC):\n"
            "1. Direito de Arrependimento (compras online): até 7 (sete) dias corridos após o recebimento, sem necessidade de justificativa. "
            "Produto deve estar na embalagem original, sem sinais de uso, com manuais e acessórios. Frete de devolução por conta da loja. "
            "Reembolso na mesma forma de pagamento em até 10 dias úteis.\n"
            "2. Troca por Defeito: até 30 (trinta) dias corridos da compra diretamente com a loja. Após 30 dias, garantia do fabricante (a loja pode intermediar).\n"
            "3. Troca por Preferência (cor, modelo): até 7 dias corridos, produto intacto, sujeito à disponibilidade de estoque. Diferenças de valor serão ajustadas.\n"
            "4. Itens NÃO elegíveis para troca: instrumentos com personalização ou setup/regulagem especial sob encomenda; itens de queima de estoque com aviso de 'venda final'; boquilhas de sopro (higiene)."
        )
    },
    "shipping_and_delivery": {
        "title": "Política de Frete e Entregas",
        "keywords": ["frete", "entrega", "prazo", "enviar", "envio", "jadlog", "correios", "pac", "sedex", "campo grande", "motoboy", "rastreamento", "rastreio"],
        "content": (
            "Entregas na Região Metropolitana de Campo Grande/MS:\n"
            "- Frete GRÁTIS para pedidos acima de R$ 500,00.\n"
            "- Taxa fixa de R$ 35,00 para pedidos abaixo de R$ 500,00.\n"
            "- Prazo: 1 a 3 dias úteis por motoboy próprio (contato telefônico prévio).\n\n"
            "Entregas para Outras Cidades / Estados:\n"
            "- PAC (Correios): 5 a 12 dias úteis (com rastreamento e seguro incluso).\n"
            "- SEDEX (Correios): 2 a 5 dias úteis (com rastreamento e seguro incluso).\n"
            "- Jadlog (.package): 3 a 8 dias úteis (com rastreamento e seguro incluso).\n"
            "- Rastreamento: enviado por e-mail e WhatsApp no formato BR + 9 alfanuméricos + BR (ex: BR4K7M2X9P1BR)."
        )
    },
    "promotions_rules": {
        "title": "Regras de Promoções e Descontos",
        "keywords": ["promoção", "promocao", "promocional", "black friday", "desconto", "cumulativo", "aniversário", "aniversario", "queima de estoque"],
        "content": (
            "Regras de Promoções:\n"
            "1. Cumulatividade: Promoções NÃO são cumulativas. O desconto de 5% do PIX NÃO se aplica sobre produtos em promoção.\n"
            "2. Estoque: Promoções sujeitas à disponibilidade de estoque. Sem direito a rain check (reserva de preço após esgotamento).\n"
            "3. Transparência: Preços promocionais devem ser informados sempre com o preço de tabela original e o percentual de desconto.\n"
            "4. Validade: Sempre verificar no sistema se a promoção encontra-se ativa (`is_active = 1`). Promoções expiradas não podem ser aplicadas."
        )
    },
    "warranty": {
        "title": "Garantia e Assistência",
        "keywords": ["garantia", "defeito de fábrica", "fabricante", "conserto", "assistência", "assistencia", "90 dias", "cobertura"],
        "content": (
            "Garantia dos Produtos:\n"
            "1. Garantia Legal: 90 (noventa) dias contra defeitos de fabricação (CDC), a contar do recebimento.\n"
            "2. Garantia do Fabricante: Adicional de 6 meses a 2 anos, conforme certificado que acompanha o produto.\n"
            "3. Não coberto: Desgaste natural de peças (trastes, cordas originais, feltros, palhetas de sopro), danos por mau uso, quedas, umidade ou consertos por terceiros não autorizados."
        )
    },
    "scope_and_accessories": {
        "title": "Escopo da Loja e Política de Acessórios",
        "keywords": ["acessório", "acessorio", "corda", "palheta", "cabo", "pedal", "case", "amplificador", "amp", "fone", "afinador", "alça", "correia"],
        "content": (
            "ESCOPO ESTRITO DA LOJA:\n"
            "A Empório da Música trabalha EXCLUSIVAMENTE com instrumentos musicais (guitarras, baixos, violões, baterias, teclados/pianos, sopros, cordas orquestrais, ukuleles).\n"
            "A loja NÃO vende acessórios avulsos (como encordoamentos/cordas avulsas, palhetas, cabos, cases/capas, pedais de efeito ou amplificadores).\n"
            "Diretriz para o assistente: Quando o cliente pedir acessórios, informe cordialmente que a loja foca exclusivamente nos instrumentos musicais e sugira lojas parceiras especializadas da cidade."
        )
    },
    "privacy_lgpd": {
        "title": "Privacidade e Proteção de Dados (LGPD)",
        "keywords": ["lgpd", "privacidade", "dados", "segurança", "excluir dados", "cadastro"],
        "content": (
            "Em conformidade com a LGPD (Lei nº 13.709/2018), os dados cadastrais (nome, telefone, e-mail, endereço) "
            "são coletados exclusivamente para emissão fiscal, entrega e atendimento. Não são vendidos nem compartilhados "
            "com terceiros para marketing. O cliente pode solicitar a exclusão de seus dados a qualquer momento via WhatsApp ou e-mail."
        )
    }
}


def query_policies(query: str, max_results: int = 2) -> List[Dict[str, str]]:
    """Retrieve the most relevant store policy sections based on keywords or return all matching."""
    query_lower = query.lower()
    scored_sections = []

    for key, data in STORE_POLICIES.items():
        score = 0
        # Title match
        if any(word in query_lower for word in data["title"].lower().split()):
            score += 3
        # Keywords match
        for kw in data["keywords"]:
            if kw in query_lower:
                score += 2
        # Content match
        if any(word in data["content"].lower() for word in query_lower.split() if len(word) > 3):
            score += 1

        if score > 0:
            scored_sections.append((score, data["title"], data["content"]))

    scored_sections.sort(key=lambda x: x[0], reverse=True)

    if not scored_sections:
        # Default fallback to general info and opening hours
        return [
            {"title": STORE_POLICIES["general_info"]["title"], "content": STORE_POLICIES["general_info"]["content"]},
            {"title": STORE_POLICIES["opening_hours"]["title"], "content": STORE_POLICIES["opening_hours"]["content"]}
        ]

    return [
        {"title": title, "content": content}
        for _, title, content in scored_sections[:max_results]
    ]


def get_all_policies() -> Dict[str, Dict[str, Any]]:
    return STORE_POLICIES

