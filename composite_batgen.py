# Composites the app's battery-test screen onto the phone in the generated cover photo,
# keeping the finger (skin + fingernail) on top. Writes assets/cover_batgen_comp.jpg.
import cv2, numpy as np
im = cv2.imread('assets/cover_batgen_photo.png').astype(np.float32)
m = cv2.imread('assets/cover_batgen_screenmask.png', 0)          # the white screen area of the photo
q = np.float32([[237.76, 923.70], [803.45, 893.30], [1183.45, 2109.68], [680.55, 2297.72]])  # screen corners (lines fitted to the mask)
scr = cv2.imread('assets/screen_battery_ok.png').astype(np.float32)
M = cv2.getPerspectiveTransform(np.float32([[0, 0], [1080, 0], [1080, 2400], [0, 2400]]), q)
H, W = im.shape[:2]
ws = cv2.warpPerspective(cv2.GaussianBlur(scr, (0, 0), 0.7), M, (W, H), flags=cv2.INTER_LANCZOS4)
hsv = cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_BGR2HSV)
skin = (((hsv[..., 0] < 22) | (hsv[..., 0] > 165)) & (hsv[..., 1] > 40)).astype(np.uint8) * 255
skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
zone = np.zeros_like(m); cv2.ellipse(zone, (758, 1488), (80, 42), 12, 0, 360, 255, -1)
nail = cv2.bitwise_and(zone, ((hsv[..., 1] > 12) | (hsv[..., 2] < 235)).astype(np.uint8) * 255)
a = cv2.bitwise_and(cv2.erode(m, np.ones((3, 3), np.uint8)), 255 - cv2.bitwise_or(skin, nail))
a = cv2.GaussianBlur(a, (0, 0), 0.9).astype(np.float32)[..., None] / 255
yy = np.mgrid[0:H, 0:W][0]; ws *= (0.97 - 0.06 * np.clip((yy - 900) / 1400, 0, 1))[..., None]
cv2.imwrite('assets/cover_batgen_comp.jpg', np.clip(im * (1 - a) + ws * a, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 95])
