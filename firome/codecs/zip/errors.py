class MultipleFilesError(Exception):
    """Zip archive contains more than one file"""


class EmptyArchiveError(Exception):
    """Zip archive contains no files"""
