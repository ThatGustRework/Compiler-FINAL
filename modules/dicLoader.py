import json
import os

class DiccionaryLoader:
    def __init__(self):
        self.adjetivos = []
        self.adverbios = []
        self.preposiciones = []
        self.sustantivos = []
        self.verbos = []
        self.pronombres = []
        self.personas = []
        self.lugares = []

    # Carga los arrays desde los archivos
    def load_data_from_file(self):
        self.adjetivos = self.parse_from_file('./diccionario/adjetivos.txt')
        self.adverbios = self.parse_from_file('./diccionario/adverbios.txt')
        self.preposiciones = self.parse_from_file('./diccionario/preposiciones.txt')
        self.sustantivos = self.parse_from_file('./diccionario/sustantivos.txt')
        self.verbos = self.parse_from_file('./diccionario/verbos.txt')
        self.pronombres = self.parse_from_file('./diccionario/pronombres.txt')
        self.personas = self.parse_from_file('./diccionario/nombres_personales.txt')
        self.lugares = self.parse_from_file('./diccionario/lugares.txt')

    # Guarda los txt como un json
    def save_txt_to_json(self):
        # Vuelca en los archivos los arrays cargados de los archivos
        self.array_to_file('./diccionario/adjetivos.json', self.adjetivos)
        self.array_to_file('./diccionario/adverbios.json', self.adverbios)
        self.array_to_file('./diccionario/preposiciones.json', self.preposiciones)
        self.array_to_file('./diccionario/sustantivos.json', self.sustantivos)
        self.array_to_file('./diccionario/verbos.json', self.verbos)
        self.array_to_file('./diccionario/pronombres.json', self.pronombres)
        self.array_to_file('./diccionario/nombres_personales.json', self.personas)
        self.array_to_file('./diccionario/lugares.json', self.lugares)

    # Crea un archivo json con todos los grupos de tokens del español
    def make_language_json(self):
        idioma = {
            "adjetivos": self.adjetivos,
            "adverbios": self.adverbios,
            "preposiciones": self.preposiciones,
            "sustantivos": self.sustantivos,
            "verbos": self.verbos,
            "pronombres": self.pronombres,
            "personas": self.personas,
            "lugares": self.lugares
        }

        # Vuelca a un json con todos los datos
        self.array_to_file('./diccionario/spanish.json', idioma)

    # Acomoda el string
    def clean_str(self, cadena):
        replacements = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'ñ': 'n', 'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O',
            'Ú': 'U', 'Ñ': 'N'
        }

        for a, b in replacements.items():
            cadena = cadena.replace(a, b)
        return cadena.upper()

    # Carga el archivo y lo parsea en base a los saltos de línea
    def parse_from_file(self, file):
        with open(file, 'r', encoding='utf-8') as f:
            str_content = f.read()

        lista_str = str_content.split(os.linesep)
        struct = {}

        for string in lista_str:
            struct[self.clean_str(string)] = 1

        return struct

    # Guarda el contenido del array en un archivo
    def array_to_file(self, file, data):
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


# Ejemplo de uso de la clase DiccionaryLoader
dic_loader = DiccionaryLoader()
dic_loader.load_data_from_file()
dic_loader.save_txt_to_json()
dic_loader.make_language_json()
