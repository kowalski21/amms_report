from pathlib import Path
import sys
import subprocess
import re


def libreoffice_exec():
    return "libreoffice"


class LibreOfficeError(Exception):
    def __init__(self, output):
        self.output = output


def convert_file(folder, source, timeout=None):
    args = [
        libreoffice_exec(),
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        folder,
        source,
    ]
    process = subprocess.run(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout
    )
    print(process.stdout.decode())
