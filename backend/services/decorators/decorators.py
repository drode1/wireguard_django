def print_import_file_info(func):
    """ Декоратор используется для принта статуса при импорте данных. """

    def wrapper(*args, **kwargs):
        print('Начался импорт данных')
        func(*args, **kwargs)
        print('Импорт данных - завершен.')
        return func

    return wrapper
