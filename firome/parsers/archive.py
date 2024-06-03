import tempfile
import zipfile
from os import path


class MultipleFilesException(Exception):

    def __str__(self):
        return "archive containing more than one file with given extension"


def unzip(src: str) -> str:
    """
    Unzip source archive returning path of extracted file

    :param src: source zip archive
    :param ext: extension of target file (to find if multiple files exist in the dir
    """

    tmp_dir = tempfile.mkdtemp(prefix="firome-")

    with zipfile.ZipFile(src) as archive:
        if len(archive.filelist) > 1:
            raise MultipleFilesException

        filename = archive.filelist[0].filename

        archive.extractall(path=tmp_dir)

    return path.abspath(path.join(tmp_dir, filename))
