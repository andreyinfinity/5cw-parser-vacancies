from configparser import ConfigParser

# Конфигурация БД для проекта
DB_NAME = "parser_vacancies"
db_ini = "database.ini"
db_section = "postgresql"


def config_db(filename=db_ini, section=db_section) -> dict:
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    if parser.has_section(section):
        params = parser.items(section)
        db = dict(params)
        db.update({'dbname': DB_NAME})
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
