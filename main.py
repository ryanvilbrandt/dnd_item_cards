import tomllib
from typing import Any

from PIL.Image import Image

from enums import VAlign
from pil_helpers import open_image, add_image, TextBox

name_box = TextBox(50, 60, 650, 50, font_size=72, font_name="fonts/Enchanted Land DEMO.otf")
subtitle_box = TextBox(50, 110, 650, 30)
description_box = TextBox(30, 660, 690, 340, valign=VAlign.TOP, shrink_font_size_to_fit=True)
picture_coords = (40, 190, 670, 450)


def build_card(toml_path: str):
    # Load the given toml dict
    toml_dict = open_toml(toml_path)
    # Call class module code
    im = get_template()
    add_text(im, toml_dict)
    return im


def open_toml(filepath: str) -> dict[str, Any]:
    with open(filepath, "rb") as f:
        return tomllib.load(f)


def get_template() -> Image:
    filepath = f"template.jpg"
    return open_image(filepath)


def add_text(im: Image, toml_dict: dict[str, Any]):
    name_box.add_text(im, toml_dict["name"])
    subtitle_box.add_text(im, toml_dict["type"])
    add_image(im, toml_dict["image_path"], *picture_coords)
    description_box.add_text(im, toml_dict["description"])


if __name__ == "__main__":
    im = build_card("items/book_of_lamashtu.toml")
    im.show()
