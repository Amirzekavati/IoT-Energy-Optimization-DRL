# فصل ۳ — روش پیشنهادی و پیاده‌سازی

## ۳-۱ معماری کلی سیستم

سیستم از چهار لایه تشکیل شده است:

1. لایه رابط کاربری (Streamlit)
2. موتور شبیه‌سازی (Node, Packet, Gateway, Energy, Scheduler, Simulator)
3. لایه یادگیری تقویتی (Environment, Reward, DQN, Trainer)
4. لایه تحلیل و ارزیابی (Metrics, Evaluator, Plots)

تصویر پیشنهادی: `assets/architecture/high_level_architecture.png`  
دیاگرام منبع: `docs/diagrams/high_level_architecture.mmd`

## ۳-۲ مدل نود و انرژی

- حالت‌ها: `active`, `sleep`, `dead`
- هزینه‌ها: Transmit، Receive، Sense، Sleep
- پارامترها در `app/config/settings.py`

## ۳-۳ تولید بسته و Gateway

- پس از Sense، نود بسته می‌سازد و در صورت Transmit به Gateway می‌فرستد
- Gateway بسته‌های تحویل‌شده را ذخیره می‌کند

## ۳-۴ شبیه‌ساز و زمان‌بند

- `Simulator`: حلقه زمانی، ثبت history
- سیاست‌های پایه:
  - Always Transmit
  - Always Sleep

## ۳-۵ محیط یادگیری تقویتی

- کتابخانه: Gymnasium
- مشاهده: نسبت انرژی نودها + پرچم زنده بودن + گام نرمال + نسبت دریافت
- عمل: برای \(n \le 10\) به صورت `Discrete(2^n)` (هر بیت = خواب/ارسال یک نود)
- پاداش: تشویق تحویل بسته و زنده ماندن؛ جریمه مصرف انرژی و مرگ نود

## ۳-۶ عامل DQN

- پیاده‌سازی با Stable-Baselines3
- آموزش، ذخیره و بارگذاری مدل در `experiments/models/`
- ارزیابی و مقایسه در ماژول `app/analytics`

## ۳-۷ داشبورد

- اجرای سیاست‌ها
- آموزش DQN
- مقایسه سیاست‌ها و نمایش نمودارها

دستور اجرا:

```bash
streamlit run main.py
```
