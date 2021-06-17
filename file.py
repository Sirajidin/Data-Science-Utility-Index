def normalize_unit_name(unit):
    if unit in {'Byte','B'}:
        unit='B'
        pass
    elif unit  in {'Kilobyte','KB','K'}:
        unit='K'
    elif unit  in { 'Megabyte','MB','M'}:
        unit='M'
    elif unit in {'Gigabyte','GB','G'}:
        unit='G'
    elif unit  in { 'Terabyte','TB','T'}:
        unit='T'
    elif unit  in {'Petabyte','PB','P'}:
        unit='p'
    elif unit  in { 'Exabyte','EB'}:
        unit='EB'
    elif unit  in { 'Zettabyte','ZB'}:
        unit='ZB'
    elif unit  in { 'Yottabyte','YB'}:
        unit='YB'
    elif unit  in { 'Bit','b'}:
        unit='b'
    else:
        unit='B'
    return unit
  
  
  
  def file_size_converter(value,original_unit,target_unit):
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
    
    print(value)
    return value * factor
