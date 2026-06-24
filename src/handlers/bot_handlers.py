import io
import os
import logging
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes, ConversationHandler

from translations import t
import services.api_service as api_service

logger = logging.getLogger(__name__)

SCHOOL_NAME = os.getenv("SCHOOL_NAME", "Our School")

# Conversation states
PICKING_LANG  = 0
PICKING_CLASS = 1

# ─────────────────────────────────────────────────────────────────────────────
# Language helpers
# ─────────────────────────────────────────────────────────────────────────────

async def get_lang(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Return the cached language for this user session, or fetch from DB if not cached."""
    if "lang" in context.user_data:
        return context.user_data["lang"]
    try:
        sub = await api_service.get_subscriber(str(user_id))
        if sub and sub.get("language"):
            lang = sub["language"]
            context.user_data["lang"] = lang
            return lang
    except Exception as e:
        logger.warning(f"Could not load language from database: {e}")
    return "en"


# ─────────────────────────────────────────────────────────────────────────────
# Keyboards
# ─────────────────────────────────────────────────────────────────────────────

def lang_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🇬🇧  English",      callback_data="lang:en"),
        InlineKeyboardButton("🇰🇭  ភាសាខ្មែរ", callback_data="lang:km"),
    ]])


def main_menu(lang: str, has_class: bool = True) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(t("btn_homework",  lang), callback_data="hw_mine")],
        [InlineKeyboardButton(t("btn_holidays",  lang), callback_data="menu_holidays")],
        [InlineKeyboardButton(t("btn_change_class", lang), callback_data="change_class")],
        [InlineKeyboardButton(t("btn_about",       lang), callback_data="menu_about")],
        [InlineKeyboardButton(t("btn_change_lang", lang), callback_data="change_lang")],
    ]
    return InlineKeyboardMarkup(rows)


def back_menu(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")
    ]])


# ─────────────────────────────────────────────────────────────────────────────
# Formatting helpers
# ─────────────────────────────────────────────────────────────────────────────

def today_str(lang: str = "en") -> str:
    now = datetime.now()
    if lang == "km":
        days = {
            "Monday": "ច័ន្ទ",
            "Tuesday": "អង្គារ",
            "Wednesday": "ពុធ",
            "Thursday": "ព្រហស្បតិ៍",
            "Friday": "សុក្រ",
            "Saturday": "សៅរ៍",
            "Sunday": "អាទិត្យ"
        }
        months = {
            "January": "មករា",
            "February": "កុម្ភៈ",
            "March": "មីនា",
            "April": "មេសា",
            "May": "ឧសភា",
            "June": "មិថុនា",
            "July": "កក្កដា",
            "August": "សីហា",
            "September": "កញ្ញា",
            "October": "តុលា",
            "November": "វិច្ឆិកា",
            "December": "ធ្នូ"
        }
        day_en = now.strftime("%A")
        month_en = now.strftime("%B")
        day_num = now.strftime("%d")
        year = now.strftime("%Y")
        
        day_km = days.get(day_en, day_en)
        month_km = months.get(month_en, month_en)
        
        return f"ថ្ងៃ{day_km}, ទី{int(day_num)} {month_km} {year}"
    return now.strftime("%A, %d %B %Y")


# ─────────────────────────────────────────────────────────────────────────────
# UI Pickers & Presenters
# ─────────────────────────────────────────────────────────────────────────────

async def show_lang_picker(target):
    """Show the language selection screen. target can be a Message or CallbackQuery."""
    text = (
        "🌐 *Choose Your Language / ជ្រើសរើសភាសា*\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🇬🇧  Please select your preferred language.\n"
        "🇰🇭  សូមជ្រើសរើសភាសាដែលអ្នកចូលចិត្ត។"
    )
    keyboard = lang_menu()
    if hasattr(target, "edit_message_text"):
        await target.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)
    else:
        await target.reply_text(text, parse_mode="Markdown", reply_markup=keyboard)


async def show_class_picker(target, lang: str, first_name: str = "", first_time: bool = False):
    """Fetch classes list from api_service and display picker buttons."""
    classes = await api_service.get_classes()

    if not classes:
        msg = t("class_none_available", lang)
        keyboard = back_menu(lang)
        if hasattr(target, "edit_message_text"):
            await target.edit_message_text(msg, parse_mode="Markdown", reply_markup=keyboard)
        else:
            await target.reply_text(msg, parse_mode="Markdown", reply_markup=keyboard)
        return False

    buttons, row = [], []
    for cls in classes:
        row.append(InlineKeyboardButton(
            f"🏫  {cls['name']}",
            callback_data=f"pick:{cls['code']}"
        ))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    if first_time:
        text = t("class_pick_welcome", lang, name=first_name)
    else:
        text = t("class_pick_change", lang)

    keyboard = InlineKeyboardMarkup(buttons)
    if hasattr(target, "edit_message_text"):
        await target.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)
    else:
        await target.reply_text(text, parse_mode="Markdown", reply_markup=keyboard)
    return True


async def show_homework(query, class_code: str, lang: str):
    """Fetch homework from api_service and display, downloading files if present."""
    data = await api_service.get_homework(class_code)

    if data is None:
        await query.edit_message_text(
            t("hw_class_not_found", lang),
            parse_mode="Markdown",
            reply_markup=back_menu(lang),
        )
        return

    if not data:
        await query.edit_message_text(
            t("hw_none_today", lang, code=class_code, date=today_str(lang)),
            parse_mode="Markdown",
            reply_markup=back_menu(lang),
        )
        return

    count = len(data)
    divider = "━━━━━━━━━━━━━━━━━━━━"
    lines = [t(
        "hw_header", lang,
        code=class_code,
        date=today_str(lang),
        count=count,
        plural="s" if count > 1 else "",
    ), ""]

    for i, hw in enumerate(data, 1):
        lines.append(t("hw_title", lang, num=i, subject=hw['subject']))
        lines.append(f"📝  {hw['description']}")
        lines.append(t("hw_due",     lang, date=hw["due_date"]))
        lines.append(t("hw_teacher", lang, name=hw["submitted_by"]))
        if hw.get("file_name"):
            lines.append(t("hw_attachment", lang))
        if i < count:
            lines.append(divider)
        lines.append("")

    lines.append(t("hw_footer", lang))
    text = "\n".join(lines)

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=back_menu(lang),
    )

    # Download all files in parallel to significantly reduce response latency
    import asyncio
    files_to_download = [
        (hw, hw["file_url"])
        for hw in data
        if hw.get("file_url") and hw.get("file_name")
    ]

    if files_to_download:
        download_tasks = [
            api_service.fetch_file(url)
            for _, url in files_to_download
        ]
        downloaded_contents = await asyncio.gather(*download_tasks)

        for (hw, _), content_bytes in zip(files_to_download, downloaded_contents):
            if content_bytes:
                try:
                    file_bytes = io.BytesIO(content_bytes)
                    file_bytes.name = hw["file_name"]
                    due_text = t('hw_due', lang, date=hw['due_date'])
                    due_caption = due_text if lang == "km" else f"_{due_text}_"
                    caption = (
                        f"📎 *{hw['subject']}*\n"
                        f"{hw['file_name']}\n"
                        f"{due_caption}"
                    )
                    await query.message.chat.send_document(
                        document=InputFile(file_bytes, filename=hw["file_name"]),
                        caption=caption,
                        parse_mode="Markdown",
                    )
                except Exception as e:
                    logger.warning(f"Could not send file {hw['file_name']}: {e}")


async def show_holidays(query, lang: str):
    """Fetch holidays from api_service and display."""
    data = await api_service.get_holidays()
    divider = "━━━━━━━━━━━━━━━━━━━━"

    if not data:
        text = t("hol_none", lang)
    else:
        lines = [t("hol_header", lang, date=today_str(lang)), ""]
        for i, h in enumerate(data, 1):
            lines.append(t("hol_title", lang, num=i, title=h['title']))
            if h["start_date"] == h["end_date"]:
                lines.append(t("hol_date_single", lang, date=h["start_date"]))
            else:
                lines.append(t("hol_date_from", lang, date=h["start_date"]))
                lines.append(t("hol_date_to",   lang, date=h["end_date"]))
            if h.get("reason"):
                lines.append(f"📌  {h['reason']}")
            if i < len(data):
                lines.append(divider)
            lines.append("")
        lines.append(t("hol_footer", lang))
        text = "\n".join(lines)

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=back_menu(lang),
    )


# ─────────────────────────────────────────────────────────────────────────────
# Handlers
# ─────────────────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user = update.effective_user
    await api_service.register_subscriber(user)
    sub = await api_service.get_subscriber(str(user.id))

    # Load stored language preference into session cache
    stored_lang = (sub or {}).get("language", "en") or "en"
    context.user_data["lang"] = stored_lang
    lang = stored_lang

    has_class = bool(sub and sub.get("class_code"))
    has_lang  = bool(sub and sub.get("language"))

    # First-ever visit: pick language first
    if not has_lang or lang == "en" and not has_class:
        if not has_lang:
            await show_lang_picker(update.message)
            return PICKING_LANG

    if has_class:
        class_code = sub["class_code"]
        text = t(
            "menu_welcome_back", lang,
            name=user.first_name,
            code=class_code,
            date=today_str(lang),
        )
        await update.message.reply_text(
            text,
            parse_mode="Markdown",
            reply_markup=main_menu(lang, has_class=True),
        )
        return ConversationHandler.END
    else:
        await show_class_picker(update.message, lang, user.first_name, first_time=True)
        return PICKING_CLASS


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback button clicks and callback queries."""
    query = update.callback_query
    await query.answer()
    user  = query.from_user
    lang  = await get_lang(user.id, context)

    # ── Language selected ────────────────────────────────────────────────────
    if query.data.startswith("lang:"):
        chosen = query.data.split(":", 1)[1]
        context.user_data["lang"] = chosen
        lang = chosen

        # Persist to backend
        await api_service.save_language(str(user.id), chosen)

        # Confirm, then check if class is already set
        sub = await api_service.get_subscriber(str(user.id))
        has_class = bool(sub and sub.get("class_code"))

        if has_class:
            text = t(
                "menu_welcome_back", lang,
                name=user.first_name,
                code=sub["class_code"],
                date=today_str(lang),
            )
            await query.edit_message_text(
                text,
                parse_mode="Markdown",
                reply_markup=main_menu(lang, has_class=True),
            )
            return ConversationHandler.END
        else:
            await show_class_picker(query, lang, user.first_name, first_time=True)
            return PICKING_CLASS

    # ── Class selected from picker ───────────────────────────────────────────
    if query.data.startswith("pick:"):
        code   = query.data.split(":", 1)[1]
        result = await api_service.save_class(str(user.id), code)
        if result is None:
            await query.edit_message_text(
                t("class_save_error", lang),
                parse_mode="Markdown",
            )
            return ConversationHandler.END

        text = t("class_registered", lang, code=code)
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=main_menu(lang, has_class=True),
        )
        return ConversationHandler.END

    # ── Homework ─────────────────────────────────────────────────────────────
    elif query.data == "hw_mine":
        sub = await api_service.get_subscriber(str(user.id))
        if not sub or not sub.get("class_code"):
            await show_class_picker(query, lang, user.first_name, first_time=True)
            return PICKING_CLASS
        await query.edit_message_text(
            t("hw_fetching", lang),
            parse_mode="Markdown",
        )
        await show_homework(query, sub["class_code"], lang)

    # ── Change class ─────────────────────────────────────────────────────────
    elif query.data == "change_class":
        sub = await api_service.get_subscriber(str(user.id))
        if not sub or not sub.get("class_code"):
            await query.answer(text=t("alert_no_class", lang), show_alert=True)
            await show_class_picker(query, lang, user.first_name, first_time=True)
            return PICKING_CLASS
        await show_class_picker(query, lang, user.first_name, first_time=False)
        return PICKING_CLASS

    # ── Change language ──────────────────────────────────────────────────────
    elif query.data == "change_lang":
        await show_lang_picker(query)
        return PICKING_LANG

    # ── Holidays ─────────────────────────────────────────────────────────────
    elif query.data == "menu_holidays":
        await show_holidays(query, lang)

    # ── About ────────────────────────────────────────────────────────────────
    elif query.data == "menu_about":
        text = t("about", lang, school=SCHOOL_NAME)
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=back_menu(lang),
        )

    # ── Back to menu ─────────────────────────────────────────────────────────
    elif query.data == "menu_back":
        sub = await api_service.get_subscriber(str(user.id))
        has_class  = bool(sub and sub.get("class_code"))
        class_line = t("menu_class_line", lang, code=sub["class_code"]) if has_class else ""
        text = t("menu_main", lang, class_line=class_line, date=today_str(lang))
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=main_menu(lang, has_class=has_class),
        )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /cancel command to abort conversation states."""
    user = update.effective_user
    lang = await get_lang(user.id, context)
    sub  = await api_service.get_subscriber(str(user.id))
    has_class = bool(sub and sub.get("class_code"))
    await update.message.reply_text(
        t("cancelled", lang),
        parse_mode="Markdown",
        reply_markup=main_menu(lang, has_class=has_class),
    )
    return ConversationHandler.END


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle arbitrary text updates from users that don't match any commands."""
    user = update.effective_user
    lang = await get_lang(user.id, context)
    sub  = await api_service.get_subscriber(str(user.id))
    has_class = bool(sub and sub.get("class_code"))
    await update.message.reply_text(
        t("use_menu", lang),
        parse_mode="Markdown",
        reply_markup=main_menu(lang, has_class=has_class),
    )
