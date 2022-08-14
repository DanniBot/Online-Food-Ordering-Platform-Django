from django.core.exceptions import ValidationError
import os

def allow_obly_images_validator(value):
    ext=os.path.splitext(value.name)[1]  ## cover_image.jpeg
    print(ext)
    valid_extensions=['.png','jpg','jpeg','gif','webp','svg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file type. Allowed types are with these extensions: '+str(valid_extensions))