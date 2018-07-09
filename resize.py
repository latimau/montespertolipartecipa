import PIL
from PIL import Image

basewidth = 300
img = Image.open('/var/www/html/trydjango18/static_in_env/media_root/uploaded_images/dj.JPG')
wpercent = (basewidth / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)))
img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
img.save('/var/www/html/trydjango18/static_in_env/media_root/uploaded_images/dj.JPG')