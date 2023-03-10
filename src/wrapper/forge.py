import requests
from .interface import Api
from bs4 import BeautifulSoup, Tag, ResultSet
from json import dump, loads
from pathlib import Path
from os import system as sys

class Forge(Api):
    
    def __init__(self, path_data, cache) -> None:
        self.__modloader : str = "Forge"
        self.__version : int = 1.1
        
        self.__index : list = []
        self.json : str = Path(f'{path_data}/forge.json')
        self.cache : str = cache

    def about(self) -> None:
        pass

    def __make_index(self) -> None:
        address : requests = requests.get('https://files.minecraftforge.net/net/minecraftforge/forge/').text
        soup : BeautifulSoup = BeautifulSoup(address, features="html.parser")
        scroll_panel_list : Tag = soup.find('ul', attrs={'class':'section-content scroll-pane'})
        mc_versions : ResultSet = scroll_panel_list.find_all('ul', attrs={'class':'nav-collapsible'})
        
        unfiltered_list : list = []
        
        for unfiltered_content in mc_versions:
            unfiltered_list.append(unfiltered_content.text)
        
        index_filtered : list = []
        unfiltered_list_size : int = len(unfiltered_list)

        for group_index in range(unfiltered_list_size):
            for version in unfiltered_list[group_index].split():
                index_filtered.append(version)

        self.__index : list = index_filtered

        del (
            soup, scroll_panel_list, mc_versions, unfiltered_list, unfiltered_list_size ,unfiltered_content, 
            index_filtered, group_index, version
             )
        
        return
    
    def __filter(self, data : list, start : int, end : int) -> list:
        try:
            temp : list = []
            size : int = len(data)

            if size > 6:
                end += 1
            elif size == 4:
                end += 1

            for url_position in range(start, end):
                shortener = data[url_position]
                link = shortener.split('=')
                link_size = len(link)
                match(link_size):
                    case 1:
                        temp.append(link[0])
                    case 3:
                        temp.append(link[2])
            
        except IndexError:
            pass

        finally:

            del (
                data, start, end, size, url_position
                 )
            
            if len(temp) < 3:
                return list()
            else:
                return temp
    
    def __make_dict(self) -> dict:
        
        self.__make_index()
        group_versions : dict = {}
        
        for key in range(len(self.__index)):
            version : int = self.__index[key]
            version_page_content : requests = requests.get(f'https://files.minecraftforge.net/net/minecraftforge/forge/index_{version}.html').text
            soup : BeautifulSoup = BeautifulSoup(version_page_content, features="html.parser")
            links : ResultSet = soup.find_all('div', attrs={'class':'link'})
            version_dict : dict = {}
            temp_list : list = []

            for link in links:
                temp_list.append(link.find('a')['href'])
            
            temp_latest : list = self.__filter(temp_list, 0, 3)
            temp_recommended : list = self.__filter(temp_list, 3, 6)

            version_dict['latest'] = temp_latest
            version_dict['recommended'] = temp_recommended
            group_versions[version] = version_dict

            del (
                version, version_page_content, version_dict, soup, link, links, temp_list, temp_latest, temp_recommended
                )

        return group_versions

    def export_json(self):
        with open(self.json, 'w') as f:
            data : dict = self.__make_dict()
            dump(data, f)

    def import_json(self):
        with open(self.json, "r") as f:
            content = f.read()
            self.data : dict = loads(content)

    def download(self, cache, version, type_build, type_file) -> None:
        file = self.data[version][type_build]
        file = [x for x in file if type_file in x][0]

        name = file.split("/")
        name = name[len(name) - 1]

        req : requests = requests.get(file).content

        if type_file == "installer":
            mode = "wb"
        else:
            mode = "w"

        dir = Path(f"{cache}/{name}")
        with open(dir, mode) as f:
            f.write(req)

        self.install(dir, "./test")

    def install(self, name, dir) -> None:
        sys(f"java -jar {name} --installServer {dir}")