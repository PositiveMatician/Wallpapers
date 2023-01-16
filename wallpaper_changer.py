



def wallpaper_changer(dest_folder='/home/positive/.local/share/backgrounds',time_interval=100):
	#images should be in jpg format
	import os 
	import time
	dest_folder = '/home/positive/Wallpapers'
	images = os.listdir(dest_folder)
	for image in images:
		os.system(f'gsettings set org.gnome.desktop.background picture-uri-dark \'file://{dest_folder}/{image}\'')
		print('hola',image)
		time.sleep(time_interval)

if __name__ == '__main__':
	wallpaper_changer(time_interval=10)
