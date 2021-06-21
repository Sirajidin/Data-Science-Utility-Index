def count_lines(path):
    with open(path,encoding='utf-8') as f:
        n=0
        for line in f:
            n+=1
    return n


def zip_count_lines(path, file_names, printout=False):
    import zipfile

    with zipfile.ZipFile(path) as zpobjct:
        file_names_dict = {}
        for item in file_names:
            with zpobjct.open(item) as f:
                n=0
                for line in f:
                    n+=1
            file_names_dict[item] = n
    if printout:
        print(file_names_dict)
    return file_names_dict


def zip_archive_list(path,printout=False):
    import zipfile
    with zipfile.ZipFile(path) as zpobjct:
        archive_list = zpobjct.namelist()
        
    if printout:
        print(list(enumerate(archive_list)))
    return archive_list

# if __name__ == '__main__':
#     zip_count_lines(path)
#     count_lines(path)
    
