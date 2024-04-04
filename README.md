# Resume LaTeX template

> LaTeX easy-to-use template for tech resume that auto-build on a github page.

![Resume Preview](src/resume-en/resume.jpg)

![Resume Preview](output/qr-code.png)

## Getting Started

> [!NOTE]
> The QR code and result pdf will be found in the `output/` folder.

### Prerequisites

To use this template, you will need to have LaTeX installed on your system. If you don't have LaTeX installed, you can use [Overleaf](https://www.overleaf.com/) to edit and compile the template.

Personally, I use LaTeX workshop extension for VSCode.

### Install

To use this template, you can either download the zip file or clone the repository:

```bash
git clone https://github.com/MorganKryze/Resume-LaTeX.git
```

### Use

Once installed, it's pretty much it, just edit the `resume.tex` file to your liking and compile it automatically with LaTeX workshop. the outcome will be a `resume.pdf` file.

> If you encounter errors in the compilation, check that you have correctly installed all the libraries needed.

Then enter in the settings > pages : select "from branch", select "gh-pages" (create the branch if it does not exist), and select "/root". Now at every push, the pdf will be updated on your own github page [preview](https://morgankryze.github.io/Resume-LaTeX/).

If you want to only one language or two languages, you can update the `options.yml` file like this (only english for example):

```yml
languages:
  - english
# - french
```

To create a qr-code, you can call the `qr-code.py` file:

```bash
python src/generate_qr_code.py
```

### Converting

If you want to use the convert.py file to convert your resume to a jpg or png file, you will need to install the dependencies with:

```bash
pip install -r requirements.txt
```

And add the poppler package to your system.

On macOs, you can install it with:

```bash
brew install poppler
```

Then, according to your os, follow the instructions [here](https://pypi.org/project/pdf2image/).

Finally, you can run the script with:

```bash
python src/convert_and_merge.py
```

This will convert your resume.pdf to a resume.jpg file (this is the manual way, you can also use the script to automatically convert your resume.pdf to a resume.jpg file at every push).

### Create your own qr-code

To do so, update the options.yml file by giving the url of your new picture, or by pasting your custom image in `src/assets/` and giving the name of the image in the options.yml file. For a url image, you can go like this:

```yml
image_source: https://raw.githubusercontent.com/MorganKryze/Signature-Generator/main/src/resources/cat.jpg
```

Furthermore, you can also change the color of the qr-code by changing the `color_panel` value in the options.yml file with the r, g b values of the color you want:

```yml
color_panel:
  - 0
  - 0
  - 0
```

## Fork of

This fork is based off of [jakegut/resume](https://github.com/jakegut/resume).

Itself based off of [sb2nov/resume](https://github.com/sb2nov/resume/).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
