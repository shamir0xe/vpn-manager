import random


class TokenGenerator:
    @staticmethod
    def generate(length: int) -> str:
        alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
        token = ''
        while len(token) < length:
            token += alphabet[random.randint(0, len(alphabet) - 1)]
        return token
