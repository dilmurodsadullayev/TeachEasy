from languages.en.base import translations as en_translations
from languages.uz.base import translations as uz_translations

def base_translations(request):
    language = request.session.get('language', 'en')  # Default til
    if language == 'uz':
        translations = uz_translations
    else:
        translations = en_translations
    return {'base_translations': translations}
