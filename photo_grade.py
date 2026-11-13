import cv2, numpy as np, sys
src, out = sys.argv[1], sys.argv[2]
im = cv2.imread(src)[6:1476]                      # drop burnt-in caption
im = cv2.fastNlMeansDenoisingColored(im, None, 4, 5, 7, 21)
f = im.astype(np.float32)/255
# white balance: phone screen should read white (80% correction)
ref = np.array([165, 193, 203], np.float32)
g = ref.mean()/ref; g = 1 + 0.8*(g-1)
f = np.clip(f*g, 0, 1)
s = 1920/f.shape[0]
f = cv2.resize(f, (round(f.shape[1]*s), 1920), interpolation=cv2.INTER_LANCZOS4)
x0 = 55; f = np.clip(f[:, x0:x0+1080], 0, 1)
# luminance levels (same for all channels -> no colour shift)
lum = f @ np.array([0.114, 0.587, 0.299], np.float32)
lo, hi = np.percentile(lum, 0.5), np.percentile(lum, 99.6)
f = np.clip((f-lo)/(hi-lo), 0, 1)
# gentle clarity
lab = cv2.cvtColor((f*255).astype(np.uint8), cv2.COLOR_BGR2LAB)
lab[..., 0] = cv2.createCLAHE(clipLimit=1.15, tileGridSize=(6, 6)).apply(lab[..., 0])
f = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR).astype(np.float32)/255
# soft S-curve
f = f*f*(3-2*f)*0.4 + f*0.6
# cool steel shadows (subtle)
lum = f.mean(axis=2, keepdims=True)
f = f + ((1-lum)**3)*np.array([0.025, 0.008, -0.012], np.float32)
# saturation: overall slightly restrained, product UI blue richer
hsv = cv2.cvtColor((np.clip(f,0,1)*255).astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
h = hsv[..., 0]; blue = ((h > 100) & (h < 120) & (hsv[...,1] > 120)).astype(np.float32)
blue = cv2.GaussianBlur(blue, (0,0), 2)
hsv[..., 1] *= 0.92 + 0.15*blue
f = cv2.cvtColor(np.clip(hsv,0,255).astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)/255
# restrained sharpening
blur = cv2.GaussianBlur(f, (0, 0), 1.2)
f = np.clip(f + 0.55*(f-blur), 0, 1)
# vignette
yy, xx = np.mgrid[0:1920, 0:1080]
d = np.sqrt(((xx-580)/720)**2 + ((yy-1150)/1150)**2)
f *= (1 - 0.35*np.clip(d-0.5, 0, 1)**1.4)[..., None]
cv2.imwrite(out, (f*255+0.5).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 96])
