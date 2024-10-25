"""
A python script which, given a folder of songs with pdfs in them, splits them into the parts of their instrument.
"""
import re
import shutil
from pathlib import Path

import pymupdf
from pymupdf import Document, Rect, Page, Point

from instrument import create_instruments, Instrument

MUSIC_FILE_EXTENSIONS = [".mp3", ".ogg", ".wav", ".flac", ".aiff", ".midi"]


def create_example_folder(examples: list[Path]):
    """
    Creates the folder "Examples" in the result directory, and copies all examples to that folder.

    :param examples: A list of Paths which point to examples (e.g. mp3, wav and midi files).
    """
    example_dir = Path.cwd().joinpath("result/Examples")
    example_dir.mkdir(exist_ok=True, parents=True)
    for example in examples:
        shutil.copy(example, example_dir.joinpath(example.name))


def get_folder_paths() -> tuple[list[Path], list[Path]]:
    """
    Gets all the paths for the scores and examples.

    :return: A list of Paths for the scores, and a list of Paths for the examples.
    """

    p = Path.cwd().joinpath("resources")
    if p.exists():
        return rec_folder_path_helper(p)
    p.mkdir()
    raise FileNotFoundError("The folder 'resources' had not been created yet. It has now been created, please place "
                            "the scores you wish to attract in this folder.")


def rec_folder_path_helper(path) -> tuple[list[Path], list[Path]]:
    """
    Helper function for `get_folder_paths()`. Recursively checks if the path provided is a score, example or
    directory. If it is a directory, recurse all subpaths.

    :param path: The path to check if it is a score, example or directory.
    :return: A list of Paths for the scores and a list of Paths for the examples.
    """
    res_scores, res_examples = [], []
    if path.is_dir():
        for sub_path in path.iterdir():
            scores, examples = rec_folder_path_helper(sub_path)
            res_scores.extend(scores)
            res_examples.extend(examples)
    else:
        if path.suffix == ".pdf":
            res_scores.append(path)
        elif path.suffix in MUSIC_FILE_EXTENSIONS:
            res_examples.append(path)
    return res_scores, res_examples


def get_page_numbers(doc: Document) -> list[int]:
    """
    This function gets the page numbers where a new instrument starts. For example: if the pdf file has piano parts
    for page 1 through 6, and guitar parts for pages 7 through 9, this would return [1, 7].

    TODO: this function currently does not work, it can't recognize font size consistently with scanned in pdfs.

    :param doc: The parts file containing all the instrument parts.
    :return: A list of the page numbers where a new instrument starts.
    """
    page_idxes = []

    page: Page
    for page_number, page in enumerate(doc.pages()):
        blocks = page.get_textpage().extractDICT()["blocks"]
        for block in blocks:
            for line in block["lines"]:
                for span in line["spans"]:
                    font_size = span["size"]
                    if font_size > 20:
                        page_idxes.append(page_number)
    return page_idxes


def extract_parts(doc: Document) -> list[tuple[Document, Path]]:
    """
    Splits a parts file up into each instrument part.

    :param doc: The parts file containing all the instrument parts.
    :return: A list of instrument parts with their new filename.
    """
    page_numbers = get_page_numbers(doc)
    pymupdf.open(doc.name)
    dir_name = "extracted_scores"
    curr_dir = (Path(doc.name).parent.joinpath(dir_name))
    curr_dir.mkdir(exist_ok=True, parents=True)
    filename = curr_dir.joinpath(Path(doc.name).name)
    shutil.copy(doc.name, filename)
    copied_doc = pymupdf.open(filename)

    result = []
    for idx in range(len(page_numbers) - 1):
        start_page = page_numbers[idx]
        end_page = page_numbers[idx + 1]
        pages = []
        for page_number in range(start_page, end_page):
            pages.append(page_number)

        this_doc = copied_doc

        new_filename = f"{this_doc.name} - instrument {idx}.pdf"
        this_doc.select(pages)
        this_doc.save(new_filename)
        newPath = curr_dir.joinpath(new_filename)
        smaller_doc = pymupdf.open(newPath)
        result.append((smaller_doc, newPath))
    return result


def clean_text(text: str) -> str:
    """
    Returns a string where every non-alphanumeric character is removed, and is standardized to lower case.

    :param text: The text to be cleaned.
    :return: Clean text.
    """
    return re.sub('[\W_]+', ' ', text).lower().strip()


def predict_instr(doc: Document, name: str) -> Instrument:
    """
    Tries to predict an instrument of the pdf file provided.
    If an instrument can't be predicted, it throws a ValueError.

    :param doc: The pdf file to predict.
    :param name: The filename of the pdf file.
    :return: The instrument predicted.
    """
    counter = {}

    for instrument in create_instruments():
        for representation in instrument.representation():
            representation = clean_text(representation)
            if representation in clean_text(name):
                return instrument

            for page in doc:
                bounds = page.bound()
                newBound = Rect(bounds.tl, Point(bounds.br.x / 3, bounds.br.y / 3))
                text = page.get_text("text", clip=newBound)
                if clean_text(representation) in clean_text(text):
                    counter[instrument] = counter.get(instrument, 0) + 1
    if len(counter) == 0:
        raise ValueError(f"No associated instrument found for {doc.name}")
    return max(counter, key=counter.get)


def allocate_instruments(doc: Document, pdf_file: Path):
    """
    Puts an instrument part into the correct folder.
    If an instrument can't be predicted, it goes the Afvalstapel (trash can).

    :param doc: The pdf document to be predicted.
    :param pdf_file: The Path object corresponding to the pdf file to be predicted.
    """
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


def extract_song(pdf_file: Path):
    """
    Extracts the song to the correct folder, or folders if the file provided contains multiple parts.

    :param pdf_file: The path to the pdf file containing a part, or multiple parts.
    """
    doc = pymupdf.open(pdf_file)
    # Check if song is already split or is still in parts
    # For now: if song is longer than 16 pages, it is definitively parts
    if doc.page_count > 16:
        docsAndNames = extract_parts(doc)
        for doc, name in docsAndNames:
            allocate_instruments(doc, name)
    else:
        allocate_instruments(doc, pdf_file)


def main():
    """
    The main function that runs the script.
    """
    scores, examples = get_folder_paths()
    print(scores)
    print("-----")
    print(examples)
    create_example_folder(examples)
    for score in scores:
        extract_song(score)


if __name__ == "__main__":
    main()
