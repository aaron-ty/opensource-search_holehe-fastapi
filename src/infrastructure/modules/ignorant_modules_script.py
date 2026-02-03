from ignorant.modules.shopping.amazon import amazon
from ignorant.modules.social_media.instagram import instagram
from ignorant.modules.social_media.snapchat import snapchat
from pydash import get
from src.infrastructure.modules.requests_logic  import RequestBaseParamsCFFIAsync

module_mapping = {
    "amazon": {
        "func": amazon,
        "active": True,
        "description": "amazon.com",
    },
    "instagram": {
        "func": instagram,
        "active": False,
        "description": "instagram.com",
        "client": {
            "request_class": RequestBaseParamsCFFIAsync,
            "use_proxy": True,
            "proxy_group": "2",
            "proxy_group_fallback": "2",
        },
    },
    "snapchat": {
        "func": snapchat,
        "active": True,
        "description": "snapchat.com",
        "method": "login",
    },
}


MODULES = list(module_mapping.keys())
ACTIVE_MODULES = [key for key in MODULES if get(module_mapping, f"{key}.active")]
