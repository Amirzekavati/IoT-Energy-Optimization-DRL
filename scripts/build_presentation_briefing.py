# -*- coding: utf-8 -*-
"""Build a Persian RTL speaker-briefing PDF for tomorrow's presentation."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs" / "presentation"
HTML_PATH = SRC / "briefing.html"
PDF_PATH = SRC / "Presentation_Briefing_FA.pdf"
PDF_FA = SRC / "گزارش_آمادگی_ارائه_فردا.pdf"
CHROME = Path("/usr/local/bin/google-chrome")
FONT_DIR = ROOT / "assets" / "fonts" / "vazirmatn"


def en(text: str) -> str:
    return f'<span class="en" dir="ltr" lang="en">{text}</span>'


def fig(rel: str, caption: str) -> str:
    src = f"../../assets/{rel}"
    return (
        f"<figure><img src='{src}' alt='{caption}'>"
        f"<figcaption>{caption}</figcaption></figure>"
    )


def say(text: str) -> str:
    return f'<div class="say"><b>چی بگو:</b> {text}</div>'


def warn(text: str) -> str:
    return f'<div class="warn">{text}</div>'


def css() -> str:
    fr = "../../assets/fonts/vazirmatn"
    return f"""
@font-face {{ font-family: Vazirmatn; src: url("{fr}/Vazirmatn-Regular.ttf") format("truetype"); font-weight: 400; }}
@font-face {{ font-family: Vazirmatn; src: url("{fr}/Vazirmatn-Medium.ttf") format("truetype"); font-weight: 500; }}
@font-face {{ font-family: Vazirmatn; src: url("{fr}/Vazirmatn-SemiBold.ttf") format("truetype"); font-weight: 600; }}
@font-face {{ font-family: Vazirmatn; src: url("{fr}/Vazirmatn-Bold.ttf") format("truetype"); font-weight: 700; }}
:root {{ --navy:#163a5f; --teal:#0f6b64; --gold:#8a5a00; --ink:#1b2430; --muted:#4a5568; --line:#d7e0ea; }}
* {{ box-sizing: border-box; }}
html, body {{
  margin: 0; padding: 0; background: #fff; color: var(--ink);
  font-family: Vazirmatn, "Noto Sans Arabic", Tahoma, sans-serif;
  font-size: 12pt; line-height: 1.95; direction: rtl; text-align: right;
}}
@page {{ size: A4; margin: 15mm 14mm 16mm 14mm; }}
@media print {{ html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  h1.ch {{ page-break-before: always; }}
  figure, table, .say, .warn, .box, .qa {{ page-break-inside: avoid; }}
}}
.en {{ unicode-bidi: isolate; direction: ltr; display: inline; font-family: "DejaVu Sans", "Segoe UI", Vazirmatn, sans-serif; font-weight: 700; white-space: nowrap; color: #14365a; padding: 0 1px; }}
.cover {{ min-height: 250mm; border: 2px solid var(--navy); padding: 18mm 12mm; display: flex; flex-direction: column; justify-content: space-between; }}
.cover h1 {{ font-size: 22pt; color: var(--navy); line-height: 1.6; margin: 10px 0; }}
.uni {{ font-size: 16pt; font-weight: 700; color: var(--navy); text-align: center; }}
.badge {{ display:inline-block; background: var(--navy); color:#fff; padding: 4px 14px; border-radius: 999px; font-size: 11pt; }}
h1.ch {{ background: linear-gradient(90deg,#163a5f,#1e4d7b); color:#fff; padding: 9px 12px; border-radius: 8px; font-size: 17pt; }}
h2 {{ color: var(--navy); border-bottom: 2px solid #c5d6e8; padding-bottom: 3px; font-size: 13.5pt; }}
p {{ margin: 0 0 9px; text-align: justify; }}
ul, ol {{ margin: 4px 0 12px; padding: 0 20px 0 0; }}
.say {{ background:#eef7f4; border-right: 5px solid var(--teal); padding: 8px 12px; border-radius: 8px; margin: 10px 0; }}
.warn {{ background:#fff8ee; border-right: 5px solid #c47b12; padding: 8px 12px; border-radius: 8px; margin: 10px 0; }}
.box {{ background:#f4f7fb; border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; margin: 10px 0; }}
.formula {{ direction:ltr; unicode-bidi:isolate; background:#f7f9fc; border:1px solid #cfdceb; border-left:4px solid #1e4d7b; border-radius:8px; padding:10px 12px; margin:12px auto; text-align:center; font-family:"DejaVu Serif","Times New Roman",serif; font-size:13pt; }}
table {{ width:100%; border-collapse: collapse; margin: 8px 0 14px; font-size: 10.5pt; }}
th, td {{ border:1px solid #c9d6e3; padding: 6px 7px; vertical-align: top; }}
th {{ background:#163a5f; color:#fff; }}
tr:nth-child(even) td {{ background:#f5f8fc; }}
tr.hl td {{ background:#e7f4ef !important; font-weight:700; }}
td.ltr, th.ltr {{ direction:ltr; unicode-bidi:isolate; text-align:center; font-family:"DejaVu Sans", Vazirmatn, sans-serif; }}
figure {{ margin: 12px 0; text-align:center; }}
figure img {{ max-width:100%; height:auto; border:1px solid var(--line); border-radius:8px; background:#fff; }}
figcaption {{ margin-top:5px; font-size:10pt; color:var(--muted); }}
.qa {{ background:#fffdf6; border:1px solid #ead9a8; border-radius:10px; padding:9px 12px; margin:9px 0; }}
.qa .q {{ font-weight:700; color:var(--gold); }}
.step {{ background:#fff; border:1px solid var(--line); border-radius:8px; padding:8px 12px; margin:8px 0; }}
.step b {{ color:var(--navy); }}
.meta td:first-child {{ width:34%; color:var(--muted); }}
"""


def body() -> str:
    return f"""
<section class="cover">
  <div style="text-align:center">
    <p class="uni">دانشگاه شهید بهشتی</p>
    <p style="text-align:center;color:#4a5568">دانشکده مهندسی و علوم کامپیوتر — گرایش هوش مصنوعی</p>
    <div class="badge">گزارش آمادگی ارائه — برای خواندن امشب و گفتن فردا</div>
  </div>
  <div style="text-align:center">
    <h1>بهینه‌سازی مصرف انرژی در شبکه‌های اینترنت اشیا با یادگیری تقویتی عمیق</h1>
    <p class="en" dir="ltr" style="display:block;text-align:center;font-size:13pt">IoT Energy Optimization using Deep Reinforcement Learning (DQN)</p>
    <p>این فایل بازنویسیِ گزارش رسمی داخل {en("docs/report")} است، اما برای ارائه شفاهی نوشته شده: چه کار کردید، فرقش با مقاله‌ها چیست، فردا چه بگویید و داشبورد را چطور اجرا کنید.</p>
  </div>
  <table class="meta" style="width:82%;margin:0 auto">
    <tr><td>دانشجو</td><td>امیرمحمد ذکاوتی اول</td></tr>
    <tr><td>استاد راهنما</td><td>دکتر منیره عبدوس</td></tr>
    <tr><td>منبع اصلی</td><td>گزارش پروژه کارشناسی، تابستان ۱۴۰۵</td></tr>
    <tr><td>نتایج رسمی</td><td>۳ گره، افق ۵۰، آموزش ۶۰۰۰، میانگین ۵ اپیزود، بذر ۴۲</td></tr>
  </table>
</section>

<h1 class="ch">۰. نقشه ارائه فردا — اول این را بخوانید</h1>
<p>گزارش رسمی پروژه سه فصل دارد: کلیات، مفاهیم و کارهای مرتبط، روش و نتایج. ارائه شما باید همین سه فصل را بگوید، نه جزئیات تک‌تک فایل‌های کد. زمان پیشنهادی ۱۵ تا ۲۰ دقیقه صحبت + پرسش.</p>
<table>
  <tr><th>دقیقه</th><th>چه بگویید</th><th>چه نشان دهید</th></tr>
  <tr><td>۰ تا ۲</td><td>عنوان، مسئله یک‌جمله‌ای، چرا انرژی مهم است</td><td>شکل اکوسیستم {en("IoT")}</td></tr>
  <tr><td>۲ تا ۵</td><td>اهداف و محدوده؛ چه چیزی را عمداً انجام ندادید</td><td>شکل مسئله سه‌ضلعی و اهداف</td></tr>
  <tr><td>۵ تا ۸</td><td>مقاله‌ها و فرق کار شما با آن‌ها</td><td>جدول مقایسه فصل ۲</td></tr>
  <tr><td>۸ تا ۱۳</td><td>معماری، انرژی فاصله‌آگاه، کانال، پاداش، {en("DQN")}</td><td>خط لوله روش + یک فرمول</td></tr>
  <tr><td>۱۳ تا ۱۷</td><td>نتایج جدول و تفسیر نمودار</td><td>جدول ۳-۳ و شکل مقایسه سیاست‌ها</td></tr>
  <tr><td>۱۷ تا ۲۰</td><td>محدودیت، آینده، جمع‌بندی یک جمله‌ای</td><td>داشبورد زنده اگر وقت بود</td></tr>
</table>
{say("یک جمله اول ارائه: «من یک شبیه‌ساز شبکه حسگر ساختم که در آن عامل DQN برای هر گره بین ارسال و خواب تصمیم می‌گیرد تا هم عمر شبکه بماند هم داده به دروازه برسد.»")}
<div class="box">
<b>چهار عدد که باید حفظ باشید:</b>
طول عمر {en("DQN")} = ۴۹٫۴ گام &nbsp;|&nbsp; بسته موفق = ۲۹٫۴ &nbsp;|&nbsp;
{en("PDR")} = ۰٫۷۶ &nbsp;|&nbsp; میانگین {en("AoI")} = ۱۶٫۲
</div>
{warn("اگر داشبورد را با ۱۰ گره و آموزش کوتاه اجرا کنید، ممکن است DQN از Random ضعیف‌تر دیده شود. اعداد رسمی فقط برای ۳ گره و ۶۰۰۰ گام آموزش معتبرند. این را خودتان اول بگویید.")}

<h1 class="ch">۱. مسئله، اهمیت و کاری که واقعاً انجام دادید</h1>
<h2>۱-۱ مسئله به زبان ارائه</h2>
<p>اینترنت اشیا ({en("Internet of Things")} یا {en("IoT")}) شبکه دستگاه‌هایی است که حس می‌کنند و داده می‌فرستند. طبق {en("Transforma Insights")} تعداد اتصالات از حدود ۲۱ میلیارد در ۲۰۲۵ به حدود ۴۸ میلیارد در ۲۰۳۵ می‌رسد [1]. خیلی از گره‌ها باتری محدود دارند و تعویض باتری سخت یا غیرممکن است.</p>
<p>مسئله این پروژه یک تصمیم دودویی در هر گام زمانی است:</p>
<ul>
  <li><b>ارسال ({en("transmit")}):</b> حس کردن + ساخت بسته + پرداخت انرژی ارسال. داده تازه‌تر می‌شود، باتری زودتر تمام می‌شود.</li>
  <li><b>خواب ({en("sleep")}):</b> هزینه خیلی کم. انرژی می‌ماند، ولی اگر همه بخوابند شبکه هیچ سرویسی ندارد.</li>
</ul>
{fig("report_images/iot_ecosystem_overview.png", "شکل ۱-۱ گزارش رسمی. تمرکز پروژه لایه اول است: گره حسگر تا دروازه، نه ابر.")}
{fig("report_images/Energy Optimization.png", "شکل ۱-۲. سه ضلع مسئله: مصرف انرژی، تأخیر/کهنگی اطلاعات، اتلاف بسته.")}
{say("بگویید: «اگر همیشه ارسال کنیم شبکه می‌میرد؛ اگر همیشه بخوابیم هیچ داده‌ای نیست. کار من ساختن سیاستی است که این سه ضلع را با هم مصالحه کند.»")}

<h2>۱-۲ اهداف واقعی پروژه</h2>
{fig("report_images/project_goals.png", "شکل ۱-۳. چهار شاخه کار: شبیه‌سازی، انرژی، یادگیری تقویتی عمیق، ارزیابی.")}
<ol>
  <li>شبیه‌ساز گره، بسته، دروازه، انرژی فاصله‌آگاه، کانال با افت بسته، و سن اطلاعات ({en("AoI")}).</li>
  <li>محیط استاندارد {en("Gymnasium")} و تابع پاداش چندهدفه.</li>
  <li>آموزش عامل {en("DQN")} با {en("Stable-Baselines3")}.</li>
  <li>مقایسه با سه خط‌پایه: ارسال دائمی، خواب دائمی، تصادفی.</li>
  <li>داشبورد {en("Streamlit")} برای اجرا، آموزش و مقایسه.</li>
</ol>

<h2>۱-۳ محدوده — این را با افتخار بگویید نه با خجالت</h2>
<ul>
  <li>شبیه‌سازی نرم‌افزاری است؛ سخت‌افزار واقعی ندارد.</li>
  <li>ارتباط تک‌گام به دروازه است؛ مسیریابی چندگامه ندارد.</li>
  <li>حداکثر ۱۰ گره برای سازگاری با {en("DQN")} گسسته.</li>
  <li>داده حسگر مصنوعی است.</li>
  <li>مدل کانال و انرژی آموزشی و فاصله‌محور است، نه مدل رادیوی کامل.</li>
  <li>در کد فعلی صف بسته جداگانه وجود ندارد؛ تصمیم هر گام فوری است.</li>
</ul>
{say("اگر استاد گفت «پس کار شما ساده است» جواب دهید: «ساده بودن عمدی است. شکاف پژوهشی گزارش رسمی همین است: سیستم سبک و قابل توضیح برای تصمیم خواب/ارسال با DQN، نه تکرار مسیریابی پیچیده مقالات.»")}

<h1 class="ch">۲. مفاهیم لازم برای حرف زدن، و فرق با مقاله‌ها</h1>
<h2>۲-۱ چند مفهوم که باید روان بگویید</h2>
<p><b>شبکه حسگر بی‌سیم ({en("WSN")}):</b> تعداد زیادی گره کم‌انرژی که داده را به چاهک یا دروازه می‌فرستند. پرهزینه‌ترین کار معمولاً ارسال رادیویی است [3].</p>
<p><b>سن اطلاعات ({en("Age of Information")} یا {en("AoI")}):</b> چقدر از آخرین به‌روزرسانی موفق در مقصد گذشته. اگر بسته برسد ریست می‌شود، وگرنه هر گام یک واحد زیاد می‌شود. با «تأخیر یک بسته در راه» فرق دارد؛ حتی اگر هیچ بسته‌ای در راه نباشد {en("AoI")} باز هم پیر می‌شود.</p>
<p><b>یادگیری تقویتی ({en("RL")}):</b> عامل با محیط تعامل می‌کند و پاداش می‌گیرد؛ برچسب صحیح از قبل نیست. اجزا: وضعیت، عمل، پاداش، سیاست [2].</p>
<p><b>{en("DQN")}:</b> تابع {en("Q(s,a)")} را با شبکه عصبی تقریب می‌زند. دو ترفند پایداری: حافظه بازپخش تجربه و شبکه هدف. برای عمل گسسته مناسب است؛ برای همین اینجا انتخاب شده.</p>
<div class="formula">Q(s,a) ≈ r + γ max<sub>a′</sub> Q(s′, a′)</div>

<h2>۲-۲ مقاله‌هایی که در گزارش اسم بردید — برای هر کدام یک پاراگراف حرف بزنید</h2>
<p>این‌ها را حفظ نکنید؛ منطق هر کدام را بگویید و بعد فرق خودتان را.</p>

<div class="box">
<b>[1] {en("Transforma Insights")}، ۲۰۲۶.</b>
آمار رشد {en("IoT")} از ۲۱ به ۴۸ میلیارد اتصال. فقط برای انگیزه مقدمه است، نه ورودی شبیه‌ساز.
</div>
<div class="box">
<b>[2] {en("Alsheikh")} و همکاران، ۲۰۱۴.</b>
مرور یادگیری ماشین در {en("WSN")}. به شما اجازه می‌دهد بگویید مدیریت انرژی هوشمند در ادبیات این حوزه جا افتاده است.
</div>
<div class="box">
<b>[3] {en("Mohamed")} و همکاران، ۲۰۱۸.</b>
مرور کاربردها و مسیریابی انرژی‌کارآمد. زمینه محدودیت انرژی و پروتکل‌های کلاسیک.
</div>
<div class="box">
<b>[4] {en("Heinzelman")} و همکاران، {en("LEACH")}، ۲۰۰۰.</b>
پروتکل کلاسیک خوشه‌بندی و چرخش سرخوشه برای پخش مصرف انرژی. نماینده روش سنتی قاعده‌محور. شما {en("LEACH")} را پیاده نکردید؛ آن را به‌عنوان نقطه شروع ادبیات می‌آورید.
</div>
<div class="box">
<b>[5] {en("Kaur")} و {en("Chanak")}، ۲۰۲۱.</b>
مسیریابی هوشمند انرژی‌کارآمد برای {en("IoT")}. پیام اصلی: روش‌های سنتی در شرایط پویا کم می‌آورند و به طرح هوشمند نیاز است.
</div>
<div class="box">
<b>[6] {en("Meng")} و همکاران، ۲۰۱۹.</b>
{en("DRL")} برای بهینه‌سازی توپولوژی شبکه‌های خودسازمان‌ده. نزدیک به ایده شماست ولی مسئله‌شان توپولوژی است نه تصمیم دودویی خواب/ارسال تک‌گام.
</div>
<div class="box">
<b>[7] {en("Liu")} و همکاران، {en("EDRP-GTDQN")}، ۲۰۲۵ — مقاله کلیدی فصل ۲.</b>
مسیریابی انرژی و تأخیر با ترکیب نظریه بازی + شبکه گراف + {en("DQN")}. اول با نظریه بازی سرخوشه انتخاب می‌شود، بعد {en("DQN")} مسیر را می‌چیند. نسبت به {en("LEACH")} و {en("DEEC")} بهبود گزارش کرده‌اند.
<b>فرق با شما:</b> آن‌ها مسیریابی و خوشه‌بندی پیچیده دارند؛ شما مدیریت مستقیم خواب/ارسال در توپولوژی ستاره‌ای ساده. مدل آن‌ها سنگین‌تر است و برای محیط آموزشی سبک مناسب نیست.
</div>
<div class="box">
<b>[8] {en("Banerjee")} و همکاران، {en("NashDQNSleep")}، ۲۰۲۵ — نزدیک‌ترین کار به ایده خواب.</b>
زمان‌بندی خواب در {en("Industrial IoT")} با {en("DQN")} و تعادل نش، برای انرژی و {en("AoI")}. تصمیم توزیع‌شده و هماهنگی بین گره‌ها.
<b>فرق با شما:</b> آن‌ها بازی چندگرهی و محیط صنعتی پیچیده‌اند. شما یک عامل مرکزی، شبکه ساده، و حلقه کامل شبیه‌ساز + داشبورد + مقایسه خط‌پایه دارید. ایده مشترک: {en("DQN")} برای خواب و توجه به {en("AoI")}.
</div>
<div class="box">
<b>[9] {en("Leong")} و همکاران، ۲۰۱۸.</b>
زمان‌بندی حسگر در سامانه سایبر-فیزیکی با {en("DRL")}. نشان می‌دهد زمان‌بندی حسگر با یادگیری تقویتی عمیق یک مسئله شناخته‌شده است.
</div>

{say("جمله جمع‌بندی ادبیات: «مقالات قوی روی مسیریابی، نظریه بازی یا اینترنت اشیا صنعتی تمرکز دارند. شکاف گزارش من این است که یک سامانه سبک، قابل اجرا و قابل توضیح برای تصمیم خواب/ارسال با DQN کم است. کار من پر کردن همین شکاف آموزشی‌پژوهشی است، نه شکست دادن EDRP-GTDQN روی بنچمارک آن‌ها.»")}

<table>
  <tr><th>کار</th><th>تمرکز</th><th>ابزار</th><th>نسبت به پروژه شما</th></tr>
  <tr><td>{en("LEACH")} [4]</td><td>خوشه‌بندی</td><td>قاعده احتمالی</td><td>سنتی؛ خط‌پایه ادبیاتی نه کدی</td></tr>
  <tr><td>{en("EDRP-GTDQN")} [7]</td><td>مسیریابی و تأخیر</td><td>بازی + {en("GCN")} + {en("DQN")}</td><td>پیچیده‌تر؛ خواب ساده ندارد</td></tr>
  <tr><td>{en("NashDQNSleep")} [8]</td><td>خواب و {en("AoI")} صنعتی</td><td>{en("Nash")} + {en("DQN")}</td><td>نزدیک‌ترین ایده؛ مدل سنگین‌تر</td></tr>
  <tr><td>{en("Meng")} / {en("Leong")} [6][9]</td><td>توپولوژی / زمان‌بندی حسگر</td><td>{en("DRL")}</td><td>مسئله متفاوت</td></tr>
  <tr class="hl"><td>پروژه حاضر</td><td>خواب/ارسال تک‌گام</td><td>{en("DQN")} + شبیه‌ساز + داشبورد</td><td>سبک، مقایسه با ۳ خط‌پایه، قابل نمایش</td></tr>
</table>

<h1 class="ch">۳. روش شما، دقیقاً چه پیاده شده</h1>
<h2>۳-۱ معماری چهارلایه</h2>
{fig("report_images/system_architecture_fa.png", "معماری سامانه: رابط کاربری، شبیه‌سازی، یادگیری تقویتی، تحلیل.")}
{fig("report_images/method_pipeline_flow.png", "شکل ۳-۱ گزارش رسمی. جریان: تنظیم پارامتر → شبیه‌سازی → تصمیم عامل → تاریخچه → معیار → مقایسه سیاست‌ها.")}
<ol>
  <li>{en("Streamlit")}: تنظیم پارامتر، اجرا، آموزش، مقایسه.</li>
  <li>شبیه‌سازی در {en("app/simulation/")}: گره، بسته، کانال، انرژی، دروازه، زمان‌بند.</li>
  <li>یادگیری در {en("app/rl/")}: محیط، پاداش، عامل، مربی.</li>
  <li>تحلیل در {en("app/analytics/")}: معیار، مقایسه، نمودار.</li>
</ol>
<p>ورود برنامه {en("main.py")} است. تنظیمات مرکزی در {en("app/config/settings.py")} است.</p>

<h2>۳-۲ یک گام شبیه‌سازی — برای پای تخته</h2>
<ol>
  <li>گره‌های زنده گرفته می‌شوند.</li>
  <li>سیاست برای هر گره {en("transmit")} یا {en("sleep")} می‌دهد.</li>
  <li>اگر ارسال: بیداری، حس کردن (۰٫۰۱ ژول)، ساخت بسته، پرداخت انرژی ارسال فاصله‌آگاه، آزمایش کانال.</li>
  <li>اگر خواب: حدود ۰٫۰۰۱ ژول.</li>
  <li>{en("AoI")} برای تحویل‌شده‌ها ریست، برای بقیه +۱.</li>
  <li>تصویر لحظه‌ای ذخیره می‌شود و به مشاهده و پاداش تبدیل می‌گردد.</li>
</ol>
<div class="formula">E<sub>tx</sub>(d) = 0.05 · [1 + 0.5 · (d / 50)<sup>2</sup>]</div>
<div class="formula">p(d) = clip(1 − 0.35 · (d / 50), 0.45, 1)</div>
<p>نکته مهم: انرژی تلاش ارسال همیشه کم می‌شود، حتی اگر بسته نرسد. دروازه در مرکز ناحیه ۱۰۰×۱۰۰ یعنی نقطه (۵۰، ۵۰) است و فقط بسته‌های موفق را نگه می‌دارد.</p>

<h2>۳-۳ محیط یادگیری</h2>
<p>مشاهده ابعاد {en("2n+3")} دارد: نسبت انرژی هر گره، پرچم زنده بودن، زمان نرمال، نسبت دریافت، {en("AoI")} نرمال. برای ۳ گره یعنی ۹ عدد.</p>
<p>عمل برای {en("n ≤ 10")} به صورت {en("Discrete(2^n)")} است. برای ۳ گره فقط ۸ عمل. هر بیت یک گره است: ۱ ارسال، ۰ خواب. برای همین سقف ۱۰ گره در داشبورد گذاشته شده؛ با ۱۰ گره ۱۰۲۴ عمل دارید و آموزش کوتاه کافی نیست.</p>
<div class="formula">r = 1.0 ΔP + 0.2 α + 0.2 η − 0.5 ΔE − 1.0 ΔD − 0.15 Ā<sub>norm</sub> − 0.2 ΔL</div>
<p>ΔP بسته موفق جدید، α نسبت زنده، η نسبت انرژی، ΔE مصرف همین گام، ΔD مرگ گره، Ā کهنگی نرمال، ΔL افت جدید. وزن‌ها دستی‌اند ({en("heuristic")})؛ اگر استاد پرسید بگویید بهینه‌سازی وزن انجام نشده و این یک محدودیت است.</p>
<p>عامل: {en("Stable-Baselines3 DQN")} با {en("MlpPolicy")}، نرخ یادگیری ۰٫۰۰۱، γ=۰٫۹۵، بافر ۵۰۰۰۰، دسته ۶۴، اکتشاف تا ۰٫۰۵.</p>

<h1 class="ch">۴. نتایج — همان اعداد گزارش رسمی</h1>
<p>تنظیمات جدول ۳-۲ گزارش: ۳ گره، انرژی اولیه ۱ ژول، افق ۵۰، آموزش ۶۰۰۰، ۵ اپیزود، بذر ۴۲، {en("LOSS_FACTOR=0.35")}، کف تحویل ۰٫۴۵.</p>
<table>
  <tr><th>سیاست</th><th class="ltr">Lifetime</th><th class="ltr">Packets</th><th class="ltr">Dropped</th><th class="ltr">PDR</th><th class="ltr">AoI</th><th>انرژی باقی</th></tr>
  <tr><td>ارسال دائمی</td><td class="ltr">15.4</td><td class="ltr">26.6</td><td class="ltr">11.2</td><td class="ltr">0.70</td><td class="ltr">—</td><td class="ltr">0.00</td></tr>
  <tr><td>خواب دائمی</td><td class="ltr">50.0</td><td class="ltr">0.0</td><td class="ltr">0.0</td><td class="ltr">0.00</td><td class="ltr">50.0</td><td class="ltr">2.85</td></tr>
  <tr><td>تصادفی</td><td class="ltr">33.0</td><td class="ltr">26.2</td><td class="ltr">11.2</td><td class="ltr">0.70</td><td class="ltr">—</td><td class="ltr">0.00</td></tr>
  <tr class="hl"><td>{en("DQN")}</td><td class="ltr">49.4</td><td class="ltr">29.4</td><td class="ltr">9.4</td><td class="ltr">0.76</td><td class="ltr">16.2</td><td class="ltr">0.03</td></tr>
</table>
{fig("charts/policy_comparison.png", "شکل ۳-۲ گزارش. DQN عمر نزدیک خواب دائمی، بسته و PDR بهتر از ارسال دائمی.")}
{fig("charts/energy_curves.png", "ارسال دائمی تا حدود گام ۱۵ می‌میرد. تصادفی تا حدود ۳۳. DQN انرژی را جیره‌بندی می‌کند و تا نزدیک ۵۰ زنده می‌ماند.")}
{fig("charts/aoi_curves.png", "خواب دائمی خط راست با شیب ۱ است. DQN گاهی سن را بالا می‌برد و بعد با ارسال ریست می‌کند؛ تازگی فدای زنده ماندن کامل شبکه نمی‌شود.")}
{say("تفسیر یک جمله‌ای جدول: «ارسال دائمی سرویس می‌دهد ولی زود می‌میرد؛ خواب دائمی زنده می‌ماند ولی سرویس صفر است؛ DQN تقریباً تا آخر زنده می‌ماند و از ارسال دائمی هم بسته موفق بیشتری می‌رساند چون افت کمتری دارد.»")}
{warn("AoI پایان‌کار برای سیاست‌هایی که همه گره‌ها مرده‌اند گمراه‌کننده است، چون میانگین فقط روی زنده‌ها حساب می‌شود و ممکن است صفر دیده شود. برای Always Transmit از روی منحنی زمانی حرف بزنید نه از عدد پایانی.")}
<p>بهره‌وری انرژی (بسته موفق بر ژول) در داده خام حدود ۹٫۸۹ برای {en("DQN")} در برابر ۸٫۸۷ برای ارسال دائمی است. جهش اصلی طول عمر است نه چند درصد بهره ژول.</p>
<p><b>محدودیت نتایج:</b> فقط همین تنظیمات. مدل کانال آموزشی است. فضای عمل با افزایش n منفجر می‌شود. ۵ اپیزود برای آزمون آماری سخت کم است.</p>
<p><b>کار آینده اگر پرسیدند:</b> {en("PPO")} یا چندعاملی برای شبکه بزرگ‌تر، وارد کردن فاصله در مشاهده، مدل کانال دقیق‌تر، آزمایش سخت‌افزار مثل {en("ESP32")}.</p>

<h1 class="ch">۵. فردا چطور اجرا کنید و چه چیزی نشان دهید</h1>
<h2>۵-۱ امشب، قبل از خواب — این را انجام دهید</h2>
<div class="step"><b>۱.</b> در پوشه پروژه محیط مجازی را فعال کنید و وابستگی را نصب کنید اگر از قبل نیست:
<div class="formula" style="text-align:left">pip install -r requirements.txt</div></div>
<div class="step"><b>۲.</b> داشبورد را باز کنید:
<div class="formula" style="text-align:left">streamlit run main.py</div></div>
<div class="step"><b>۳.</b> در نوار کناری دقیقاً این‌ها را بگذارید تا به گزارش نزدیک شوید:<br>
تعداد گره = <b>۳</b> (نه ۱۰ پیش‌فرض) &nbsp;|&nbsp; حداکثر گام = <b>۵۰</b> (نه ۲۰۰) &nbsp;|&nbsp;
انرژی اولیه = ۱ &nbsp;|&nbsp; بذر = ۴۲ &nbsp;|&nbsp; گام آموزش = <b>۶۰۰۰</b> (لغزنده ممکن است روی ۳۰۰۰ باشد؛ جابه‌جا کنید)</div>
<div class="step"><b>۴.</b> {en("Train DQN")} را بزنید و صبر کنید تا مدل در {en("experiments/models/dqn_iot_energy")} ذخیره شود. این کار را امشب بکنید تا فردا آموزش زنده طول نکشد.</div>
<div class="step"><b>۵.</b> یک‌بار {en("Compare Policies")} را بزنید و ببینید جدول ظاهر می‌شود. اسکرین‌شات بگیرید برای پشتیبان اگر وای‌فای سالن مشکل داشت.</div>

<h2>۵-۲ سناریوی نمایش زنده در جلسه</h2>
<p>اگر وقت کم است، آموزش را تکرار نکنید؛ مدل ذخیره‌شده را بار کنید.</p>
<ol>
  <li>همان تنظیمات ۳ / ۵۰ / ۴۲ را نگه دارید.</li>
  <li>سیاست را {en("Always Transmit")} بگذارید و {en("Run Simulation")} بزنید. نشان دهید شبکه زود می‌میرد و بسته می‌آید.</li>
  <li>سیاست {en("Always Sleep")} را اجرا کنید. نشان دهید انرژی می‌ماند و بسته صفر است، {en("AoI")} بالا می‌رود.</li>
  <li>سیاست {en("DQN")} را اجرا کنید. نقشه گره‌ها، منحنی انرژی و {en("PDR")} را نشان دهید.</li>
  <li>در پایان {en("Compare Policies")} تا جدول چهار سیاست یک‌جا دیده شود.</li>
</ol>
{warn("داشبورد انگلیسی است. روی دکمه‌ها با انگشت توضیح فارسی بدهید: Run Simulation یعنی اجرای یک سیاست؛ Train DQN یعنی آموزش؛ Compare Policies یعنی مقایسه چند اپیزودی.")}
<p>اگر آموزش یا مدل خراب شد، وحشت نکنید. نمودارهای رسمی داخل گزارش و پوستر را نشان دهید و بگویید این‌ها با همان تنظیمات جدول ۳-۲ بازتولید شده‌اند. فایل‌ها:</p>
<ul>
  <li>{en("assets/charts/policy_comparison.png")}</li>
  <li>{en("assets/charts/energy_curves.png")}</li>
  <li>{en("assets/charts/aoi_curves.png")}</li>
  <li>پوستر: {en("docs/poster/poster.html")} یا {en("Final_Poster_A1.pdf")} اگر چاپ کرده‌اید</li>
  <li>گزارش رسمی: {en("docs/report/IoT-Energy-Optimization-DRL-Report.pdf")}</li>
</ul>

<h2>۵-۳ چه چیزهایی را نشان ندهید مگر پرسیدند</h2>
<ul>
  <li>کد داخلی {en("reward.py")} خط‌به‌خط — مگر جزئیات پاداش را بخواهند.</li>
  <li>نوت‌بوک‌ها؛ فقط بگویید شش دفتر آزمایش گام‌به‌گام وجود دارد.</li>
  <li>آموزش ۶۰۰۰ گام زنده وسط حرف زدن؛ وقت را می‌کشد.</li>
</ul>

<h1 class="ch">۶. پرسش‌هایی که احتمال دارد فردا بیاید</h1>
<div class="qa"><div class="q">چرا {en("DQN")} نه {en("PPO")}؟</div>
<div class="a">چون عمل گسسته و برای ۳ گره فقط ۸ تاست. {en("DQN")} انتخاب استاندارد همین فضاست. برای شبکه بزرگ‌تر {en("PPO")} یا چندعاملی منطقی‌تر است و در کارهای آینده آمده.</div></div>
<div class="qa"><div class="q">چرا ۳ گره نه ۱۰؟</div>
<div class="a">با ۳ گره فضای عمل ۸ تایی است و ۶۰۰۰ گام برای نشان دادن یادگیری کافی است. با ۱۰ گره ۱۰۲۴ عمل است و بودجه کوتاه معمولاً کم است. عدد ۳ برای شفافیت است.</div></div>
<div class="qa"><div class="q">مختصات گره را عامل می‌بیند؟</div>
<div class="a">نه مستقیم. فاصله از راه تخلیه انرژی و افت بسته دیده می‌شود. این محدودیت مشاهده است.</div></div>
<div class="qa"><div class="q">چرا از کتابخانه آماده استفاده کردید؟</div>
<div class="a">ارزش کار در صورت‌بندی مسئله {en("IoT")} و حلقه ارزیابی است، نه بازنویسی {en("DQN")}. استفاده از {en("Stable-Baselines3")} رایج و قابل دفاع است.</div></div>
<div class="qa"><div class="q">این پژوهش است یا مهندسی؟</div>
<div class="a">هر دو. پژوهش در {en("MDP")}، پاداش و مقایسه؛ مهندسی در معماری ماژولار و داشبورد.</div></div>
<div class="qa"><div class="q">اگر {en("DQN")} از تصادفی بدتر شد چه می‌گویید؟</div>
<div class="a">همگرا نشده: فضا بزرگ یا بودجه کم یا پاداش بد. در تنظیم رسمی گزارش این اتفاق نیفتاده.</div></div>
<div class="qa"><div class="q">نوآوری شما دقیقاً چیست؟</div>
<div class="a">الگوریتم {en("DQN")} مال ادبیات است. مال شما: شبیه‌ساز فاصله‌آگاه با افت و {en("AoI")}، مشاهده و پاداش، اتصال به عامل، مقایسه سه خط‌پایه، و ابزار نمایش. طبق شکاف فصل ۲: سامانه سبک خواب/ارسال.</div></div>

<h1 class="ch">۷. برگه تقلب یک‌صفحه‌ای — قبل از ورود به سالن</h1>
<div class="box">
<p><b>عنوان:</b> بهینه‌سازی انرژی {en("IoT")} با {en("DQN")}.</p>
<p><b>مسئله:</b> هر گره در هر گام ارسال یا خواب.</p>
<p><b>روش:</b> شبیه‌ساز + {en("Gymnasium")} + {en("DQN")} + سه خط‌پایه + داشبورد.</p>
<p><b>نتیجه:</b> عمر ۴۹٫۴، بسته ۲۹٫۴، {en("PDR")} برابر ۰٫۷۶، {en("AoI")} برابر ۱۶٫۲.</p>
<p><b>فرق با مقالات:</b> آن‌ها مسیریابی/بازی/صنعت سنگین؛ من تصمیم خواب/ارسال تک‌گام و قابل نمایش.</p>
<p><b>محدودیت:</b> تک‌گام، ۳ گره، کانال ساده، پاداش دستی.</p>
<p><b>دمو:</b> گره=۳، گام=۵۰، بذر=۴۲، آموزش از قبل، بعد مقایسه سیاست‌ها.</p>
<p><b>جمله آخر:</b> «یادگیری تقویتی عمیق در این شبیه‌سازی کنترل‌شده، مصالحه بهتری میان عمر شبکه و سرویس داده ساخت؛ تعمیم به سخت‌افزار واقعی کار بعدی است.»</p>
</div>
<p style="color:#4a5568;font-size:10.5pt">منابع کامل همان ۹ مرجع گزارش رسمی در {en("docs/report/IoT-Energy-Optimization-DRL-Report.pdf")} و {en("docs/references/references.bib")} است. این فایل جایگزین آن گزارش نیست؛ راهنمای گفتن آن است.</p>
"""


def build_html() -> str:
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<title>گزارش آمادگی ارائه فردا</title>
<style>{css()}</style>
</head>
<body>
{body()}
</body>
</html>
"""


def main() -> None:
    SRC.mkdir(parents=True, exist_ok=True)
    HTML_PATH.write_text(build_html(), encoding="utf-8")
    tmp = SRC / "_tmp.pdf"
    if tmp.exists():
        tmp.unlink()
    cmd = [
        str(CHROME),
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        "--no-pdf-header-footer",
        "--allow-file-access-from-files",
        "--user-data-dir=/tmp/chrome-briefing-pdf",
        "--virtual-time-budget=8000",
        f"--print-to-pdf={tmp.resolve()}",
        HTML_PATH.resolve().as_uri(),
    ]
    subprocess.run(cmd, check=True, cwd=str(ROOT), timeout=90)
    tmp.replace(PDF_PATH)
    # copy persian name
    PDF_FA.write_bytes(PDF_PATH.read_bytes())
    import fitz

    doc = fitz.open(PDF_PATH)
    print("pages", doc.page_count, "bytes", PDF_PATH.stat().st_size)
    doc.close()


if __name__ == "__main__":
    main()
