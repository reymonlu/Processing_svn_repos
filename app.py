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
from settings import (
    HEADERS,
    TIMEOUT,
    PROTOCOL,
    LIST_DOMAIN_FILE,
    LIST_BAD_DOMAINS,
    LIST_GOOD_DOMAINS
)


@cache
async def get_data(index: int, domain: str) -> None:
    """Make request to domain and copy request content into filename

    Args:
        domain (str): resources domain
        filename (str, optional): filename where to save request content.
            Defaults to "entries.txt".
    """
    status: int = 404
    origin: str = PROTOCOL + "://" + domain.strip("\n")
    filename: str = re.search(r"\w+", domain).group()
    filename += f"_{index}"
    full_url: str = f"{origin}/.svn/entries"

    print(
        f"{BColors.BOLD}{BColors.HEADER}Processing:\t[{full_url}]{BColors.ENDC}"
    )
    if url_is_valid(full_url):
        try:
            res = requests.get(full_url, headers=HEADERS, timeout=TIMEOUT)
            status = res.status_code

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
                        domain=full_url,
                    )
                )
                asyncio.create_task(
                    writeInFile(
                        content,
                        filename=f"entries_{filename}.txt",
                    )
                )
                asyncio.create_task(writeInFile(
                    full_url, filename=LIST_GOOD_DOMAINS, mode="a"
                ))
                return
        except Exception:
            pass

    asyncio.create_task(writeInFile(full_url, filename=LIST_BAD_DOMAINS, mode="a"))
    print(
        f"{BColors.FAIL}\t\tNo entries file or .svn folder\t\t\t[{status}]{BColors.ENDC}"
    )
    return


async def process_domains(f: TextIOWrapper):
    for index, domain in enumerate(f, start=1):
        if domain.strip() != "":
            await asyncio.create_task(get_data(index, domain))


@timer
async def run() -> None:
    await readFile(LIST_DOMAIN_FILE, process_domains)
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
