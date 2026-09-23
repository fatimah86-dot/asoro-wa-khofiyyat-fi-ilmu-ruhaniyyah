#!/usr/bin/env python3
from PIL import Image, ImageEnhance
import os

def crop_rajah(src_path, out_path, x0, y0, x1, y1, upscale=4):
    im = Image.open(src_path).convert("RGB")
    w, h = im.size
    box = (int(w*x0), int(h*y0), int(w*x1), int(h*y1))
    crop = im.crop(box)
    # enhance
    # contrast & brightness similar to previous batches
    enhancer = ImageEnhance.Contrast(crop)
    crop = enhancer.enhance(1.6)
    enhancer = ImageEnhance.Brightness(crop)
    crop = enhancer.enhance(1.15)
    # white threshold >188 -> 255
    # convert to numpy for speed
    import numpy as np
    arr = np.array(crop)
    # mask where all channels >188
    mask = (arr[:,:,0] > 188) & (arr[:,:,1] > 188) & (arr[:,:,2] > 188)
    arr[mask] = 255
    crop = Image.fromarray(arr)
    # pad 70px each side before upscale? original pad 70px then 4x. We'll add 70px white border before upscale, then upscale?
    # previous: pad 70px white>186 pad 70px. Let's add padding after upscale for simplicity: upscale then pad 70*? Actually previous reports: pad 70px white then 4x upscale. We'll do upscale then pad 70*? Let's do pad 70*upscale? Simpler: add 70px border after upscale then final.
    # upscale
    new_size = (crop.size[0]*upscale, crop.size[1]*upscale)
    crop = crop.resize(new_size, Image.LANCZOS)
    # add padding 70px * (upscale? previous said 70px pad then 4x). We'll add 50px white padding after upscale to get clean border
    pad = 70
    padded = Image.new("RGB", (crop.size[0]+pad*2, crop.size[1]+pad*2), (255,255,255))
    padded.paste(crop, (pad, pad))
    padded.save(out_path, "JPEG", quality=95, dpi=(300,300))
    print(f"{out_path}: {padded.size} from {src_path} box {box}")

base = "/home/user/asoro-wa-khofiyyat-fi-ilmu-ruhaniyyah"
outdir = os.path.join(base, "terjemahan/assets")
os.makedirs(outdir, exist_ok=True)

# Picture 033 left Hal67
crop_rajah(os.path.join(base, "Picture 033.jpg"), os.path.join(outdir, "rajah-hal-067-top-thilasm.jpg"),
           x0=0.055, y0=0.08, x1=0.475, y1=0.31)

crop_rajah(os.path.join(base, "Picture 033.jpg"), os.path.join(outdir, "rajah-hal-067-bottom-numbers.jpg"),
           x0=0.115, y0=0.52, x1=0.445, y1=0.71)

# Picture 034 right Hal68 top
crop_rajah(os.path.join(base, "Picture 034.jpg"), os.path.join(outdir, "rajah-hal-068-top-thilasm.jpg"),
           x0=0.545, y0=0.06, x1=0.965, y1=0.37)

# Picture 034 right Hal68 bottom box
crop_rajah(os.path.join(base, "Picture 034.jpg"), os.path.join(outdir, "rajah-hal-068-bottom-box.jpg"),
           x0=0.565, y0=0.52, x1=0.835, y1=0.78)

# Picture 034 left Hal69 - 4 lines numbers
crop_rajah(os.path.join(base, "Picture 034.jpg"), os.path.join(outdir, "rajah-hal-069-thilasm.jpg"),
           x0=0.20, y0=0.48, x1=0.475, y1=0.74)

# Picture 035 right Hal70 wafaq
crop_rajah(os.path.join(base, "Picture 035.jpg"), os.path.join(outdir, "rajah-hal-070-wafaq.jpg"),
           x0=0.605, y0=0.55, x1=0.875, y1=0.88)

# Picture 035 left Hal71 four squares
crop_rajah(os.path.join(base, "Picture 035.jpg"), os.path.join(outdir, "rajah-hal-071-four-squares.jpg"),
           x0=0.175, y0=0.17, x1=0.455, y1=0.35)

print("done batch14 crops")
