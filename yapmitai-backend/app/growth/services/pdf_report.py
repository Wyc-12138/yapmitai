import json
from pathlib import Path
from typing import Any

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas

_FONT_REGISTERED = False


def _ensure_font() -> str:
    global _FONT_REGISTERED
    font_name = "STSong-Light"
    if not _FONT_REGISTERED:
        pdfmetrics.registerFont(UnicodeCIDFont(font_name))
        _FONT_REGISTERED = True
    return font_name


def _wrap_text(text: str, max_chars: int = 46) -> list[str]:
    lines: list[str] = []
    paragraph = str(text).replace("\r", "")
    for block in paragraph.split("\n"):
        block = block.strip()
        if not block:
            lines.append("")
            continue
        while len(block) > max_chars:
            lines.append(block[:max_chars])
            block = block[max_chars:]
        lines.append(block)
    return lines


def _draw_page(
    pdf: canvas.Canvas,
    title: str,
    body: str,
    font_name: str,
) -> None:
    width, height = A4
    pdf.setFont(font_name, 16)
    pdf.drawString(2 * cm, height - 2 * cm, title)
    pdf.setFont(font_name, 10)
    y = height - 3 * cm
    for line in _wrap_text(body):
        if y < 2 * cm:
            pdf.showPage()
            pdf.setFont(font_name, 10)
            y = height - 2 * cm
        pdf.drawString(2 * cm, y, line)
        y -= 0.45 * cm
    pdf.showPage()


def _section_text(data: Any) -> str:
    if isinstance(data, dict):
        parts = []
        for key, value in data.items():
            if isinstance(value, (list, dict)):
                parts.append(f"{key}:\n{json.dumps(value, ensure_ascii=False, indent=2)}")
            else:
                parts.append(f"{key}: {value}")
        return "\n\n".join(parts)
    if isinstance(data, list):
        return "\n\n".join(f"- {item}" for item in data)
    return str(data)


def _execution_recommendations_text(context: dict[str, Any]) -> str:
    llm_text = str(context.get("execution_recommendations") or "").strip()
    if llm_text:
        return llm_text
    return (
        "暂无执行建议，请根据前述市场、品牌、内容与投放方案自行制定落地计划。"
    )


def generate_growth_strategy_report(task: dict[str, Any], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    font_name = _ensure_font()
    pdf = canvas.Canvas(str(output_path), pagesize=A4)
    context = task.get("context") or {}

    summary = (
        f"Growth Strategy Report\n"
        f"任务编号：{task.get('id')}\n"
        f"用户需求：{task.get('prompt')}\n"
        f"产品：{task.get('product')}\n"
        f"目标市场：{task.get('market')}\n"
        f"目标用户：{task.get('target_customer')}\n"
        f"预算：{task.get('budget')}\n"
        f"状态：{task.get('status')}\n"
        f"执行步骤：市场分析 → 品牌战略 → 内容资产 → 广告投放"
    )
    _draw_page(pdf, "第一页 · 项目摘要", summary, font_name)
    _draw_page(
        pdf,
        "第二页 · 市场分析",
        _section_text(context.get("market_report") or {}),
        font_name,
    )
    _draw_page(
        pdf,
        "第三页 · 品牌战略",
        _section_text(context.get("brand_strategy") or {}),
        font_name,
    )
    _draw_page(
        pdf,
        "第四页 · 内容资产",
        _section_text(context.get("content_assets") or {}),
        font_name,
    )
    _draw_page(
        pdf,
        "第五页 · 广告方案",
        _section_text(context.get("media_plan") or {}),
        font_name,
    )
    _draw_page(
        pdf,
        "第六页 · 执行建议",
        _execution_recommendations_text(context),
        font_name,
    )
    pdf.save()
    return output_path
