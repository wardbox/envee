from PIL import Image, ImageDraw, ImageFont


def draw_text_on_lcd(
    text, font_path, font_size, text_color=(255, 255, 255), lcd_width=160, lcd_height=80
):
    # Create a blank image with a white background (or any other color of choice)
    lcd_image = Image.new("RGB", (lcd_width, lcd_height), (0, 0, 0))

    # Load a font
    font = ImageFont.truetype(font_path, font_size)

    # Prepare to draw text
    draw = ImageDraw.Draw(lcd_image)

    # Get text size
    text_width, text_height = draw.textsize(text, font=font)

    # Calculate the position for the text to be centered
    text_position = ((lcd_width - text_width) // 2, (lcd_height - text_height) // 2)

    # Draw text onto the image
    draw.text(text_position, text, font=font, fill=text_color)

    # The LCD image is ready to be used with the text
    return lcd_image
