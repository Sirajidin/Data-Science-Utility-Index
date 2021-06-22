nrows = 3
import zipfile
with zipfile.ZipFile('Z:\\L2_data\\MDL\\20210621\\20210621_mdl_6_33_0.csv.zip') as zpobjct:
    with zpobjct.open('mdl_6_33_0.csv','r') as f:
        header = next(f).decode().strip().split(',')
        rows = []
        for i in range(nrows):
            row = next(f).decode().strip().split(',')
            row = dict(zip(header,row))
            rows.append(row)
pd.DataFrame(rows)

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
        unit = unit_language[language][_unit]
        return unit_abbrv,unit
    
    return unit_abbrv
  
  
  
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




def count_lines(path):
    with open(path,encoding='utf-8') as f:
        n=0
        for line in f:
            n+=1
    return n


def zip_count_lines(path,file_name):
    import zipfile
    with zipfile.ZipFile(path) as z:
        with z.open(file_name) as f:
            n=0
            for line in f:
                n+=1
    return n

# if __name__ == '__main__':
#     zip_count_lines(path)
#     count_lines(path)
    

    
def zip_files(dir_path):
    import zipfile
    with zipfile.ZipFile(f'{dir_path}.zip', 'w', zipfile.ZIP_DEFLATED) as zipobj:
        file_paths = get_file_paths(dir_path)
        for item in tqdm(file_paths):
            zipobj.write(item,arcname=item.replace(dir_path,''))
