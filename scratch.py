from PIL import Image

files = [
    "potion_of_healing.png",
    "potion_of_greater_healing.png",
    "potion_of_superior_healing.png",
    "potion_of_supreme_healing.png",
]

for filename in files:
    im = Image.open("images/" + filename)
    resized_im = im.resize((745, 1040))
    resized_im.show()
    resized_im.save("images/" + filename)
