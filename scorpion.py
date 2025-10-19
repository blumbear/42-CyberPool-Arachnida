from PIL import Image
import exifread
import os
import argparse

def format_gps_coordinates(lat_data, lat_ref, lon_data, lon_ref):
	"""Convertit les coordonnées DMS en format lisible"""
		
	lat_degrees = float(lat_data.values[0])
	lat_minutes = float(lat_data.values[1])
		
	if '/' in str(lat_data.values[2]):
		parts = str(lat_data.values[2]).split('/')
		lat_seconds = float(parts[0]) / float(parts[1])
	else:
		lat_seconds = float(lat_data.values[2])

	lat_decimal = lat_degrees + lat_minutes/60 + lat_seconds/3600
	if lat_ref == 'S':
		lat_decimal = -lat_decimal
		
	# Convertir longitude DMS vers décimales  
	lon_degrees = float(lon_data.values[0])
	lon_minutes = float(lon_data.values[1])

	if '/' in str(lon_data.values[2]):
		parts = str(lon_data.values[2]).split('/')
		lon_seconds = float(parts[0]) / float(parts[1])
	else:
		lon_seconds = float(lon_data.values[2])

	lon_decimal = lon_degrees + lon_minutes/60 + lon_seconds/3600
	if lon_ref == 'W':
		lon_decimal = -lon_decimal
		
	return lat_decimal, lon_decimal

def format_gps_data(tags):
	"""Formate les données GPS de manière lisible"""
		
	gps_lat = None
	gps_lon = None
	gps_lat_ref = None
	gps_lon_ref = None
	gps_alt = None
	gps_time = None
	gps_date = None
		
	# Extraire les données GPS
	for tag, value in tags.items():
		if 'GPS GPSLatitude' == tag and 'Ref' not in tag:
			gps_lat = value
		elif 'GPS GPSLatitudeRef' == tag:
			gps_lat_ref = str(value)
		elif 'GPS GPSLongitude' == tag and 'Ref' not in tag:
			gps_lon = value
		elif 'GPS GPSLongitudeRef' == tag:
			gps_lon_ref = str(value)
		elif 'GPS GPSAltitude' == tag and 'Ref' not in tag:
			try:
				gps_alt = float(value)
			except (ValueError, TypeError):
				if '/' in str(value):
					parts = str(value).split('/')
					gps_alt = float(parts[0]) / float(parts[1])
				else:
					gps_alt = None
		elif 'GPS GPSTimeStamp' == tag:
			gps_time = value
		elif 'GPS GPSDate' == tag:
			gps_date = str(value)
		
	# Formater l'affichage
	if gps_lat and gps_lon and gps_lat_ref and gps_lon_ref:
		lat_decimal, lon_decimal = format_gps_coordinates(gps_lat, gps_lat_ref, gps_lon, gps_lon_ref)

		print(f"\n\033[1;31m🌍 GÉOLOCALISATION (Format):\033[0m")
		print(f" • \033[1;91mPosition GPS\033[0m: \033[93m{lat_decimal:.6f}°{gps_lat_ref}, {lon_decimal:.6f}°{gps_lon_ref}\033[0m")

		lat_sec = float(str(gps_lat.values[2]).split('/')[0]) / float(str(gps_lat.values[2]).split('/')[1]) if '/' in str(gps_lat.values[2]) else float(gps_lat.values[2])
		lon_sec = float(str(gps_lon.values[2]).split('/')[0]) / float(str(gps_lon.values[2]).split('/')[1]) if '/' in str(gps_lon.values[2]) else float(gps_lon.values[2])
	
		print(f" • \033[1;91mCoordonnées DMS\033[0m: \033[93m{gps_lat.values[0]}°{gps_lat.values[1]}'{lat_sec:.1f}\"{gps_lat_ref}, {gps_lon.values[0]}°{gps_lon.values[1]}'{lon_sec:.1f}\"{gps_lon_ref}\033[0m")
		
		if gps_alt:
			print(f" • \033[1;91mAltitude\033[0m: \033[93m{gps_alt:.1f}m\033[0m")
		
		if gps_date and gps_time:
			time_str = f"{int(gps_time.values[0]):02d}:{int(gps_time.values[1]):02d}:{int(gps_time.values[2]):02d}"
			print(f" • \033[1;91mDate/Heure GPS\033[0m: \033[93m{gps_date} {time_str}\033[0m")
		
		# Lien Google Maps
		maps_url = f"https://www.google.com/maps?q={lat_decimal},{lon_decimal}"
		return (maps_url)
	else:
		print(f"\n\033[1;31m🌍 GÉOLOCALISATION:\033[0m")
		print(f" • \033[1;91mDonnées GPS incomplètes\033[0m")
		return None


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
	'EXIF ComponentsConfiguration',
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
			format_gps_data(tags)  # Passer le dictionnaire tags, pas gps_tags
		else:
			print(f"\n\033[1;31m🌍 GÉOLOCALISATION:\033[0m")
			print(f" • \033[1;91mAucune donnée GPS trouvée\033[0m")

		if gps_tags:
			print(f"\n\033[1;31m🌍 GÉOLOCALISATION (Not Format):\033[0m")
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
	supported_formats = [
		".jpg",
		".jpeg",
		".png",
		".gif",
		".bmp",
	]
	files = file_lister(foldername)
	for image in files:
		if any(image.lower().endswith(fmt) for fmt in supported_formats):
			extract_data(foldername + image)

def main():
	parser = argparse.ArgumentParser(description='Scorpion - EXIF Metadata Extractor')

	parser.add_argument('-p', '--path',
					type=str,
					default='./data/',
					help='Indicate the path where the scorpion will find the images'
				)

	parser.add_argument('-a', '--anonimize',
					action='store_true',
					help='Allow the scorpion to delete the EXIF data'
				)

	args = parser.parse_args()

	extract_data_from_folder(args.path)

if __name__ == "__main__":
	main()