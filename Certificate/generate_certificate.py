from PIL import Image, ImageDraw, ImageFont

def create_certificate(name, template_path, font_path, font_size, position, output_path):
    # Load the certificate template
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)
    
    # Load the font
    font = ImageFont.load_path(font_path) 

    # Calculate text width and height
    text_width, text_height = 200, 200
    
    # Calculate the position: this example assumes 'position' is the center where the name should be placed
    x = position[0] - text_width / 2
    y = position[1] - text_height / 2
    
    # Position adjustment might be necessary depending on your template
    draw.text((x, y), name, font=font, align="center", fill="black")
    
    # Save the modified image
    image.save(output_path)

# Example usage
name = "John Doe"
template_path = "Certificate\certificate_template.png"
font_path = "Certificate\times.ttf" # Example font path
font_size = 40
position = (500, 300) # This should be adjusted based on your template
output_path = "Certificate\personalized_certificate.png"

create_certificate(name, template_path, font_path, font_size, position, output_path)