#!/usr/bin/env python3
from PIL import Image, ImageEnhance
import os, numpy as np
def crop_rajah(src_path, out_path, x0, y0, x1, y1):
    im = Image.open(src_path).convert("RGB")
    w,h = im.size
    box = (int(w*x0), int(h*y0), int(w*x1), int(h*y1))
    crop = im.crop(box)
    crop = ImageEnhance.Contrast(crop).enhance(1.6)
    crop = ImageEnhance.Brightness(crop).enhance(1.15)
    arr = np.array(crop)
    mask = (arr[:,:,0] > 188) & (arr[:,:,1] > 188) & (arr[:,:,2] > 188)
    arr[mask]=255
    crop = Image.fromarray(arr)
    crop = crop.resize((crop.size[0]*4, crop.size[1]*4), Image.LANCZOS)
    pad=70
    padded = Image.new("RGB", (crop.size[0]+pad*2, crop.size[1]+pad*2), (255,255,255))
    padded.paste(crop, (pad,pad))
    padded.save(out_path, "JPEG", quality=95, dpi=(300,300))
    print(f"{out_path} {padded.size} box {box}")

base="/home/user/asoro-wa-khofiyyat-fi-ilmu-ruhaniyyah"
outdir = base+"/terjemahan/assets"
# v3 tighter
crop_rajah(base+"/Picture 033.jpg", outdir+"/rajah-hal-067-top-thilasm.jpg", 0.095, 0.08, 0.46, 0.295)
crop_rajah(base+"/Picture 033.jpg", outdir+"/rajah-hal-067-bottom-numbers.jpg", 0.145, 0.56, 0.435, 0.64)
crop_rajah(base+"/Picture 034.jpg", outdir+"/rajah-hal-068-top-thilasm.jpg", 0.56, 0.062, 0.925, 0.285)
crop_rajah(base+"/Picture 034.jpg", outdir+"/rajah-hal-068-bottom-box.jpg", 0.575, 0.53, 0.818, 0.73)
crop_rajah(base+"/Picture 034.jpg", outdir+"/rajah-hal-069-thilasm.jpg", 0.225, 0.495, 0.455, 0.595)
crop_rajah(base+"/Picture 035.jpg", outdir+"/rajah-hal-070-wafaq.jpg", 0.63, 0.595, 0.855, 0.845)
crop_rajah(base+"/Picture 035.jpg", outdir+"/rajah-hal-071-four-squares.jpg", 0.188, 0.188, 0.442, 0.315)
print("v3 done")
