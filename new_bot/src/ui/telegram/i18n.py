from typing import Dict

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "welcome": "Welcome to SubsMarket! 🚀",
        "my_clubs_title": "<b>My Clubs</b> 👑",
        "my_clubs_empty": "You don't have any subscriptions yet.",
        "search_title": "🔍 <b>Search Clubs</b>\nSelect a category:",
        "search_found": "🔍 Found {count} clubs in {category}:",
        "category_video": "🎬 Video",
        "category_music": "🎵 Music",
        "category_all": "📂 All",
        "btn_video": "🎬 Video",
        "btn_music": "🎵 Music", 
        "btn_all": "📂 All",
        "join_status": "ℹ️ Join Status: {status}",
        "club_price": "💰 Price: {amount} ₸",
        "club_members": "👥 Members: {count} / {capacity}",
        "club_status": "ℹ️ Status: {status}",
        "club_id": "🆔 ID: <code>{club_id}</code>",
        "btn_back": "🔙 Back",
    },
    "ru": {
        "welcome": "Добро пожаловать в SubsMarket! 🚀",
        "my_clubs_title": "<b>Мои Клубы</b> 👑",
        "my_clubs_empty": "У вас пока нет подписок.",
        "search_title": "🔍 <b>Поиск Клубов</b>\nВыберите категорию:",
        "search_found": "🔍 Найдено {count} клубов в категории {category}:",
        "category_video": "🎬 Видео",
        "category_music": "🎵 Музыка",
        "category_all": "📂 Все",
        "btn_video": "🎬 Видео",
        "btn_music": "🎵 Музыка",
        "btn_all": "📂 Все",
        "join_status": "ℹ️ Статус вступления: {status}",
        "club_price": "💰 Цена: {amount} ₸",
        "club_members": "👥 Участники: {count} / {capacity}",
        "club_status": "ℹ️ Статус: {status}",
        "club_id": "🆔 ID: <code>{club_id}</code>",
        "btn_back": "🔙 Назад",
    },
    "kk": {
        "welcome": "SubsMarket-ке қош келдіңіз! 🚀",
        "my_clubs_title": "<b>Менің Клубтарым</b> 👑",
        "my_clubs_empty": "Сізде әзірге жазылымдар жоқ.",
        "search_title": "🔍 <b>Клубтарды іздеу</b>\nСанатты таңдаңыз:",
        "search_found": "🔍 {category} санатында {count} клуб табылды:",
        "category_video": "🎬 Видео",
        "category_music": "🎵 Музыка",
        "category_all": "📂 Барлығы",
        "btn_video": "🎬 Видео",
        "btn_music": "🎵 Музыка",
        "btn_all": "📂 Барлығы",
        "join_status": "ℹ️ Қосылу мәртебесі: {status}",
        "club_price": "💰 Бағасы: {amount} ₸",
        "club_members": "👥 Қатысушылар: {count} / {capacity}",
        "club_status": "ℹ️ Күйі: {status}",
        "club_id": "🆔 ID: <code>{club_id}</code>",
        "btn_back": "🔙 Арқаға",
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
