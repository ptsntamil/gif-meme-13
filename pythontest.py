from PIL import Image
from PIL import ImageDraw, ImageSequence
from PIL import ImageFont
import io
#Open the desired Image you want to add text on
im = Image.open("./giphy_1.gif")
x,y = im.size
frames = []
index = 0
# Loop over each frame in the animated image
for frame in ImageSequence.Iterator(im):
    # Draw the text on the frame
    d = ImageDraw.Draw(frame)
    fnt = ImageFont.truetype("./freedom-font/Freedom-10eM.ttf", size=15)
    d.text((x-80, y-15), "Postaba", fill="white", font=fnt)
    del d

    # However, 'frame' is still the animated image with many frames
    # It has simply been seeked to a later frame
    # For our list of frames, we only want the current frame

    # Saving the image without 'save_all' will turn it into a single frame image, and we can then re-open it
    # To be efficient, we will save it to a stream, rather than to file
    b = io.BytesIO()
    frame.save(b, format="GIF")
    frame = Image.open(b)
    # frame.convert("RGB").save("out"+str(index)+".jpg")
    # index = index+1
    # Then append the single frame image to a list of frames
    frames.append(frame)
# Save the frames as a new image
frames[0].save('out.gif', save_all=True, append_images=frames[1:])


# # from PIL import Image
#import images2gif as i2g
# # images = i2g.readGif("./SampleGIFImage_40kbmb.gif", False)
# # watermark = Image.open("Watermark.gif")
# # for i in images: i.paste(watermark, (1, 1))

# # i2g.writeGif('Out.gif', images, 0.5) # You may wish to play with the timing, etc.
# # exit()

#from  images2gif import readGif, writeGif
# frames = i2g.readGif("./SampleGIFImage_40kbmb.gif",False)
# for frame in frames:
#     frame.thumbnail((100,100), Image.ANTIALIAS)
# i2g.writeGif('rose99.gif', frames)