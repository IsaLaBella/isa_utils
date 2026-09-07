import os
import shutil
import fnmatch

from typing import Iterable, Any, TypeAlias

# ---------------------------------------------------------------------------- #
#                               Helper Functions                               #
# ---------------------------------------------------------------------------- #

def is_str_or_bytes_or_pathlike(x: Any) -> bool:

    # x is pathlike if it has the attribute __fspath__.
    return isinstance(x, (str, bytes)) or hasattr(x, "__fspath__")

# ---------------------------------------------------------------------------- #
#                      Functions for Searching Directories                     #
# ---------------------------------------------------------------------------- #

def search_for_matching_subdirs_in_directory(directory: os.FileDescriptorOrPath, match_pattern: str | bytes | os.PathLike | Iterable[str | bytes | os.PathLike], search_in_matching_subdirs: bool = False) -> list[str | bytes | os.PathLike]:
    """
    Recursively collects all subdirectories in the specified directory whose names match the given unix shell-style search pattern.

    Args:
        directory (str): The path to the directory to search.
        match_pattern (str | bytes | Iterable[str | bytes]): The unix shell-style search pattern(s) to match subdirectory names against. Can be a single pattern or list of patterns.
        search_in_matching_subdirs (bool): Whether to search for subdirectories matching the search pattern inside directories which themselves already match the search pattern. Useful when collecting a list of directories to delete.

    Returns:
        list[str]: A list of subdirectory paths that match the given pattern.
    """
    
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory {directory} does not exist.")

    if is_str_or_bytes_or_pathlike(match_pattern):
        # fnmatch.fnmatch() accepts str, bytes or os.Pathlike as arguments.
        match_pattern = [match_pattern]

    if not isinstance(match_pattern, Iterable):
        # Type checking is performed here, otherwise type errors may result in confusing error messages
        # (e.g. match_pattern=1 results in "'int' object is not iterable," which may lead users to think that the argument must be a list or tuple).
        raise TypeError(f"match_pattern must be str, bytes, os.PathLike object or iterable, not {type(match_pattern).__name__}.")

    matched_subdirs = []
    
    for root, dirs, _ in os.walk(directory, topdown=True):
        new_matched_subdirs = []

        for dirname in dirs:
            for pattern in match_pattern:
                if fnmatch.fnmatch(dirname, pattern):
                    new_matched_subdirs.append(dirname)

        if not search_in_matching_subdirs:
            # Remove matching subdirectories so that their contents are not also searched for matches.
            for subdir in new_matched_subdirs:
                dirs.remove(subdir)

        for subdir in new_matched_subdirs:
            matched_subdirs.append(os.path.join(root, subdir))

    return matched_subdirs

def search_for_matching_files_in_directory(directory: os.FileDescriptorOrPath, match_pattern:  str | bytes | os.PathLike | Iterable[str | bytes | os.PathLike]) -> list[str | bytes | os.PathLike]:
    """
    Collects all files in the specified directory (including those in subdirectories) whose names match the given unix shell-style search pattern.

    Args:
        directory (str): The path to the directory to search.
        match_pattern (str | Iterable[str]): The unix shell-style search pattern(s) to match directory names against. Can be a single pattern or list of patterns.

    Returns:
        list[str]: A list of file paths that match the given pattern.
    """
    
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory {directory} does not exist.")

    if is_str_or_bytes_or_pathlike(match_pattern):
        # fnmatch.fnmatch() accepts str, bytes or os.Pathlike as arguments.
        match_pattern = [match_pattern]

    if not isinstance(match_pattern, Iterable):
        # Type checking is performed here, otherwise type errors may result in confusing error messages
        # (e.g. match_pattern=1 results in "'int' object is not iterable," which may lead users to think that the argument must be a list or tuple).
        raise TypeError(f"match_pattern must be str, bytes, os.PathLike object or iterable, not {type(match_pattern).__name__}.")
    
    matched_files = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            for pattern in match_pattern:
                if fnmatch.fnmatch(file_name, pattern):
                    matched_files.append(os.path.join(root, file_name))
                    break

    return matched_files

# ---------------------------------------------------------------------------- #
#                   Functions for Removing Files and Folders                   #
# ---------------------------------------------------------------------------- #

def remove_files_and_directories(paths: str | bytes | os.PathLike | Iterable[str | bytes | os.PathLike], delete_non_empty_dirs = False) -> None:
    
    if is_str_or_bytes_or_pathlike(paths):
        # fnmatch.fnmatch() accepts str, bytes or os.Pathlike as arguments.
        paths = [paths]

    for path in paths:

        if os.path.isfile(path):
            os.remove(path)
        else:
            if delete_non_empty_dirs:
                shutil.rmtree(path)
            else:
                os.rmdir(path)

def clean_directory(directory: os.FileDescriptorOrPath, match_pattern: str | bytes | os.PathLike | Iterable[str | bytes | os.PathLike]) -> None:

    dirs_to_remove = search_for_matching_subdirs_in_directory(directory, match_pattern)
    remove_files_and_directories(dirs_to_remove, delete_non_empty_dirs=True)

    files_to_remove = search_for_matching_files_in_directory(directory, match_pattern)
    remove_files_and_directories(files_to_remove)

# ---------------------------------------------------------------------------- #
#                                 Main Program                                 #
# ---------------------------------------------------------------------------- #

if __name__ == "__main__":

    removeList = [
        "__pycache__",
        ".pytest_cache",
        "*.log",
        "*.pyc"
    ]

    clean_directory(".", removeList)