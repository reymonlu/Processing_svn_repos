import re
import asyncio
import requests
from http import HTTPStatus
from functools import cache
from io import TextIOWrapper

from colors import BColors
from decorators import timer
from utils import writeInFile, readFile
from utils import extract_dirs_files_urls_to_dict

ORIGINS = ["https://steamboatlife.com", "http://fpcambridge.org"]
HEADERS = {
    "content-type": "text/html",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
}


@cache
async def get_data(url: str, filename: str) -> None:
    """Make request to url and copy request content into filename

    Args:
        url (str): resources url
        filename (str, optional): filename where to save request content.
            Defaults to "entries.txt".
    """
    status_code = None
    try:
        full_url = f"{url}/.svn/entries"
        res = requests.get(full_url, headers=HEADERS)
        print("__________________", res.ok)
        status_code = res.status_code
        if res.status_code == HTTPStatus.OK:
            content = res.content.decode("utf-8")
            asyncio.create_task(
                writeInFile(
                    extract_dirs_files_urls_to_dict(
                        content, origin=url,
                        full_url=full_url
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
        else:
            raise Exception("Bad response")
    except Exception:
        print(
            f"{BColors.FAIL}No entries file:\t[{full_url}]\tstatus_code:\
                \t[{status_code}]"
        )
    return None


async def process_domains(f: TextIOWrapper):
    url_prefix: str = "https://"
    for index, domain in enumerate(f, start=1):
        url = f"{url_prefix}{domain}"
        domain_name = re.search(r"\w+", domain).group()
        await asyncio.create_task(
            get_data(url.strip("\n"), f"{domain_name}_{index}"))
    # for origin, filename in zip(ORIGINS, ["steamboatlife", "fpcambridge"]):

    # print(f.readline())
    # print(f.readline())
    # print(f.readline())


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
