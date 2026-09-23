#!/usr/bin/env python3
from PIL import Image, ImageEnhance
import os, numpy as np

def crop_rajah(src_path, out_path, x0, y0, x1, y1, upscale=4):
    im = Image.open(src_path).convert("RGB")
    w, h = im.size
    box = (int(w*x0), int(h*y0), int(w*x1), int(h*y1))
    crop = im.crop(box)
    enhancer = ImageEnhance.Contrast(crop)
    crop = enhancer.enhance(1.6)
    enhancer = ImageEnhance.Brightness(crop)
    crop = enhancer.enhance(1.15)
    arr = np.array(crop)
    mask = (arr[:,:,0] > 188) & (arr[:,:,1] > 188) & (arr[:,:,2] > 188)
    arr[mask] = 255
    crop = Image.fromarray(arr)
    new_size = (crop.size[0]*upscale, crop.size[1]*upscale)
    crop = crop.resize(new_size, Image.LANCZOS)
    pad = 70
    padded = Image.new("RGB", (crop.size[0]+pad*2, crop.size[1]+pad*2), (255,255,255))
    padded.paste(crop, (pad, pad))
    padded.save(out_path, "JPEG", quality=95, dpi=(300,300))
    print(f"{out_path}: {padded.size} box {box} src {w}x{h}")

base = "/home/user/asoro-wa-khofiyyat-fi-ilmu-ruhaniyyah"
outdir = os.path.join(base, "terjemahan/assets")
os.makedirs(outdir, exist_ok=True)

# Hal067 top - only thilasm handwritten block, exclude zigzag left and shadow right
crop_rajah(os.path.join(base, "Picture 033.jpg"), os.path.join(outdir, "rajah-hal-067-top-thilasm.jpg"),
           x0=0.075, y0=0.085, x1=0.46, y1=0.30)

# Hal067 bottom - only 2 lines numbers, exclude headings
crop_rajah(os.path.join(base, "Picture 033.jpg"), os.path.join(outdir, "rajah-hal-067-bottom-numbers.jpg"),
           x0=0.135, y0=0.56, x1=0.44, y1=0.655)

# Hal068 top - handwritten top only, exclude heading below
crop_rajah(os.path.join(base, "Picture 034.jpg"), os.path.join(outdir, "rajah-hal-068-top-thilasm.jpg"),
           x0=0.565, y0=0.075, x1=0.945, y1=0.325)

# Hal068 bottom - boxed thilasm only
crop_rajah(os.path.join(base, "Picture 034.jpg"), os.path.join(outdir, "rajah-hal-068-bottom-box.jpg"),
           x0=0.575, y0=0.53, x1=0.825, y1=0.74)

# Hal069 - 4 lines numbers only, exclude "تم" heading
crop_rajah(os.path.join(base, "Picture 034.jpg"), os.path.join(outdir, "rajah-hal-069-thilasm.jpg"),
           x0=0.22, y0=0.49, x1=0.46, y1=0.62)

# Hal070 - wafaq star only, tight
crop_rajah(os.path.join(base, "Picture 035.jpg"), os.path.join(outdir, "rajah-hal-070-wafaq.jpg"),
           x0=0.625, y0=0.59, x1=0.86, y1=0.86)

# Hal071 - four squares only
crop_rajah(os.path.join(base, "Picture 035.jpg"), os.path.join(outdir, "rajah-hal-071-four-squares.jpg"),
           x0=0.185, y0=0.185, x1=0.445, y1=0.33)

print("v2 done")
