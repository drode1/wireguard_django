def print_import_file_info(func):
    """ Декоратор используется для принта статуса при импорте данных. """

    def wrapper(*args, **kwargs):
        print(f'Начался импорт данных')
        func(*args, **kwargs)
        print(f'Импорт данных - завершен.')
        return func

    return wrapper
