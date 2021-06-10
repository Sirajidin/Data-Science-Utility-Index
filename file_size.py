def file_size(path,numeric=True,unit='Byte',language='EN',verbose=False):
    import os
    file_size = os.path.getsize(path)
    #file_size = os.stat('temp/equity_price20210601/equity_price20210601.txt').st_size
    
    
    #file = open('temp/equity_price20210601/equity_price20210601.txt')
    #file.seek(0, os.SEEK_END)
    #file.tell()
    
    # from pathlib import Path
    # Path(r'temp/equity_price20210601/equity_price20210601.txt').stat()
    # file=Path(r'temp/equity_price20210601/equity_price20210601.txt').stat().st_size
    
    if unit in {'Byte','B'}:
        _unit='B'
        pass
    elif unit  in {'Kilobyte','KB','K'}:
        _unit='K'
        file_size = file_size / 1024
    elif unit  in { 'Megabyte','MB','M'}:
        _unit='M'
        file_size = file_size / 1024**2
    elif unit in {'Gigabyte','GB','G'}:
        _unit='G'
        file_size = file_size / pow(1024,3)
    elif unit  in { 'Terabyte','TB','T'}:
        _unit='T'
        file_size = file_size / pow(1024,4)
    elif unit  in {'Petabyte','PB','P'}:
        _unit='p'
        file_size = file_size / pow(1024,5)
    elif unit  in { 'Exabyte','EB'}:
        _unit='EB'
        file_size = file_size / pow(1024,6)
    elif unit  in { 'Zettabyte','ZB'}:
        _unit='ZB'
        file_size = file_size / pow(1024,7)
    elif unit  in { 'Yottabyte','YB'}:
        _unit='YB'
        file_size = file_size / pow(1024,8)
    elif unit  in { 'Bit','b'}:
        _unit='b'
        file_size = file_size * 8
    
    if file_size != 1 and language == 'EN':
        unit = unit + 's'
    
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
    if language == 'ZH':
        unit = unit_map[language][_unit]

    if verbose:
        path = os.path.split(path)
        output = f'Relative dir: {path[0]}\n  |\n  +-- file: {path[1]}'
        output = f'{output}\n        |\n        +-- size: {file_size} {unit}'
        if numeric:
            print(output)
    else:
        output = unit
    if numeric:
        output = file_size
    else:
        output =(file_size,output)
        
    return output

file_size(path='temp/equity_price20210601/equity_price20210601.txt')
