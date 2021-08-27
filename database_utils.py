def pandas_alchemy_engine(
        database: str = '',
        driver: str = 'pyodbc',
        dialect: str = 'mssql',
        db_connection_string: dict = {
            'username': '',
            'password': '',
            'host': '',
            'port': '',
        }
):
    """
    pyodbc,pymssql,mysqlclient
    :param database:
    :param driver:
    :param dialect:
    :param dbcondict:
    :return:
    """
    if db_connection_string['port']:
        db_connection_string['port'] = ':' + db_connection_string['port']
    # dialect+driver://username:password@host:port/database
    temp_str1 = f"{dialect}+{driver}://{db_connection_string['username']}:{db_connection_string['password']}"
    db_connection_string = f"{temp_str1}@{db_connection_string['host']}{db_connection_string['port']}/{database}"

    if driver == 'pyodbc':
        engine = create_engine(f'{db_connection_string}?driver=ODBC Driver 17 for SQL Server')
    else:
        engine = create_engine(f'{db_connection_string}?charset=utf8')

    return engine
