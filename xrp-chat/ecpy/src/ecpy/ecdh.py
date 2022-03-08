from hashlib         import sha256
from ecpy.curves     import Curve, Point


def point_to_bytes(P: Point) -> bytes:
    curve = P.curve
    return bytes(curve.encode_point(P, compressed=True))

def bytes_to_point(curve, b: bytes) -> Point:
    return curve.decode_point(b)

def ecdh(curve: Curve, sk: bytes, pk: bytes):
    d = int.from_bytes(sk, 'big')
    P = bytes_to_point(curve, pk)
    pre_hash_shared_secret = point_to_bytes(d * P)
    return sha256(pre_hash_shared_secret).digest()