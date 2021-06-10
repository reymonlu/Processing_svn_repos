import re
import json
from typing import Optional
from functools import cache

from colors import BColors


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
        end="\t\t\t\t",
    )
    # Extract dirs and files
    dirs_files: list[tuple(str)] = re.findall(r"(.+\n(file|dir)\n)", text)
    data = {"dirs": [], "files": []}
    for dir_file, typeStr in dirs_files:
        resource, *_ = dir_file.split("\n")
        resource = f"{origin}/{resource.strip()}"
        if "file" in typeStr:
            data['files'].append(resource)
        elif "dir" in typeStr:
            data['dirs'].append(resource)
    print(f"{BColors.OKGREEN}[OK]{BColors.ENDC}")
    return data
