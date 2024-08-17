from PIL import Image, ImageFile, UnidentifiedImageError

ImageFile.LOAD_TRUNCATED_IMAGES = True


def resize_image(image_path, size_img):
    try:
        with Image.open(image_path) as img:
            ancho, alto = img.size
            if alto != size_img or ancho != size_img:
                if ancho > alto:
                    nuevo_alto = size_img
                    nuevo_ancho = int((ancho / alto) * nuevo_alto)
                    img = img.resize(
                        (nuevo_ancho, nuevo_alto), Image.Resampling.BILINEAR
                    )
                elif alto > ancho:
                    nuevo_ancho = size_img
                    nuevo_alto = int((alto / ancho) * nuevo_ancho)
                    img = img.resize(
                        (nuevo_ancho, nuevo_alto), Image.Resampling.BILINEAR
                    )
                else:
                    img.thumbnail((size_img, size_img))
                img.save(image_path)
    except (FileExistsError, UnidentifiedImageError):
        print("Error al Redimensionar la imagen")


def crop_image(image_path, size_img):
    try:
        with Image.open(image_path) as img:
            ancho, alto = img.size
            if alto != size_img or ancho != size_img:
                lado = min(ancho, alto)
                left = (ancho - lado) / 2
                top = (alto - lado) / 2
                right = (ancho + lado) / 2
                bottom = (alto + lado) / 2
                img = img.crop((left, top, right, bottom))
                img.save(image_path)
    except (FileExistsError, UnidentifiedImageError):
        print("Erro al Recortar la imagen")
