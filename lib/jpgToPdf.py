import os
from PIL import Image

def jpgToPdf(save_dir):
    fs = os.listdir('./tmp')

    im1, imagelist = [], []
    for f in fs:
        f = f.lower()
        if not (f.endswith('.jpg') or f.endswith('.png')):
            continue
        dir = './tmp/' + f
        img = Image.open(dir)
        img = img.convert('RGB')
        if im1:
            imagelist.append(img)
            continue
        im1.append(img)

    im1[0].save(f'{save_dir}/output.pdf', save_all=True, append_images=imagelist)

    for f in fs:
        dir = './tmp/' + f
        os.remove(dir)