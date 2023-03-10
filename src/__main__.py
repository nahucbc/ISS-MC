from wrapper.forge import Forge
from small_def import if_not_exist_mkdir, data, cache

if_not_exist_mkdir(data)
if_not_exist_mkdir(cache)

forge : Forge = Forge(data, cache)

print("#########\nInit Script Server For Minecraft\n#########\n")
print("1> Make Database")
print("2> Install ")

option = input(">")
match(option):
    case("1"):
        forge.export_json()

    case("2"):
        forge.import_json()
        forge.download(cache, "1.19", "latest", "installer")
        