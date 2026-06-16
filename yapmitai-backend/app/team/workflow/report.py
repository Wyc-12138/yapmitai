from __future__ import annotations

from html import escape
from pathlib import Path
import sys
from typing import Any


PROJECT_PACKAGES = Path(__file__).resolve().parents[3] / ".packages"
if PROJECT_PACKAGES.exists() and str(PROJECT_PACKAGES) not in sys.path:
    sys.path.insert(0, str(PROJECT_PACKAGES))


FIELD_LABELS = {
    "summary": "执行摘要",
    "analysis": "分析结果",
    "recommendations": "行动建议",
    "deliverables": "交付成果",
    "opportunities": "市场机会",
    "risks": "风险提示",
    "next_steps": "下一步计划",
    "target_customer": "目标客户",
    "market_size": "市场规模",
    "industry_trend": "行业趋势",
    "top_competitors": "主要竞品",
    "positioning": "品牌定位",
    "slogan": "品牌口号",
    "usp": "核心卖点",
    "competitive_advantage": "竞争优势",
    "channel_strategy": "渠道策略",
    "growth_strategy": "增长策略",
}


def _label(value: Any) -> str:
    key = str(value)
    return FIELD_LABELS.get(key, key.replace("_", " ").strip().title())


def _plain_text(value: Any) -> str:
    if value is None:
        return "暂无内容"
    if isinstance(value, bool):
        return "是" if value else "否"
    return str(value).strip() or "暂无内容"


def _register_chinese_font(pdfmetrics: Any, TTFont: Any, UnicodeCIDFont: Any) -> str:
    candidates = (
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/simsun.ttc"),
    )
    for path in candidates:
        if not path.exists():
            continue
        try:
            pdfmetrics.registerFont(
                TTFont("YapmitChinese", str(path), subfontIndex=0)
            )
            return "YapmitChinese"
        except Exception:
            continue
    font_name = "STSong-Light"
    pdfmetrics.registerFont(UnicodeCIDFont(font_name))
    return font_name


def generate_workflow_report(
    *,
    task_name: str,
    team_name: str,
    prompt: str,
    sections: list[dict[str, Any]],
    output_path: Path,
) -> Path:
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import cm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.platypus import (
            KeepTogether,
            PageBreak,
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "生成中文 PDF 需要 reportlab，请执行：python -m pip install reportlab==4.4.1"
        ) from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    font_name = _register_chinese_font(pdfmetrics, TTFont, UnicodeCIDFont)
    width, height = A4
    palette = {
        "primary": colors.HexColor("#315DA9"),
        "primary_soft": colors.HexColor("#EDF4FF"),
        "text": colors.HexColor("#283443"),
        "muted": colors.HexColor("#6F7C8E"),
        "border": colors.HexColor("#D9E4F2"),
        "panel": colors.HexColor("#F8FAFD"),
    }

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName=font_name,
        fontSize=24,
        leading=34,
        alignment=TA_CENTER,
        textColor=palette["text"],
        spaceAfter=12,
    )
    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=10,
        leading=18,
        alignment=TA_CENTER,
        textColor=palette["muted"],
    )
    section_style = ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading1"],
        fontName=font_name,
        fontSize=16,
        leading=24,
        textColor=palette["primary"],
        spaceBefore=8,
        spaceAfter=10,
    )
    field_style = ParagraphStyle(
        "FieldTitle",
        parent=styles["Heading2"],
        fontName=font_name,
        fontSize=11,
        leading=18,
        textColor=palette["text"],
        spaceBefore=7,
        spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName=font_name,
        fontSize=10,
        leading=18,
        textColor=palette["text"],
        spaceAfter=6,
        wordWrap="CJK",
    )
    bullet_style = ParagraphStyle(
        "Bullet",
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        bulletIndent=2,
        spaceAfter=4,
    )
    meta_label_style = ParagraphStyle(
        "MetaLabel",
        parent=body_style,
        fontSize=9,
        textColor=palette["muted"],
    )

    def paragraph(value: Any, style: ParagraphStyle = body_style) -> Paragraph:
        text = escape(_plain_text(value)).replace("\n", "<br/>")
        return Paragraph(text, style)

    def render_value(value: Any, level: int = 0) -> list[Any]:
        flowables: list[Any] = []
        if isinstance(value, dict):
            if not value:
                return [paragraph("暂无内容")]
            for key, item in value.items():
                heading = Paragraph(escape(_label(key)), field_style)
                rendered = render_value(item, level + 1)
                flowables.append(KeepTogether([heading, *rendered[:1]]))
                flowables.extend(rendered[1:])
            return flowables
        if isinstance(value, (list, tuple)):
            if not value:
                return [paragraph("暂无内容")]
            for index, item in enumerate(value, start=1):
                if isinstance(item, (dict, list, tuple)):
                    flowables.append(
                        Paragraph(f"{index}.", field_style)
                    )
                    flowables.extend(render_value(item, level + 1))
                else:
                    flowables.append(
                        Paragraph(
                            f"• {escape(_plain_text(item))}",
                            bullet_style,
                        )
                    )
            return flowables
        return [paragraph(value)]

    def draw_page(canvas: Any, document: Any) -> None:
        canvas.saveState()
        canvas.setStrokeColor(palette["border"])
        canvas.line(1.7 * cm, height - 1.25 * cm, width - 1.7 * cm, height - 1.25 * cm)
        canvas.setFont(font_name, 8)
        canvas.setFillColor(palette["muted"])
        canvas.drawString(1.7 * cm, 1.15 * cm, "YAPMITAI · AI 工作流报告")
        canvas.drawRightString(
            width - 1.7 * cm,
            1.15 * cm,
            f"第 {document.page} 页",
        )
        canvas.restoreState()

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=1.8 * cm,
        leftMargin=1.8 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title=f"{task_name} - AI工作流报告",
        author="YAPMITAI",
    )

    story: list[Any] = [
        Spacer(1, 1.5 * cm),
        Paragraph("AI 工作流执行报告", title_style),
        Paragraph(escape(task_name), subtitle_style),
        Spacer(1, 1.1 * cm),
    ]
    overview = Table(
        [
            [Paragraph("工作流", meta_label_style), paragraph(task_name)],
            [Paragraph("AI 团队", meta_label_style), paragraph(team_name)],
            [Paragraph("用户需求", meta_label_style), paragraph(prompt)],
        ],
        colWidths=[2.4 * cm, 13.2 * cm],
        hAlign="LEFT",
    )
    overview.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), palette["primary_soft"]),
                ("BACKGROUND", (1, 0), (1, -1), palette["panel"]),
                ("BOX", (0, 0), (-1, -1), 0.6, palette["border"]),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, palette["border"]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    story.extend([overview, PageBreak()])

    for index, section in enumerate(sections, start=1):
        title = section.get("title") or f"第 {index} 阶段"
        story.append(Paragraph(escape(str(title)), section_style))
        story.extend(render_value(section.get("content", {})))
        if index < len(sections):
            story.extend([Spacer(1, 0.35 * cm), PageBreak()])

    document.build(story, onFirstPage=draw_page, onLaterPages=draw_page)
    return output_path
