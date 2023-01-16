
def url_maker(page='',tags='',width='',height='',rating='',score='',user=''):
	rating_list = ['safe','questionable','questionableplus','questionableless','explicit']
	if page != '':
		page = 'page='+str(page) 
	if tags != '':
		tags = tags.replace(' ','+')
	if width != '':
		width = 'width:'+str(width) 
	if height != '':
		height = 'height:'+str(height) 
	if score != '':
		#..20  means less than 20 score and 20.. means more than 20 score
		score = 'score:'+str(score)
	if user != '':
		user = 'user:'+user
	if rating in rating_list:
		rating = 'rating:'+rating 
	else:
		rating = ''
	
	url = f'https://konachan.com/post?{page}&tags={tags}%20{width}%20{height}%20{rating}%20{score}%20{user}'
	
	return url  


def resposer(url):
	import requests
	try:
		response = requests.get(url)
	except:
		print('url error')
		response=None
	finally:
		return response

def souper(response):
	from bs4 import BeautifulSoup
	if response:
		soup = BeautifulSoup(response.text , 'html.parser')
	return soup

def soup_cleaner(soup):
	soup = soup.find('div',attrs = {'class':'content'})
	div_trashs = ['quick-edit','index-hover-overlay','index-hover-info','paginator']
	for trash in div_trashs:
		compose = soup.find('div',attrs = {'id':trash})
		compose.decompose()

	trashs=['iframe']
	for trash in trashs:
		compose = soup.find(trash)
		compose.decompose()

	return soup 
def is_soup_empty(cleaned_soup):
	p_tags =  cleaned_soup.find_all('p')
	if p_tags:
		for p in p_tags:
			if p.text == 'Nobody here but us chickens!':
				return True
	return False

def link_extractor(cleaned_soup):

	a_tags = cleaned_soup.find_all('a',attrs = {'class':"directlink largeimg"})
	link_list = list()
	for a in a_tags:
		a = a['href']
		link_list.append(a)
	return link_list


def image_downloader(link_list,download_location='/home/positive/Wallpaper',img_format = '.jpg',image_limit=10,file_name_to_include=''):
	'''Takes a list of url and downloads them'''
	from url_downloader import save_file
	
    
	#Downloading everything from the link_list
	for img_position,urls in enumerate(link_list):
		print('Image downloading;',len(link_list)-img_position,' left')
		print(urls)
        #Keeping it short
		if img_position > image_limit:
			break

		save_file(url = urls,file_name=file_name_to_include+str(img_position)+img_format,file_path=download_location)



if __name__ == '__main__':
	import time

	usr_input = ''#input('Any tag to include?\n')
	tag= ''
	if usr_input:
		tag = usr_input.replace(' ','+')

	url = url_maker(height='1080',width='1920',rating='explicit',score='200..',tags=tag)
	response = resposer(url)

	soup = souper(response)
	cleaned_soup = soup_cleaner(soup)
	if not is_soup_empty(cleaned_soup):
		link_list = link_extractor(cleaned_soup)
		image_downloader(link_list,file_name_to_include=str(time.time()))	
	else:
		print('Soup was empty')	
