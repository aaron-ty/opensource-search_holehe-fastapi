from typing import Any, Optional
from pydantic import BaseModel

# Import the module mappings from the script files
from src.infrastructure.modules.holehe_modules_script import module_mapping as holehe_module_mapping
from src.infrastructure.modules.ignorant_modules_script import module_mapping as ignorant_module_mapping


class ModuleConfig(BaseModel):
    """Configuration for a single module with proxy settings filtered out."""
    func: Any
    active: bool
    description: str
    method: Optional[str] = None
    client: Optional[dict] = None
    
    class Config:
        arbitrary_types_allowed = True


def _filter_proxy_settings(client_config: Optional[dict]) -> Optional[dict]:
    """Remove all proxy-related settings from client configuration."""
    if not client_config:
        return None
    
    # Filter out proxy settings
    filtered_config = {
        key: value 
        for key, value in client_config.items() 
        if not any(proxy_term in key.lower() for proxy_term in ['proxy', 'useproxy'])
    }
    
    # Ensure use_proxy is always False (direct connections only)
    if filtered_config:
        filtered_config['use_proxy'] = False
    
    return filtered_config if filtered_config else None


# ===== HOLEHE MODULES (Email) =====
# Convert holehe module mapping to ModuleConfig objects WITH PROXY FILTERING
HOLEHE_MODULES: dict[str, ModuleConfig] = {}
for module_name, config in holehe_module_mapping.items():
    HOLEHE_MODULES[module_name] = ModuleConfig(
        func=config["func"],
        active=config["active"],
        description=config["description"],
        method=config.get("method"),
        client=_filter_proxy_settings(config.get("client"))  #   FILTER PROXY SETTINGS
    )


# ===== IGNORANT MODULES (Phone) =====
# Convert ignorant module mapping to ModuleConfig objects WITH PROXY FILTERING
IGNORANT_MODULES: dict[str, ModuleConfig] = {}
for module_name, config in ignorant_module_mapping.items():
    IGNORANT_MODULES[module_name] = ModuleConfig(
        func=config["func"],
        active=config["active"],
        description=config["description"],
        method=config.get("method"),
        client=_filter_proxy_settings(config.get("client"))  #   FILTER PROXY SETTINGS
    )


def get_all_holehe_modules() -> list[str]:
    """Get list of all holehe module names."""
    return list(HOLEHE_MODULES.keys())


def get_active_holehe_modules() -> list[str]:
    """Get list of active holehe module names."""
    return [name for name, config in HOLEHE_MODULES.items() if config.active]


def get_all_ignorant_modules() -> list[str]:
    """Get list of all ignorant module names."""
    return list(IGNORANT_MODULES.keys())


def get_active_ignorant_modules() -> list[str]:
    """Get list of active ignorant module names."""
    return [name for name, config in IGNORANT_MODULES.items() if config.active]


def get_holehe_module(name: str) -> Optional[ModuleConfig]:
    """Get holehe module configuration by name."""
    return HOLEHE_MODULES.get(name)


def get_ignorant_module(name: str) -> Optional[ModuleConfig]:
    """Get ignorant module configuration by name."""
    return IGNORANT_MODULES.get(name)