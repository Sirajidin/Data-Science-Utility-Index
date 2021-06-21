def file_size(path,numeric=True,unit='Byte',language='EN',verbose=False,decimal=2,is_archive=False,archive_format='zip'):
    """
    """
    import os
    if is_archive:
        if archive_format == 'zip':
            file_size = original_size_of_zip(path) 
        else:
            raise NotImplementedError
    else:
        file_size = os.path.getsize(path)
        #file_size = os.stat('temp/equity_price20210601/equity_price20210601.txt').st_size


        #file = open('temp/equity_price20210601/equity_price20210601.txt')
        #file.seek(0, os.SEEK_END)
        #file.tell()

        # from pathlib import Path
        # Path(r'temp/equity_price20210601/equity_price20210601.txt').stat()
        # file=Path(r'temp/equity_price20210601/equity_price20210601.txt').stat().st_size
    
    file_size = file_size_converter(value=file_size,original_unit='Byte',target_unit=unit)
    unit_abbrv,unit_en = normalize_unit_name(unit,language='EN')
    
    if file_size != 1 and language == 'EN':
        unit_en = unit_en + 's'
            
    if verbose:
        path = os.path.split(path)
        output = f'Relative dir: {path[0]}\n  |\n  +-- file: {path[1]}'
        output = f'{output}\n        |\n        +-- size: {file_size:.{decimal}f} {unit_en}'
        if numeric:
            print(output)
    else:
        output = unit_abbrv
        
    if numeric:
        output = round(file_size,decimal)
    else:
        output =(file_size,output)
        
    return output


def file_size_converter(value, original_unit, target_unit, decimal=None):
    import pandas as pd
    unit_table = pd.DataFrame(
                #     'B'           'K',              'M'               'G'                'T'              'P'                'EB'              'ZB'             'YB'              'b'
       data= [
                [ 1.         , 1 / pow(1024, 1), 1 / pow(1024, 2), 1 / pow(1024, 3), 1 / pow(1024, 4), 1 / pow(1024, 5), 1 / pow(1024, 6), 1 / pow(1024, 7), 1 / pow(1024, 8),         8.       ],#B

                [pow(1024, 1), 1.              , 1 / pow(1024, 1), 1 / pow(1024, 2), 1 / pow(1024, 3), 1 / pow(1024, 4), 1 / pow(1024, 5), 1 / pow(1024, 6), 1 / pow(1024, 7), pow(1024, 1) * 8.],#K

                [pow(1024, 2), pow(1024, 1)    , 1.              , 1 / pow(1024, 1), 1 / pow(1024, 2), 1 / pow(1024, 3), 1 / pow(1024, 4), 1 / pow(1024, 5), 1 / pow(1024, 6), pow(1024, 2) * 8 ],#M

                [pow(1024, 3), pow(1024, 2)    , pow(1024, 1)    ,  1.             , 1 / pow(1024, 1), 1 / pow(1024, 2), 1 / pow(1024, 3), 1 / pow(1024, 4), 1 / pow(1024, 5), pow(1024, 3) * 8 ],#G

                [pow(1024, 4), pow(1024, 3)    , pow(1024, 2)    , pow(1024, 1)    , 1.              , 1 / pow(1024, 1), 1 / pow(1024, 2), 1 / pow(1024, 3), 1 / pow(1024, 4), pow(1024, 4) * 8 ],#T

                [pow(1024, 5), pow(1024, 4)    , pow(1024, 3)    , pow(1024, 2)    , pow(1024, 1)    , 1.              , 1 / pow(1024, 1), 1 / pow(1024, 2), 1 / pow(1024, 3), pow(1024, 5) * 8 ],#P

                [pow(1024, 6), pow(1024, 5)    , pow(1024, 4)    , pow(1024, 3)    , pow(1024, 2)    , pow(1024, 1)    , 1.              , 1 / pow(1024, 1), 1 / pow(1024, 2), pow(1024, 6) * 8 ],#EB

                [pow(1024, 7), pow(1024, 6)    , pow(1024, 5)    , pow(1024, 4)    , pow(1024, 3)    , pow(1024, 2)    , pow(1024, 1)    , 1.              , 1 / pow(1024, 1), pow(1024, 7) * 8 ],#ZB

                [pow(1024, 8), pow(1024, 7)    , pow(1024, 6)    , pow(1024, 5)    , pow(1024, 4)    , pow(1024, 3)    , pow(1024, 2)    , pow(1024, 1)    , 1.              , pow(1024, 8) * 8 ],#YB


                [1 / 8       , 1 / 8 / pow(1024,1), 1 / 8 / pow(1024,2), 1 / 8 / pow(1024,3), 1 / 8 / pow(1024,4), 1 / 8 / pow(1024,5), 1 / 8 / pow(1024,6), 1 / 8 / pow(1024,7), 1 / 8 / pow(1024,8),  1. ]#b
             ],
        index=pd.Index(['B', 'K', 'M', 'G', 'T', 'P', 'EB', 'ZB', 'YB', 'b'], dtype='object', name='from'),
        columns=pd.Index(['B', 'K', 'M', 'G', 'T', 'P', 'EB', 'ZB', 'YB', 'b'], dtype='object', name='to')
    )

    original_unit = normalize_unit_name(original_unit)
    target_unit = normalize_unit_name(target_unit)
    
    factor = unit_table.loc[original_unit,target_unit]
    value = value * factor
    

    if target_unit in ('B','b'):
        decimal = 0
        
    if decimal:
        value = round(value,decimal)
    
    return value


def original_size_of_zip(zip_path):
    total_file_size = 0
    import zipfile
    with zipfile.ZipFile(zip_path, 'r') as zipobj:
        for item in zipobj.namelist():   
            if '.zip' in item:
                from io import BytesIO
                zfiledata = BytesIO(zipobj.read(item))
                total_file_size += original_size_of_zip(zfiledata)
            else:
                item_info = zipobj.getinfo(item)
                total_file_size += item_info.file_size
                
    return total_file_size


def normalize_unit_name(unit='b', language=None):
    
    unit_language = {
        'ZH':{
            'bit': '比特',
            'B': '字节',
            'k': '千字节',
            'M': '兆',
            'G': '千兆',
            'T': '太',
            'P': '拍',
            'EB': '艾',
            'ZB': '泽',
            'YB': '尧'
        },
        'EN':{
            'bit': 'bit',
            'B': 'Byte',
            'k': 'Kilobyte',
            'M': 'Megabyte',
            'G': 'Gigabyte',
            'T': 'Terabyte',
            'P': 'Petabyte',
            'EB': 'Exabyte',
            'ZB': 'Zettabyte',
            'YB': 'Yottabyte'
        }
    }
    
    unit_names = {
        'bit': ['bit', 'b'],
        'B': ['Byte', 'B'],
        'K': ['Kilobyte', 'KB', 'K'],
        'M': ['Megabyte', 'MB', 'M'],
        'G': ['Gigabyte', 'GB', 'G'],
        'T': ['Terabyte', 'TB', 'T'],
        'P': ['Petabyte', 'PB', 'P'],
        'EB': ['Exabyte', 'EB'],
        'ZB': ['Zettabyte', 'ZB'],
        'YB': ['Yottabyte', 'YB'],
    }
    
    unit_names_lower = {
        'bit': {'b', 'bit'},
         'B': {'b', 'byte'},
         'K': {'k', 'kb', 'kilobyte'},
         'M': {'m', 'mb', 'megabyte'},
         'G': {'g', 'gb', 'gigabyte'},
         'T': {'t', 'tb', 'terabyte'},
         'P': {'p', 'pb', 'petabyte'},
         'EB': {'eb', 'exabyte'},
         'ZB': {'zb', 'zettabyte'},
         'YB': {'yb', 'yottabyte'}
    }
    
    unit_lower = unit.lower()
    

    _unit = unit
    
    if unit_lower in unit_names_lower['B']  and unit!='b':
        unit_abbrv = 'B'
    elif unit_lower in unit_names_lower['K']:
        unit_abbrv = 'K'
    elif unit_lower in unit_names_lower['M']:
        unit_abbrv = 'M'
    elif unit_lower in unit_names_lower['G']:
        unit_abbrv = 'G'
    elif unit_lower in unit_names_lower['T']:
        unit_abbrv = 'T'
    elif unit_lower in unit_names_lower['P']:
        unit_abbrv = 'p'
    elif unit_lower in unit_names_lower['EB']:
        unit_abbrv = 'EB'
    elif unit_lower in unit_names_lower['ZB']:
        unit_abbrv = 'ZB'
    elif unit_lower in unit_names_lower['YB']:
        unit_abbrv = 'YB'
    elif unit_lower in unit_names_lower['bit']:
        unit_abbrv = 'bit'
    else:
        raise ValueError(unit,unit_names)
    
    if language:
        unit = unit_language[language][unit_abbrv]
        return unit_abbrv,unit
    
    return unit_abbrv
