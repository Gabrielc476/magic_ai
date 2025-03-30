# spellcrafting/ai/name_generator.py
"""
Gerador de nomes para magias.
"""
from typing import List, Dict, Any, Optional, Tuple
import random
from collections import Counter

from spellcrafting.core import MagicalComponentInterface, MagicalEffectInterface, AIModelInterface


class SpellNameGenerator(AIModelInterface):
    """
    Gerador de nomes criativos para magias com base em seus componentes e efeitos.
    """

    def __init__(self):
        """Inicializa o gerador de nomes."""
        self._element_adjectives = {
            "fogo": ["Flamejante", "Ardente", "Incandescente", "Vulcânico", "Calcinante",
                     "Abrasador", "Ígneo", "Pirético", "Combustivo", "Candente"],
            "água": ["Aquático", "Fluido", "Congelante", "Marítimo", "Glacial",
                     "Ondulante", "Líquido", "Oceânico", "Hidratante", "Diluído"],
            "terra": ["Terrestre", "Rochoso", "Pétreo", "Sólido", "Mineral",
                      "Cristalino", "Sedimentar", "Telúrico", "Geológico", "Montanhoso"],
            "ar": ["Ventoso", "Etéreo", "Tempestuoso", "Aéreo", "Ciclônico",
                   "Atmosférico", "Volátil", "Gasoso", "Nebuloso", "Alado"],
            "luz": ["Luminoso", "Radiante", "Brilhante", "Celestial", "Divino",
                    "Iluminado", "Resplandecente", "Fulgurante", "Solar", "Aurífero"],
            "trevas": ["Sombrio", "Obscuro", "Tenebroso", "Umbroso", "Noturno",
                       "Penumbroso", "Lutuoso", "Sinistro", "Eclipsado", "Abissal"]
        }

        self._element_nouns = {
            "fogo": ["Chama", "Inferno", "Explosão", "Conflagração", "Combustão",
                     "Fogueira", "Braseiro", "Incêndio", "Fornalha", "Pira"],
            "água": ["Onda", "Tsunami", "Dilúvio", "Torrente", "Gêiser",
                     "Maré", "Cascata", "Chuva", "Neblina", "Oceano"],
            "terra": ["Escudo", "Muralha", "Proteção", "Barreira", "Fortaleza",
                      "Montanha", "Pedra", "Cristal", "Terremoto", "Pilar"],
            "ar": ["Tempestade", "Furacão", "Rajada", "Vendaval", "Ciclone",
                   "Brisa", "Tornado", "Vórtice", "Tufão", "Zéfiro"],
            "luz": ["Aura", "Halo", "Benção", "Purificação", "Ressurreição",
                    "Clarão", "Aurora", "Alvorada", "Esplendor", "Iluminação"],
            "trevas": ["Maldição", "Corrupção", "Dissolução", "Degeneração", "Pestilência",
                       "Eclipse", "Crepúsculo", "Sombra", "Escuridão", "Abismo"]
        }

        self._effect_adjectives = {
            "dano": ["Devastador", "Destrutivo", "Mortal", "Letal", "Flagelante"],
            "cura": ["Restaurador", "Curativo", "Revitalizante", "Regenerativo", "Reconfortante"],
            "controle": ["Dominante", "Subjugador", "Controlador", "Restritivo", "Imobilizador"],
            "proteção": ["Defensivo", "Protetor", "Inviolável", "Impenetrável", "Escudante"],
            "ilusão": ["Ilusório", "Enganador", "Dissimulador", "Fantasmagórico", "Velado"],
            "invocação": ["Invocativo", "Convocatório", "Conjuratório", "Chamativo", "Atrativo"]
        }

        self._effect_nouns = {
            "dano": ["Destruição", "Ruína", "Calamidade", "Aniquilação", "Devastação"],
            "cura": ["Recuperação", "Renovação", "Restauração", "Rejuvenescimento", "Revitalização"],
            "controle": ["Domínio", "Autoridade", "Sujeição", "Controle", "Poder"],
            "proteção": ["Salvaguarda", "Defesa", "Escudo", "Armadura", "Proteção"],
            "ilusão": ["Miragem", "Fantasia", "Devaneio", "Delírio", "Simulacro"],
            "invocação": ["Invocação", "Convocação", "Chamado", "Conjuração", "Cântico"]
        }

        self._name_patterns = [
            lambda adj, noun, elem: f"{adj} {noun}",
            lambda adj, noun, elem: f"{noun} {adj}",
            lambda adj, noun, elem: f"{noun} de {elem.capitalize()}",
            lambda adj, noun, elem: f"{adj} {noun} de {elem.capitalize()}"
        ]

        self._trained = True  # Este gerador não requer treinamento formal

    def train(self) -> bool:
        """
        Este gerador não requer treinamento formal.

        Returns:
            Sempre retorna True
        """
        return True

    def predict(self, input_data: Any) -> str:
        """
        Gera um nome para a magia com base nos componentes e efeito.

        Args:
            input_data: Pode ser uma tupla (components, effect) ou um dicionário
                        com 'components' e 'effect'

        Returns:
            Nome gerado para a magia
        """
        components = None
        effect = None

        # Extrai componentes e efeito do input
        if isinstance(input_data, tuple) and len(input_data) == 2:
            components, effect = input_data
        elif isinstance(input_data, dict):
            components = input_data.get('components', [])
            effect = input_data.get('effect')
        else:
            components = input_data

        # Determina o elemento dominante
        if not components:
            return "Magia Desconhecida"

        element_counts = Counter(comp.element for comp in components)
        dominant_element = element_counts.most_common(1)[0][0]

        # Determina a categoria do efeito (se fornecido)
        effect_category = "dano"  # Categoria padrão
        if effect:
            effect_text = (effect.name + " " + effect.description).lower()

            # Determina a categoria com base nas palavras-chave
            if any(keyword in effect_text for keyword in ["cura", "restaura", "vida", "regenera", "saúde"]):
                effect_category = "cura"
            elif any(
                    keyword in effect_text for keyword in ["controle", "imobiliza", "paralisa", "restringe", "domina"]):
                effect_category = "controle"
            elif any(keyword in effect_text for keyword in ["escudo", "barreira", "proteção", "defesa", "armadura"]):
                effect_category = "proteção"
            elif any(keyword in effect_text for keyword in ["ilusão", "ilude", "invisível", "engana", "disfarça"]):
                effect_category = "ilusão"
            elif any(keyword in effect_text for keyword in ["invoca", "conjura", "convoca", "chama", "traz"]):
                effect_category = "invocação"

        # Seleciona adjetivo e substantivo com base no elemento e categoria de efeito
        if random.random() < 0.7:  # 70% de chance de usar adjetivo baseado no elemento
            adjective = random.choice(self._element_adjectives[dominant_element])
        else:  # 30% de chance de usar adjetivo baseado no efeito
            adjective = random.choice(self._effect_adjectives[effect_category])

        if random.random() < 0.7:  # 70% de chance de usar substantivo baseado no elemento
            noun = random.choice(self._element_nouns[dominant_element])
        else:  # 30% de chance de usar substantivo baseado no efeito
            noun = random.choice(self._effect_nouns[effect_category])

        # Seleciona um padrão de nome aleatório
        name_pattern = random.choice(self._name_patterns)

        # Gera o nome
        return name_pattern(adjective, noun, dominant_element)

    def generate_name(
            self,
            components: List[MagicalComponentInterface],
            effect: Optional[MagicalEffectInterface] = None
    ) -> str:
        """
        Gera um nome para a magia com base nos componentes e efeito.

        Args:
            components: Lista de componentes da magia
            effect: Efeito primário da magia (opcional)

        Returns:
            Nome gerado para a magia
        """
        return self.predict((components, effect))

    def generate_multiple_names(
            self,
            components: List[MagicalComponentInterface],
            effect: Optional[MagicalEffectInterface] = None,
            count: int = 3
    ) -> List[str]:
        """
        Gera múltiplos nomes para a magia com base nos componentes e efeito.

        Args:
            components: Lista de componentes da magia
            effect: Efeito primário da magia (opcional)
            count: Número de nomes para gerar

        Returns:
            Lista de nomes gerados
        """
        names = []
        for _ in range(count):
            names.append(self.generate_name(components, effect))

        # Evita nomes duplicados
        unique_names = list(dict.fromkeys(names))

        # Se gerou menos nomes únicos que o solicitado, gera mais
        while len(unique_names) < count:
            new_name = self.generate_name(components, effect)
            if new_name not in unique_names:
                unique_names.append(new_name)

        return unique_names