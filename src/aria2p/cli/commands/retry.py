"""Command to retry failed downloads."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aria2p.client import ClientException

if TYPE_CHECKING:
    from aria2p.api import API


def retry(api: API, gids: list[str] | None = None, do_all: bool = False) -> int:  # noqa: FBT001,FBT002
    """Retry subcommand.

    Parameters:
        api: The API instance to use.
        gids: The GIDs of the downloads to retry.
        do_all: Retry all failed downloads if True.

    Returns:
        int: 0 if all success, 1 if one failure.
    """
    try:
        downloads = api.get_downloads(None if do_all else gids)
    except ClientException as error:
        print(str(error), file=sys.stderr)
        return 1

    failed_downloads = [d for d in downloads if d.has_failed]
    result = api.retry_downloads(failed_downloads)

    if all(not isinstance(item, ClientException) for item in result):
        return 0

    for item in result:
        if isinstance(item, ClientException):
            print(item, file=sys.stderr)

    return 1
