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





def file_size(path,numeric=True,unit='Byte',language='EN',verbose=False,decimal=2,is_archive=False,archive_format='zip'):
    import os
    if is_archive:
        if archive_format == 'zip':
            file_size = original_size_of_zip(path) 
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
    _unit = normalize_unit_name(unit)
    
    
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
        
    if _unit in ('B','b'):
        decimal = 0
            
    if verbose:
        path = os.path.split(path)
        output = f'Relative dir: {path[0]}\n  |\n  +-- file: {path[1]}'
        print(decimal)
        output = f'{output}\n        |\n        +-- size: {file_size:.{decimal}f} {unit}'
        if numeric:
            print(output)
    else:
        output = unit
    if numeric:
        
        output = round(file_size,decimal)
    else:
        output =(file_size,output)
        
    return output


if __name__ == '__main__':
    file_size(path='D:\datayes\work\data.zip',numeric=True,unit='M',language='EN',verbose=True,decimal=2,is_archive=True)
    
    
 



def get_file_paths(dir_path):
    import os
    filePaths = []
    for root, directories, files in os.walk(dir_path):
        for filename in files:
            #filePath = os.path.join(os.path.split(dir_path)[1], filename)
            filePath = os.path.join(root, filename)
            filePaths.append(filePath)
    return filePaths




import zipfile
with zipfile.ZipFile(f'{dir_path}.zip', 'w', zipfile.ZIP_DEFLATED) as zipobj:
    file_paths = get_file_paths(dir_path)
    for item in file_paths:
        zipobj.write(item,arcname=os.path.split(item)[1])
        

        
import concurrent.futures

def wirte_out(Series,file_name,dir_path):
    path = os.path.join(dir_path,file_name+'.zip')
    try:
        compression_opts = dict(method='zip',archive_name=f'{file_name}.csv')
        Series.to_csv(path,index=False,compression=compression_opts)
        #Series.to_csv(f"ttt{path}.csv",index=False)
        return True
    except Exception as exc:
        print(exc)
        return False
    
    
    
time_start = time.time()
dir_path = 'D:\datayes\work\data'

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    future_to_Channel ={}
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    for Channel in all_Channel:
        future_to_Channel[executor.submit(
            wirte_out,
            all_Channel[Channel],
            Channel,
            dir_path)] = Channel
        
    for future in concurrent.futures.as_completed(future_to_Channel):
        Channel = future_to_Channel[future]
        try:
            data = future.result()
        except Exception as exc:
            print(f'{Channel} generated an exception: {exc}') 
        else:
            print(f'{Channel} returned {data}')
            
print(f'{time.time() - time_start:.2f} seconds time to process')





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






from io import BytesIO
def original_size_of_zip(zip_path,zip_path_str='D:\datayes\work\data.zip',is_full_path=False,depth=1):
    out_strings = []
    out_strings.append(os.path.normpath(zip_path_str))
    total_file_size = 0
                    
    import zipfile
    with zipfile.ZipFile(zip_path, 'r') as zipobj:
        for item in zipobj.namelist():   
            if '.zip' in item:
                zfiledata = BytesIO(zipobj.read(item))
                leding_space = ' ' * depth * 4
                file_path_str = f'{leding_space}{zip_path_str}/{item}/'
                total_file_size += original_size_of_zip(zfiledata,zip_path_str=file_path_str,depth=depth+1)
            else:
                
                item_info = zipobj.getinfo(item)
                total_file_size += item_info.file_size
                leding_space = ' ' * (depth - 1) * 4
                file_path_str = f'{leding_space}{zip_path_str}{item}'
                
                file_path_str = os.path.normpath(file_path_str)
                out_str = f'{file_path_str}  -->  {item_info.file_size}'
                out_strings.append(out_str)
                
    print('\n'.join(out_strings))
    return total_file_size,
