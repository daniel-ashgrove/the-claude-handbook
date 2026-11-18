"""The order server over Streamable HTTP, for hosts that reach it remotely."""
import os
from urllib.parse import urlsplit

import anyio
import jwt
from mcp.server.auth.provider import AccessToken
from mcp.server.auth.settings import AuthSettings
from mcp.server.transport_security import TransportSecuritySettings
from starlette.requests import Request
from starlette.responses import JSONResponse

from .server import create_server

PUBLIC_URL = os.environ["SHOP_MCP_URL"]      # exactly what people enter in Claude
ISSUER = os.environ["SHOP_AUTH_ISSUER"]      # the shop's sign-in service
JWKS_URL = os.environ["SHOP_AUTH_JWKS_URL"]  # where it publishes its signing keys
SCOPE = "orders:read"


class ShopTokenVerifier:
    """Accepts only tokens that the shop's sign-in service issued for this server."""

    def __init__(self) -> None:
        self.keys = jwt.PyJWKClient(JWKS_URL)  # fetched when first needed, then cached

    async def verify_token(self, token: str) -> AccessToken | None:
        try:
            key = await anyio.to_thread.run_sync(
                self.keys.get_signing_key_from_jwt, token)
            claims = jwt.decode(token, key, algorithms=["RS256"],
                                audience=PUBLIC_URL, issuer=ISSUER)
        except jwt.PyJWTError:
            return None  # refused: the client gets a 401 and must sign in again
        return AccessToken(
            token=token,
            client_id=str(claims.get("client_id") or claims.get("azp", "")),
            scopes=str(claims.get("scope", "")).split(),
            expires_at=claims.get("exp"),
            resource=PUBLIC_URL,
            subject=claims.get("sub"),
        )


server = create_server(
    auth=AuthSettings(
        issuer_url=ISSUER,
        resource_server_url=PUBLIC_URL,
        required_scopes=[SCOPE],
        validate_token_resource=False,  # the verifier checks the audience itself
    ),
    token_verifier=ShopTokenVerifier(),
)


@server.custom_route("/health", methods=["GET"])
async def health(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok"})  # for uptime checks; needs no token


host = urlsplit(PUBLIC_URL).netloc
app = server.streamable_http_app(
    stateless_http=True,  # older clients too: no session, so any copy can answer
    transport_security=TransportSecuritySettings(
        allowed_hosts=[host, f"{host}:*"]),  # refuse requests for any other name
)
