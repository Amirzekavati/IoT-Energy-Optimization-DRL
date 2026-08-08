# متن نهایی پوستر

**عنوان فارسی:** بهینه‌سازی مصرف انرژی در شبکه‌های اینترنت اشیا با یادگیری تقویتی عمیق  
**عنوان انگلیسی:** IoT Energy Optimization using Deep Reinforcement Learning (DQN)

**دانشجو:** امیرمحمد ذکاوتی  
**استاد راهنما:** دکتر منیره عبدوس  
**دانشگاه:** دانشگاه شهید بهشتی  
**سال:** ۱۴۰۴

## نتایج ران نهایی (seed=42)

تنظیمات: ۳ نود | افق ۵۰ | آموزش ۶۰۰۰ | میانگین ۵ اپیزود

| سیاست | Lifetime | Packets | PDR | Mean AoI | Energy باقی‌مانده |
|-------|----------|---------|-----|----------|-------------------|
| Always Transmit | 15.4 | 26.6 | 0.70 | — | 0.00 |
| Always Sleep | 50.0 | 0.0 | 0.00 | 50.0 | 2.85 |
| Random | 33.0 | 26.2 | 0.70 | — | 0.00 |
| **DQN** | **49.4** | **29.4** | **0.76** | **16.2** | **0.03** |

## تصاویر داخل پوستر

- معماری: `assets/architecture/high_level_architecture.png`
- مقایسه معیارها: `assets/charts/policy_comparison.png`
- انرژی در زمان: `assets/charts/energy_curves.png`
- AoI در زمان: `assets/charts/aoi_curves.png`
- بسته‌ها در زمان: `assets/charts/packets_curves.png`
- آمار خام: `assets/charts/poster_metrics.json`
