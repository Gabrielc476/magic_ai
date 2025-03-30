# Sistema de Crafting de Magia

Um sistema modular para criação de magias baseado em componentes, implementado com padrões de design e princípios de programação orientada a objetos.

## Visão Geral

Este sistema permite criar magias através da combinação de componentes mágicos, seguindo regras específicas e calculando automaticamente o poder, nível e efeitos da magia resultante. O sistema foi projetado com modularidade, extensibilidade e manutenibilidade em mente, utilizando diversos padrões de design para separar responsabilidades e permitir fácil expansão.

## Estrutura do Projeto

```
spellcrafting/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── interfaces.py     # Interfaces e classes abstratas
│   ├── component.py      # Componente mágico
│   ├── effect.py         # Efeito mágico
│   ├── spell.py          # Magia completa
├── system/
│   ├── __init__.py
│   ├── crafting_system.py   # Sistema de crafting principal
│   ├── recipe_manager.py    # Gerenciador de receitas
│   ├── element_manager.py   # Gerenciador de elementos e compatibilidades
├── calculators/
│   ├── __init__.py
│   ├── power_calculator.py   # Estratégia para cálculo de poder
│   ├── level_calculator.py   # Estratégia para cálculo de nível
│   ├── scaling_calculator.py # Estratégia para cálculo de escalonamento
├── ai/
│   ├── __init__.py
│   ├── recommendation_engine.py  # Motor de recomendação
│   ├── effect_predictor.py       # Preditor de efeitos
│   ├── name_generator.py         # Gerador de nomes
│   ├── vector_converter.py       # Conversor para vetores numéricos
├── rules/
│   ├── __init__.py
│   ├── combination_rules.py   # Regras de combinação
├── factories/
│   ├── __init__.py
│   ├── component_factory.py   # Fábrica de componentes
│   ├── effect_factory.py      # Fábrica de efeitos
│   ├── spell_factory.py       # Fábrica de magias
└── utils/
    ├── __init__.py
    ├── constants.py          # Constantes do sistema
    ├── enums.py              # Enumerações (Raridade, Elemento, etc.)
    ├── observers.py          # Observadores para eventos do sistema
```

## Padrões de Design Implementados

### 1. Strategy Pattern
Permite definir diferentes estratégias para cálculos como poder, nível e escalonamento da magia.

**Implementação:** `calculators/power_calculator.py`, `calculators/level_calculator.py`

**Benefícios:**
- Flexibilidade para trocar algoritmos sem alterar as classes cliente
- Facilidade para implementar novos algoritmos de cálculo
- Eliminação de grandes estruturas condicionais

### 2. Factory Pattern
Centraliza a criação de objetos complexos como componentes, efeitos e magias.

**Implementação:** `factories/__init__.py`

**Benefícios:**
- Encapsulamento da lógica de criação
- Facilidade para modificar o processo de criação
- Consistência na criação de objetos

### 3. Observer Pattern
Permite que objetos se registrem para receber notificações sobre eventos no sistema.

**Implementação:** `utils/observers.py`

**Benefícios:**
- Baixo acoplamento entre o sistema e os observadores
- Facilidade para adicionar novos observadores
- Notificações em tempo real sobre eventos

### 4. Command Pattern
Encapsula operações em objetos, permitindo parametrização e filas de execução.

**Implementação:** Regras de combinação em `rules/combination_rules.py`

**Benefícios:**
- Desacoplamento entre o invocador e o receptor
- Facilidade para adicionar novas operações
- Suporte para operações compostas

### 5. Template Method Pattern
Define o esqueleto de um algoritmo, permitindo que subclasses modifiquem partes específicas.

**Implementação:** Métodos de cálculo na classe `Spell`

**Benefícios:**
- Reutilização de código
- Consistência na estrutura do algoritmo
- Flexibilidade para personalizar partes específicas

### 6. Singleton Pattern (implícito)
Garante que uma classe tenha apenas uma instância e fornece um ponto global de acesso.

**Benefícios:**
- Acesso global a recursos compartilhados
- Controle sobre o número de instâncias
- Economia de recursos do sistema

## Sistema de IA

O sistema inclui componentes de IA para melhorar a experiência de crafting:

1. **Motor de Recomendação**: Sugere componentes compatíveis para completar uma magia.
2. **Preditor de Efeitos**: Prevê o efeito mais provável para uma combinação de componentes.
3. **Gerador de Nomes**: Cria nomes temáticos para as magias com base em seus componentes e efeitos.

Estas funcionalidades usam uma combinação de regras baseadas em especialistas e algoritmos de machine learning.

## Como Usar

Veja o arquivo `example.py` para um exemplo completo de uso do sistema. Aqui está um resumo básico:

```python
# Configurar o sistema
system = setup_system()

# Criar uma magia
spell = system.create_spell(
    "Tornado de Chamas",
    ["Pena de Fênix", "Essência de Chamas", "Brisa Etérea", "Sussurro do Vento"]
)

# Obter recomendações de componentes
recommendation_engine = ComponentRecommendationEngine(system)
recommendation_engine.train()
recommended = recommendation_engine.predict([component1, component2])

# Prever efeito
effect_predictor = EffectPredictor(system)
effect_predictor.train()
predicted_effect = effect_predictor.predict([component1, component2, component3])

# Gerar nome
name_generator = SpellNameGenerator()
spell_name = name_generator.generate_name(components, effect)
```

## Extensão do Sistema

O sistema foi projetado para ser facilmente extensível:

1. **Novos Componentes**: Registre novos componentes através do `ComponentFactory`.
2. **Novos Efeitos**: Crie e registre efeitos via `EffectFactory`.
3. **Novas Regras**: Implemente a interface `CombinationRuleInterface` e adicione ao sistema.
4. **Novas Estratégias de Cálculo**: Implemente as interfaces específicas de calculadora.
5. **Novos Observadores**: Implemente a interface `ObserverInterface` e registre no sistema.

## Conclusão

Este sistema de crafting de magia demonstra como os padrões de design podem ser aplicados para criar um sistema modular, extensível e fácil de manter. A arquitetura permite adicionar novas funcionalidades com o mínimo de alterações no código existente, seguindo os princípios SOLID da programação orientada a objetos.