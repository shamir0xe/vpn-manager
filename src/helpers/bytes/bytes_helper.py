class BytesHelper:
    @staticmethod
    def padding(b: bytes, padding: int) -> bytes:
        if padding < len(b):
            padding = len(b)
        return b + b' ' * (padding - len(b))
