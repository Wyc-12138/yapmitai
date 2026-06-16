import json
from collections import OrderedDict

from app.growth.services.llm import growth_llm_service

_MAX_CACHE_SIZE = 5000
_translation_cache: OrderedDict[str, str] = OrderedDict()


def _remember(source: str, translation: str) -> None:
    _translation_cache[source] = translation
    _translation_cache.move_to_end(source)
    while len(_translation_cache) > _MAX_CACHE_SIZE:
        _translation_cache.popitem(last=False)


async def translate_batch(texts: list[str]) -> dict[str, str]:
    unique_texts = list(dict.fromkeys(text.strip() for text in texts if text.strip()))
    result = {
        text: _translation_cache[text]
        for text in unique_texts
        if text in _translation_cache
    }
    missing = [text for text in unique_texts if text not in result]
    if not missing:
        return result

    items = [{"id": str(index), "text": text} for index, text in enumerate(missing)]
    response = await growth_llm_service.complete_json(
        system_prompt=(
            "You translate Simplified Chinese SaaS user interfaces into concise, natural "
            "English. Preserve model names, product names, IDs, numbers, URLs, punctuation, "
            "template variables, and line breaks. Do not explain. Return one JSON object "
            'with this exact shape: {"translations":{"0":"English text"}}.'
        ),
        user_prompt=json.dumps({"items": items}, ensure_ascii=False),
        temperature=0.1,
    )
    translations = response.get("translations", {})
    if not isinstance(translations, dict):
        translations = {}

    for item in items:
        source = item["text"]
        translated = translations.get(item["id"], source)
        if not isinstance(translated, str) or not translated.strip():
            translated = source
        translated = translated.strip()
        result[source] = translated
        _remember(source, translated)
    return result
