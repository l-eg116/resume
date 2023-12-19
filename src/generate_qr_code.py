import sys
from pathlib import Path

import PIL
import qrcode
import requests
from load_yaml import load_options
from PIL import Image, ImageDraw
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


# Constants
DOWNLOADS_DIR = "src/downloads"
ASSETS_DIR = "src/assets"

OPTIONS_FILENAME = "options.yml"
ROUNDED_LOGO_FILENAME = "rounded-logo.png"
QR_CODE_FILENAME = "qr-code.png"
LOGO_FILENAME_DEFAULT = "logo.jpg"
CORNER_RADIUS = 100

RESUME_URL = "https://morgankryze.github.io/Resume-LaTeX/"


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


def fetch_image_from_remote(url: str) -> None:
    """Fetch an image from a remote URL.

    Args:
    ----
        url (str): The URL of the image to be fetched.

    Returns:
    -------
        None
    """
    try:
        response = requests.get(url, timeout=10)
        with Path.open(f"{DOWNLOADS_DIR}/{LOGO_FILENAME_DEFAULT}", "wb") as f:
            f.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image from {url}: {e}")


def process_image(options: str) -> bool:
    """Process the image to be used as the QR code.

    Args:
    ----
        options (str): The options for the image source.

    Returns:
    -------
        bool: True if the image was processed successfully, False otherwise.
    """
    if options.startswith("http"):
        fetch_image_from_remote(options)
        return True
    return False


if __name__ == "__main__":
    if not hasattr(PIL.Image, "Resampling"):
        PIL.Image.Resampling = PIL.Image

    options = load_options(f"src/{OPTIONS_FILENAME}")
    is_remote = process_image(options["image_source"])
    color_panel = tuple(options["color_panel"])
    filename = LOGO_FILENAME_DEFAULT if is_remote else options["image_source"]
    if is_remote:
        print("Image fetched successfully!")
        im = Image.open(f"{DOWNLOADS_DIR}/{filename}")
        im = im.crop((0, 0, min(im.size), min(im.size)))
        im = add_corners(im, CORNER_RADIUS)
        im.save(f"{DOWNLOADS_DIR}/{ROUNDED_LOGO_FILENAME}")
    else:
        im = Image.open(f"{ASSETS_DIR}/{filename}")
        im = add_corners(im, CORNER_RADIUS)
        im.save(f"{ASSETS_DIR}/{ROUNDED_LOGO_FILENAME}")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
    )

    qr.add_data(RESUME_URL)

    qr_img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        embeded_image_path=(
            f"{DOWNLOADS_DIR}/{ROUNDED_LOGO_FILENAME}"
            if is_remote
            else f"{ASSETS_DIR}/{ROUNDED_LOGO_FILENAME}"
        ),
    )

    qr_inner_eyes_img = qr.make_image(
        image_factory=StyledPilImage,
        eye_drawer=RoundedModuleDrawer(radius_ratio=0.9),
        color_mask=SolidFillColorMask(
            front_color=color_panel,
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
    final_image.save(QR_CODE_FILENAME)
    print("QR code generated successfully!")
