from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey


def keygen() -> tuple[str, str]:
    """ Генерирует приватные и публичные ключи для интерфейсов и пиров. """

    private = X25519PrivateKey.generate()

    import base64
    return (
        base64.b64encode(
            private.private_bytes(
                serialization.Encoding.Raw,
                serialization.PrivateFormat.Raw,
                serialization.NoEncryption(),
            ),
        ).decode(),
        base64.b64encode(
            private.public_key().public_bytes(
                serialization.Encoding.Raw,
                serialization.PublicFormat.Raw,
            ),
        ).decode(),
    )


if __name__ == '__main__':
    pass
