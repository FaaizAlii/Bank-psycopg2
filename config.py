from configparser import ConfigParser


def config(filename='database.ini', section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    data = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            data[param[0]] = param[1]
    else:
        raise Exception("Error Connecting to Db")
    return data


