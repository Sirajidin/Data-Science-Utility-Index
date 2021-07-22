import logging
from .file_utils import return_csv_buffer_from_zip
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def get_sequence_dict(path, key_column, sequence_column, pwd='', file_name=''):
    logger.info(
        f"Start getting sequence dict from path:{path}, key_column:{key_column},sequence_column:{sequence_column} ")
    if path.suffix == '.zip':
        if pwd:
            csv_buffer = return_csv_buffer_from_zip(zip_path=path, file_name=file_name, pwd=pwd)
            csv_df = pd.read_csv(csv_buffer, usecols=[key_column, sequence_column], dtype={key_column: 'category'},
                                 index_col=False)
        else:
            csv_df = pd.read_csv(path, usecols=[key_column, sequence_column], dtype={key_column: 'category'},
                                 index_col=False)
    else:
        csv_df = pd.read_csv(path, usecols=[key_column, sequence_column], dtype={key_column: 'category'},
                             index_col=False)

    _categories = set(csv_df[key_column].cat.categories)
    sequence_dict = {item: csv_df[csv_df[key_column] == item][sequence_column].values for item in _categories}
    del csv_df
    logger.info(f"Finished getting sequence dict from path:{path}")

    return sequence_dict


def get_sequence_dict_iter(path, key_column, sequence_column, line_chunks=2000000):
    logger.info(
        f"Start getting sequence dict iteratively from path:{path}, key_column:{key_column},sequence_column:{sequence_column},line_chunks: {line_chunks} ")
    if path.suffix == '.zip':
        iter_csv_df = pd.read_csv(
            filepath_or_buffer=path,
            iterator=True,
            usecols=[key_column, sequence_column],
            dtype={key_column: 'category'},
            chunksize=line_chunks,
            index_col=False,
            compression="zip"
        )
    elif path.suffix == '.csv':
        iter_csv_df = pd.read_csv(
            filepath_or_buffer=path,
            iterator=True,
            usecols=[key_column, sequence_column],
            dtype={key_column: 'category'},
            chunksize=line_chunks,
            index_col=False,
        )

    sequence_dict = {}

    for i, df in enumerate(iter_csv_df):
        logger.info(f"Iteration {i + 1} ")
        _categories = set(df[key_column].cat.categories)
        if i == 0:
            sequence_dict = {item: df[df[key_column] == item][sequence_column].values for item in _categories}
        else:
            for item in _categories:
                sequence_dict[item] = np.concatenate(
                    (sequence_dict.get(item, np.empty(0)), df[df[key_column] == item][sequence_column].values), axis=0)

    del df, iter_csv_df

    logger.info(f"Finished getting sequence dict iteratively from path:{path}")

    return sequence_dict


def missing_sequence(sequence: np.ndarray, min_sequence=1, max_sequence=None) -> pd.Series:
    if max_sequence is None:
        max_sequence = sequence.max()

    logger.info(f"Getting missing_sequence in {len(sequence)} numbers")
    right_sequence = range(min_sequence, max_sequence + 1)
    original_sequence = set(sequence)
    missing_sequences = pd.Series([x for x in right_sequence if x not in original_sequence], dtype='float64')

    logger.info(f"Got missing_sequence {len(missing_sequences)} ")

    return missing_sequences


def check_if_unique_sequence(sequence):
    logger.info(f"Check_if_unique_sequence  in {len(sequence)} numbers")

    from collections import Counter
    most_common = Counter(sequence).most_common(1)
    del sequence
    most_common = most_common[0][1]

    if most_common == 1:
        logger.info(f"sequence is unique")
        return True
    else:
        logger.error(f"sequence is not unique")
        return False


def sequence_dict_from_two_files(
        first_file_info={
            'path': '',
            'key_column': '',
            'sequence_column': ''
        },
        second_file_info={
            'path': '',
            'key_column': '',
            'sequence_column': ''
        }
):
    logger.info(
        f"Start getting sequence dict iteratively from two_files: {first_file_info['path']} and {second_file_info['path']} ")

    first_sequnece_dict = get_sequence_dict_iter(
        path=first_file_info['path'],
        key_column=first_file_info['key_column'],
        sequence_column=first_file_info['sequence_column'],
        line_chunks=2000000)

    second_sequence_dict = get_sequence_dict_iter(
        path=second_file_info['path'],
        key_column=second_file_info['key_column'],
        sequence_column=second_file_info['sequence_column'],
        line_chunks=2000000)

    assert set(first_sequnece_dict.keys()) == set(second_sequence_dict.keys()), 'key_columns are not the same'

    logger.info(f"merging first_sequence_dict and second_sequence_dict sequences on the same key ")
    for key in first_sequnece_dict:
        first_sequnece_dict[key] = np.concatenate([first_sequnece_dict[key], second_sequence_dict[key]])
        del second_sequence_dict[key]
    del second_sequence_dict
    logger.info(f"merged")

    logger.info(f"check_if_unique_sequence ")
    for key in first_sequnece_dict:
        logger.info(f"check_if_unique_sequence for {key}")
        assert check_if_unique_sequence(first_sequnece_dict[key]), f'{key} not unique sequence'
    logger.info("all sequence are unique")

    logger.info(
        f"Finished getting sequence dict iteratively from two_files: {first_file_info['path']} and {second_file_info['path']} ")
    return first_sequnece_dict
