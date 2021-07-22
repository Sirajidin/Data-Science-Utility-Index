from pandas import Timestamp
import fnmatch
import pprint
import os
import zipfile
import concurrent
import pathlib
import shutil
import logging
import io

logger = logging.getLogger(__name__)


def filter_datetime_string(datetime_string, start_time, end_time):
    start_time = Timestamp(start_time)
    end_time = Timestamp(end_time)
    try:
        time_stamp = Timestamp(datetime_string)
        if start_time <= time_stamp <= end_time:
            return True
        else:
            return False
    except:
        return False


def get_paths(dir_path, printout=False, filter_string='', recursive=True):
    file_paths = []
    if recursive:
        for root, directories, files in os.walk(dir_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                if filter_string:
                    if fnmatch.fnmatch(filename, filter_string):
                        file_paths.append(filepath)
                else:
                    file_paths.append(filepath)
    else:
        file_paths = os.listdir(dir_path)
        if filter_string:
            file_paths = [os.path.join(dir_path, item) for item in file_paths if fnmatch.fnmatch(item, filter_string)]
    if printout:
        pprint.pprint(file_paths)
    return file_paths


def write_out_pandas_data(series_or_dataframe, dir_path, file_name, zip_name=None, file_format='csv', index=False,
                          **kwarg):
    if file_format.lower() == 'csv':
        if zip_name:
            path = os.path.join(dir_path, zip_name + '.zip')
            try:
                compression_opts = dict(method='zip', archive_name=f'{file_name}.csv')
                series_or_dataframe.to_csv(
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
                path = os.path.join(dir_path, file_name + '.csv')
                series_or_dataframe.to_csv(
                    path,
                    index=index,
                    **kwarg)
                return True

            except Exception as exc:
                print(exc)
                return False


def zip_files(source_dir, out_dir, zip_name, delete_source_dir=False):
    zip_path = os.path.join(out_dir, f'{zip_name}.zip')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipobj:
        file_paths = get_paths(source_dir)
        for item in file_paths:
            zipobj.write(item, arcname=item.replace(source_dir, ''))

    if delete_source_dir:
        shutil.rmtree(source_dir)


def zip_archive_list(path, printout=False, filter_string=''):
    with zipfile.ZipFile(path) as zpobjct:
        archive_list = zpobjct.namelist()

    if filter_string:
        archive_list = [item for item in archive_list if fnmatch.fnmatch(item, filter_string)]

    if printout:
        print(list(enumerate(archive_list)))
    return archive_list


def return_csv_buffer_from_zip(zip_path, file_name, **kwargs):
    with zipfile.ZipFile(zip_path) as zip_object:
        return zip_object.open(file_name, mode='r', **kwargs)


def split_files_in_zip_by_n_lines(zip_path, out_dir, file_line_num=2000000, **kwargs):
    unzipped_buffer = return_files_in_zip(zip_path=zip_path, **kwargs)
    for item in unzipped_buffer:
        split_zipextfile_by_n_lines(zipextfile_name=item.name, zipextfile_object=item, out_dir=out_dir,
                                    file_line_num=file_line_num)


def return_files_in_zip(zip_path, **kwargs):
    with zipfile.ZipFile(zip_path) as zip_object:
        for name in zip_object.namelist():
            # name_ = name.encode('cp437').decode('gbk')
            if pathlib.Path(name).is_dir():
                continue
            yield io.TextIOWrapper(zip_object.open(name, mode='r', **kwargs), encoding='utf-8')


def split_zipextfile_by_n_lines(zipextfile_name, zipextfile_object, out_dir, out_file_prefix='', file_line_num=2000000,
                                first_line_as_header=True, header='', n_splits=0, delimiter=None):
    zipextfile_path = pathlib.Path(zipextfile_name)

    if first_line_as_header:
        if not header:
            header = next(zipextfile_object)
        else:
            raise Exception(f"first_line_as_header:{first_line_as_header},but header not equal to ''")
    else:
        if header:
            pass
        else:
            raise Exception(f"first_line_as_header:{first_line_as_header},but header is not given")

    split_num = 0
    for i, line in enumerate(zipextfile_object):
        if i % file_line_num == 0:
            split_num += 1
            if not out_file_prefix:
                out_file_prefix = zipextfile_path.stem

            out_file_path = pathlib.Path(out_dir).joinpath(zipextfile_path.parent.as_posix(),
                                                           f'{out_file_prefix}__{split_num}{zipextfile_path.suffix}')

            logger.info(f"split No.{split_num} ,start writing {file_line_num} lines to path:{out_file_path},")
            if split_num > n_splits > 0:
                return split_num

            with open(out_file_path, 'a') as f_out:
                f_out.write(header)

        with open(out_file_path, 'a') as f_out:
            f_out.write(line)


def split_file_by_n_lines(file_path, out_dir, out_file_prefix='', file_line_num=2000000, first_line_as_header=True,
                          header='',
                          delimiter=None):
    file_path = pathlib.Path(file_path)

    with open(file_path, 'r') as f:
        if first_line_as_header:
            if not header:
                header = next(f)
            else:
                raise Exception(f"first_line_as_header:{first_line_as_header},but header not equal to ''")
        else:
            if header:
                pass
            else:
                raise Exception(f"first_line_as_header:{first_line_as_header},but header is not given")

        split_num = 0
        for i, line in enumerate(f):
            if i % file_line_num == 0:
                split_num += 1
                if not out_file_prefix:
                    out_file_prefix = file_path.stem

                out_file_path = pathlib.Path(out_dir).joinpath(file_path.parent.as_posix(),
                                                               f'{out_file_prefix}__{split_num}{file_path.suffix}')

                logger.info(f"split No.{split_num} ,start writing {file_line_num} lines to path:{out_file_path},")

                with open(out_file_path, 'a') as f_out:
                    f_out.write(header)

            with open(out_file_path, 'a') as f_out:
                f_out.write(line)


def thread_write(pandas_sequence_dict, out_dir):
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        if not pathlib.Path(out_dir).exists():
            pathlib.Path(out_dir).mkdir(parents=True)

        for key in pandas_sequence_dict:
            file_name = key
            pd_data = pandas_sequence_dict[key]
            executor.submit(
                write_out_pandas_data,
                pd_data,
                out_dir,
                file_name,
                file_name,  # zip_name
                header=['ApplSeqNum']
            )


def prepare_out_dir(dir_path, safe: bool = True):
    logger.info(f"preparing output directory --> {dir_path}, safe：{safe}")

    if not pathlib.Path(dir_path).exists():
        pathlib.Path(dir_path).mkdir(parents=True)
        logger.info(f"newly created directory:{dir_path}")

    else:
        temp_log = f"directory:{dir_path} exists"
        logger.info(temp_log)

        if safe:
            raise FileExistsError(f"{temp_log},please use another directory name")
        else:
            import shutil

            shutil.rmtree(dir_path)
            logger.info(f"{dir_path} deleted")

            pathlib.Path(dir_path).mkdir(parents=True)
            logger.info(f"recreated the deleted directory:{dir_path}")
