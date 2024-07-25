import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image, ImageDraw, ImageOps
import PIL.Image
import os


class qr_code:
    def __init__(self, data, inner_eye_color=(0, 0, 0), outer_eye_color=(0, 0, 0), logo=None, logo_rounded=True):
        self.data = data
        self.inner_eye_color = inner_eye_color
        self.outer_eye_color = outer_eye_color
        self.logo = logo
        self.logo_rounded = logo_rounded
        if not hasattr(PIL.Image, 'Resampling'):
            PIL.Image.Resampling = PIL.Image

    def style_inner_eyes(self, img):
        img_size = img.size[0]
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rectangle((40, 40, 70, 70), fill=255)  # top left eye
        draw.rectangle((img_size - 70, 40, img_size - 40, 70),
                       fill=255)  # top right eye
        draw.rectangle((40, img_size - 70, 70, img_size - 40),
                       fill=255)  # bottom left eye
        return mask

    def add_corners(self, im, rad):
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill='#ffffff')
        alpha = Image.new('L', im.size, '#ffffff')
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)),
                    (w - rad, h - rad))

        im.putalpha(alpha)
        return im
    
    def add_gradient_background(self , image_path, output_path, color1, color2, direction='vertical', ratio_func=None):
        if ratio_func is None:
            ratio_func = lambda x: x

        # Open the original image
        original_image = Image.open(image_path).convert("RGBA")
        width, height = original_image.size

        # Create a new image with the same size and RGBA mode
        gradient_image = Image.new("RGBA", (width, height))

        # Create a drawing context
        draw = ImageDraw.Draw(gradient_image)

        # Draw the gradient
        if direction == 'vertical':
            for y in range(height):
                ratio = ratio_func(y / float(height))
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
        elif direction == 'horizontal':
            for x in range(width):
                ratio = ratio_func(x / float(width))
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                draw.line([(x, 0), (x, height)], fill=(r, g, b))

        combined_image = Image.alpha_composite(gradient_image, original_image)

        combined_image.save(output_path)

    def style_outer_eyes(self, img):
        img_size = img.size[0]
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rectangle((20, 20, 90, 90), fill=255)  # top left eye
        draw.rectangle((img_size - 90, 20, img_size - 20, 90),
                       fill=255)  # top right eye
        draw.rectangle((20, img_size - 90, 90, img_size - 20),
                       fill=255)  # bottom left eye
        draw.rectangle((40, 40, 70, 70), fill=0)  # top left eye
        draw.rectangle((img_size - 70, 40, img_size - 40, 70),
                       fill=0)  # top right eye
        draw.rectangle((40, img_size - 70, 70, img_size - 40),
                       fill=0)  # bottom left eye
        return mask

    def generate_qr_code(self):
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H, border=2)
        qr.add_data(self.data)
        qr.make(fit=True)
        if self.logo is not None:
            self.add_gradient_background(f'{self.logo}', f'{self.logo}_temp.png' , (0, 0, 0), (94, 56, 199), 'vertical' , lambda x : x**1.7)
            im = Image.open(f'{self.logo}_temp.png')
            if self.logo_rounded:
                im = self.add_corners(im, 100)
            im.save(f'{self.logo}_temp.png')
        qr_inner_eyes_img = qr.make_image(image_factory=StyledPilImage,
                                          eye_drawer=RoundedModuleDrawer(
                                              radius_ratio=1),
                                          color_mask=SolidFillColorMask(front_color=self.inner_eye_color))

        qr_outer_eyes_img = qr.make_image(image_factory=StyledPilImage,
                                          eye_drawer=RoundedModuleDrawer(
                                              radius_ratio=1),
                                          color_mask=SolidFillColorMask(front_color=self.outer_eye_color))
        qr_img = None
        if self.logo is not None:
            qr_img = qr.make_image(image_factory=StyledPilImage,
                                module_drawer=RoundedModuleDrawer(),
                                embeded_image_path=f'{self.logo}_temp.png')
            os.remove(f'{self.logo}_temp.png')
        else :
            qr_img = qr.make_image(image_factory=StyledPilImage,
                                module_drawer=RoundedModuleDrawer())

        inner_eye_mask = self.style_inner_eyes(qr_img)
        outer_eye_mask = self.style_outer_eyes(qr_img)
        intermediate_img = Image.composite(
            qr_inner_eyes_img, qr_img, inner_eye_mask)
        final_image = Image.composite(
            qr_outer_eyes_img, intermediate_img, outer_eye_mask)


        
        return final_image
        final_image.save('qrcode.png')
        # finally delete the temp image

        








# how to send QR code 


# logo_to_send = None
# if special_event.logo.name != None and special_event.logo.name != "":
#     logo_to_send = special_event.logo.path
# self.make_qr(
#     ser.validated_data['email'], logo_to_send)

# mail_with_image(
#     sender='esla889900@gmail.com',
#     sender_password='erls gvry oilr dtqy',
#     recever=ser.validated_data['email'],
#     subject=f'{special_event.name} Qr For Registration',
#     body=qrMailTemplateForEvent(
#         event=special_event.name,
#     ).getTemplate(),
#     images=[str(settings.BASE_DIR / 'events' /
#                 'qr_codes' / f'{ser.validated_data["email"]}.png')]
# ).send_mail()

# os.remove(settings.BASE_DIR / 'events' / 'qr_codes' /
#           f'{ser.validated_data["email"]}.png')