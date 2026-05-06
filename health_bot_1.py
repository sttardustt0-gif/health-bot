#!/usr/bin/env python3
"""
Telegram Health Bot - Arabic Clinical Nutrition Bot
Requirements: pip install python-telegram-bot==20.7
Usage: Set BOT_TOKEN environment variable or replace directly in the script.
"""

import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8755358074:AAF2tqx3YN4MmMwrhyAGa3FlOONBbck-M8o")

# ─── Button Labels ────────────────────────────────────────────────────────────
BTN_DIABETES      = "مرض السكري"
BTN_PRESSURE      = "ارتفاع ضغط الدم"
BTN_HEART         = "أمراض القلب"
BTN_LIVER         = "أمراض الكبد"
BTN_KIDNEY        = "أمراض الكلى"
BTN_IBS           = "القولون العصبي"
BTN_CELIAC        = "السلياك"
BTN_BMI           = "حساب مؤشر كتلة الجسم (BMI)"
BTN_NUTRITION     = "حساب الاحتياجات الغذائية"
BTN_CONTACT       = "📞 تواصل معنا"

# ─── Responses ────────────────────────────────────────────────────────────────
RESPONSES = {
    BTN_DIABETES: """*مرض السكري*

📌 *الأعراض:*
• زيادة العطش
• كثرة التبول
• التعب
• تشوش الرؤية

🍽️ *التغذية السريرية:*
• تنظيم الوجبات
• تقليل السكريات
• اختيار الحبوب الكاملة
• الإكثار من الألياف

💊 *أدوية شائعة:*
• الميتفورمين
• الإنسولين

⚠️ *التداخلات:*
• انخفاض السكر عند تخطي الوجبات
• الحذر مع المكملات

⚠️ *تنويه:*
المعلومات للتثقيف الصحي ولا تغني عن الطبيب.""",

    BTN_PRESSURE: """*ارتفاع ضغط الدم*

📌 *الأعراض:*
• صداع
• دوخة
• غالباً بدون أعراض

🍽️ *التغذية السريرية:*
• تقليل الملح
• تجنب الأطعمة المصنعة

💊 *أدوية شائعة:*
• مدرات البول
• أدوية الضغط

⚠️ *التداخلات:*
• زيادة الملح تقلل فعالية العلاج

⚠️ *تنويه:*
المعلومات للتثقيف الصحي ولا تغني عن الطبيب.""",

    BTN_HEART: """*أمراض القلب*

📌 *الأعراض:*
• ألم في الصدر
• ضيق تنفس

🍽️ *التغذية السريرية:*
• تقليل الدهون
• تقليل الملح

💊 *أدوية شائعة:*
• مميعات الدم

⚠️ *التداخلات:*
• تتأثر بفيتامين K

⚠️ *تنويه:*
المعلومات للتثقيف الصحي ولا تغني عن الطبيب.""",

    BTN_LIVER: """*أمراض الكبد*

📌 *الأعراض:*
• تعب
• اصفرار الجلد

🍽️ *التغذية السريرية:*
• تقليل الدهون
• تجنب الكحول

💊 *أدوية:*
• حسب الحالة

⚠️ *التداخلات:*
• الحذر من الأدوية

⚠️ *تنويه:*
المعلومات للتثقيف الصحي ولا تغني عن الطبيب.""",

    BTN_KIDNEY: """*أمراض الكلى*

📌 *الأعراض:*
• تورم
• تعب

🍽️ *التغذية السريرية:*
• تقليل الصوديوم
• التحكم بالبروتين

💊 *أدوية:*
• أدوية ضغط

⚠️ *التداخلات:*
• الحذر من البوتاسيوم

⚠️ *تنويه:*
المعلومات للتثقيف الصحي ولا تغني عن الطبيب.""",

    BTN_IBS: """ *القولون العصبي*

📌 *الأعراض:*
• انتفاخ
• ألم

🍽️ *التغذية السريرية:*
• تقليل المهيجات
• تنظيم الوجبات

💊 *أدوية:*
• مضادات التقلص

⚠️ *التداخلات:*
• التوتر يزيد الحالة

⚠️ *تنويه:*
المعلومات للتثقيف الصحي ولا تغني عن الطبيب.""",

    BTN_CELIAC: """ *السلياك*

📌 *الأعراض:*
• إسهال
• انتفاخ

🍽️ *التغذية السريرية:*
• منع الغلوتين

💊 *العلاج:*
• حمية فقط

⚠️ *التداخلات:*
• أي غلوتين يضر

⚠️ *تنويه:*
المعلومات للتثقيف الصحي ولا تغني عن الطبيب.""",

    BTN_BMI: """ *حساب مؤشر كتلة الجسم (BMI)*

يمكنك الحساب من هنا:
🔗 https://www.calculator.net/bmi-calculator.html

 *التصنيف:*
• أقل من 18.5 ← نقص وزن
• 18.5 – 24.9 ← طبيعي
• 25 – 29.9 ← زيادة وزن
• 30+ ← سمنة

⚠️ *تنويه:*
النتائج تقديرية ولا تُغني عن استشارة مختص.""",

    BTN_NUTRITION: """ *حساب الاحتياجات الغذائية*

احسب احتياجك اليومي من هنا:
🔗 https://www.calculator.net/calorie-calculator.html

📌 *يشمل:*
• السعرات
• البروتين
• الهدف الغذائي

⚠️ *تنويه:*
النتائج للتثقيف الصحي وليست خطة علاجية.""",

    BTN_CONTACT: """📞 *تواصل معنا*

نسعد بخدمتكم والإجابة على استفساراتكم المتعلقة بالتغذية السريرية.

يمكنكم التواصل عبر:

📱 *رقم الهاتف:*
8001188111

🕒 *ساعات العمل:*
من الأحد إلى الخميس
من 9:00 صباحاً إلى 5:00 مساءً

💬 سيتم الرد على جميع الاستفسارات في أقرب وقت ممكن.

نشكر ثقتكم 💙

⚠️ *تنويه:*
خدمة التواصل مخصصة للاستفسارات العامة، ولا تُستخدم كبديل عن الاستشارة الطبية المباشرة.""",
}

# ─── Keyboard Layout ──────────────────────────────────────────────────────────
MAIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(BTN_DIABETES),   KeyboardButton(BTN_PRESSURE)],
        [KeyboardButton(BTN_HEART),      KeyboardButton(BTN_LIVER)],
        [KeyboardButton(BTN_KIDNEY),     KeyboardButton(BTN_IBS)],
        [KeyboardButton(BTN_CELIAC),     KeyboardButton(BTN_BMI)],
        [KeyboardButton(BTN_NUTRITION),  KeyboardButton(BTN_CONTACT)],
    ],
    resize_keyboard=True,
)

# ─── Handlers ────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "مرحباً بك في خدمات التغذية السريرية 🏥💙\n\nنقدّم لك إرشادات غذائية مبنية على أسس علمية لدعم صحتك وتحسين نمط حياتك.\n\n📌 *خدماتنا تشمل:*\n• معلومات شاملة عن الأمراض (السكري، الضغط، القلب، الكبد، الكلى، القولون، وغيرها)\n• إرشادات التغذية السريرية لكل حالة\n• حساب مؤشر كتلة الجسم (BMI)\n• حساب الاحتياجات الغذائية اليومية\n• خدمة التواصل للاستفسارات والدعم\n\n⚠️ *تنويه:*\nجميع المعلومات المقدمة تندرج ضمن التثقيف الصحي في مجال التغذية السريرية، ولا تُغني عن استشارة الطبيب أو الأخصائي الصحي المختص.\n\nيرجى اختيار الخدمة المناسبة من القائمة أدناه 👇",
        reply_markup=MAIN_KEYBOARD,
        parse_mode="Markdown",
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    response = RESPONSES.get(text)
    if response:
        await update.message.reply_text(response, parse_mode="Markdown", reply_markup=MAIN_KEYBOARD)
    else:
        await update.message.reply_text(
            "⚠️ لم أفهم طلبك. يرجى اختيار أحد الخيارات من القائمة.",
            reply_markup=MAIN_KEYBOARD,
        )

# ─── Main ────────────────────────────────────────────────────────────────────
def main() -> None:
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Please set your BOT_TOKEN before running.")
        print("   Option 1: export BOT_TOKEN='your_token_here'")
        print("   Option 2: Replace 'YOUR_BOT_TOKEN_HERE' in the script.")
        return

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button))

    print("✅ Bot is running... Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
