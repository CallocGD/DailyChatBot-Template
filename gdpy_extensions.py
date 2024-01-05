"""

GDPY Extensions 
---------------

An add-on library for gd.py that allows for 
socks4 and socks5 proxy support through `aiohttp_socks`

::

    from gdpy_extensions import ProxyClient

    async def get_daily():
        client = ProxyClient(proxy_url="socks5://localhost:9050")
        daily_level = await client.get_daily()
        ...

"""

from aiohttp import ClientSession
from aiohttp_socks import (
    ProxyConnector,
    ProxyTimeoutError,
    ProxyConnectionError,
    ProxyError,
)
from gd import Client, Session, HTTPClient
from attrs import field, define, frozen


__license__ = "MIT"
__version__ = "0.0.2"
__author__ = "Calloc"


COMMON_PROXY_ERRORS = ProxyTimeoutError, ProxyConnectionError, ProxyError
"""Makes it very simple to write an exception since it is common 
for proxies to fail a request"""


@define(slots=False)
class ProxyHTTPClient(HTTPClient):
    """Enforces gdpy to go through any proxy and that has support for
    socks4 , socks5 and http"""

    proxy_url:str = field(factory=str)
    rdns: bool = field(default=False)
    transport: ProxyConnector = field(init=False)

    def __attrs_post_init__(self) -> None:
        self.transport = ProxyConnector.from_url(self.proxy_url, rdns=self.rdns)
        return super().__attrs_post_init__()

    def __hash__(self) -> int:
        return id(self)

    async def create_session(self) -> ClientSession:
        return ClientSession(
            skip_auto_headers=self.SKIP_HEADERS, connector=self.transport, timeout=30
        )

    def rotate_proxy(self, proxy_url: str, rdns: bool = True):
        """Used to rotate a proxy. This is good from when
        one of several things have happened

        - The Server has banned your proxy (403 Forbidden)
        - The Server has Rate-limited your proxy (429 Too Many Requests)
        - The Proxy itself is dead (Connection Failure)...
        """
        self.rdns = rdns
        self.proxy_url = proxy_url
        self.transport = ProxyConnector.from_url(proxy_url, rdns=self.rdns)


@frozen()
class ProxySession(Session):
    proxy_url: str
    http: ProxyHTTPClient = field(init=False)

    def __attrs_post_init__(self):
        # see: https://www.attrs.org/en/stable/init.html#post-init
        object.__setattr__(self, "http", ProxyHTTPClient(proxy_url=self.proxy_url))


@define(slots=False)
class ProxyClient(Client):
    proxy_url: str = field(factory=str)
    session: ProxySession = field(init=False)

    def __attrs_post_init__(self):
        self.session = ProxySession(self.proxy_url)
        self.rotate_proxy = self.http.rotate_proxy

    @property
    def http(self):
        return self.session.http

