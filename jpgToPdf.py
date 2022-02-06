import os
from PIL import Image

fs = os.listdir('./output')

im1, imagelist = [], []
for f in fs:
    f = f.lower()
    if not (f.endswith('.jpg') or f.endswith('.png')):
        continue
    dir = './output/' + f
    img = Image.open(dir)
    img = img.convert('RGB')
    if im1:
        imagelist.append(img)
        continue
    im1.append(img)

im1[0].save('./output/output.pdf', save_all=True, append_images=imagelist)