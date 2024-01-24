from PIL import Image, ImageSequence

GIF_PATH = "./giphy_1.gif"
IMAGE_PATH = "./logo.png"

gif = Image.open(GIF_PATH)
gifname = gif.filename.split("/")[-1]
print(gifname)
image = Image.open(IMAGE_PATH).resize((70,20))
x,y = gif.size
ix,iy = image.size
frames = [f.copy() for f in ImageSequence.Iterator(gif)]

for i, frame in enumerate(frames):
    frame = frame.convert("RGBA")

    frame.paste(image, (x-ix-10,y-iy), image)
    frames[i] = frame

frames[0].save('watermark_' + gifname, save_all=True, append_images=frames[1:])