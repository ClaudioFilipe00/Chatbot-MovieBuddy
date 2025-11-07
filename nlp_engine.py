import re
import unidecode


GENRE_VARIATIONS = {
    "ação": ["acao", "ação"],
    "animação": ["animacao", "animação"],
    "comédia": ["comedia", "comédia"],
    "drama": ["drama"],
    "terror": ["terror"],
    "romance": ["romance"],
    "aventura": ["aventura"],
    "ficção científica": ["ficcao cientifica", "ficção científica"],
    "documentário": ["documentario", "documentário"],
    "família": ["familia", "família"],
    "fantasia": ["fantasia"],
    "história": ["historia", "história"],
    "música": ["musica", "música"],
    "mistério": ["misterio", "mistério"],
    "filme de tv": ["filme de tv", "tv movie"],
    "suspense": ["suspense"],
    "guerra": ["guerra"],
    "faroeste": ["faroeste", "western"],
    "crime": ["crime"]
}


LANG_VARIATIONS = {
    "en": ["ingles", "inglês", "Ingles", "Inglês"],
    "fr": ["frances", "francês", "Frances", "Francês"],
    "es": ["espanhol", "Espanhol"],
    "pt": ["portugues", "português", "Portugues", "Português"],
    "it": ["italiano", "Italiano"],
    "de": ["alemao", "alemão", "Alemao", "Alemão"],
    "tr": ["turco", "Turco"],
    "ja": ["japones", "japonês", "Japones", "Japonês"],
    "ko": ["coreano", "Coreano"],
    "ru": ["russo", "Russo"]
}

CANONICAL_NORMALIZED = {}
for canonical, variations in GENRE_VARIATIONS.items():
    for var in variations:
        kn = unidecode.unidecode(var).lower()
        CANONICAL_NORMALIZED[kn] = canonical

LANGS_NORMALIZED = {}
for code, variations in LANG_VARIATIONS.items():
    for var in variations:
        kn = unidecode.unidecode(var).lower()
        LANGS_NORMALIZED[kn] = code


GENRE_KEYS_SORTED = sorted(CANONICAL_NORMALIZED.keys(), key=len, reverse=True)
LANG_KEYS_SORTED = sorted(LANGS_NORMALIZED.keys(), key=len, reverse=True)

GENRE_PATTERNS = [(k, re.compile(rf"(?<!\w){re.escape(k)}(?!\w)", flags=re.IGNORECASE | re.UNICODE)) for k in GENRE_KEYS_SORTED]
LANG_PATTERNS = [(k, re.compile(rf"(?<!\w){re.escape(k)}(?!\w)", flags=re.IGNORECASE | re.UNICODE)) for k in LANG_KEYS_SORTED]

def _find_keyword_in_text_normalized(patterns, text_norm):
    """
    Recebe lista de (key, compiled_pattern) e texto já normalizado (sem acentos).
    Retorna a chave normalizada encontrada ou None.
    """
    for key, pat in patterns:
        if pat.search(text_norm):
            return key
    return None

def extrair_genero_idioma(texto: str):
    texto_original = texto or ""
    texto = texto_original.lower()
    texto_norm = unidecode.unidecode(texto)  
    
    chave_gen_norm = _find_keyword_in_text_normalized(GENRE_PATTERNS, texto_norm)
    genero = CANONICAL_NORMALIZED.get(chave_gen_norm) if chave_gen_norm else None

    chave_lang_norm = _find_keyword_in_text_normalized(LANG_PATTERNS, texto_norm)
    idioma = LANGS_NORMALIZED.get(chave_lang_norm) if chave_lang_norm else None

    return genero, idioma