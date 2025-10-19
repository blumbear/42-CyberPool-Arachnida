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
		print(f"\n\033[1;35m{'='*60}\033[0m")
		print(f"\033[1;33m📷 IMAGE: {imagePath}\033[0m")
		print(f"\033[1;35m{'='*60}\033[0m")

		print(f"\n\033[1;36m📋 MÉTADONNÉES DE BASE:\033[0m")
		print(f" • \033[1;32mFormat\033[0m: \033[37m{img.format}\033[0m")
		print(f" • \033[1;32mMode\033[0m: \033[37m{img.mode}\033[0m")
		print(f" • \033[1;32mTaille\033[0m: \033[37m{img.size}\033[0m")
		print(f" • \033[1;32mPalette\033[0m: \033[37m{img.palette}\033[0m")
	with open(imagePath, "rb") as image:
		tags = exifread.process_file(image)
		gps_tags = []
		device_tags = []
		time_tags = []
		camera_tags = []
		tech_tags = []
	
		for tag, value in tags.items():
			if tag in interesting_tags:
				if 'GPS' in tag:
					gps_tags.append((tag, value))
				elif 'Model' in tag or 'Software' in tag or 'Host' in tag or 'Lens' in tag:
					device_tags.append((tag, value))
				elif 'DateTime' in tag or 'Date' in tag or 'Time' in tag:
					time_tags.append((tag, value))
				elif 'Exposure' in tag or 'FNumber' in tag or 'ISO' in tag or 'Flash' in tag or 'Focal' in tag:
					camera_tags.append((tag, value))
				else:
					tech_tags.append((tag, value))

		if gps_tags:
			print(f"\n\033[1;31m🌍 GÉOLOCALISATION (SENSIBLE):\033[0m")
			for tag, value in gps_tags:
				print(f" • \033[1;91m{tag}\033[0m: \033[93m{value}\033[0m")
		
		if device_tags:
			print(f"\n\033[1;34m📱 INFORMATIONS APPAREIL:\033[0m")
			for tag, value in device_tags:
				print(f" • \033[1;94m{tag}\033[0m: \033[96m{value}\033[0m")
		
		if time_tags:
			print(f"\n\033[1;35m⏰ MÉTADONNÉES TEMPORELLES:\033[0m")
			for tag, value in time_tags:
				print(f" • \033[1;95m{tag}\033[0m: \033[97m{value}\033[0m")
		
		if camera_tags:
			print(f"\n\033[1;32m📸 PARAMÈTRES DE PRISE DE VUE:\033[0m")
			for tag, value in camera_tags:
				print(f" • \033[1;92m{tag}\033[0m: \033[37m{value}\033[0m")
		
		if tech_tags:
			print(f"\n\033[1;36m⚙️  INFORMATIONS TECHNIQUES:\033[0m")
			for tag, value in tech_tags:
				print(f" • \033[1;96m{tag}\033[0m: \033[37m{value}\033[0m")

def file_lister(folder):
	return os.listdir(folder)

def extract_data_from_folder(foldername):
	supported_format = [
		".JPG",
		".jpg",
		".PNG",
		".png",
		".gif",
		".bmp",
	]
	files = file_lister(foldername)
	for image in files:
		if image[-4:] in supported_format:
			extract_data(foldername + image)

extract_data_from_folder("./data/")