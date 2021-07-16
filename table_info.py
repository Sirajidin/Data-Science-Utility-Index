def table_meta(
    database = 'db',
    table_name = '',
    driver='pyodbc',
    dialect='mssql',
    dbcondict={
        'username':'',
        'password':'',
        'host':'',
        'port':'',   
    }
):
    from sqlalchemy import create_engine
    if dbcondict['port']:
        dbcondict['port'] = ':' + dbcondict['port']
    
    #dialect+driver://username:password@host:port/database
    dbconstr = f"{dialect}+{driver}://{dbcondict['username']}:{dbcondict['password']}@{dbcondict['host']}{dbcondict['port']}/{database}"
        
    if driver == 'pyodbc':
        engine = create_engine(f'{dbconstr}?driver=ODBC Driver 17 for SQL Server')
    elif driver=='pymssql':
        engine = create_engine(f'{dbconstr}?charset=utf8')
        
    import pandas as pd
    
    df = pd.read_sql(f'''
        select tbl_clmns.TABLE_NAME,
               al_clmns.column_id,
               tbl_clmns.ORDINAL_POSITION,
               CASE
                   WHEN tbl_cnstrnts.CONSTRAINT_TYPE = '' or tbl_cnstrnts.CONSTRAINT_TYPE is null THEN '--'
                   ELSE tbl_cnstrnts.CONSTRAINT_TYPE
                   END       CONSTRAINT_TYPE,


               al_clmns.name COLUMN_NAME,
               CAST(CASE
                   WHEN extndd_prprts.value = '' or extndd_prprts.value is null THEN '--'
                   ELSE extndd_prprts.value
                   END   as NVARCHAR(4000))    MS_Description,-- isnull(extndd_prprts.value, '--')  MS_Description,
               tbl_clmns.DATA_TYPE,
               tbl_clmns.IS_NULLABLE,-- al_clmns.is_nullable,
               al_clmns.max_length,-- tbl_clmns.CHARACTER_MAXIMUM_LENGTH
               al_clmns.precision,
               al_clmns.scale,
               al_clmns.is_computed

        --        al_clmns.is_identity,
        --        al_clmns.system_type_id,
        --        al_clmns.user_type_id,
        --        al_clmns.is_computed,
        --        al_clmns.is_replicated

        from {database}.sys.all_columns as al_clmns
                 left join {database}.sys.extended_properties as extndd_prprts
                           on extndd_prprts.major_id = al_clmns.object_id
                               and al_clmns.column_id = extndd_prprts.minor_id

                 left join (select tbl_cnstrnts.CONSTRAINT_NAME,
                                   tbl_cnstrnts.CONSTRAINT_TYPE,
                                   ky_clmn_usg.COLUMN_NAME,
                                   ky_clmn_usg.TABLE_NAME
                            from {database}.INFORMATION_SCHEMA.TABLE_CONSTRAINTS as tbl_cnstrnts
                                     join {database}.INFORMATION_SCHEMA.KEY_COLUMN_USAGE as ky_clmn_usg
                                          on tbl_cnstrnts.TABLE_NAME = ky_clmn_usg.TABLE_NAME
                                              AND tbl_cnstrnts.CONSTRAINT_CATALOG = ky_clmn_usg.CONSTRAINT_CATALOG
                                              AND tbl_cnstrnts.CONSTRAINT_SCHEMA = ky_clmn_usg.CONSTRAINT_SCHEMA
                                              AND tbl_cnstrnts.CONSTRAINT_NAME = ky_clmn_usg.CONSTRAINT_NAME
                            where tbl_cnstrnts.TABLE_NAME = '{table_name}') as tbl_cnstrnts
                           on tbl_cnstrnts.COLUMN_NAME = al_clmns.name
                 join (select clmns.TABLE_NAME,
                              clmns.COLUMN_NAME,
                              clmns.ORDINAL_POSITION,
                              clmns.IS_NULLABLE,
                              clmns.DATA_TYPE,
                              clmns.CHARACTER_MAXIMUM_LENGTH,
                              clmns.CHARACTER_SET_NAME


                       from {database}.INFORMATION_SCHEMA.COLUMNS as clmns
                       where clmns.TABLE_NAME = '{table_name}'
        -- and clmns.COLUMN_NAME=''
        ) as tbl_clmns
                      on tbl_clmns.COLUMN_NAME = al_clmns.name

        where al_clmns.object_id = (select OBJECT_ID('{database}..{table_name}') objct_id)


        ''',con=engine)
    
    if driver=='pymssql':
        df.loc[:,'MS_Description'] = df.apply(lambda x:x['MS_Description'].decode(), axis=1)
    return df
