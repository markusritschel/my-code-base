# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-03
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import filecmp
from functools import wraps
import logging


log = logging.getLogger(__name__)


# TODO: write test
def check_input_for_duplicates(func):
    """A decorator that checks a list of file paths (the first and only argument of the wrapped function) for duplicates.
    For example, when you call a function with a list of many files as input, the decorator checks the input for
    duplicates before the read-in routine actually processes the files.
    The decorator makes use of the :func:`os.stat` signatures (file type, size, and modification time) to compare files
    pair-wise.

    Detected duplicates are dropped from the list such that the function can deal with the cleaned-up list.
    """
    # The functools.wraps decorator ensures that `func` can still be parsed by Sphinx. Usually, decorated functions can not be parsed by Sphinx.
    @wraps(func)
    def wrapper(file_list):
        if not isinstance(file_list, list) or len(file_list) <= 1:
            return func(file_list)
        remove_idx = []
        for i, f1 in enumerate(file_list):
            for f2 in file_list[i + 1:]:
                res = filecmp.cmp(f1,f2, shallow=True)  # Note: shallow=False would compare the actual file contents
                if res:
                    remove_idx.append(i)
        filtered_file_list = [i for j, i in enumerate(file_list) if j not in remove_idx]
        remove_files = [i for j, i in enumerate(file_list) if j in remove_idx]
        if remove_idx:
            log.info("Found and ignored %s duplicates in file list.", len(remove_idx))
            for entry in remove_files:
                log.debug("Ignored %s", entry)
        return func(filtered_file_list)

    return wrapper
