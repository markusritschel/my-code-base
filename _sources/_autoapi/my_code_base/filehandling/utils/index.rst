:py:mod:`my_code_base.filehandling.utils`
=========================================

.. py:module:: my_code_base.filehandling.utils


Module Contents
---------------

.. py:function:: check_input_for_duplicates(func)

   A decorator that checks a list of file paths (the first and only argument of the wrapped function) for duplicates.
   For example, when you call a function with a list of many files as input, the decorator checks the input for
   duplicates before the read-in routine actually processes the files.
   The decorator makes use of the :func:`os.stat` signatures (file type, size, and modification time) to compare files
   pair-wise.

   Detected duplicates are dropped from the list such that the function can deal with the cleaned-up list.


