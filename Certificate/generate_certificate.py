from PIL import Image, ImageDraw, ImageFont


def create_certificate(
        name, date, course
):
    template_path = "certificate_template.png"
    font_path = "Certificate/times.ttf"
    name_position = (1000, 707)
    output_path = "./personalized_certificate.png"

    # Load the certificate template
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)

    # Load the font
    name_font = ImageFont.truetype(font_path, 150)
    # Add name text
    name_text_width = draw.textlength(name, font=name_font)

    # Calculate the position
    x = name_position[0] - name_text_width / 2
    y = name_position[1] - 80
    draw.text((x, y), name, font=name_font, align="center", fill="black")

    # Add date text
    date_font = ImageFont.truetype(font_path, 40)
    date_text_width = draw.textlength(date, font=date_font)
    draw.text((550 - date_text_width / 2, 1010), date, font=date_font, align="center", fill="black")

    # Add course name text
    course_font = ImageFont.truetype(font_path, 30)
    course_text_width = draw.textlength(course, font=course_font)
    draw.text((1000 - course_text_width / 2, 915), course, font=course_font, align="center", fill="black")

    # Save the modified image
    image.save(output_path)


# Example usage
name = "Katelyn Choo Choo"
date = "21 September 2023"
course = "Digital Literacy Trainer 1"

create_certificate(name, date, course)
