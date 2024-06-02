import PIL.Image
im1 = PIL.Image.open("1.jpg").convert("RGB")
im2 = PIL.Image.open("2.jpg").convert("RGB")
im3 = PIL.Image.open("3.jpg").convert("RGB")
images = [im1,im2,im3]
images[0].save("out.pdf", save_all=True, append_images=images[1:])
