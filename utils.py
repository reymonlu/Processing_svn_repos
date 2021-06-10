import re
import json
from typing import Optional
from functools import cache

from colors import BColors


async def writeInFile(content: str, **kwargs: dict) -> Optional[bool]:
    """Write text/dict into specified filename

    Args:
        content (str): content to write in file, can be a dictionary or text

    Raises:
        Exception: if not filename specified

    Returns:
        Optional[bool]: True if successful else raise Exception
    """
    filename = kwargs.get("filename", None)
    print(
        f"{BColors.OKBLUE}Writing request content in file {filename}...\
          {BColors.ENDC}",
        end="\t",
    )
    if filename is not None and filename.strip() != "":
        with open(kwargs.get("filename"), "w") as f:
            if kwargs.get("newline", True) is True:
                content = f"\n{content}"
            if kwargs.get("is_json", False) is True:
                json.dump(content, f, indent=2)
            else:
                f.write(content)
        print(f"{BColors.OKGREEN}[OK]{BColors.ENDC}")
        return True
    raise Exception("You must specify a filepath or filename to create")


@cache
def processing_bytes(content: bytes) -> str:
    """Remove empty lines, txt with length less or equals than 2
      and unencod character such as:

    Args:
        content (bytes): text to process

    Returns:
        str: text processed
    """
    print(
        f"{BColors.OKBLUE}Processing request content...{BColors.ENDC}",
        end="\t",
    )
    new_content = "\n".join(
        list(
            filter(
                lambda txt: len(txt) > 2,
                re.sub(r"\n{2,}|\n\n", "\n", content.decode("utf-8")).split(
                    "\n"
                ),
            )
        )
    )
    print(f"{BColors.OKGREEN}[OK]{BColors.ENDC}")
    return new_content


@cache
def extract_dirs_files_urls_to_dict(
    text: str, origin="http://127.0.0.1"
) -> dict:
    """Extract directories and files urls in dictionary

    Args:
        text (str): text to process
    Returns:
        dict[str: list]: contains files and directories
    """
    print(
        f"{BColors.OKBLUE}Extracting directories and files...{BColors.ENDC}",
        end="\t",
    )
    data = {"dirs": [], "files": []}
    text_arr = text.strip().split("\n")
    for i, line in enumerate(text_arr):
        line = line.strip()
        if i > 0:
            ressource = f"{origin}/{text_arr[i - 1].strip()}"
            if line == "dir":
                data["dirs"].append(ressource)
            elif line == "file":
                data["files"].append(ressource)
    print(f"{BColors.OKGREEN}[OK]{BColors.ENDC}")
    return data
