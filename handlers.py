from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
import database
import card_generator
import utils
import os
from config import ADMIN_ID

# Conversation states
NAME, TITLE, COMPANY, PHONE, EMAIL, WEBSITE = range(6)

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("🪪 Create Business Card", callback_data="menu_create")],
        [InlineKeyboardButton("🎨 Choose Template", callback_data="menu_template"),
         InlineKeyboardButton("👀 Preview Card", callback_data="menu_preview")],
        [InlineKeyboardButton("💾 Download Card", callback_data="menu_download"),
         InlineKeyboardButton("❓ Help", callback_data="menu_help")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    utils.ensure_temp_directory()
    uid = update.effective_user.id
    await database.register_user(uid)
    
    welcome = (
        "👋 Welcome to *CardForge Bot*!\n"
        "Create stunning, professional digital business cards in minutes.\n\n"
        "✨ *Design beautiful business cards*\n"
        "🎨 *Choose from multiple premium templates*\n"
        "📱 *Generate QR codes automatically*\n"
        "🚀 *Fast, modern, and easy to use*\n\n"
        "Tap a button below to start creating your digital business card."
    )
    if update.message:
        await update.message.reply_text(welcome, reply_markup=get_main_menu(), parse_mode="Markdown")
    return ConversationHandler.END

async def start_convo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['card_build'] = {}
    await query.message.reply_text("🪪 Let's begin! Please enter your *Full Name*:", parse_mode="Markdown")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['card_build']['name'] = update.message.text
    await update.message.reply_text("💼 What is your *Job Title*?", parse_mode="Markdown")
    return TITLE

async def get_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['card_build']['title'] = update.message.text
    await update.message.reply_text("🏢 Enter your *Company Name*:", parse_mode="Markdown")
    return COMPANY

async def get_company(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['card_build']['company'] = update.message.text
    await update.message.reply_text("📞 Enter your professional *Phone Number*:", parse_mode="Markdown")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['card_build']['phone'] = update.message.text
    await update.message.reply_text("✉️ Enter your *Email Address*:", parse_mode="Markdown")
    return EMAIL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['card_build']['email'] = update.message.text
    await update.message.reply_text("🌐 Enter your *Website URL*:", parse_mode="Markdown")
    return WEBSITE

async def get_website(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    context.user_data['card_build']['website'] = update.message.text
    context.user_data['card_build']['template'] = "Modern"
    
    # Save parameters block into local persistent tables mapping records
    await database.save_card(uid, context.user_data['card_build'])
    await update.message.reply_text("🎉 Business card records updated successfully! Use the menu to generate a live preview.", reply_markup=get_main_menu())
    return ConversationHandler.END

async def menu_routing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    
    if query.data == "menu_template":
        kb = [[InlineKeyboardButton("Light Theme Mode", callback_data="tpl_Modern")],
              [InlineKeyboardButton("Dark Theme Mode", callback_data="tpl_Dark Theme")],
              [InlineKeyboardButton("🔙 Main Menu", callback_data="go_home")]]
        await query.edit_message_text("🎨 *Select Card Theme Configuration Style:*", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
        
    elif query.data.startswith("tpl_"):
        selected_tpl = query.data.split("_")[1]
        card = await database.get_card(uid)
        if card:
            card['template'] = selected_tpl
            await database.save_card(uid, card)
            await query.message.reply_text(f"✅ Template design profile successfully targeted to: `{selected_tpl}`")
        else:
            await query.message.reply_text("❌ No active profile records found. Tap *Create Business Card* first.")
            
    elif query.data == "menu_preview" or query.data == "menu_download":
        card = await database.get_card(uid)
        if not card:
            await query.message.reply_text("❌ You have not created a business card profile yet. Tap *Create Business Card*.")
            return
            
        path = card_generator.render_business_card(card, uid)
        if os.path.exists(path):
            with open(path, 'rb') as f:
                await query.message.reply_document(document=f, filename="business_card.png", caption="✨ Here is your customized high-resolution business card canvas graphic asset payload.")
            utils.clean_user_files(uid)
        else:
            await query.message.reply_text("❌ Core image compilation execution failure loop error.")
            
    elif query.data == "go_home":
        await query.edit_message_text("Tap a button below to start creating your digital business card.", reply_markup=get_main_menu())
    elif query.data == "menu_help":
        await query.message.reply_text("❓ *CardForge Bot Help Panel*\n\nProvide your core details to generate a high-resolution print-ready business card complete with an automatically embedded active contact vCard QR matrix.")

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    users = await database.get_total_users()
    cards = await database.get_total_cards()
    await update.message.reply_text(f"📊 *CardForge Infrastructure Analytics:*\n\nRegistered Users: `{users}`\nGenerated Production Vectors: `{cards}`", parse_mode="Markdown")

