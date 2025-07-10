import os
import tomllib
from csv import DictWriter, DictReader
from typing import Any, List, Tuple, Optional, TypedDict

import qrcode
from PIL.Image import Image

from enums import VAlign
from pil_helpers import open_image, add_image, TextBox, save_page

name_box = TextBox(50, 30, 650, 110, font_size=72, font_name="fonts/Enchanted Land DEMO.otf",
                   shrink_font_size_to_fit=True)
subtitle_box = TextBox(50, 110, 650, 30)
description_box = TextBox(40, 670, 670, 320, valign=VAlign.TOP, shrink_font_size_to_fit=True)
picture_coords = (40, 190, 670, 450)


class CardListRow(TypedDict):
    filepath: str
    count: int


def open_toml(filepath: str) -> dict[str, Any]:
    with open(filepath, "rb") as f:
        return tomllib.load(f)


def build_card_list():
    with open("card_list.csv", "w", newline='') as f:
        writer = DictWriter(f, ["Name", "Path", "Count"])
        writer.writeheader()
        for dirpath, dirnames, filenames in os.walk("items"):
            for filename in filenames:
                if not filename.endswith(".toml"):
                    continue
                filepath = os.path.join(dirpath, filename)
                toml_dict = open_toml(filepath)
                try:
                    writer.writerow({"Name": toml_dict["name"], "Path": filepath, "Count": 1})
                except KeyError:
                    print("jfklskjds")


def get_card_list() -> Optional[list[CardListRow]]:
    if not os.path.isfile("card_list.csv"):
        build_card_list()
        print("card_list.csv has been created. Edit that file to include only the cards you want, "
              "and run this script again.")
        return None
    card_list_rows = []
    with open("card_list.csv") as f:
        reader = DictReader(f)
        for row in reader:
            card_list_rows.append({"filepath": row["Path"], "count": int(row["Count"])})
    return card_list_rows


def check_cards(toml_dicts: dict[str, dict]):
    print("About to create image for the following cards:")
    for path in toml_dicts:
        print(path)


def build_cards(card_list_rows: list[CardListRow]):
    cards = []
    for row in card_list_rows:
        filepath = row["filepath"]
        cards += build_card(filepath, open_toml(filepath), row["count"])
    save_cards_to_pages(cards)


def build_card(toml_path: str, toml_dict: dict = None, count: int = 1) -> Optional[List[Image]]:
    print(toml_path)
    if toml_dict is None:
        toml_dict = open_toml(toml_path)
    image_list = []
    for _ in range(count):
        if toml_dict.get("image_is_card"):
            im = open_image("images/" + toml_dict["image_path"])
        else:
            im = get_template()
            add_text(im, toml_dict)
            if "url" in toml_dict:
                add_qr_code(im, toml_dict)
        image_list.append(im)
    return image_list


def get_template() -> Image:
    return open_image("template.jpg")


def add_text(im: Image, toml_dict: dict[str, Any]):
    name_box.add_text(im, toml_dict["name"])
    subtitle = toml_dict["type"]
    if toml_dict.get("requires_attunement"):
        subtitle += " (requires attunement)"
    subtitle_box.add_text(im, subtitle)
    add_image(im, toml_dict["image_path"], *picture_coords)
    description_box.add_text(im, toml_dict["description"])


def add_qr_code(im: Image, toml_dict: dict[str, Any]):
    if "url" in toml_dict:
        if toml_dict["url"] is None:
            return
        else:
            url = toml_dict["url"]
    else:
        url = f"wiki.harebrained.dev/s/em/{toml_dict['name']}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img: Image = qr.make_image()
    qr_width, qr_height = qr_img.size
    width, _ = im.size
    im.paste(qr_img, (width - qr_width - 30, 580 - qr_height))


def gen_chunks(chunk_list, n):
    for i in range(0, len(chunk_list), n):
        yield chunk_list[i:i + n]


def save_cards_to_pages(card_list: List[Image], grid: Tuple[int, int] = (3, 3), folder: str = "pages"):
    os.makedirs(f"output/{folder}", exist_ok=True)
    for i, chunk in enumerate(gen_chunks(card_list, grid[0] * grid[1])):
        filename = f"output/{folder}/{i + 1:>03}.png"
        print(f"Saving {filename}")
        save_page(chunk, grid, filename, cut_line_width=0)


def main():
    toml_dicts = get_card_list()
    if toml_dicts is None:
        return
    build_cards(toml_dicts)
    # im = build_card("items/magic_items/common/mystery_key.toml")
    # im[0].show()


if __name__ == "__main__":
    main()
