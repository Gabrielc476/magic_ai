# spellcrafting/utils/config_manager.py
"""
Gerenciador de configuração centralizado para o sistema de crafting.
"""
from typing import Dict, Any, Optional, List
import json
import os


class ConfigManager:
    """
    Gerenciador de configuração centralizado para o sistema de crafting.
    Permite carregar, salvar e acessar configurações globais.
    """

    _instance = None

    def __new__(cls, config_file: Optional[str] = None):
        """Implementa o padrão Singleton."""
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_file: Optional[str] = None):
        """
        Inicializa o gerenciador de configuração.

        Args:
            config_file: Caminho para o arquivo de configuração (opcional)
        """
        if self._initialized:
            return

        self._config_file = config_file or "spellcrafting_config.json"
        self._config = self._load_default_config()

        # Tenta carregar a configuração do arquivo, se existir
        if os.path.exists(self._config_file):
            try:
                with open(self._config_file, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                    self._config.update(file_config)
            except Exception as e:
                print(f"Erro ao carregar configuração: {e}")

        self._initialized = True

    def _load_default_config(self) -> Dict[str, Any]:
        """
        Carrega a configuração padrão.

        Returns:
            Dicionário com configurações padrão
        """
        return {
            # Configurações gerais
            "min_components_for_spell": 3,
            "max_component_power": 10,
            "default_component_power": 5,

            # Configurações de nível
            "max_spell_level": 9,
            "cantrip_level": 0,
            "spell_level_thresholds": [
                (10, 0),  # Cantrip
                (15, 1),  # Nível 1
                (25, 2),  # Nível 2
                (35, 3),  # Nível 3
                (50, 4),  # Nível 4
                (65, 5),  # Nível 5
                (80, 6),  # Nível 6
                (100, 7),  # Nível 7
                (125, 8),  # Nível 8
                (float('inf'), 9)  # Nível 9
            ],

            # Multiplicadores de raridade
            "rarity_multipliers": {
                "comum": 1.0,
                "incomum": 1.2,
                "raro": 1.5,
                "épico": 2.0,
                "lendário": 3.0
            },

            # Pontos por raridade
            "rarity_points": {
                "comum": 0,
                "incomum": 2,
                "raro": 5,
                "épico": 10,
                "lendário": 20
            },

            # Elementos e suas combinações
            "primary_elements": ["fogo", "água", "terra", "ar", "luz", "trevas"],
            "powerful_element_combinations": [
                ["fogo", "ar"],
                ["água", "trevas"],
                ["luz", "ar"],
                ["terra", "fogo"],
                ["trevas", "fogo"],
                ["luz", "trevas"]
            ],

            # Elementos opostos
            "opposing_elements": [
                ["fogo", "água"],
                ["terra", "ar"],
                ["luz", "trevas"]
            ],

            # Compatibilidades elementais
            "element_compatibilities": {
                "fogo": ["ar", "terra"],
                "água": ["ar", "terra"],
                "terra": ["fogo", "água"],
                "ar": ["fogo", "água"],
                "luz": ["ar", "fogo"],
                "trevas": ["terra", "água"]
            },

            # Parâmetros para IA
            "ai": {
                "use_sklearn": True,
                "default_vector_size": 14,
                "element_vector_size": 6
            },

            # Logging
            "logging": {
                "enabled": True,
                "log_file": "spellcrafting.log",
                "log_level": "info"
            }
        }

    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtém um valor de configuração.

        Args:
            key: Chave de configuração
            default: Valor padrão se a chave não existir

        Returns:
            Valor da configuração ou valor padrão
        """
        # Suporta acesso aninhado com notação de ponto (ex: "ai.use_sklearn")
        if "." in key:
            parts = key.split(".")
            config = self._config
            for part in parts[:-1]:
                if part not in config:
                    return default
                config = config[part]

            return config.get(parts[-1], default)

        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Define um valor de configuração.

        Args:
            key: Chave de configuração
            value: Valor a ser definido
        """
        # Suporta acesso aninhado com notação de ponto
        if "." in key:
            parts = key.split(".")
            config = self._config
            for part in parts[:-1]:
                if part not in config:
                    config[part] = {}
                config = config[part]

            config[parts[-1]] = value
        else:
            self._config[key] = value

    def save(self, config_file: Optional[str] = None) -> bool:
        """
        Salva a configuração em um arquivo.

        Args:
            config_file: Caminho para o arquivo (usa o padrão se não especificado)

        Returns:
            True se salvou com sucesso, False caso contrário
        """
        file_path = config_file or self._config_file

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar configuração: {e}")
            return False

    def reset(self) -> None:
        """Restaura a configuração para os valores padrão."""
        self._config = self._load_default_config()

    def get_all(self) -> Dict[str, Any]:
        """
        Retorna a configuração completa.

        Returns:
            Dicionário com todas as configurações
        """
        return self._config.copy()