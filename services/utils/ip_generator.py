def generate_random_ip() -> str:
    from random import randint
    return '.'.join(
        str(randint(0, 255)) for _ in range(4)
    )


if __name__ == '__main__':
    pass
