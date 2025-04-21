from PIL import Image

def crop_before_next_avatar(img_path, save_path):
    im = Image.open(img_path)
    width, height = im.size
    pixels = im.load()

    bg_color = pixels[0, 0]
    avatar_x = 24  # Ajusta según el margen izquierdo de los avatares
    avatar_count = 0
    cut_y = height

    y = 40
    while y < height:
        if pixels[avatar_x, y] != bg_color:
            avatar_count += 1
            # Salta todas las filas donde está el avatar
            while y < height and pixels[avatar_x, y] != bg_color:
                y += 1
            # Si es el segundo avatar, recorta ahí
            if avatar_count == 2:
                cut_y = y - 10  # Un pequeño margen arriba del avatar
                break
        y += 1

    im_cropped = im.crop((0, 0, width, cut_y))
    im_cropped.save(save_path)