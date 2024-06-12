# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-03
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import filecmp
from functools import wraps
import logging
import pytest


log = logging.getLogger(__name__)


def check_input_for_duplicates(func):
    """
    A decorator that checks a list of file paths for duplicates before processing them.

    This decorator takes a function as input and returns a wrapped function that performs the following steps:
        1. Checks if the input is a list and contains more than one element.
        2. Compares each pair of file paths in the list using the `os.stat` signatures (file type, size, and modification time).
        3. Removes any duplicates from the list.
        4. Calls the original function with the cleaned-up list of file paths.

    Parameters
    ----------
    func (function): The function to be decorated.

    Returns
    -------
    function: The wrapped function.

    Example
    -------
    >>> pytest.skip()
    >>> @check_input_for_duplicates
    >>> def process_files(file_list):
    >>>     # Process the files
    >>>     pass

    .. note::
        The wrapped function can still be parsed by Sphinx due to the :obj:`functools.wraps` decorator.

    """
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
