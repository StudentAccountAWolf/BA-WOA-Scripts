from PIL import Image, ImageChops
from tkinter import filedialog

# Lade vier Diagramme
diagramm1 = Image.open(filedialog.askopenfilename())
diagramm2 = Image.open(filedialog.askopenfilename())
diagramm3 = Image.open(filedialog.askopenfilename())
diagramm4 = Image.open(filedialog.askopenfilename())

collage = Image.new('RGB', (3140, 2500))

def add_image_to_collage(image, collage, position, size):
    resized_image = image.resize(size, Image.LANCZOS)
    collage.paste(resized_image, position, resized_image)

add_image_to_collage(diagramm1, collage, (0, 0), (1210, 1000))
add_image_to_collage(diagramm2, collage, (1210, 0), (1210, 1000))
add_image_to_collage(diagramm3, collage, (0, 1000), (1210, 1000))
add_image_to_collage(diagramm4, collage, (1210, 1000), (1210, 1000))

# Funktion zum Zuschneiden der Collage, um den transparenten Teil zu entfernen
def trim(im):
    bg = Image.new(im.mode, im.size)
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

# Zuschneiden der Collage
collage = trim(collage)

# Speichere die Collage
collage.save(r"M:\Benutzer\Downloads\collage.png")
