# spellcrafting/ai/vector_converter.py
"""
Conversores para transformar componentes e efeitos em vetores numéricos.
"""
from typing import List, Dict
from spellcrafting.core import MagicalComponentInterface, MagicalEffectInterface


class VectorConverter:
    """
    Classe para converter objetos do domínio mágico em vetores numéricos
    utilizáveis por algoritmos de machine learning.
    """

    def __init__(self):
        """Inicializa o conversor de vetores."""
        self._elements = ["fogo", "água", "terra", "ar", "luz", "trevas"]
        self._rarities = {"comum": 0, "incomum": 0.25, "raro": 0.5, "épico": 0.75, "lendário": 1.0}
        self._effect_keywords = {
            "fogo": ["fogo", "flam", "queim", "calor", "incendi"],
            "água": ["água", "gelo", "congel", "aquá", "fluido"],
            "terra": ["terra", "rocha", "escudo", "proteç", "barreira"],
            "ar": ["ar", "vento", "tempestade", "furacão", "brisa"],
            "luz": ["luz", "cura", "restau", "iluminaç", "brilho"],
            "trevas": ["trevas", "escurid", "sombra", "corrupç", "veneno"]
        }

    def component_to_vector(self, component: MagicalComponentInterface) -> List[float]:
        """
        Converte um componente em um vetor de características numéricas.

        Args:
            component: Componente mágico

        Returns:
            Vetor de características numéricas
        """
        # Codificação dos elementos (one-hot encoding)
        element_vec = [1.0 if component.element == e else 0.0 for e in self._elements]

        # Normaliza potência para o intervalo [0,1]
        power_norm = component.power / 10.0

        # Codificação da raridade
        rarity_value = self._rarities.get(component.rarity, 0.0)

        # Combina todas as características em um único vetor
        return element_vec + [power_norm, rarity_value]

    def components_to_vector(self, components: List[MagicalComponentInterface]) -> List[float]:
        """
        Cria um vetor representando a combinação de componentes.

        Args:
            components: Lista de componentes mágicos

        Returns:
            Vetor de características numéricas
        """
        # Para cada tipo de elemento, soma a potência de todos os componentes
        element_power = {e: 0.0 for e in self._elements}

        # Conta o número de componentes por elemento
        element_count = {e: 0 for e in self._elements}

        # Calcula a raridade média
        rarity_sum = 0.0

        for comp in components:
            element_power[comp.element] += comp.power
            element_count[comp.element] += 1
            rarity_sum += self._rarities.get(comp.rarity, 0.0)

        # Normaliza as potências
        max_power = max(max(element_power.values()), 1.0)  # Evita divisão por zero
        element_power_norm = [element_power[e] / max_power for e in self._elements]

        # Normaliza as contagens
        element_count_norm = [element_count[e] / len(components) for e in self._elements]

        # Inclui a raridade média
        rarity_avg = rarity_sum / len(components)

        # Inclui o número total de componentes (normalizado para [0,1] assumindo máximo de 10)
        num_components_norm = min(len(components) / 10.0, 1.0)

        return element_power_norm + element_count_norm + [rarity_avg, num_components_norm]

    def effect_to_vector(self, effect: MagicalEffectInterface) -> List[float]:
        """
        Converte um efeito em um vetor de características numéricas.

        Args:
            effect: Efeito mágico

        Returns:
            Vetor de características numéricas
        """
        # Verifica a presença de palavras-chave no nome e descrição
        text = (effect.name + " " + effect.description).lower()
        element_vec = []

        for element, keywords in self._effect_keywords.items():
            # 1 se qualquer palavra-chave estiver presente, 0 caso contrário
            present = 0.0
            for keyword in keywords:
                if keyword in text:
                    present = 1.0
                    break
            element_vec.append(present)

        # Normaliza o poder base para o intervalo [0,1]
        power_norm = min(effect.base_power / 100.0, 1.0)

        return element_vec + [power_norm]

    def encode_effect_label(self, effect_name: str, effect_dict: Dict[str, int]) -> int:
        """
        Codifica o nome do efeito como um inteiro para classificação.

        Args:
            effect_name: Nome do efeito
            effect_dict: Dicionário mapeando nomes de efeitos para índices

        Returns:
            Índice do efeito
        """
        if effect_name not in effect_dict:
            effect_dict[effect_name] = len(effect_dict)

        return effect_dict[effect_name]

    def decode_effect_label(self, label: int, effect_dict: Dict[str, int]) -> str:
        """
        Decodifica o índice do efeito de volta para o nome.

        Args:
            label: Índice do efeito
            effect_dict: Dicionário mapeando nomes de efeitos para índices

        Returns:
            Nome do efeito
        """
        for name, idx in effect_dict.items():
            if idx == label:
                return name

        return "Unknown Effect"