# spellcrafting/core/spell.py
"""
Implementação de magias.
"""
from typing import List, Dict, Any, Optional
from .interfaces import (
    SpellInterface,
    MagicalComponentInterface,
    MagicalEffectInterface,
    PowerCalculatorInterface,
    LevelCalculatorInterface,
    ElementDominanceCalculatorInterface,
    ScalingCalculatorInterface
)


class Spell(SpellInterface):
    """
    Magia criada a partir de componentes mágicos.
    """

    def __init__(
            self,
            name: str,
            components: List[MagicalComponentInterface],
            primary_effect: Optional[MagicalEffectInterface] = None,
            secondary_effects: Optional[List[MagicalEffectInterface]] = None,
            power_calculator: Optional[PowerCalculatorInterface] = None,
            level_calculator: Optional[LevelCalculatorInterface] = None,
            element_calculator: Optional[ElementDominanceCalculatorInterface] = None,
            scaling_calculator: Optional[ScalingCalculatorInterface] = None
    ):
        """
        Inicializa uma magia.

        Args:
            name: Nome da magia
            components: Lista de componentes mágicos
            primary_effect: Efeito primário da magia
            secondary_effects: Efeitos secundários da magia
            power_calculator: Calculadora de poder
            level_calculator: Calculadora de nível
            element_calculator: Calculadora de elemento dominante
            scaling_calculator: Calculadora de escalonamento
        """
        if len(components) < 3:
            raise ValueError("Uma magia precisa de pelo menos 3 componentes")

        self._name = name
        self._components = components
        self._primary_effect = primary_effect
        self._secondary_effects = secondary_effects if secondary_effects else []

        self._power_calculator = power_calculator
        self._level_calculator = level_calculator
        self._element_calculator = element_calculator
        self._scaling_calculator = scaling_calculator

        # Inicializa propriedades calculadas
        self._power = self._calculate_power()
        self._dominant_element = self._determine_dominant_element()
        self._level = self._determine_level()
        self._scaled_effect = self._calculate_scaled_effect()

    @property
    def name(self) -> str:
        """Retorna o nome da magia."""
        return self._name

    @property
    def components(self) -> List[MagicalComponentInterface]:
        """Retorna os componentes da magia."""
        return self._components.copy()

    @property
    def primary_effect(self) -> Optional[MagicalEffectInterface]:
        """Retorna o efeito primário da magia."""
        return self._primary_effect

    @property
    def secondary_effects(self) -> List[MagicalEffectInterface]:
        """Retorna os efeitos secundários da magia."""
        return self._secondary_effects.copy()

    @property
    def power(self) -> int:
        """Retorna o poder calculado da magia."""
        return self._power

    @property
    def dominant_element(self) -> str:
        """Retorna o elemento dominante da magia."""
        return self._dominant_element

    @property
    def level(self) -> int:
        """Retorna o nível da magia."""
        return self._level

    def _calculate_power(self) -> int:
        """Calcula o poder da magia."""
        if self._power_calculator:
            return self._power_calculator.calculate(self._components)

        # Implementação padrão se não houver calculadora específica
        # Calcula o poder com base na potência e raridade dos componentes
        base_power = sum(component.power for component in self._components)
        rarity_multiplier = 1.0

        for component in self._components:
            if component.rarity == "comum":
                rarity_multiplier *= 1.0
            elif component.rarity == "incomum":
                rarity_multiplier *= 1.2
            elif component.rarity == "raro":
                rarity_multiplier *= 1.5
            elif component.rarity == "épico":
                rarity_multiplier *= 2.0
            elif component.rarity == "lendário":
                rarity_multiplier *= 3.0

        return round(base_power * rarity_multiplier)

    def _determine_dominant_element(self) -> str:
        """Determina o elemento dominante da magia."""
        if self._element_calculator:
            return self._element_calculator.calculate(self._components)

        # Implementação padrão se não houver calculadora específica
        # Conta a frequência de cada elemento
        elements = {}
        for component in self._components:
            if component.element in elements:
                elements[component.element] += component.power
            else:
                elements[component.element] = component.power

        # Retorna o elemento com a maior potência combinada
        return max(elements, key=elements.get)

    def _determine_level(self) -> int:
        """Determina o nível da magia (0-9)."""
        if self._level_calculator:
            return self._level_calculator.calculate(self._power, self._components)

        # Implementação padrão se não houver calculadora específica
        # Base de pontuação a partir do poder
        base_score = self._power

        # Adiciona pontos por componentes de raridade superior
        rarity_points = 0
        for component in self._components:
            if component.rarity == "comum":
                rarity_points += 0
            elif component.rarity == "incomum":
                rarity_points += 2
            elif component.rarity == "raro":
                rarity_points += 5
            elif component.rarity == "épico":
                rarity_points += 10
            elif component.rarity == "lendário":
                rarity_points += 20

        # Adiciona pontos pelo número de componentes além do mínimo (3)
        component_points = max(0, (len(self._components) - 3) * 3)

        # Adiciona pontos por combinações de elementos específicas
        element_points = 0
        present_elements = set(component.element for component in self._components)

        # Combinações elementais poderosas
        powerful_combinations = [
            {"fogo", "ar"},  # Tempestade de fogo
            {"água", "trevas"},  # Magia negra aquática
            {"luz", "ar"},  # Magias celestiais
            {"terra", "fogo"},  # Magias vulcânicas
            {"trevas", "fogo"},  # Magia demoníaca
            {"luz", "trevas"}  # Magias de dualidade (muito raras)
        ]

        for combo in powerful_combinations:
            if combo.issubset(present_elements):
                element_points += 5

        # Combinação de todos os elementos (extremamente poderosa)
        if len(present_elements) >= 4:
            element_points += 10
        if len(present_elements) >= 5:
            element_points += 20

        # Calcula a pontuação total
        total_score = base_score + rarity_points + component_points + element_points

        # Mapeia para níveis de magia
        if total_score < 10:
            return 0  # Cantrip (truque)
        elif total_score < 15:
            return 1
        elif total_score < 25:
            return 2
        elif total_score < 35:
            return 3
        elif total_score < 50:
            return 4
        elif total_score < 65:
            return 5
        elif total_score < 80:
            return 6
        elif total_score < 100:
            return 7
        elif total_score < 125:
            return 8
        else:
            return 9  # Magia mais poderosa

    def _calculate_scaled_effect(self) -> Dict[int, Dict[str, Any]]:
        """Calcula como o efeito da magia escala com base no nível."""
        if self._scaling_calculator and self._primary_effect:
            return self._scaling_calculator.calculate(self)

        # Implementação padrão se não houver calculadora específica
        if not self._primary_effect:
            return {}

        base_effect = self._primary_effect
        scaling = {}

        # Define como o efeito escala por nível
        for level in range(max(1, self._level), 10):
            # Aumento de poder base escala de forma não linear
            power_increase = base_effect.base_power * (1 + (level - self._level) * 0.5)

            # Aumento de alcance/área de efeito
            base_range = 10  # pés
            increased_area = base_range * (1 + (level - self._level) * 0.3)

            # Aumento de duração
            base_duration = 1  # rodada/minuto
            increased_duration = base_duration * (1 + (level - self._level) * 0.5)

            # Efeitos adicionais baseados no elemento dominante
            additional_effects = []
            if level - self._level >= 2:  # A cada 2 níveis, adiciona um efeito
                if self._dominant_element == "fogo":
                    additional_effects.append(f"Dano adicional de {5 * (level - self._level)} de fogo por rodada")
                elif self._dominant_element == "água":
                    additional_effects.append(f"Reduz a velocidade do alvo em {5 * (level - self._level)} pés")
                elif self._dominant_element == "terra":
                    additional_effects.append(f"Cria terreno difícil num raio de {5 * (level - self._level)} pés")
                elif self._dominant_element == "ar":
                    additional_effects.append(f"Empurra alvos até {5 * (level - self._level)} pés")
                elif self._dominant_element == "luz":
                    additional_effects.append(f"Cura aliados em {3 * (level - self._level)} pontos de vida")
                elif self._dominant_element == "trevas":
                    additional_effects.append(f"Causa condição de cegueira por {level - self._level} rodadas")

            scaling[level] = {
                "poder": round(power_increase),
                "alcance": round(increased_area),
                "duracao": round(increased_duration),
                "efeitos_adicionais": additional_effects
            }

        return scaling

    def add_component(self, component: MagicalComponentInterface) -> None:
        """Adiciona um componente à magia e recalcula propriedades."""
        self._components.append(component)

        # Recalcula propriedades ao adicionar novo componente
        self._power = self._calculate_power()
        self._dominant_element = self._determine_dominant_element()
        self._level = self._determine_level()
        self._scaled_effect = self._calculate_scaled_effect()

    def scale(self, casting_level: int) -> Dict[str, Any]:
        """Retorna a versão escalonada da magia com base no nível de conjuração."""
        if casting_level <= self._level:
            return {
                "poder": self._primary_effect.base_power if self._primary_effect else 0,
                "alcance": 10,  # Padrão básico
                "duracao": 1,  # Padrão básico
                "efeitos_adicionais": []
            }

        if casting_level in self._scaled_effect:
            return self._scaled_effect[casting_level]

        return None  # Não pode ser escalonada além do nível 9

    def get_level_description(self) -> str:
        """Retorna uma descrição textual do nível da magia."""
        if self._level == 0:
            return "Truque (Cantrip)"

        level_descriptions = {
            1: "Nível 1 (Básica)",
            2: "Nível 2 (Aprendiz)",
            3: "Nível 3 (Adepto)",
            4: "Nível 4 (Avançada)",
            5: "Nível 5 (Superior)",
            6: "Nível 6 (Arcana)",
            7: "Nível 7 (Arcana Superior)",
            8: "Nível 8 (Mística)",
            9: "Nível 9 (Lendária)"
        }

        return level_descriptions.get(self._level, f"Nível {self._level}")

    def get_caster_requirements(self) -> str:
        """Retorna os requisitos mínimos para um conjurador usar esta magia."""
        if self._level == 0:
            return "Qualquer conjurador iniciante pode usar esta magia."

        caster_level = max(1, self._level * 2 - 1)

        return f"Requer um conjurador de nível {caster_level} ou superior."

    def to_dict(self) -> Dict[str, Any]:
        """Converte a magia para um dicionário."""
        return {
            "name": self._name,
            "level": self._level,
            "level_description": self.get_level_description(),
            "power": self._power,
            "dominant_element": self._dominant_element,
            "components": [comp.to_dict() for comp in self._components],
            "primary_effect": self._primary_effect.to_dict() if self._primary_effect else None,
            "secondary_effects": [effect.to_dict() for effect in self._secondary_effects],
            "caster_requirements": self.get_caster_requirements(),
            "scaled_effects": self._scaled_effect
        }

    def __str__(self) -> str:
        """Retorna uma representação em string da magia."""
        components_str = ", ".join(component.name for component in self._components)
        secondary_effects_str = ", ".join(
            str(effect) for effect in self._secondary_effects) if self._secondary_effects else "Nenhum"

        desc_base = (f"Magia: {self._name}\n"
                     f"Classificação: {self.get_level_description()}\n"
                     f"Poder: {self._power}\n"
                     f"Elemento dominante: {self._dominant_element}\n"
                     f"Componentes: {components_str}\n"
                     f"Efeito primário: {self._primary_effect}\n"
                     f"Efeitos secundários: {secondary_effects_str}\n"
                     f"{self.get_caster_requirements()}")

        # Adiciona informações de escalonamento se não for um truque
        if self._level > 0 and self._scaled_effect:
            desc_base += "\n\nEscalonamento por Nível:"
            for level, effect in self._scaled_effect.items():
                add_effects = ", ".join(effect["efeitos_adicionais"]) if effect["efeitos_adicionais"] else "Nenhum"
                desc_base += f"\n  Nível {level}: Poder {effect['poder']}, Alcance {effect['alcance']} pés, Duração {effect['duracao']} rodadas"
                if add_effects != "Nenhum":
                    desc_base += f"\n    Efeitos adicionais: {add_effects}"

        return desc_base