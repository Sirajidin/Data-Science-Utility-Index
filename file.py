def normalize_unit_name(unit, language='EN'):
    unit_lower = unit.lower()
    unit_map = {
        'ZH':{
            'b':'比特',
            'B':'字节',
            'k':'千字节',
            'M':'兆',
            'G':'千兆',
            'T':'太',
            'P':'拍',
            'EB':'艾',
            'ZB':'泽',
            'YB':'尧'
        }
    }

    
    if unit_lower in {'Byte'.lower(),'B'.lower()}:
        return 'B'
    elif unit_lower  in {'Kilobyte'.lower(), 'KB'.lower(), 'K'.lower()}:
        return 'K'
    elif unit_lower  in {'Megabyte'.lower(), 'MB'.lower(), 'M'.lower()}:
        return 'M'
    elif unit_lower in {'Gigabyte'.lower(), 'GB'.lower(), 'G'.lower()}:
        return 'G'
    elif unit_lower  in {'Terabyte'.lower(), 'TB'.lower(), 'T'.lower()}:
        return 'T'
    elif unit_lower  in {'Petabyte'.lower(), 'PB'.lower(), 'P'.lower()}:
        return 'p'
    elif unit_lower  in {'Exabyte'.lower(), 'EB'.lower()}:
        return 'EB'
    elif unit_lower  in {'Zettabyte'.lower(), 'ZB'.lower()}:
        return 'ZB'
    elif unit_lower  in {'Yottabyte'.lower(), 'YB'.lower()}:
        return 'YB'
    elif unit  in {'Bit','b','bit'}:
        return 'b'
    else:
        raise ValueError(unit)
    
    if language == 'ZH':
        unit = unit_map[language][_unit]
  
  
  
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
