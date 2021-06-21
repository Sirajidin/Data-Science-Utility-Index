def get_file_paths(dir_path,printout=False):
    import os
    filePaths = []
    for root, directories, files in os.walk(dir_path):
        for filename in files:
            #filePath = os.path.join(os.path.split(dir_path)[1], filename)
            filePath = os.path.join(root, filename)
            filePaths.append(filePath)
    if printout:
        print(filePaths)
    return filePaths


def write_out_pandas_data(Series_or_DataFrame, dir_path, file_name, zip_name = None, file_format='csv', index=False, **kwarg):
    import os
    
    if file_format.lower() == 'csv':
        if zip_name:
            path = os.path.join(dir_path,zip_name+'.zip')
            try:
                compression_opts = dict(method='zip',archive_name=f'{file_name}.csv')
                Series_or_DataFrame.to_csv(
                    path,
                    index=index,
                    compression=compression_opts,
                    **kwarg)
                
                return True
            except Exception as exc:
                print(exc)
                return False
        else:
            try:
                path = os.path.join(dir_path,file_name+'.csv')
                Series_or_DataFrame.to_csv(
                        path,
                        index=index,
                        **kwarg)
                return True
            
            except Exception as exc:
                print(exc)
                return False
            
            
def zip_files(source_dir, out_dir, zip_name, progress_bar=False, delete_source_dir=False):
    import zipfile
    import os
    from tqdm import tqdm
    zip_path = os.path.join(out_dir,f'{zip_name}.zip')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipobj:
        file_paths = get_file_paths(source_dir)
        for item in tqdm(file_paths,disable=not progress_bar):
            zipobj.write(item,arcname=item.replace(source_dir,''))
            
    if delete_source_dir:
        import shutil
        shutil.rmtree(source_dir)
