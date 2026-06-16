import json
from pathlib import Path
from typing import Any


def _text(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) if isinstance(data, (dict, list)) else str(data)


def _write_basic_pdf(task: dict[str, Any], output_path: Path) -> Path:
    sections = [
        ("Project summary", {
            "prompt": task.get("prompt"),
            "product": task.get("product"),
            "market": task.get("market"),
            "target_customer": task.get("target_customer"),
            "budget": task.get("budget"),
        }),
        ("Market analysis", task["context"].get("market_report", {})),
        ("Brand strategy", task["context"].get("brand_strategy", {})),
        ("Content assets", task["context"].get("content_assets", {})),
        ("Media plan", task["context"].get("media_plan", {})),
    ]
    lines: list[str] = []
    for title, body in sections:
        lines.extend([title, json.dumps(body, ensure_ascii=True, indent=2), ""])
    wrapped: list[str] = []
    for line in "\n".join(lines).splitlines():
        wrapped.extend(line[index : index + 88] for index in range(0, len(line), 88))
    pages = [wrapped[index : index + 54] for index in range(0, len(wrapped), 54)] or [[]]

    objects: list[bytes] = []
    page_refs = " ".join(f"{4 + index * 2} 0 R" for index in range(len(pages)))
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(
        f"<< /Type /Pages /Kids [{page_refs}] /Count {len(pages)} >>".encode()
    )
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    for index, page_lines in enumerate(pages):
        page_number = 4 + index * 2
        content_number = page_number + 1
        objects.append(
            (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
                f"/Resources << /Font << /F1 3 0 R >> >> "
                f"/Contents {content_number} 0 R >>"
            ).encode()
        )
        commands = ["BT", "/F1 9 Tf", "46 800 Td", "12 TL"]
        for line in page_lines:
            escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            commands.extend([f"({escaped}) Tj", "T*"])
        commands.append("ET")
        stream = "\n".join(commands).encode("ascii")
        objects.append(
            f"<< /Length {len(stream)} >>\nstream\n".encode()
            + stream
            + b"\nendstream"
        )

    output = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for number, body in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{number} 0 obj\n".encode())
        output.extend(body)
        output.extend(b"\nendobj\n")
    xref_offset = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n".encode())
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode())
    output.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n"
        ).encode()
    )
    output_path.write_bytes(output)
    return output_path


def generate_growth_strategy_report(task: dict[str, Any], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        from reportlab.pdfgen import canvas
    except ModuleNotFoundError:
        return _write_basic_pdf(task, output_path)

    font = "STSong-Light"
    pdfmetrics.registerFont(UnicodeCIDFont(font))
    pdf = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4
    sections = [
        ("项目摘要", {
            "任务": task.get("prompt"),
            "产品": task.get("product"),
            "目标市场": task.get("market"),
            "目标用户": task.get("target_customer"),
            "预算": task.get("budget"),
        }),
        ("市场分析", task["context"].get("market_report", {})),
        ("品牌战略", task["context"].get("brand_strategy", {})),
        ("内容资产", task["context"].get("content_assets", {})),
        ("广告方案", task["context"].get("media_plan", {})),
    ]
    for title, body in sections:
        pdf.setFont(font, 17)
        pdf.drawString(2 * cm, height - 2 * cm, title)
        pdf.setFont(font, 9)
        y = height - 3 * cm
        for block in _text(body).splitlines():
            while len(block) > 58:
                pdf.drawString(2 * cm, y, block[:58])
                block = block[58:]
                y -= 0.42 * cm
            if y < 2 * cm:
                pdf.showPage()
                pdf.setFont(font, 9)
                y = height - 2 * cm
            pdf.drawString(2 * cm, y, block)
            y -= 0.42 * cm
        pdf.showPage()
    pdf.save()
    return output_path
