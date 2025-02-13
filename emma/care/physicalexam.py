from capybara.llm import llm

from ..prompt import exam_report_prompt
from ..utils import extract_json_from_text


async def exam_report_ocr(pic_urls: list) -> str:
    prompt = exam_report_ocr()
    query = [{"type": "text", "text": prompt}] + [
        {
            "type": "image_url",
            "image_url": {"url": url},
        }
        for url in pic_urls
    ]
    response = await llm(query, model="qwen-vl-max", temperature=0.1, is_text=True)
    return extract_json_from_text(response)
