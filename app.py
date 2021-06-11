import re
import asyncio
import requests
from http import HTTPStatus
from functools import cache
from io import TextIOWrapper

from colors import BColors
from decorators import timer
from utils import (
    url_is_valid,
    writeInFile,
    readFile,
    extract_dirs_files_urls_to_dict,
)
from utils import HEADERS

ORIGINS = ["https://steamboatlife.com", "http://fpcambridge.org"]


@cache
async def get_data(index: int, domain: str) -> None:
    """Make request to domain and copy request content into filename

    Args:
        domain (str): resources domain
        filename (str, optional): filename where to save request content.
            Defaults to "entries.txt".
    """
    status_code = 404
    protocol: str = "https://"
    domain = domain.strip("\n")
    origin = f"{protocol}{domain}"
    filename = re.search(r"\w+", domain).group()
    filename += f"_{index}"
    full_url = f"{protocol}{domain}/.svn/entries"
    if url_is_valid(full_url):
        try:
            res = requests.get(
                full_url, headers=HEADERS, allow_redirects=False
            )
            status_code = res.status_code

            if res.status_code == HTTPStatus.OK:
                content = res.content.decode("utf-8")
                asyncio.create_task(
                    writeInFile(
                        extract_dirs_files_urls_to_dict(
                            content, origin=origin, full_url=full_url
                        ),
                        filename=f"data_{filename}.json",
                        is_json=True,
                        newline=False,
                    )
                )
                asyncio.create_task(
                    writeInFile(
                        content,
                        filename=f"entries_{filename}.txt",
                    )
                )
            return
        except Exception:
            pass
    print(
        f"{BColors.FAIL}No entries file:\t[{full_url}]\tstatus_code:\
                    \t[{status_code}]"
    )
    return


def f(i, d):
    print(i, d)


async def process_domains(f: TextIOWrapper):
    for index, domain in enumerate(f, start=1):
        await asyncio.create_task(get_data(index, domain))


@timer
async def run() -> None:
    await readFile("domains.txt", process_domains)
    return None


if __name__ == "__main__":
    times_total = 0
    _, time = asyncio.run(run())
    COLOR = (
        BColors.OKGREEN
        if time < 1.5
        else (BColors.WARNING if time < 2.5 else BColors.FAIL)
    )

    print(
        f"{BColors.HEADER}The time it took: {BColors.ENDC}{COLOR}{time}s\
        {BColors.ENDC}"
    )
