import requests
from .interface import Api
from bs4 import BeautifulSoup
from json import dump

class Forge(Api):
    
    def __init__(self) -> None:
        self.__modloader : str = "Forge"
        self.__version = int = 1.1
        self.__address : requests = requests.get('https://files.minecraftforge.net/net/minecraftforge/forge/')

    def about(self) -> None:
        print(self.__modloader)
        print(self.__version)

    def __make_index(self) -> None:
        soup : BeautifulSoup = BeautifulSoup(self.__address.text, features="html.parser")
        
        versions = soup.find('ul', attrs={'class':'section-content scroll-pane'})
        versions = versions.find_all('ul', attrs={'class':'nav-collapsible'})
        
        self.__index : list = []
        
        for i in versions:
            self.__index.append(i.text)
        
        del soup
        del versions
        
        index_clear = []
        
        for key in range(len(self.__index)):
            for version in self.__index[key].split():
                index_clear.append(version)
        
        
        self.__index = index_clear

    def __filter(self, data : list, start : int, end : int) -> list:
        try:
            temp = list()
            num = len(data)
            if num > 6:
                end += 1
            if num == 4:
                end += 1
            for number in range(start, end):
                shortener = data[number]
                link = shortener.split('=')
                match(len(link)):
                    case 1:
                        temp.append(link[0])
                    case 3:
                        temp.append(link[2])
                
        except IndexError as er:
            pass
        finally:
            del data 
            del start
            del  end
            num = len(temp)
            if num < 3:
                del num
                return list()
            else:
                del num 
                return temp
    
    def __make_dict(self) -> dict:
        
        self.__make_index()
        versions = dict()
        
        for key in range(len(self.__index)):
            version = dict()
            index = self.__index[key]
            page: requests = requests.get(f'https://files.minecraftforge.net/net/minecraftforge/forge/index_{index}.html')
            soup : BeautifulSoup = BeautifulSoup(page.text, features="html.parser")
            links = soup.find_all('div', attrs={'class':'link'})
            
            
            temp_list = list()
            for link in links:
                temp_list.append(link.find('a')['href'])
            
            temp_latest : list = self.__filter(temp_list, 0, 3)
            
            temp_recommended : list = self.__filter(temp_list, 3, 6)

            version['latest'] = temp_latest
            version['recommended'] = temp_recommended
            versions[index] = version

        return versions

    def export_to_json(self):
        with open('data.json', 'w') as f:
            dump(self.__make_dict(), f)

        
        