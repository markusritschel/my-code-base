:py:mod:`my_code_base.filehandling.utils`
=========================================

.. py:module:: my_code_base.filehandling.utils


Module Contents
---------------

.. py:function:: check_input_for_duplicates(func)

   A decorator that checks a list of file paths for duplicates before processing them.

   This decorator takes a function as input and returns a wrapped function that performs the following steps:
       1. Checks if the input is a list and contains more than one element.
       2. Compares each pair of file paths in the list using the `os.stat` signatures (file type, size, and modification time).
       3. Removes any duplicates from the list.
       4. Calls the original function with the cleaned-up list of file paths.

   :param func (function):
   :type func (function): The function to be decorated.

   :returns: **function**
   :rtype: The wrapped function.

   .. rubric:: Example

   >>> pytest.skip()
   >>> @check_input_for_duplicates
   >>> def process_files(file_list):
   >>>     # Process the files
   >>>     pass

   .. note::
       The wrapped function can still be parsed by Sphinx due to the :obj:`functools.wraps` decorator.


