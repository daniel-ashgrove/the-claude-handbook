"""A stand-in for the shop's sign-in service, for local testing only.

Run once to create a signing key and jwks.json, then serve jwks.json and use
the printed token. Never use this key or these tokens anywhere real.
"""
import json
import sys
import time
from pathlib import Path

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from jwt.algorithms import RSAAlgorithm

HERE = Path(__file__).parent
KEY_FILE = HERE / "test_key.pem"


def signing_key() -> rsa.RSAPrivateKey:
    if not KEY_FILE.exists():
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        KEY_FILE.write_bytes(key.private_bytes(
            serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption()))
    key = serialization.load_pem_private_key(KEY_FILE.read_bytes(), password=None)
    assert isinstance(key, rsa.RSAPrivateKey)
    return key


def main(issuer: str, audience: str, scope: str) -> None:
    key = signing_key()
    public = json.loads(RSAAlgorithm.to_jwk(key.public_key()))
    public.update(kid="test", use="sig", alg="RS256")
    (HERE / "jwks.json").write_text(json.dumps({"keys": [public]}))
    now = int(time.time())
    claims = {"iss": issuer, "aud": audience, "sub": "agent-17",
              "client_id": "local-test", "scope": scope,
              "iat": now, "exp": now + 3600}
    print(jwt.encode(claims, key, algorithm="RS256", headers={"kid": "test"}))


if __name__ == "__main__":
    # make_test_token.py ISSUER AUDIENCE [SCOPE]
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "orders:read")
