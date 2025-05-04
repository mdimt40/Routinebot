import requests
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
import json

# Telegram Bot Token
TOKEN = "7688240432:AAEZ79y-SIa1GfEteuF5S8vyWXHY_KGMLDo"  # Replace with your actual bot token

# Configure logging
logging.basicConfig(
    filename='users.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    filemode='a'
)

# HTML log initialization
def init_html_log():
    with open("diuresult_log.html", "a", encoding="utf-8") as f:
        if f.tell() == 0:
            f.write("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>DIU Result Bot Logs</title>
                <style>
                    body {
                        font-family: 'Poppins', Arial, sans-serif;
                        padding: 20px;
                        background-color: #f5f5f5;
                    }
                    .log {
                        margin-bottom: 12px;
                        padding: 10px;
                        background: white;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        border-left: 4px solid #3BAE47;
                    }
                    .time {
                        color: #3BAE47;
                        font-weight: bold;
                    }
                    h2 {
                        color: #3BAE47;
                        border-bottom: 2px solid #3BAE47;
                        padding-bottom: 8px;
                    }
                    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');
                </style>
            </head>
            <body>
            <h2>📊 DIU Result Bot Logs</h2>
            """)

def write_html_log(message):
    with open("diuresult_log.html", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f'<div class="log"><span class="time">[{timestamp}]</span> {message}</div>\n')

# Main Menu Keyboard
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📚 Check Result", callback_data='check_result')],
        [InlineKeyboardButton("ℹ️ About", callback_data='about'),
         InlineKeyboardButton("🆘 Help", callback_data='help')],
        [InlineKeyboardButton("🌟 Follow us", url="https://facebook.com/diuinsider.bd"),
         InlineKeyboardButton("🌐Website", url="https://diuresult.mdimtiaz.site")]
    ]
    return InlineKeyboardMarkup(keyboard)

# /start command with enhanced design
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_msg = f"""
✨ *Welcome {user.first_name} to DIU Result Bot * ✨

🏆 *Powered by DIU Insider* - Your trusted academic companion

🔹 *Fast result retrieval*
🔹 *All semester support*
🔹 *CGPA calculation*
🔹 *Beautiful presentation*

📌 *Use the menu below to get started!*
📌[Check on website](https://diuresult.mdimtiaz.site)
📌[Follow developer](https://facebook.com/mdimt41)
    """

    if update.message:
        await update.message.reply_text(
            welcome_msg,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=main_menu_keyboard()
        )
    else:
        await update.callback_query.edit_message_text(
            welcome_msg,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=main_menu_keyboard()
        )

    # Log user interaction
    log_msg = f"👤 New user: {user.full_name} (@{user.username}) | ID: {user.id}"
    logging.info(log_msg)
    write_html_log(log_msg)

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🆘 *DIU Result Bot Help*

📌 *How to use:*
1. Tap *'Check Result'* from the main menu
2. Send your Student ID (e.g. 111-11-111)
3. Select your semester
4. Get your detailed results instantly!

🔹 *Features:*
- Results for all semesters
- Beautiful result presentation
- CGPA calculation
- Fast and reliable service

📢 *Join our channel:* [DIU Insider](https://t.me/diuinsider)
💬 *Support group:* @diucommunity
    """
    
    if update.message:
        await update.message.reply_text(
            help_text,
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(),
            disable_web_page_preview=True
        )
    else:
        await update.callback_query.edit_message_text(
            help_text,
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(),
            disable_web_page_preview=True
        )

# About command
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = """
🌟 *About DIU Result Bot*

This bot is developed by *DIU Insider* team to help DIU students check their results easily.

📌 *Version:* 2.0
📅 *Last Updated:* June 2024

👨‍💻 *Developer:*
*MD Imtiaz*
- [Portfolio](https://mdimiaz.site)
- [Facebook](https://facebook.com/mdimt41)
- [GitHub](https://github.com/mdimt40)

🌐 *Official Links:*
- [Website](https://diuresult.mdimiaz.site)
- [Facebook Page](https://facebook.com/diuinsider.bd)
- [Telegram Channel](https://t.me/diuinsider)

💡 *This is an unofficial bot for educational purposes.*
    """
    
    if update.message:
        await update.message.reply_text(
            about_text,
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(),
            disable_web_page_preview=True
        )
    else:
        await update.callback_query.edit_message_text(
            about_text,
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(),
            disable_web_page_preview=True
        )

# Handle menu callbacks
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'check_result':
        await query.edit_message_text(
            "📝 *Please enter your Student ID:*\n_(Example: 111-11-111)_",
            parse_mode="Markdown"
        )
        context.user_data['awaiting_id'] = True
    elif query.data == 'help':
        await help_command(update, context)
    elif query.data == 'about':
        await about_command(update, context)
    elif query.data == 'back_to_menu':
        await start(update, context)

# Handle student ID input
async def handle_student_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'awaiting_id' not in context.user_data:
        return
    
    student_id = update.message.text.strip()
    context.user_data['student_id'] = student_id
    context.user_data['awaiting_id'] = False

    user = update.message.from_user
    log_msg = f"👤 User: {user.full_name} (@{user.username}) | 🆔 StudentID: {student_id}"
    logging.info(log_msg)
    write_html_log(log_msg)

    # Semester selection keyboard
    keyboard = [
        [
            InlineKeyboardButton("Spring 2025", callback_data='251'),
            InlineKeyboardButton("Summer 2025", callback_data='252'),
            InlineKeyboardButton("Fall 2025", callback_data='253')
        ],
        [
            InlineKeyboardButton("Spring 2024", callback_data='241'),
            InlineKeyboardButton("Summer 2024", callback_data='242'),
            InlineKeyboardButton("Fall 2024", callback_data='243')
        ],
        [
            InlineKeyboardButton("Spring 2023", callback_data='231'),
            InlineKeyboardButton("Summer 2023", callback_data='232'),
            InlineKeyboardButton("Fall 2023", callback_data='233')
        ],
        [
            InlineKeyboardButton("Older Semesters", callback_data='older'),
            InlineKeyboardButton("🔙 Menu", callback_data='back_to_menu')
        ]
    ]

    await update.message.reply_text(
        f"✅ *Received ID:* `{student_id}`\n\n"
        "*Select your semester:*\n"
        "_Choose from the buttons below_",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Handle older semesters selection
async def handle_older_semesters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("Spring 2022", callback_data='221'),
            InlineKeyboardButton("Summer 2022", callback_data='222'),
            InlineKeyboardButton("Fall 2022", callback_data='223')
        ],
        [
            InlineKeyboardButton("Spring 2021", callback_data='211'),
            InlineKeyboardButton("Summer 2021", callback_data='212'),
            InlineKeyboardButton("Fall 2021", callback_data='213')
        ],
        [
            InlineKeyboardButton("Spring 2020", callback_data='201'),
            InlineKeyboardButton("Summer 2020", callback_data='202'),
            InlineKeyboardButton("Fall 2020", callback_data='203')
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data='back_semester'),
            InlineKeyboardButton("🔙 Menu", callback_data='back_to_menu')
        ]
    ]

    await query.edit_message_text(
        "📚 *Older Semesters*\n"
        "_Select your semester:_",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Handle result fetching
async def handle_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'older':
        await handle_older_semesters(update, context)
        return
    elif query.data == 'back_semester':
        student_id = context.user_data.get('student_id', 'N/A')
        await query.edit_message_text(
            f"✅ *Your ID:* `{student_id}`\n\n"
            "*Select your semester:*",
            parse_mode="Markdown"
        )
        return
    elif query.data in ['back_to_menu', 'menu']:
        await start(update, context)
        return

    semester_id = query.data
    student_id = context.user_data.get('student_id')

    try:
        await query.edit_message_text("🔄 *Fetching your results...*\n_Please wait..._", parse_mode="Markdown")

        info_url = f"https://proxy.mdimt40.workers.dev/result/studentInfo?studentId={student_id}"
        result_url = f"https://proxy.mdimt40.workers.dev/result?semesterId={semester_id}&studentId={student_id}"

        info_response = requests.get(info_url)
        result_response = requests.get(result_url)

        try:
            info_response.raise_for_status()
            info = info_response.json()
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            info = None
            logging.warning(f"Error fetching student info: {e}")

        try:
            result_response.raise_for_status()
            result = result_response.json()
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            result = None
            logging.warning(f"Error fetching result: {e}")

        if not result or not info:
            error_msg = """
❌ *No Results Found*

We couldn't find results for:
• ID: `{student_id}`
• Semester: {semester}

_Possible reasons:_
• Incorrect ID format
• Semester not published yet
• Server maintenance

⚠️ Please double-check and try again.
            """.format(
                student_id=student_id,
                semester={"1": "Spring", "2": "Summer", "3": "Fall"}[semester_id[2]] + " 20" + semester_id[:2]
            )
            
            keyboard = [
                [InlineKeyboardButton("🔄 Try Again", callback_data='check_result'),
                 InlineKeyboardButton("🔙 Menu", callback_data='back_to_menu')]
            ]
            
            await query.edit_message_text(
                error_msg,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            write_html_log(f"⚠️ No result for {student_id} | {semester_id}")
            return

        # Calculate CGPA
        total_credits = sum(course['totalCredit'] for course in result)
        total_points = sum(course['pointEquivalent'] * course['totalCredit'] for course in result)
        cgpa = round(total_points / total_credits, 2)

        # Format beautiful result message
        semester_name = {"1": "Spring", "2": "Summer", "3": "Fall"}[semester_id[2]] + " 20" + semester_id[:2]
        
        msg = f"""
🎓 *DIU Academic Result* 🎓

*✦ Student:* {info.get('studentName', 'N/A')}
*✦ ID:* `{student_id}`
*✦ Program:* {info.get('progShortName', 'N/A')}
*✦ Semester:* {semester_name}

📊 *Performance Summary:*
• *CGPA:* `{cgpa}`
• *Total Credits:* {total_credits}

📝 *Course Results:*
        """

        for course in result:
            msg += f"""
▬▬▬▬▬▬▬▬▬▬▬▬▬
*{course['customCourseId']}* - {course['courseTitle']}
   • *Grade:* {course['gradeLetter']} ({course['pointEquivalent']})
   • *Credit:* {course['totalCredit']}
   • *Evaluation:* {'✅ Submitted' if course['tevalSubmitted'] else '❌ Not Submitted'}
            """

        msg += """

🔹 *Generated by* [DIU Insider](https://diuresult.mdimtiaz.site)
📢 *Join our channel:* [@diuinsider](https://t.me/diuinsider)
        """

        keyboard = [
            [InlineKeyboardButton("🔍 Check Another", callback_data='check_result'),
             InlineKeyboardButton("🔙 Menu", callback_data='back_to_menu')]
        ]

        await query.edit_message_text(
            msg,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
            disable_web_page_preview=True
        )
        write_html_log(f"📩 Result sent for {student_id} | {semester_id} | CGPA: {cgpa}")

    except Exception as e:
        error_msg = f"""
❌ *Error Occurred*

We encountered an issue while processing your request.

*Error details:* `{str(e)}`

⚠️ Please try again later or contact support.
        """
        
        keyboard = [
            [InlineKeyboardButton("🔄 Try Again", callback_data='check_result'),
             InlineKeyboardButton("🔙 Menu", callback_data='back_to_menu')]
        ]
        
        await query.edit_message_text(
            error_msg,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        write_html_log(f"❌ Error for {student_id} | {semester_id}: {str(e)}")

# Start the bot
if __name__ == '__main__':
    init_html_log()
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CallbackQueryHandler(menu_handler, pattern='^(check_result|help|about|back_to_menu|menu)$'))
    app.add_handler(CallbackQueryHandler(handle_result))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_student_id))

    print("🚀 DIU Result Bot is running with enhanced menus...")
    app.run_polling()
