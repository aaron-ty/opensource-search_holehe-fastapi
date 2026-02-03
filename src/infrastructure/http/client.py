import asyncio
from typing import Any, Optional, Dict
import httpx
import random

from src.core.logging import get_logger
from src.core.config import get_settings
settings = get_settings()
logger = get_logger(__name__)


class ConfigurableHTTPClient:
    """
    HTTP client that respects module-specific configurations.
    Supports HTTP/1.1 and HTTP/2, custom headers, and various settings.
    NO PROXY - Direct connections only.
    """
    
    def __init__(
        self,
        timeout: Optional[int] = None,
        verify_ssl: Optional[bool] = None,
        headers: Optional[dict] = None,
        http2: bool = False,
        impersonate: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize HTTP client with configuration.
        """
        self.timeout = timeout or settings.HTTP_TIMEOUT
        self.verify_ssl = verify_ssl if verify_ssl is not None else settings.HTTP_VERIFY_SSL
        self.http2 = http2
        self.impersonate = impersonate
        self.custom_headers = headers or {}
        self.extra_kwargs = kwargs
        
        # Build default headers based on impersonation
        self.default_headers = self._build_headers()
        
        logger.info(f"HTTP client initialized: HTTP/2={http2}, Impersonate={impersonate}, DirectConnection=True")
    
    def _build_headers(self) -> Dict[str, str]:
        """Build headers based on impersonation settings."""
        headers = {}
        
        # Common headers for all impersonations
        common_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }
        
        if self.impersonate == "chrome99_android":
            headers.update({
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 Mobile Safari/537.36",
                **common_headers
            })
        elif self.impersonate == "chrome99":
            headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
                **common_headers
            })
        else:
            # Default modern Chrome
            headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                **common_headers
            })
        
        # Merge with custom headers
        headers.update(self.custom_headers)
        return headers
    
    async def request(
        self,
        method: str,
        url: str,
        headers: Optional[dict] = None,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        params: Optional[dict] = None,
        allow_redirects: bool = True,
        **kwargs
    ) -> httpx.Response:
        """
        Make an HTTP request with module-specific configuration.
        NO PROXY - Direct connections only.
        """
        # Merge headers: defaults < custom < request-specific
        merged_headers = {**self.default_headers, **(headers or {})}
        
        # Create client with configuration - NO PROXY
        client_kwargs = {
            "timeout": self.timeout,
            "verify": self.verify_ssl,
            "follow_redirects": allow_redirects,
            "http2": self.http2,
        }
        
        #   ENSURE NO PROXY IS USED
        client_kwargs["proxies"] = None
        
        async with httpx.AsyncClient(**client_kwargs) as client:
            try:
                logger.debug(f"DIRECT CONNECTION: {method} {url}")
                
                response = await client.request(
                    method=method.upper(),
                    url=url,
                    headers=merged_headers,
                    data=data,
                    json=json,
                    params=params,
                    **kwargs
                )
                
                logger.debug(f"Response: {method} {url} -> {response.status_code}")
                return response
                
            except httpx.TimeoutException:
                logger.error(f"Request timeout: {method} {url}")
                raise
            except httpx.HTTPError as e:
                logger.error(f"HTTP error: {method} {url} - {str(e)}")
                raise
    
    async def get(self, url: str, **kwargs) -> httpx.Response:
        """Make a GET request with direct connection."""
        return await self.request("GET", url, **kwargs)
    
    async def post(self, url: str, **kwargs) -> httpx.Response:
        """Make a POST request with direct connection."""
        return await self.request("POST", url, **kwargs)


class ModuleCompatibleClient:
    """
    Client interface compatible with holehe/ignorant modules.
    Maps legacy client configurations to modern HTTP client.
    NO PROXY SUPPORT - Direct connections only.
    """
    
    def __init__(
        self,
        request_class: Optional[str] = None,
        use_proxy: bool = False,  # IGNORED - no proxy support
        proxy_group: Optional[str] = None,  # IGNORED
        proxy_group_fallback: Optional[str] = None,  # IGNORED
        impersonate: Optional[str] = "chrome99",
        timeout: int = settings.HTTP_TIMEOUT,
        headers: Optional[dict] = None,
        **kwargs
    ):
        """
        Initialize module-compatible client.
        """
        #   ENFORCE DIRECT CONNECTIONS
        if use_proxy or proxy_group or proxy_group_fallback:
            logger.warning("Proxy configuration requested but IGNORED - using direct connection")
        
        # Determine HTTP version from request_class
        http2 = self._should_use_http2(request_class)
        
        # Create configured HTTP client with DIRECT CONNECTION
        self.client = ConfigurableHTTPClient(
            timeout=timeout,
            headers=headers,
            http2=http2,
            impersonate=impersonate,
            **kwargs
        )
        
        logger.info(f"Module client initialized: HTTP/2={http2}, Impersonate={impersonate}")
    
    def _should_use_http2(self, request_class: Optional[str]) -> bool:
        """Determine if HTTP/2 should be used based on request class."""
        if not request_class:
            return False
        
        http2_classes = ["RequestBaseParamsH2", "RequestH2"]
        return any(h2_class in str(request_class) for h2_class in http2_classes)
    
    async def get(self, url: str, **kwargs) -> httpx.Response:
        """Make a GET request with direct connection."""
        return await self.client.get(url, **kwargs)
    
    async def post(self, url: str, **kwargs) -> httpx.Response:
        """Make a POST request with direct connection."""
        return await self.client.post(url, **kwargs)
    
    async def put(self, url: str, **kwargs) -> httpx.Response:
        """Make a PUT request with direct connection."""
        return await self.client.request("PUT", url, **kwargs)
    
    async def head(self, url: str, **kwargs) -> httpx.Response:
        """Make a HEAD request with direct connection."""
        return await self.client.request("HEAD", url, **kwargs)
    
    async def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """Make a generic request with direct connection."""
        return await self.client.request(method, url, **kwargs)