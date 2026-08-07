"""
Fill the Lockwood 4:3 poster template with project content.

Usage:
    python scripts/build_poster.py
"""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Pt, Emu


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = Path(
    r"c:\Users\amirz\Downloads\PosterPresentations.com-Virtual(4.3-Ratio)-Template-Lockwood (1).pptx"
)
OUTPUT = ROOT / "docs" / "poster" / "IoT_Energy_Optimization_Poster.pptx"

ARCH = ROOT / "assets" / "architecture" / "high_level_architecture.png"
CHART_CMP = ROOT / "assets" / "charts" / "policy_comparison.png"
CHART_ENERGY = ROOT / "assets" / "charts" / "energy_curves.png"

INK = RGBColor(0x1A, 0x23, 0x32)
ACCENT = RGBColor(0x0F, 0x4C, 0x81)


def _set_runs(paragraph, text, size_pt, bold=False, color=INK, font_name="Tahoma"):
    paragraph.clear()
    run = paragraph.add_run()
    run.text = text
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font_name


def set_block(shape, title_or_lines, *, size_pt=16, bold=False, align=PP_ALIGN.RIGHT, color=INK):
    """Set one or more paragraphs into a text placeholder."""
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True

    lines = title_or_lines if isinstance(title_or_lines, list) else [title_or_lines]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.level = 0
        _set_runs(p, line, size_pt=size_pt, bold=bold, color=color)


def set_body_paragraphs(shape, paragraphs, *, size_pt=13, align=PP_ALIGN.RIGHT):
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    try:
        tf.auto_size = None
    except Exception:
        pass

    for i, block in enumerate(paragraphs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.level = 0
        p.space_after = Pt(6)
        _set_runs(p, block, size_pt=size_pt, bold=False, color=INK)


def build():
    if not TEMPLATE.exists():
        raise FileNotFoundError(f"Template not found: {TEMPLATE}")

    prs = Presentation(str(TEMPLATE))
    slide = prs.slides[0]
    shapes = list(slide.shapes)

    # Mapped by inspection of Lockwood 4:3 template placeholders
    body_tl, title_tl = shapes[0], shapes[1]
    body_bl, title_bl = shapes[2], shapes[3]
    body_tm, title_tm = shapes[4], shapes[5]
    title_tr, body_tr = shapes[6], shapes[7]
    title_br, body_br = shapes[8], shapes[9]
    meta, subtitle, title = shapes[10], shapes[11], shapes[12]

    # Header
    set_block(
        title,
        "بهینه‌سازی مصرف انرژی در شبکه‌های اینترنت اشیا با یادگیری تقویتی عمیق",
        size_pt=28,
        bold=True,
        align=PP_ALIGN.CENTER,
        color=ACCENT,
    )
    set_block(
        subtitle,
        "IoT Energy Optimization using Deep Reinforcement Learning (DQN)",
        size_pt=16,
        bold=False,
        align=PP_ALIGN.CENTER,
        color=INK,
    )
    set_block(
        meta,
        "دانشجو: امیرمحمد ذکاوتی  |  استاد راهنما: دکتر منیره عبدوس  |  دانشگاه شهید بهشتی  |  ۱۴۰۴",
        size_pt=12,
        bold=False,
        align=PP_ALIGN.CENTER,
        color=INK,
    )

    # Top-left: Problem
    set_block(title_tl, "مسئله و انگیزه", size_pt=18, bold=True, align=PP_ALIGN.RIGHT, color=ACCENT)
    set_body_paragraphs(
        body_tl,
        [
            "نودهای حسگر IoT معمولاً با باتری محدود کار می‌کنند. ارسال مداوم عمر شبکه را کم می‌کند و خواب بیش از حد کیفیت پایش را پایین می‌آورد.",
            "اتصالات جهانی IoT از حدود ۲۱ میلیارد (۲۰۲۵) به حدود ۴۸ میلیارد (۲۰۳۵) می‌رسد [1]. بنابراین تصمیم هوشمند بین Transmit و Sleep ضروری است.",
        ],
        size_pt=12,
    )

    # Top-middle: Objectives
    set_block(title_tm, "اهداف پروژه", size_pt=18, bold=True, align=PP_ALIGN.RIGHT, color=ACCENT)
    set_body_paragraphs(
        body_tm,
        [
            "• شبیه‌سازی شبکه IoT با مدل انرژی",
            "• آموزش عامل DQN برای تصمیم Transmit / Sleep",
            "• مقایسه با Always Transmit، Always Sleep و Random",
            "• داشبورد تعاملی با Streamlit",
        ],
        size_pt=12,
    )

    # Top-right: Method
    set_block(title_tr, "روش پیشنهادی", size_pt=18, bold=True, align=PP_ALIGN.RIGHT, color=ACCENT)
    set_body_paragraphs(
        body_tr,
        [
            "• حالت نود: active / sleep / dead",
            "• مشاهده: انرژی نودها + زنده بودن + زمان",
            "• عمل: Sleep یا Transmit برای هر نود",
            "• پاداش: بسته و عمر بیشتر − مصرف انرژی − مرگ نود",
            "• ابزار: Python، Gymnasium، Stable-Baselines3، Streamlit",
        ],
        size_pt=12,
    )

    # Bottom-left: Results
    set_block(title_bl, "نتایج کلیدی", size_pt=18, bold=True, align=PP_ALIGN.RIGHT, color=ACCENT)
    set_body_paragraphs(
        body_bl,
        [
            "تنظیمات: ۳ نود | افق ۵۰ گام | آموزش ۸۰۰۰ گام | میانگین ۵ اپیزود",
            "Always Transmit → Lifetime 17 | Packets 48 | Energy 0.00",
            "Always Sleep → Lifetime 50 | Packets 0 | Energy 2.85",
            "Random → Lifetime 38.6 | Packets 48 | Energy 0.00",
            "DQN → Lifetime 50 | Packets 42 | Energy 0.37",
            "پیام: DQN عمر شبکه را حفظ می‌کند و هم‌زمان داده تحویل می‌دهد.",
        ],
        size_pt=11,
    )

    # Bottom-right: Conclusion + refs
    set_block(title_br, "نتیجه‌گیری و مراجع", size_pt=18, bold=True, align=PP_ALIGN.RIGHT, color=ACCENT)
    set_body_paragraphs(
        body_br,
        [
            "DQN مصالحه‌ای میان تحویل بسته و حفظ انرژی یاد می‌گیرد. داشبورد امکان آموزش، اجرا و مقایسه سیاست‌ها را فراهم می‌کند.",
            "آینده: Multi-Agent RL، مدل کانال واقعی، مسیریابی چندگامه، سخت‌افزار.",
            "[1] Transforma Insights, 2026",
            "[4] Heinzelman et al., LEACH, 2000",
            "[8] Banerjee et al., NashDQNSleep, 2025",
            "[9] Leong et al., DRL Sensor Scheduling, 2018",
        ],
        size_pt=11,
    )

    # Center graphic band (between top bodies and bottom panels)
    band_top = Emu(7_400_000)
    band_height = Emu(9_400_000)
    gap = Emu(250_000)
    left_x = Emu(900_000)
    usable_width = prs.slide_width - Emu(1_800_000)
    img_w = int((usable_width - 2 * gap) / 3)

    images = [
        ARCH,
        CHART_CMP,
        CHART_ENERGY,
    ]
    x = left_x
    for path in images:
        if not path.exists():
            raise FileNotFoundError(path)
        # Keep aspect ratio and fit inside the target box
        pic = slide.shapes.add_picture(str(path), x, band_top, width=img_w)
        if pic.height > band_height:
            ratio = band_height / pic.height
            pic.height = band_height
            pic.width = int(pic.width * ratio)
            pic.left = int(x + (img_w - pic.width) / 2)
        if pic.height < band_height:
            pic.top = int(band_top + (band_height - pic.height) / 2)
        x = x + img_w + gap

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUTPUT))
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    build()
