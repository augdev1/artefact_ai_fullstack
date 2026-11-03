"""Deterministic Guardrails and Scope Checker for Empório da Música."""

import re
from typing import Tuple, Optional

ACCESSORY_KEYWORDS = [
    r"\bpalheta(s)?\b",
    r"\bencordoamento(s)?\b",
    r"\bcorda(s)? avulsa(s)?\b",
    r"\bcabo(s)? (p10|xlr|guitarra|instrumento)\b",
    r"\bpedal(is)? (de guitarra|de efeito|de distorção|delay|reverb|pedaleira)\b",
    r"\bamplificador(es)?\b",
    r"\bcubo(s)? de guitarra\b",
    r"\bcase(s)?\b",
    r"\bcapa(s)? avulsa(s)?\b",
    r"\bafinador(es)?\b",
    r"\bcorreia(s)?\b",
    r"\bbaqueta(s)?\b",
    r"\bcaixa de som\b",
]

OFF_TOPIC_KEYWORDS = [
    r"\breceita de\b",
    r"\bcódigo (em )?(python|java|javascript|c\+\+|php)\b",
    r"\bprogramação\b",
    r"\beleição\b",
    r"\bpolítica partidária\b",
    r"\bfutebol resultado\b",
    r"\bclima amanhã\b",
    r"\bprevisão do tempo\b",
]

class ScopeGuardrail:
    @staticmethod
    def check_scope(user_message: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Evaluate if a user message violates the store's scope boundaries.
        Returns:
            (is_out_of_scope: bool, reason: str | None, suggested_response: str | None)
        """
        msg_lower = user_message.lower().strip()

        # Check for non-musical / totally irrelevant topics
        for pattern in OFF_TOPIC_KEYWORDS:
            if re.search(pattern, msg_lower):
                return (
                    True,
                    "off_topic",
                    "Olá! Aqui na Empório da Música nosso foco total é o universo dos instrumentos musicais. "
                    "Infelizmente não consigo te ajudar com esse assunto, mas se você tiver qualquer dúvida sobre violões, guitarras, teclados, "
                    "baterias ou outros instrumentos, estou à disposição!"
                )

        # Check for accessories (Store Policy Section 1 & 7.1)
        for pattern in ACCESSORY_KEYWORDS:
            if re.search(pattern, msg_lower):
                # Ensure they are not asking about an instrument that happens to use cords (e.g. 'violão de nylon')
                # Strings on guitar/specs are ok, but asking to buy cords/picks alone is an accessory
                is_standalone_accessory = any(term in msg_lower for term in [
                    "comprar corda", "vende corda", "tem corda", "preço da corda", "encordoamento",
                    "palheta", "amplificador", "cabo p10", "cabo", "pedal", "pedaleira", "case", "capa", "baqueta", "afinador"
                ])
                if is_standalone_accessory:
                    return (
                        True,
                        "accessory_request",
                        "Aqui na Empório da Música nós trabalhamos exclusivamente com a venda de instrumentos musicais completos "
                        "(violões, guitarras, baixos, baterias, teclados, sopros e orquestrais). Não comercializamos acessórios avulsos "
                        "como cordas, palhetas, cabos, amplificadores ou pedais. "
                        "Recomendamos consultar lojas de acessórios musicais parceiras no centro de Campo Grande! "
                        "Posso te ajudar a escolher algum instrumento do nosso catálogo?"
                    )

        return (False, None, None)

