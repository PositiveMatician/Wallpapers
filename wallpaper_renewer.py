import requests,os,time
from bs4 import BeautifulSoup



def url_maker(page='', tags='', width='', height='', rating='', score='', user=''):
    rating_list = ['safe', 'questionable',
                   'questionableplus', 'questionableless', 'explicit']
    if page != '':
        page = 'page='+str(page)
    if tags != '':
        tags = tags.replace(' ', '+')
    if width != '':
        width = 'width:'+str(width)
    if height != '':
        height = 'height:'+str(height)
    if score != '':
        # ..20  means less than 20 score and 20.. means more than 20 score
        score = 'score:'+str(score)
    if user != '':
        user = 'user:'+user
    if rating in rating_list:
        rating = 'rating:'+rating
    else:
        rating = ''

    url = f'https://konachan.com/post?{page}&tags={tags}%20{width}%20{height}%20{rating}%20{score}%20{user}'

    return url


def url_soup_maker(url):
    try:
        response = requests.get(url)
    except:
        print('url error')
        response = None
    if response:
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        soup = None
    return soup


def soup_cleaner(cleaned_soup):
    cleaned_soup = cleaned_soup.find('div', attrs={'class': 'content'})
    div_trashs = ['quick-edit', 'index-hover-overlay',
                  'index-hover-info', 'paginator']
    for trash in div_trashs:
        compose = cleaned_soup.find('div', attrs={'id': trash})
        compose.decompose()

    trashs = ['iframe']
    for trash in trashs:
        compose = cleaned_soup.find(trash)
        compose.decompose()

    return cleaned_soup


def is_soup_empty(cleaned_soup):
	p_tags = cleaned_soup.find_all('p')
	if p_tags:
		for p in p_tags:
			if p.text == 'Nobody here but us chickens!':
				return True
	return False


def link_extractor(cleaned_soup):

	a_tags = cleaned_soup.find_all('a', attrs={'class': "directlink largeimg"})
	link_list = list()
	for a in a_tags:
		a = a['href']
		link_list.append(a)
	return link_list


def image_downloader(link_list, download_location='/home/positive/Wallpaper/temp/', img_format='.jpg', image_limit=10, file_name_to_include=''):
    '''Takes a list of url and downloads them'''

    # Downloading everything from the link_list
    for img_position,urls in enumerate(link_list):
        

        #Keeping it short
        if img_position > image_limit:
            break
        response = requests.get(urls,stream=True)
        if response.status_code:
            with open(download_location+file_name_to_include+str(img_position)+img_format,'wb') as file:
                print('Image downloading;',len(link_list)-img_position,' left')
                file.write(response.content)


def wallpaper_downloader(wallpaper_folder):
       image_downloader(link_extractor(soup_cleaner(url_soup_maker(url_maker(height='1080',width='1920',rating='safe',score='200..')))),image_limit=15,download_location=wallpaper_folder)
 

def wallpaper_changer(wallpaper_folder='/home/positive/Wallpaper/temp/'):
    wallpaper_downloader(wallpaper_folder)
    images = os.listdir(wallpaper_folder)
    images.sort()
    for image in images:
        os.system(f'gsettings set org.gnome.desktop.background picture-uri \'file://{wallpaper_folder}/{image}\'')
        print('Wallpaper Changed')
        time.sleep(3)




if __name__=='__main__':
    log_file = '/home/positive/Wallpaper/wallpaper_changer_log'
    if not os.path.exists(log_file):
        file = open(log_file, 'w')
        file.close()



    with open(log_file) as file:
        log = file.read()
    if log != 'running':
        with open(log_file,'w') as file:
            file.write('running')
        try:
            wallpaper_changer()
            with open(log_file,'w') as file:
                file.write('')                 
        except Exception as err:
            print(err)
            with open(log_file,'w') as file:
                file.write(str(err))

               


    #/home/user/.local/share/application/
