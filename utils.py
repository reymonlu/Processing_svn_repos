import re
import json
import requests
from functools import cache
from http import HTTPStatus
from io import TextIOWrapper
from typing import Optional, Callable

from colors import BColors
from settings import HEADERS


@cache
def display_timer(time: float) -> None:
    """Format print time

    Args:
        time (float): time to print
    """
    COLOR = (
        BColors.OKGREEN
        if time < 1.5
        else (BColors.WARNING if time < 2.5 else BColors.FAIL)
    )

    print(
        f"{BColors.HEADER}The time it took: {BColors.ENDC}{COLOR}{time}s\
        {BColors.ENDC}"
    )
    return


@cache
def url_is_valid(url: str) -> bool:
    """Check url is valid by making head request and checking status code

    Args:
        url (str): url to check

    Returns:
        bool: is valid
    """
    try:
        res = requests.head(url, headers=HEADERS, timeout=5)
        return HTTPStatus.OK <= res.status_code <= HTTPStatus.NOT_MODIFIED
    except Exception:
        return False


async def writeInFile(content: str, **kwargs: dict) -> Optional[bool]:
    """Write text/dict into specified filename

    Args:
        content (str): content to write in file, can be a dictionary or text
        kwargs (dict): meta data such as:
          filename (str): file where to write,
          is_json (bool): write in json file,
          newline (bool): if True line ends with '\n'

    Raises:
        Exception: if not filename specified

    Returns:
        Optional[bool]: True if successful else raise Exception
    """
    filename = kwargs.get("filename", None)
    print(
        f"\t{BColors.OKBLUE}Writing request content in file...\
          {BColors.ENDC}",
        end="\t\t",
    )
    if filename is not None and filename.strip() != "":
        with open(kwargs.get("filename"), kwargs.get("mode", "w")) as f:
            if kwargs.get("newline", True) is True:
                content = f"{content}\n"
            if kwargs.get("is_json", False) is True:
                json.dump(content, f, indent=2)
            else:
                f.write(content)

        print(f"{BColors.OKGREEN}[OK]{BColors.ENDC}")
        return True
    raise Exception("You must specify a filepath or filename to create")


async def readFile(filename: str, callback: Callable) -> None:
    """Read file and execute given callback on this file

    Args:
        filename (str): file to read
        callback (Callable): callaback to execute on file
    Returns:
        None:
    """
    with open(filename, "r") as f:
        await callback(f)


@cache
def extract_dirs_files_urls_to_dict(
    text: str, origin="http://127.0.0.1", full_url=None
) -> dict:
    """Extract directories and files urls from file content to a dictionary

    Args:
        text (str): text to process
    Returns:
        dict[str: list]: contains files and directories
    """

    # Extract dirs and files
    dirs_files: list[tuple(str)] = re.findall(r"(.+\n(file|dir)\n)", text)
    if len(dirs_files) == 0:
        raise Exception("Bad url")
    print(
        f"\t{BColors.OKBLUE}Extracting directories and files...{BColors.ENDC}",
        end="\t\t\t",
    )
    data = {"dirs": [], "files": []}
    for dir_file, typeStr in dirs_files:
        resource, *_ = dir_file.split("\n")
        resource = f"{origin}/{resource.strip()}"
        if "file" in typeStr:
            data["files"].append(resource)
        elif "dir" in typeStr:
            data["dirs"].append(resource)

    print(f"{BColors.OKGREEN}[OK]{BColors.ENDC}")
    return data
