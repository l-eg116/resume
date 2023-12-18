import PIL
import qrcode
from PIL import Image, ImageDraw
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer


def add_corners(im: Image, rad: int) -> Image:
    """Modify the input image by adding rounded corners.

    Args:
    ----
        im (Image): The input image to be modified.
        rad (int): The radius of the rounded corners.

    Returns:
    -------
        Image: The modified image with rounded corners.
    """
    circle = Image.new("L", (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new("L", im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


def style_inner_eyes(img: Image) -> Image:
    """Return a mask image with rectangles drawn on the inner eyes.

    Args:
    ----
        img (Image): The input image on which the inner eyes will be styled.

    Returns:
    -------
        Image: The output mask image with rectangles drawn on the inner eyes.
    """
    img_size = img.size[0]
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((60, 60, 90, 90), fill=255)  # top left eye
    draw.rectangle(
        (img_size - 90, 60, img_size - 60, 90),
        fill=255,
    )  # top right eye
    draw.rectangle(
        (60, img_size - 90, 90, img_size - 60),
        fill=255,
    )  # bottom left eye
    return mask


def style_outer_eyes(img: Image) -> Image:
    """Apply styling to the outer eyes of the input image.

    Args:
    ----
        img (Image): The input image.

    Returns:
    -------
        Image: The styled mask image with the outer eyes.
    """
    img_size = img.size[0]
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((40, 40, 110, 110), fill=255)  # top left eye
    draw.rectangle(
        (img_size - 110, 40, img_size - 40, 110),
        fill=255,
    )  # top right eye
    draw.rectangle(
        (40, img_size - 110, 110, img_size - 40),
        fill=255,
    )  # bottom left eye
    draw.rectangle((60, 60, 90, 90), fill=0)  # top left eye
    draw.rectangle(
        (img_size - 90, 60, img_size - 60, 90),
        fill=0,
    )  # top right eye
    draw.rectangle(
        (60, img_size - 90, 90, img_size - 60),
        fill=0,
    )  # bottom left eye

    return mask
    return mask


if __name__ == "__main__":
    if not hasattr(PIL.Image, "Resampling"):
        PIL.Image.Resampling = PIL.Image

    im = Image.open("src/assets/logo.jpg")
    im = add_corners(im, 100)
    im.save("src/assets/rounded-logo.png")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
    )

    qr.add_data("https://morgankryze.github.io/Resume-LaTeX/")

    qr_img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        embeded_image_path="src/assets/rounded-logo.png",
    )

    qr_inner_eyes_img = qr.make_image(
        image_factory=StyledPilImage,
        eye_drawer=RoundedModuleDrawer(radius_ratio=0.9),
        color_mask=SolidFillColorMask(
            front_color=(233, 167, 135),
        ),
    )

    qr_outer_eyes_img = qr.make_image(
        image_factory=StyledPilImage,
        eye_drawer=RoundedModuleDrawer(radius_ratio=0.9),
    )

    inner_eye_mask = style_inner_eyes(qr_img)
    outer_eye_mask = style_outer_eyes(qr_img)

    intermediate_img = Image.composite(
        qr_inner_eyes_img,
        qr_img,
        inner_eye_mask,
    )
    final_image = Image.composite(
        qr_outer_eyes_img,
        intermediate_img,
        outer_eye_mask,
    )
    final_image.save("qr-code.png")
    print("Done!")
