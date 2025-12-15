from typing import Dict

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "welcome": "Welcome to SubsMarket! 🚀",
        "my_clubs": "<b>My Clubs</b> 👑\n\nSelect a club to manage:",
        "no_clubs": "You don't have any clubs yet. Create one with /create_club",
        "search_title": "🔍 <b>Search Clubs</b>\nSelect a category:",
        "search_found": "🔍 Found {count} clubs in {category}:",
        "category_video": "🎬 Video",
        "category_music": "🎵 Music",
        "category_all": "📂 All",
        "btn_video": "🎬 Video",
        "btn_music": "🎵 Music", 
        "btn_all": "📂 All",
        "join_status": "ℹ️ Join Status: {status}",
    },
    "ru": {
        "welcome": "Добро пожаловать в SubsMarket! 🚀",
        "my_clubs": "<b>Мои Клубы</b> 👑\n\nВыберите клуб для управления:",
        "no_clubs": "У вас пока нет клубов. Создайте его через /create_club",
        "search_title": "🔍 <b>Поиск Клубов</b>\nВыберите категорию:",
        "search_found": "🔍 Найдено {count} клубов в категории {category}:",
        "category_video": "🎬 Видео",
        "category_music": "🎵 Музыка",
        "category_all": "📂 Все",
        "btn_video": "🎬 Видео",
        "btn_music": "🎵 Музыка",
        "btn_all": "📂 Все",
        "join_status": "ℹ️ Статус вступления: {status}",
    },
    "kk": {
        "welcome": "SubsMarket-ке қош келдіңіз! 🚀",
        "my_clubs": "<b>Менің Клубтарым</b> 👑\n\nБасқару үшін клубты таңдаңыз:",
        "no_clubs": "Сізде әзірге клубтар жоқ. /create_club арқылы жасаңыз",
        "search_title": "🔍 <b>Клубтарды іздеу</b>\nСанатты таңдаңыз:",
        "search_found": "🔍 {category} санатында {count} клуб табылды:",
        "category_video": "🎬 Видео",
        "category_music": "🎵 Музыка",
        "category_all": "📂 Барлығы",
        "btn_video": "🎬 Видео",
        "btn_music": "🎵 Музыка",
        "btn_all": "📂 Барлығы",
        "join_status": "ℹ️ Қосылу мәртебесі: {status}",
    }
}

DEFAULT_LANG = "ru"

def get_text(key: str, lang: str = DEFAULT_LANG, **kwargs) -> str:
    # Fallback to default if lang not supported of empty
    if not lang or lang not in TRANSLATIONS:
        lang = DEFAULT_LANG
    
    text = TRANSLATIONS[lang].get(key, TRANSLATIONS[DEFAULT_LANG].get(key, key))
    if kwargs:
        return text.format(**kwargs)
    return text
