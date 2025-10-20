import argparse
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

def init_dir(res_dir):
	if not os.path.exists(res_dir):
		os.makedirs(res_dir)

def download_image(img_url, save_path):
	try:
		response = requests.get(img_url, stream=True)
		if response.status_code == 200:
			with open(save_path, 'wb') as f:
				for chunk in response.iter_content(1024):
					f.write(chunk)
			print(f"✅ Downloaded: {img_url}")
			return True
		else:
			print(f"❌ Failed ({response.status_code}): {img_url}")
			return False
	except requests.exceptions.Timeout:
		print(f"⏱️ Timeout: {img_url}")
	except requests.exceptions.ConnectionError:
		print(f"🔌 Connection error: {img_url}")
	except Exception as e:
		print(f"💥 Error downloading {img_url}: {e}")
	return False

def scrape_url(url, save_dir, recursive, length, domain):

	supported_formats = [
	".jpg",
	".jpeg",
	".png",
	".gif",
	".bmp",
	]

	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'html.parser')

	images = soup.find_all('img')

	for img in images:
		img_url = img.get('src') or img.get('data-src')
		if (img_url):
			full_url = urljoin(url, img_url)

		if any(full_url.lower().endswith(fmt) for fmt in supported_formats):
			filename = os.path.basename(urlparse(full_url).path)
			if not filename:
				filename = f"iamge_{hash(full_url)}.jpg"

			save_path = os.path.join(save_dir, filename)
			print(f"Downloading: {full_url}")
			download_image(full_url, save_path)
	
	if recursive and length > 0:
		links = soup.find_all('a', href=True)
		for link in links:
			link = urljoin(url, link['href'])
			if urlparse(link).netloc == urlparse(url).netloc or domain == True:
				scrape_url(link, save_dir, recursive, length - 1, domain)


def main():
	parser = argparse.ArgumentParser(description="Spider - Web image scraper")

	parser.add_argument('-r', '--recursive',
						action='store_true',
						help='Enable recursive download'
					)

	parser.add_argument('-l', '--length',
						type=int,
						default=5,
						help='Maximum depth level for recursive download (default: 5)'
					)

	parser.add_argument('-p', '--path',
						type=str,
						default='data/',
						help='Indicate the path where the download files will be saved'
					)
	
	parser.add_argument('-d', '--domain',
						type=str,
						default=False,
						help="Ask to the spider stay to on the same domain"
					)

	parser.add_argument('url',
						help='URL to scrape for image'
					)

	args = parser.parse_args()

	init_dir(args.path)

	print(f"URL à scraper: {args.url}")
	print(f"Dossier de destination: {args.path}")
	print(f"Mode récursif: {args.recursive}")
	print(f"Profondeur max: {args.length}")
	print(f"domain: {args.domain}")

	scrape_url(args.url, args.path, args.recursive, args.length, args.domain)

if __name__ == "__main__":
	main()