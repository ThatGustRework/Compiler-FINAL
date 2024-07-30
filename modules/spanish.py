import json

FIN = -1  # Valor constante que indica el final de los tokens

lexema = ''  # Variable para almacenar el lexema actual
tok = None  # Variable para almacenar el token actual
tokens = []  # Lista para almacenar los tokens del texto
current_token_index = 0  # Índice actual en la lista de tokens


class SpanishDb:
    # Constructor de la clase
    def __init__(self):
        self.bd = None  # Base de datos que se cargará desde el archivo JSON
        self.ADJECTIVES = []
        self.ADVERBS = []
        self.PLACES = []
        self.PEOPLE = []
        self.PREPOSITIONS = []
        self.PRONOUNS = []
        self.SUBJECTS = []
        self.VERBS = []
        self.load_bd_from_file()  # Carga la base de datos desde un archivo JSON
        self.add_conjugated_verbs()  # Agrega las formas conjugadas de los verbos
        print('SPANISHDB DONE')

    # Carga la base de datos desde un archivo JSON
    def load_bd_from_file(self):
        # Lee el archivo JSON y convierte su contenido a una cadena
        with open('./diccionario/spanish.json', 'r', encoding='utf-8') as file:
            str_content = file.read()

        # Parsea la cadena JSON a un objeto Python
        struct = json.loads(str_content)

        # Valida que el JSON se haya parseado correctamente
        if struct and str_content:
            self.ADJECTIVES = list(struct.get('adjetivos', {}).keys())
            self.ADVERBS = list(struct.get('adverbios', {}).keys())
            self.PLACES = list(struct.get('lugares', {}).keys())
            self.PEOPLE = list(struct.get('personas', {}).keys())
            self.PREPOSITIONS = list(struct.get('preposiciones', {}).keys())
            self.PRONOUNS = list(struct.get('pronombres', {}).keys())
            self.SUBJECTS = list(struct.get('sustantivos', {}).keys())
            self.VERBS = list(struct.get('verbos', {}).keys())
        else:
            # Imprime un mensaje de error si el JSON no se parseó correctamente
            print("Error: JSON de idioma mal armado.")

    # Agrega formas conjugadas de los verbos a la lista de verbos
    def add_conjugated_verbs(self):
        conjugated = []  # Lista para almacenar las formas conjugadas

        if isinstance(self.VERBS, list):
            for verb in self.VERBS:
                forms = self.conjugate_verb(verb)  # Conjuga el verbo
                if forms:
                    conjugated.extend(forms)  # Agrega las formas conjugadas a la lista

            # Añade las formas conjugadas a la lista original de verbos
            self.VERBS.extend(conjugated)
        else:
            print('VERBS is not a list')  # Imprime un mensaje de error si VERBS no es una lista

    # Conjuga un verbo en sus formas regulares
    def conjugate_verb(self, verb):
        endings = {
            'AR': ['O', 'AS', 'A', 'AMOS', 'ÁIS', 'AN'],
            'ER': ['O', 'ES', 'E', 'EMOS', 'ÉIS', 'EN'],
            'IR': ['O', 'ES', 'E', 'IMOS', 'ÍS', 'EN']
        }

        if verb.endswith('ARSE'):
            stem = verb[:-4]
            pronoun = "ME "
            verb_type = 'AR'
        elif verb.endswith('ERSE'):
            stem = verb[:-4]
            pronoun = "ME "
            verb_type = 'ER'
        elif verb.endswith('IRSE'):
            stem = verb[:-4]
            pronoun = "ME "
            verb_type = 'IR'
        elif verb.endswith('AR'):
            stem = verb[:-2]
            verb_type = 'AR'
            pronoun = ""
        elif verb.endswith('ER'):
            stem = verb[:-2]
            verb_type = 'ER'
            pronoun = ""
        elif verb.endswith('IR'):
            stem = verb[:-2]
            verb_type = 'IR'
            pronoun = ""
        else:
            return None

        # Conjuga el verbo y devuelve las formas conjugadas
        conjugated_forms = [f"{pronoun}{stem}{ending}" for ending in endings[verb_type]]
        return conjugated_forms

    # Encuentra el tipo de token para una palabra dada
    def find_word_token(self, word):
        resu = []  # Lista para almacenar los tipos de tokens encontrados

        # Lista de listas y funciones para verificar los tipos de palabras
        list_fn = [
            {'list': self.ADJECTIVES, 'val': 'adjetivo'},
            {'list': self.ADVERBS, 'val': 'adverbio'},
            {'list': self.PREPOSITIONS, 'val': 'preposicion'},
            {'list': self.SUBJECTS, 'val': 'sustantivo'},
            {'list': self.VERBS, 'val': 'verbo'},
            {'list': self.PRONOUNS, 'val': 'pronombre'},
            {'list': self.PEOPLE, 'val': 'personas'},
            {'list': self.PLACES, 'val': 'lugar'}
        ]

        # Verifica cada palabra contra las categorías definidas
        for item in list_fn:
            if self.find_elem_nomb(item['list'], word):
                resu.append(item['val'])  # Agrega el tipo de token al resultado si se encuentra en la lista

        if word.isdigit():
            resu.append('numero')  # Agrega 'numero' si la palabra es un número

        return resu  # Devuelve los tipos de tokens encontrados

    # Función auxiliar para verificar si una palabra está en una lista de elementos
    def find_elem_nomb(self, items, word):
        if not isinstance(items, list):
            print('Items is not a list:', items)
            return False

        # Normaliza la cadena para eliminar acentos y caracteres especiales
        def clean_str(cadena):
            replacements = {
                'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
                'ñ': 'n', 'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O',
                'Ú': 'U', 'Ñ': 'N'
            }
            for a, b in replacements.items():
                cadena = cadena.replace(a, b)
            return cadena.upper()

        word = clean_str(word)
        items = [clean_str(item) for item in items]

        return word in items

    # Analiza un texto y determina el tipo de cada palabra
    def analyse_text(self, texto):
        print('Analizando ', texto)

        final = []  # Lista para almacenar los resultados del análisis

        bloques = texto.split(" ")  # Divide el texto en palabras por espacios

        # Itera sobre cada palabra y encuentra su tipo de token
        for elem in bloques:
            print(elem)
            token = self.find_word_token(elem)
            final.append({"word": elem, "token": token})  # Almacena el resultado en la lista final
        return final  # Devuelve la lista con los resultados

    # Analiza un texto y devuelve el resultado en forma de lista
    def analyse_text_array(self, texto):
        resu = self.analyse_text(texto)  # Obtiene los resultados del análisis
        salida = {}  # Diccionario para almacenar el resultado final

        for item in resu:
            salida[item["word"]] = item["token"]  # Asigna el tipo de token a cada palabra en el diccionario

        return salida  # Devuelve el diccionario con los resultados

    def analyse_text_file(self, file):
        with open(file, 'r', encoding='utf-8') as f:
            input_content = f.read()

        lines = input_content.split('.')

        for line in lines:
            if line.strip() == '':
                continue

            clean_line = line.replace('\r', '').replace('\n', '')
            # IMPRIME LA LINEA LIMPIA
            print(clean_line)

            global tokens, current_token_index, tok
            tokens = line.strip().split()
            current_token_index = 0
            tok = self.scanner()

            self.Oracion()

            if tok != FIN:
                self.error()

            print('La oración es válida.')

    # Verifica si el token actual es el esperado y avanza al siguiente token
    def parea(self, expected_token):
        global tok
        if tok == expected_token:
            tok = self.scanner()  # Obtiene el siguiente token
        else:
            self.error()  # Muestra un error si el token no es el esperado

    # Muestra un mensaje de error y termina el proceso
    def error(self):
        print('Syntax error')
        exit(1)

    def scanner(self):
        global current_token_index, tokens, lexema
        if current_token_index >= len(tokens):
            return FIN  # Retorna FIN si se ha llegado al final de los tokens

        token = tokens[current_token_index]  # Obtiene el token actual
        current_token_index += 1
        lexema = token  # Almacena el lexema actual
        return token  # Retorna el token actual

    # Analiza una oración
    def Oracion(self):
        self.Sujeto()  # Analiza el sujeto de la oración
        self.Predicado()  # Analiza el predicado de la oración

    # Analiza el sujeto de una oración
    def Sujeto(self):
        self.Nombre()  # Analiza el nombre del sujeto

    # Analiza el predicado de una oración
    def Predicado(self):
        if tok in self.VERBS:
            self.parea(tok)  # Verifica y avanza si el token es un verbo
            self.Complemento()  # Analiza el complemento del predicado

    # Analiza un complemento de una oración
    def Complemento(self):
        if tok in self.ADJECTIVES or tok in self.ADVERBS or tok in self.SUBJECTS:
            self.parea(tok)  # Verifica y avanza si el token es un adjetivo, adverbio o sustantivo

    # Analiza un nombre en una oración
    def Nombre(self):
        if tok in self.SUBJECTS or tok in self.PRONOUNS:
            self.parea(tok)  # Verifica y avanza si el token es un sustantivo o pronombre


# Ejemplo de uso de la clase SpanishDb
spanish_db = SpanishDb()