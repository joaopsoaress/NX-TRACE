"""HTTP utilities"""

import requests
from typing import Dict, Optional, Any
from dataclasses import dataclass

@dataclass
class HTTPResponse:
    status_code: int
    content: bytes
    text: str
    headers: Dict
    elapsed: float
    url: str

class HTTPClient:
    
    def __init__(self, timeout: int=10, verify_ssl: bool = True,
                 proxy: Optional[str] = None, headers: Optional[Dict] = None):
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.proxy = proxy
        self.session = requests.Session()

        # Default headers
        self.session.headers.update({
            "User-Agent": "NX-TRACE-Scanner/2.0.0",
            "Accept": "application/json, */*"
        })

        # Custom headers
        if headers:
            self.session.headers.update(headers)
        
        # Proxy configuration
        if proxy:
            self.session.proxies = {
                "http": proxy,
                "https": proxy
            }

    def request(self, method: str, url: str, **kwargs) -> Optional[HTTPResponse]:
        """Make HTTP request with error handling"""
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                verify=self.verify_ssl,
                allow_redirects=False,
                **kwargs
            )
            
            return HTTPResponse(
                status_code=response.status_code,
                content=response.content,
                text=response.text,
                headers=dict(response.headers),
                elapsed=response.elapsed.total_seconds(),
                url=response.url
            )
            
        except requests.exceptions.Timeout:
            return None
        except requests.exceptions.ConnectionError:
            return None
        except Exception:
            return None
    
    def get(self, url: str, **kwargs) -> Optional[HTTPResponse]:
        return self.request("GET", url, **kwargs)
    
    def post(self, url: str, **kwargs) -> Optional[HTTPResponse]:
        return self.request("POST", url, **kwargs)
    
    def put(self, url: str, **kwargs) -> Optional[HTTPResponse]:
        return self.request("PUT", url, **kwargs)
    
    def delete(self, url: str, **kwargs) -> Optional[HTTPResponse]:
        return self.request("DELETE", url, **kwargs)