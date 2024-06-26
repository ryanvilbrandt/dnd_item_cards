import os
import tomllib
from typing import Any, List, Tuple, Optional

from PIL.Image import Image

from enums import VAlign
from pil_helpers import open_image, add_image, TextBox, save_page

name_box = TextBox(50, 30, 650, 110, font_size=72, font_name="fonts/Enchanted Land DEMO.otf",
                   shrink_font_size_to_fit=True)
subtitle_box = TextBox(50, 110, 650, 30)
description_box = TextBox(40, 670, 670, 320, valign=VAlign.TOP, shrink_font_size_to_fit=True)
picture_coords = (40, 190, 670, 450)


def build_cards():
    cards = []
    for dirpath, dirnames, filenames in os.walk("items"):
        for filename in filenames:
            if not filename.endswith(".toml"):
                continue
            filepath = os.path.join(dirpath, filename)
            image_list = build_card(filepath)
            if image_list:
                print(filepath)
                # im.show()
                cards += image_list
    save_cards_to_pages(cards)


def build_card(toml_path: str) -> Optional[List[Image]]:
    # Load the given toml dict
    toml_dict = open_toml(toml_path)
    if toml_dict.get("skip"):
        return None
    image_list = []
    for _ in range(toml_dict.get("count", 1)):
        if toml_dict.get("image_is_card"):
            im = open_image("images/" + toml_dict["image_path"])
        else:
            im = get_template()
            add_text(im, toml_dict)
        image_list.append(im)
    return image_list


def open_toml(filepath: str) -> dict[str, Any]:
    with open(filepath, "rb") as f:
        return tomllib.load(f)


def get_template() -> Image:
    filepath = "template.jpg"
    return open_image(filepath)


def add_text(im: Image, toml_dict: dict[str, Any]):
    name_box.add_text(im, toml_dict["name"])
    subtitle = toml_dict["type"]
    if toml_dict.get("requires_attunement"):
        subtitle += " (requires attunement)"
    subtitle_box.add_text(im, subtitle)
    add_image(im, toml_dict["image_path"], *picture_coords)
    description_box.add_text(im, toml_dict["description"])


def gen_chunks(chunk_list, n):
    for i in range(0, len(chunk_list), n):
        yield chunk_list[i:i + n]


def save_cards_to_pages(card_list: List[Image], grid: Tuple[int, int] = (3, 3), folder: str = "pages"):
    os.makedirs(f"output/{folder}", exist_ok=True)
    for i, chunk in enumerate(gen_chunks(card_list, grid[0] * grid[1])):
        filename = f"output/{folder}/{i + 1:>03}.png"
        print(f"Saving {filename}")
        save_page(chunk, grid, filename, cut_line_width=0)


if __name__ == "__main__":
    build_cards()
    # cards = [
    #     build_card("items/spellwrought_tattoo_see_invisibility.toml"),
    # ]
    # save_cards_to_pages(cards)
    # im = build_card("items/magic_items/common/hat_of_vermin.toml")[0]
    # im.show()
