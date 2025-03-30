# spellcrafting/ai/ai_manager.py
"""
Gerenciador central para as funcionalidades de IA do sistema.
"""
from typing import List, Optional
from spellcrafting.core import MagicalComponentInterface, MagicalEffectInterface
from spellcrafting.system.crafting_system import CraftingSystem
from .recommendation_engine import ComponentRecommendationEngine
from .effect_predictor import EffectPredictor, ElementalAffinityPredictor
from .name_generator import SpellNameGenerator
from .vector_converter import VectorConverter
from spellcrafting.core import MagicalEffect
from collections import Counter


class AIManager:
    """
    Gerenciador central para todas as funcionalidades de IA do sistema.
    Facilita o acesso e uso dos diversos modelos de IA implementados.
    """

    def __init__(self, crafting_system: CraftingSystem):
        """
        Inicializa o gerenciador de IA.

        Args:
            crafting_system: Sistema de crafting usado pelos modelos
        """
        self._crafting_system = crafting_system
        self._vector_converter = VectorConverter()

        # Inicializa os diversos modelos
        self._recommendation_engine = ComponentRecommendationEngine(
            crafting_system, self._vector_converter
        )
        self._effect_predictor = EffectPredictor(
            crafting_system, self._vector_converter
        )
        self._elemental_affinity_predictor = ElementalAffinityPredictor(
            crafting_system
        )
        self._name_generator = SpellNameGenerator()

        # Flag para indicar se os modelos estão treinados
        self._trained = False

    def train_all_models(self) -> bool:
        """
        Treina todos os modelos de IA disponíveis.

        Returns:
            True se todos os modelos foram treinados com sucesso, False caso contrário
        """
        success = True

        try:
            # Tenta treinar cada modelo
            if not self._recommendation_engine.train():
                success = False

            if not self._effect_predictor.train():
                success = False

            # O preditor de afinidade elemental e o gerador de nomes não precisam de treinamento

            self._trained = success
            return success

        except Exception as e:
            print(f"Erro durante o treinamento dos modelos de IA: {e}")
            return False

    def get_component_recommendations(
            self,
            components: List[MagicalComponentInterface],
            count: int = 3
    ) -> List[MagicalComponentInterface]:
        """
        Obtém recomendações de componentes com base nos componentes atuais.

        Args:
            components: Lista de componentes atuais
            count: Número de recomendações desejadas

        Returns:
            Lista de componentes recomendados
        """
        if not self._trained:
            self._recommendation_engine.train()

        # Limita o count a no máximo 5 para evitar excesso de recomendações
        count = min(count, 5)

        try:
            return self._recommendation_engine.predict(components)[:count]
        except Exception as e:
            print(f"Erro ao gerar recomendações: {e}")
            # Retorna uma lista vazia em caso de erro
            return []

    def predict_effect(
            self,
            components: List[MagicalComponentInterface],
            use_elemental_affinity: bool = False
    ) -> MagicalEffectInterface:
        """
        Prevê o efeito mais provável para uma combinação de componentes.

        Args:
            components: Lista de componentes
            use_elemental_affinity: Se True, usa o preditor de afinidade elemental

        Returns:
            Efeito mágico previsto
        """
        if not self._trained and not use_elemental_affinity:
            self._effect_predictor.train()

        try:
            if use_elemental_affinity:
                return self._elemental_affinity_predictor.predict(components)
            else:
                return self._effect_predictor.predict(components)
        except Exception as e:
            print(f"Erro ao prever efeito: {e}")
            # Cria um efeito genérico em caso de erro
            return self._create_generic_effect(components)

    def generate_spell_name(
            self,
            components: List[MagicalComponentInterface],
            effect: Optional[MagicalEffectInterface] = None,
            count: int = 1
    ) -> List[str]:
        """
        Gera nomes para uma magia com base nos componentes e efeito.

        Args:
            components: Lista de componentes
            effect: Efeito da magia (opcional)
            count: Número de nomes para gerar

        Returns:
            Lista de nomes gerados
        """
        try:
            if count == 1:
                return [self._name_generator.generate_name(components, effect)]
            else:
                return self._name_generator.generate_multiple_names(components, effect, count)
        except Exception as e:
            print(f"Erro ao gerar nome: {e}")
            # Gera um nome genérico em caso de erro
            return ["Magia Arcana"]

    def explain_recommendation(self, components: List[MagicalComponentInterface]) -> str:
        """
        Explica por que esses componentes foram recomendados.

        Args:
            components: Lista de componentes recomendados

        Returns:
            Texto explicativo
        """
        try:
            return self._recommendation_engine.explain_recommendation(components)
        except Exception as e:
            print(f"Erro ao explicar recomendação: {e}")
            return "Estes componentes foram selecionados com base em análise de compatibilidade mágica."

    def _create_generic_effect(self, components: List[MagicalComponentInterface]) -> MagicalEffectInterface:
        """
        Cria um efeito genérico com base nos componentes, para uso em casos de fallback.

        Args:
            components: Lista de componentes

        Returns:
            Efeito mágico genérico
        """
        if not components:
            return MagicalEffect("Efeito Desconhecido", "Produz um efeito mágico imprevisível", 5)

        # Determina o elemento dominante
        element_counts = Counter(comp.element for comp in components)
        dominant_element = element_counts.most_common(1)[0][0]

        # Calcula o poder total
        total_power = sum(comp.power for comp in components)

        return MagicalEffect(
            f"Manifestação de {dominant_element.capitalize()}",
            f"Produz uma manifestação mágica de {dominant_element}",
            total_power
        )