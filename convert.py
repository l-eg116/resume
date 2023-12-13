from pdf2image import convert_from_path

if __name__ == "__main__":
    pages = convert_from_path("resume.pdf")

    if len(pages) > 1:
        for i in range(len(pages)):
            pages[i].save("page" + str(i) + ".jpg", "JPEG")
    else:
        pages[0].save("resume.jpg", "JPEG")
