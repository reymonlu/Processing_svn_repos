import asyncio
import requests
from functools import cache

from colors import BColors
from decorators import timer
from utils import writeInFile
from utils import extract_dirs_files_urls_to_dict

ORIGIN = "https://steamboatlife.com"


@timer
@cache
async def get_data(url: str, filename: str = "entries.txt") -> None:
    """Make request to url and copy request content into filename

    Args:
        url (str): resources url
        filename (str, optional): filename where to save request content.
            Defaults to "entries.txt".
    """
    res = requests.get(url)
    content = res.content.decode("utf-8")
    asyncio.create_task(
        writeInFile(
            extract_dirs_files_urls_to_dict(content, origin=ORIGIN),
            filename="dirs_files.json",
            is_json=True,
            newline=False,
        )
    )
    asyncio.create_task(
        writeInFile(
            content,
            filename=filename,
        )
    )
    return None


if __name__ == "__main__":
    _, time = asyncio.run(get_data(f"{ORIGIN}/.svn/entries"))
    COLOR = (
        BColors.OKGREEN
        if time < 1.5
        else (BColors.WARNING if time < 2.5 else BColors.FAIL)
    )

    print(
        f"{BColors.HEADER}The time it took: {BColors.ENDC}{COLOR}{time}s\
        {BColors.ENDC}"
    )
