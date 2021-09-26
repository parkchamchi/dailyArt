#Format image as a single page with description

from PIL import Image, ImageFont, ImageDraw
import urllib.request

def formatArt(art):
	filename = "img.jpg"
	pagesize = (2480, 3508)
	margin = 0.05
	textboxsize = 0.1

	#Get the image from URL...
	urllib.request.urlretrieve(art["primaryImage"], filename)
	img = Image.open(filename)

	#resize it
	if (img.height / img.width < pagesize[1]  * (1 - 2*margin - textboxsize) / (pagesize[0] * (1 - 2*margin))): #if normal size
		imgwidth = int(pagesize[0] * (1 - 2*margin))
		imgheight = int(imgwidth * (img.height / img.width))
	else: #vertically long
		imgheight = int(pagesize[1] * (1 - 2*margin - textboxsize))
		imgwidth = int(imgheight * (img.width / img.height))

	img = img.resize((imgwidth, imgheight), Image.LANCZOS)

	#Make the page to print...
	page = Image.new("CMYK", pagesize, 1)
	
	#Paste the image...
	topleftcorner = int(pagesize[0] * margin) #where the image would be located
	page.paste(img, (topleftcorner, topleftcorner))

	#Paste the text...
	font = ImageFont.truetype("font/NotoSans/NotoSans-Regular.ttf", size = 50) #the font
	draw = ImageDraw.Draw(page) #the drawing context

	text = getText(art, font, int(pagesize[0] / font.getlength("n"))) #the text to put

	draw.text((topleftcorner, topleftcorner*2 + imgheight), text, font = font) #Draw the text
	page.save(filename, "JPEG")

	return filename

#textline_px: the width of a line of the text in pixels
#version without ImageFont.ImageFont.getlength()
def getText(art, font, linelen):
	pri = [
		"title", "artistDisplayName"
	]
	sec = [
		"medium", "dimensions",
		"objectDate", "period", "artistDisplayBio",
		"objectID", "isHighlight", "culture"
	]

	#primary
	text = ""
	text += art[pri[0]] + ", " + art[pri[1]] + "\n\n"

	#check if it fits...
	if (len(text) > linelen): #if it doesn't...
		text = art[pri[0]] + ",\n" + art[pri[1]] + "\n\n" #add newline

	#secondary
	cur_line_keys = [] #keys to be put on one line
	cur_line_len = 0
	for key in sec:
		if art[key] == "":
			continue

		new_str = key + ": " + str(art[key]) + ", " #the string of the current key

		if cur_line_len + len(new_str) < linelen: #if it fits
			cur_line_len += len(new_str)
			cur_line_keys.append(key)
		else:
			#make a line
			for key2put in cur_line_keys:
				text += key2put + ": " + str(art[key2put]) + ", "
			text += "\n"
			
			cur_line_px = 0
			cur_line_keys = [key]
	#put the rest
	for key2put in cur_line_keys:
		text += key2put + ": " + str(art[key2put]) + ", "
	text = text[:-2]

	return text