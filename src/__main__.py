from wrapper.forge import Forge
from os import getcwd, mkdir
from os.path import exists

paths = [f"{getcwd()}/data/"]

if not exists(paths[0]):
    mkdir(paths[0])

print("#########\nInit Script Server For Minecraft\n#########\n")
print("1> Make Database")
option = input(">")

match(option):
    case("1"):
        forge : Forge = Forge()

        forge.export_to_json()