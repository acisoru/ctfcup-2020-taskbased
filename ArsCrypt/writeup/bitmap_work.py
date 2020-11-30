from PIL import Image, ImageFont
import io
counter = 0

def image_to_bitmap(text="", imagepath=""):
    if text:
        mode="text"
    else:
        mode="image"

    if mode == "text":
        img = Image.new('L', (300, 100), color=0)
        img_w, img_h = img.size
        font = ImageFont.truetype("courbi.ttf", 48)
        mask = font.getmask(text, mode='L')
        mask_w, mask_h = mask.size
        print(mask_w, mask_h)
        print(type(mask))
        d = Image.core.draw(img.im, 0)
        d.draw_bitmap(((img_w - mask_w)/2, (img_h - mask_h)/2), mask, 255)
    else:
        img = Image.open(imagepath)

        # Provide the target width and height of the image
        (width, height) = (300, 100)
        img = img.resize((width, height))

    #img.show()
    rgb_im = img.convert('RGB')

    bits = []
    for y in range(100):
        for x in range(300):
            r, g, b = rgb_im.getpixel((x, y))

            if mode=="text":
                bits.append(r)
            else:
                bits.append((r+g+b)//3)
    #print("#test image")
    #print(len(bits))
    #bf_memory_to_image(bits)
    #print("# test image done")
    return bits

def bf_memory_to_image(bf_memory):
    global counter
    #print(bf_memory)
    img = Image.new('L', (300, 100), color=0)
    for y in range(100):
        for x in range(300):
            if (x+y*300 in bf_memory and isinstance(bf_memory, dict)) or isinstance(bf_memory, list):
                img.putpixel((x, y), (bf_memory[x+y*300]))
                #img.putpixel((x, y), (0,0,0))

    img.show()
    img.save(f"Last_image_{counter}.png")
    counter+=1

if __name__ == "__main__":
    image_to_bitmap(text="T")
    image_to_bitmap(imagepath="unnamed.png")