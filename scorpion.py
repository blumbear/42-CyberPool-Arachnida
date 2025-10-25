from PIL import Image
import exif
import os
import argparse
import subprocess

def format_gps_coordinates(lat_data, lat_ref, lon_data, lon_ref):
	"""Convertit les coordonnées DMS en format lisible"""
		
	lat_degrees = lat_data[0]
	lat_minutes = lat_data[1]
	lat_seconds = lat_data[2]

	lat_decimal = lat_degrees + lat_minutes/60 + lat_seconds/3600
	if lat_ref == 'S':
		lat_decimal = -lat_decimal
		
	# Convertir longitude DMS vers décimales  
	lon_degrees = lon_data[0]
	lon_minutes = lon_data[1]
	lon_seconds = lon_data[2]

	lon_decimal = lon_degrees + lon_minutes/60 + lon_seconds/3600
	if lon_ref == 'W':
		lon_decimal = -lon_decimal
		
	return lat_decimal, lon_decimal

def format_gps_data(gps_tags):
	"""Formate les données GPS de manière lisible"""

	gps_lat = None,
	gps_lon = None,
	gps_lat_ref = None,
	gps_lon_ref = None,
	gps_alt = None,
	gps_time = None,
	gps_date = None
		
	# Extraire les données GPS
	for tag in gps_tags:
		if tag[0] == 'gps_latitude' and 'ref' not in tag[0]:
			gps_lat = tag[1]
		elif tag[0] == 'gps_latitude_ref':
			gps_lat_ref = str(tag[1])
		elif tag[0] == 'gps_longitude' and 'ref' not in tag[0]:
			gps_lon = tag[1]
		elif tag[0] == 'gps_longitude_ref':
			gps_lon_ref = str(tag[1])
		elif tag[0] == 'gps_altitude' and 'ref' not in tag[0]:
			try:
				gps_alt = float(tag[1])
			except (ValueError, TypeError):
				if '/' in str(tag[1]):
					parts = str(tag[1]).split('/')
					gps_alt = float(parts[0]) / float(parts[1])
				else:
					gps_alt = None
		elif tag[0] == 'gps_timestamp':
			gps_time = tag[1]
		elif tag[0] == 'gps_datestamp':
			gps_date = str(tag[1])
		
	# Formater l'affichage
	if gps_lat and gps_lon and gps_lat_ref and gps_lon_ref:
		lat_decimal, lon_decimal = format_gps_coordinates(gps_lat, gps_lat_ref, gps_lon, gps_lon_ref)

		print(f"\n\033[1;31m🌍 GÉOLOCALISATION (Format):\033[0m")
		print(f" • \033[1;91mPosition GPS\033[0m: \033[93m{lat_decimal:.6f}°{gps_lat_ref}, {lon_decimal:.6f}°{gps_lon_ref}\033[0m")

		lat_sec = gps_lat[2]
		lon_sec = gps_lon[2]
	
		print(f" • \033[1;91mCoordonnées DMS\033[0m: \033[93m{gps_lat[0]}°{gps_lat[1]}'{lat_sec:.1f}\"{gps_lat_ref}, {gps_lon[0]}°{gps_lon[1]}'{lon_sec:.1f}\"{gps_lon_ref}\033[0m")
		
		if gps_alt:
			print(f" • \033[1;91mAltitude\033[0m: \033[93m{gps_alt:.1f}m\033[0m")
		
		if gps_date and gps_time:
			time_str = f"{int(gps_time[0]):02d}:{int(gps_time[1]):02d}:{int(gps_time[2]):02d}"
			print(f" • \033[1;91mDate/Heure GPS\033[0m: \033[93m{gps_date} {time_str}\033[0m")
		
		# Lien Google Maps
		maps_url = f"https://www.google.com/maps?q={lat_decimal},{lon_decimal}"
		print(f" • \033[1;91mGoogle Maps\033[0m: \033[94m{maps_url}\033[0m")
		return (None)
	else:
		print(f"\n\033[1;31m🌍 GÉOLOCALISATION:\033[0m")
		print(f" • \033[1;91mDonnées GPS incomplètes\033[0m")
		return None

def handle_error(error):
	if 'UnicodeDecodeError occurred during unpack operation' in error:
		return 'UnicodeDecodeError occurred during unpack operation'
	return None

def extract_data(imagePath):

	categories = {
		'device_info': [
			'make',
			'model', 
			'lens_make',
			'lens_model',
			'lens_specification',
			'software',
			'maker_note'
		],
			
		'datetime_info': [
			'datetime',
			'datetime_original',
			'datetime_digitized',
			'offset_time',
			'offset_time_original',
			'offset_time_digitized',
			'subsec_time_original',
			'subsec_time_digitized'
		],

		'camera_settings': [
			'f_number',
			'aperture_value',
			'exposure_time',
			'shutter_speed_value',
			'photographic_sensitivity',
			'exposure_bias_value',
			'exposure_mode',
			'exposure_program',
			'flash',
			'focal_length',
			'focal_length_in_35mm_film',
			'white_balance',
			'metering_mode',
			'scene_capture_type',
			'scene_type',
			'brightness_value'
		],
		
		'image_specs': [
			'pixel_x_dimension',
			'pixel_y_dimension',
			'x_resolution',
			'y_resolution',
			'resolution_unit',
			'orientation',
			'color_space',
			'components_configuration',
			'compression'
		],

		'technical_metadata': [
			'exif_version',
			'flashpix_version',
			'sensing_method',
			'subject_area',
			'y_and_c_positioning',
			'jpeg_interchange_format',
			'jpeg_interchange_format_length',
			'_exif_ifd_pointer'
		],

		'gps_info': [
			'gps_latitude',
			'gps_latitude_ref',
			'gps_longitude',
			'gps_longitude_ref',
			'gps_altitude',
			'gps_altitude_ref',
			'gps_timestamp',
			'gps_datestamp',
			'gps_speed',
			'gps_speed_ref',
			'gps_img_direction',
			'gps_img_direction_ref',
			'gps_dest_bearing',
			'gps_dest_bearing_ref',
			'gps_horizontal_positioning_error',
			'_gps_ifd_pointer'
		]
	}

	with Image.open(imagePath) as img:
		print(f"\n\033[1;35m{'='*60}\033[0m")
		print(f"\033[1;33m📷 IMAGE: {imagePath}\033[0m")
		print(f"\033[1;35m{'='*60}\033[0m")

		print(f"\n\033[1;36m📋 MÉTADONNÉES DE BASE:\033[0m")
		print(f" • \033[1;32mFormat\033[0m: \033[37m{img.format}\033[0m")
		print(f" • \033[1;32mMode\033[0m: \033[37m{img.mode}\033[0m")
		print(f" • \033[1;32mTaille\033[0m: \033[37m{img.size}\033[0m")
		print(f" • \033[1;32mPalette\033[0m: \033[37m{img.palette}\033[0m")

	with open(imagePath, "rb") as img:
		try:
			image = exif.Image(img)
			list_all = sorted(image.list_all())
			gps_tags = []
			device_tags = []
			time_tags = []
			camera_tags = []
			tech_tags = []
		
			for tag in list_all:
				try:
					value = image.get(tag)
				except Exception as e:
					value = f"<error reading tag: {tag}>"

				if tag in categories['gps_info']:
					gps_tags.append((tag, value))
				elif tag in categories['device_info']:
					device_tags.append((tag, value))
				elif tag in categories['datetime_info']:
					time_tags.append((tag, value))
				elif tag in categories['camera_settings']:
					camera_tags.append((tag, value))
				else:
					tech_tags.append((tag, value))

			if gps_tags:
				format_gps_data(gps_tags)  # Passer le dictionnaire tags, pas gps_tags
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
		except Exception as e:
			print(f"\n\033[1;31m❌ ERREUR LECTURE EXIF:\033[0m")
			print(f" • \033[1;91mImpossible de lire les données EXIF de cette image\033[0m")
			print(f" • \033[1;91mErreur\033[0m: \033[93m{str(e)}\033[0m")
			print(f" • \033[1;91mFormat potentiellement corrompu ou non supporté\033[0m")
			
			try:
				from PIL.ExifTags import TAGS
				with Image.open(imagePath) as img:
					exifdata = img.getexif()
					if exifdata:
						print(f"\n\033[1;33m📋 MÉTADONNÉES PIL (limitées):\033[0m")
						for tag_id in exifdata:
							tag = TAGS.get(tag_id, tag_id)
							data = exifdata.get(tag_id)
							print(f" • \033[1;93m{tag}\033[0m: \033[37m{data}\033[0m")
					else:
						print(f" • \033[1;91mAucune donnée EXIF trouvée avec PIL\033[0m")
			except Exception as pil_error:
				print(f" • \033[1;91mÉchec avec PIL également\033[0m: {pil_error}")

def file_lister(folder):
	return os.listdir(folder)

def delete_exif_data(imagePath, replace):
	try:
		base_name = os.path.splitext(imagePath)[0]
		extension = os.path.splitext(imagePath)[1]
		if replace:
			outputPath = f"{base_name}{extension}"
		else:
			outputPath = f"{base_name}_anonymized{extension}"

		if outputPath != imagePath:
			subprocess.run(['cp', imagePath, outputPath], check=True)

		result = subprocess.run([
			'exiftool',
			'-all=',
			'-overwrite_original',
			outputPath
		], capture_output=True, text=True)

		if result.returncode == 0:
			print(f"Anonymized image saved: {outputPath}")
		else:
			print(f"Exiftool error: {result.stderr}")

	except subprocess.CalledProcessError as e:
		print(f"Error during anonymization: {e}")
	except FileNotFoundError:
		print("exiftool is not installed. Install it with: sudo apt install libimage-exiftool-perl")

def extract_data_from_folder(foldername, anonimize, replace_anonimize):
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
			if (anonimize):
				delete_exif_data(foldername + image, False)
			elif (replace_anonimize):
				delete_exif_data(foldername + image, replace_anonimize)


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
	
	parser.add_argument('-ra', '--replace-anonimize',
					action='store_true',
					help='Allow the scorpion to delete the EXIF data'
				)

	args = parser.parse_args()

	extract_data_from_folder(args.path, args.anonimize, args.replace_anonimize)

if __name__ == "__main__":
	main()
