import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
im=np.asarray(Image.open('/tmp/claude-0/-home-user-motion/d86c8453-9a2c-569b-bc2b-fa9f9db94074/images/1.webp').convert('RGB')).astype(float)
L=im.mean(2)
# phone: dark bezel component + holes
dark=L<90
lab,n=ndimage.label(dark)
sizes=ndimage.sum(dark,lab,range(1,n+1))
bez=lab==(np.argmax(sizes)+1)
phone=ndimage.binary_fill_holes(ndimage.binary_closing(bez,iterations=3))
m=Image.new('L',(1200,1200),0);d=ImageDraw.Draw(m)
d.polygon([(668,800),(690,772),(735,740),(1060,722),(1125,756),(1146,795),(1150,975),(1120,992),(1050,1008),(900,1044),(780,1072),(700,1032),(672,1000)],fill=255)
diag=np.asarray(m)>0
# refine diag top/sides: drop pure-white pixels connected to outside
lab2,_=ndimage.label(L>=251)
b2=set(np.unique(np.r_[lab2[0],lab2[-1],lab2[:,0],lab2[:,-1]]))-{0}
diag&=~np.isin(lab2,list(b2))
diag=ndimage.binary_closing(ndimage.binary_opening(diag,iterations=4),iterations=8)
diag=ndimage.binary_fill_holes(diag)
obj=phone|diag
objf=ndimage.gaussian_filter(obj.astype(float),0.7)
sh=np.clip((250-L)/250,0,1)*0.9
a=np.maximum(objf,np.where(obj,1,sh))
rgb=np.where(obj[...,None],im,np.array([20,40,80.]))
# blend edge colors
rgb=np.where((objf>0.02)[...,None]&~obj[...,None],im*objf[...,None]+np.array([20,40,80.])*(1-objf[...,None]),rgb)
Image.fromarray(np.dstack([rgb,a*255]).clip(0,255).astype(np.uint8),'RGBA').save('prod.png')
