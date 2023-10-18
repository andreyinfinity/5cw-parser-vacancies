from configparser import ConfigParser

# Название БД для проекта
DB_NAME = "parser_vacancies"


def config_db(filename="database.ini", section="postgresql") -> dict:
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    if parser.has_section(section):
        params = parser.items(section)
        db = dict(params)
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
