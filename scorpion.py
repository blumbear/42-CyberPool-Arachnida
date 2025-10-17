from PIL import Image
import exifread
import os

def extract_data(imagePath):

	useless_data = [
		'JPEGThumbnail'
	]

	interesting_tags = [
	# Géolocalisation (critiques)
	'GPS GPSLatitude',
	'GPS GPSLongitude', 
	'GPS GPSAltitude',
	'GPS GPSDate',
	'GPS GPSTimeStamp',
	'GPS GPSLatitudeRef',
	'GPS GPSLongitudeRef',
	'GPS GPSAltitudeRef',

	# Informations sur l'appareil
	'Image Model',
	'Image Software',
	'Image HostComputer',
	'EXIF LensMake',
	'EXIF LensModel',

	# Métadonnées temporelles
	'Image DateTime',
	'EXIF DateTimeOriginal',
	'EXIF DateTimeDigitized',

	# Paramètres de prise de vue
	'EXIF ExposureTime',
	'EXIF FNumber',
	'EXIF ISOSpeedRatings',
	'EXIF FocalLength',
	'EXIF Flash',
			
	# Informations techniques
	'Image XResolution',
	'Image YResolution',
	'EXIF ComponentsConfiguration'
	'EXIF ExifImageWidth',
	'EXIF ExifImageLength',
	'EXIF ColorSpace'
	]

	with Image.open(imagePath) as img:
		print("\nMétadonnées de l'image :")
		print(f" - Format : {img.format}")
		print(f" - Mode : {img.mode}")
		print(f" - Taille : {img.size}")
		print(f" - Palette : {img.palette}")
		# print(f" - Infos supplémentaires : {img.info}")
	print()
	with open(imagePath, "rb") as image:
		tags = exifread.process_file(image)
		for tag, value in tags.items():
			if tag in interesting_tags:
			# if tag not in useless_data:
				print(f"Key: {tag} => {value}")

def file_lister(folder):
	return os.listdir(folder)

# def extract_data_from_folder(foldername):
# 	files = file_lister(foldername)
# 	for image in files:
# 		if 
extract_data("image/IMG_4325.JPG")