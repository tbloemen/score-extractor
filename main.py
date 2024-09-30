"""
A python script which, given a folder of songs with pdf's in them, splits them into the parts of their instrument.
"""
import re
import shutil
from pathlib import Path

import pymupdf
from pymupdf import Document, Rect, Page, Point

from instrument import create_instruments, Instrument

MUSIC_FILE_EXTENSIONS = [".mp3", ".ogg", ".wav", ".flac", ".aiff", ".midi"]


def create_example_folder(examples: list[Path]):
    dir = Path.cwd().joinpath("result/Examples")
    dir.mkdir(exist_ok=True, parents=True)
    for example in examples:
        shutil.copy(example, dir.joinpath(example.name))


def get_folder_paths() -> tuple[list[Path], list[Path]]:
    p = Path.cwd().joinpath("resources")
    return rec_folder_path_helper(p)


def rec_folder_path_helper(path) -> tuple[list[Path], list[Path]]:
    res_scores, res_examples = [], []
    if path.is_dir():
        for subpath in path.iterdir():
            scores, examples = rec_folder_path_helper(subpath)
            res_scores.extend(scores)
            res_examples.extend(examples)
    else:
        if path.suffix == ".pdf":
            res_scores.append(path)
        elif path.suffix in MUSIC_FILE_EXTENSIONS:
            res_examples.append(path)
    return res_scores, res_examples


def extract_parts(doc) -> None:
    pass

def clean_text(text: str) -> str:
    return re.sub('[\W_]+', ' ', text).lower().strip()

def predict_instr(doc: Document, name: str) -> Instrument:
    counter = {}

    for instrument in create_instruments():
        for representation in instrument.representation():
            representation = clean_text(representation)
            if representation in clean_text(name):
                return instrument

            page: Page
            for page in doc:
                bounds: Rect = page.bound()
                newBound = Rect(bounds.tl, Point(bounds.br.x/3, bounds.br.y/3))
                text = page.get_text("text", clip=newBound)
                if clean_text(representation) in clean_text(text):
                    counter[instrument] = counter.get(instrument, 0) + 1
    if len(counter) == 0:
        raise ValueError(f"No associated instrument found for {doc.name}")
    return max(counter, key=counter.get)


def extract_song(pdf_file: Path):
    doc = pymupdf.open(pdf_file)
    # Check if song is already split or is still in parts
    # For now: if song is longer than 16 pages, it is definitively parts
    if doc.page_count > 16:
        extract_parts(doc)
    else:
        try:
            instrument = predict_instr(doc, pdf_file.name)
            print(instrument)
            my_dir = Path.cwd().joinpath(f"result/{instrument}")
            my_dir.mkdir(exist_ok=True, parents=True)
            shutil.copy(pdf_file, my_dir.joinpath(pdf_file.name))
        except ValueError:
            my_dir = Path.cwd().joinpath("result/Afvalstapel")
            my_dir.mkdir(exist_ok=True, parents=True)
            shutil.copy(pdf_file, my_dir.joinpath(pdf_file.name))

def main():
    """
    The main function that runs the script.
    """
    print("Hello world")
    scores, examples = get_folder_paths()
    print(scores)
    print("-----")
    print(examples)
    create_example_folder(examples)
    for score in scores:
        extract_song(score)


if __name__ == "__main__":
    main()
