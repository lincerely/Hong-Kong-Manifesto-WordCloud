# coding: utf-8
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import operator


#config
mask_path = "./data/hk_mask.png"
data_path = "./data/Manifesto_words_E_revised.txt"
content_font_path = "./ttf/FiraSans-SemiBold.ttf"
title_font_path = "./ttf/FiraSans-SemiBold.ttf"

title = "Manifesto\nof\nCarrie\nLam"

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % (80 + font_size/3)


mask = np.array(Image.open(mask_path))
image_color = ImageColorGenerator(mask)
text = open(data_path).read()

#word cloud settings
wc = WordCloud(font_path=content_font_path)
wc.max_words = 500
wc.background_color= "#FFFFFF"
wc.min_font_size =7
wc.scale=5
wc.prefer_horizontal = 1
wc.mode='RGBA'
wc.mask = mask

#wc creation
wc = wc.generate(text)
default_colors = wc.to_array()
wc.recolor(color_func=image_color, random_state=3)

image = wc.to_image()

#add border
image_size = image.size
new_size = tuple(map(operator.add,image.size,(200,200)))
new_img = Image.new("RGB", new_size,"white")
pos = tuple(map(operator.sub,new_size,image_size)) 
pos = tuple(map(operator.div,pos,(2,2)))
new_img.paste(image, pos)
image = new_img

#create title block
draw = ImageDraw.Draw(image)
draw.polygon([(0,0),(0,1000),(1000,0)],fill=(38, 201, 128))
title_font = ImageFont.truetype(title_font_path, 120)
draw.text((100,100),title, (255, 255, 255), font=title_font)

image.show()
image.save("hk_wc.png")
