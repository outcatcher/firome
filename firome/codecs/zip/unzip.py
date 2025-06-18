import tempfile
import zipfile
from pathlib import Path

from .errors import EmptyArchiveError, MultipleFilesError


def unzip(src: Path) -> Path:
    """Unzip source archive returning path of extracted file."""
    tmp_dir = tempfile.mkdtemp(prefix="firome-")

    with zipfile.ZipFile(src) as archive:
        if len(archive.filelist) == 0:
            raise EmptyArchiveError(src)

        if len(archive.filelist) > 1:
            raise MultipleFilesError(src)

        filename = archive.filelist[0].filename

        archive.extractall(path=tmp_dir)

    return Path(tmp_dir, filename).resolve()
