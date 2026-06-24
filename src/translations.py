"""
Translations for the School Telegram Bot.
Supported languages: English (en), Khmer (km)
"""

STRINGS = {
    # ── Language picker ──────────────────────────────────────────────────────
    "lang_pick_title": {
<<<<<<< HEAD
        "en": "🌐 *Choose Your Language / ជ្រើសរើសភាសា*\n━━━━━━━━━━━━━━━━━━━━\n🇬🇧  Please select your preferred language.\n🇰🇭  សូមជ្រើសរើសភាសាដែលអ្នកចូលចិត្ត។",
        "km": "🌐 *Choose Your Language / ជ្រើសរើសភាសា*\n━━━━━━━━━━━━━━━━━━━━\n🇬🇧  Please select your preferred language.\n🇰🇭  សូមជ្រើសរើសភាសាដែលអ្នកចូលចិត្ត។",
=======
        "en": "🌐 *Choose Your Language*\n\n────────────────────────────\nPlease select your preferred language:",
        "km": "🌐 *ជ្រើសរើសភាសា*\n\n────────────────────────────\nសូមជ្រើសរើសភាសាដែលអ្នកចូលចិត្ត:",
>>>>>>> 0107596f5457f0bb1b3a42df5df7b8180e7999da
    },
    "lang_btn_en": {
        "en": "🇬🇧  English",
        "km": "🇬🇧  English",
    },
    "lang_btn_km": {
        "en": "🇰🇭  ភាសាខ្មែរ",
        "km": "🇰🇭  ភាសាខ្មែរ",
    },
    "lang_saved": {
<<<<<<< HEAD
        "en": "✨ *Language Configured*\n━━━━━━━━━━━━━━━━━━━━\n✅ Your language has been set to *English*.",
        "km": "✨ *ការកំណត់ភាសាត្រូវបានរក្សាទុក*\n━━━━━━━━━━━━━━━━━━━━\n✅ ភាសានិយាយត្រូវបានកំណត់ទៅជា *ភាសាខ្មែរ*។",
=======
        "en": "✅ Language set to *English*.",
        "km": "✅ បានកំណត់ភាសា *ខ្មែរ*។",
>>>>>>> 0107596f5457f0bb1b3a42df5df7b8180e7999da
    },

    # ── Class picker ─────────────────────────────────────────────────────────
    "class_pick_welcome": {
<<<<<<< HEAD
        "en": "👋 *Welcome, {name}!*\n━━━━━━━━━━━━━━━━━━━━\nTo start receiving updates, please select your child's class code from the options below:\n\nℹ️ _Note: You only need to register your class once._",
        "km": "👋 *សូមស្វាគមន៍, {name}!*\n━━━━━━━━━━━━━━━━━━━━\nដើម្បីចាប់ផ្តើមទទួលព័ត៌មាន សូមជ្រើសរើសលេខកូដថ្នាក់រៀនរបស់កូនអ្នកខាងក្រោម៖\n\nℹ️ បញ្ជាក់៖ អ្នកត្រូវចុះឈ្មោះថ្នាក់រៀននេះតែម្តងប៉ុណ្ណោះ។",
    },
    "class_pick_change": {
        "en": "✏️ *Change Class*\n━━━━━━━━━━━━━━━━━━━━\nPlease select your child's new class code:",
        "km": "✏️ *ប្តូរថ្នាក់រៀន*\n━━━━━━━━━━━━━━━━━━━━\nសូមជ្រើសរើសលេខកូដថ្នាក់រៀនថ្មីរបស់កូនអ្នក៖",
    },
    "class_none_available": {
        "en": "⚠️ *No Classes Available*\n━━━━━━━━━━━━━━━━━━━━\nThere are no classes registered in the system yet. Please contact the school office for setup assistance.",
        "km": "⚠️ *មិនទាន់មានថ្នាក់រៀននៅឡើយទេ*\n━━━━━━━━━━━━━━━━━━━━\nមិនទាន់មានថ្នាក់រៀនណាមួយត្រូវបានបញ្ចូលក្នុងប្រព័ន្ធទេ។ សូមទាក់ទងការិយាល័យសាលាសម្រាប់ជំនួយ។",
    },
    "class_registered": {
        "en": "🎉 *Class Registered successfully!*\n━━━━━━━━━━━━━━━━━━━━\n🏫 Class Code:  `{code}`\n━━━━━━━━━━━━━━━━━━━━\n\n✅ You're all set! I will now automatically deliver homework, holiday updates, and announcements for this class.\n\n_You can modify your class at any time via the menu._",
        "km": "🎉 *បានចុះឈ្មោះថ្នាក់រៀនដោយជោគជ័យ!*\n━━━━━━━━━━━━━━━━━━━━\n🏫 លេខកូដថ្នាក់រៀន៖  `{code}`\n━━━━━━━━━━━━━━━━━━━━\n\n✅ រួចរាល់ហើយ! ខ្ញុំនឹងផ្ញើជូនអ្នកនូវកិច្ចការផ្ទះ ថ្ងៃឈប់សម្រាក និងសេចក្តីប្រកាសផ្សេងៗសម្រាប់ថ្នាក់នេះ។\n\nអ្នកអាចប្តូរថ្នាក់រៀនបានគ្រប់ពេលតាមរយៈម៉ឺនុយ។",
    },
    "class_save_error": {
        "en": "⚠️ *Save Error*\n━━━━━━━━━━━━━━━━━━━━\nWe couldn't save your class registration. Please run /start to try again.",
        "km": "⚠️ *កំហុសក្នុងការរក្សាទុក*\n━━━━━━━━━━━━━━━━━━━━\nមិនអាចរក្សាទុកការចុះឈ្មោះថ្នាក់រៀនរបស់អ្នកបានទេ។ សូមវាយពាក្យ /start ដើម្បីសាកល្បងម្តងទៀត។",
=======
        "en": "👋 *Welcome, {name}!*\n\n────────────────────────────\nTo get started, please select your\nchild's class from the list below:\n\n_You only need to do this once._",
        "km": "👋 *សូមស្វាគមន៍, {name}!*\n\n────────────────────────────\nដើម្បីចាប់ផ្តើម សូមជ្រើសរើស\nថ្នាក់រៀនរបស់កូនអ្នកពីបញ្ជីខាងក្រោម:\n\n_អ្នកត្រូវធ្វើវាតែម្តងប៉ុណ្ណោះ។_",
    },
    "class_pick_change": {
        "en": "✏️ *Change Class*\n\n────────────────────────────\nSelect your child's new class:",
        "km": "✏️ *ប្តូរថ្នាក់រៀន*\n\n────────────────────────────\nជ្រើសរើសថ្នាក់រៀនថ្មីរបស់កូនអ្នក:",
    },
    "class_none_available": {
        "en": "⚠️ *No Classes Available*\n\n────────────────────────────\nNo classes have been set up yet.\nPlease contact the school office for assistance.",
        "km": "⚠️ *មិនមានថ្នាក់រៀន*\n\n────────────────────────────\nមិនទាន់មានថ្នាក់រៀនណាមួយទេ។\nសូមទាក់ទងការិយាល័យសាលា។",
    },
    "class_registered": {
        "en": "✅ *Class Registered*\n\n────────────────────────────\n🏫  Your child's class:  *{code}*\n────────────────────────────\n\nAll set! I'll remember this for next time.\nYou can change it anytime from the menu.",
        "km": "✅ *បានចុះឈ្មោះថ្នាក់រៀន*\n\n────────────────────────────\n🏫  ថ្នាក់រៀនរបស់កូន:  *{code}*\n────────────────────────────\n\nរួចរាល់ហើយ! ខ្ញុំនឹងចងចាំសម្រាប់ពេលក្រោយ។\nអ្នកអាចប្តូរវាបានគ្រប់ពេលពីម៉ឺនុយ។",
    },
    "class_save_error": {
        "en": "⚠️ *Error*\n\nCould not save your class. Please try /start again.",
        "km": "⚠️ *កំហុស*\n\nមិនអាចរក្សាទុកថ្នាក់រៀនបានទេ។ សូមសាកល្បង /start ម្តងទៀត។",
>>>>>>> 0107596f5457f0bb1b3a42df5df7b8180e7999da
    },

    # ── Main menu ────────────────────────────────────────────────────────────
    "menu_welcome_back": {
<<<<<<< HEAD
        "en": "👋 *Welcome back, {name}!*\n━━━━━━━━━━━━━━━━━━━━\n🏫 Class:  *{code}*\n📅 Today:  {date}\n━━━━━━━━━━━━━━━━━━━━\n\nWhat details would you like to retrieve today?",
        "km": "👋 *សូមស្វាគមន៍មកវិញ, {name}!*\n━━━━━━━━━━━━━━━━━━━━\n🏫 ថ្នាក់រៀន៖  *{code}*\n📅 ថ្ងៃនេះ៖    {date}\n━━━━━━━━━━━━━━━━━━━━\n\nតើអ្នកចង់មើលព័ត៌មានអ្វីខ្លះថ្ងៃនេះ?",
    },
    "menu_main": {
        "en": "🏠 *Main Menu*\n━━━━━━━━━━━━━━━━━━━━\n{class_line}📅 Today:  {date}\n━━━━━━━━━━━━━━━━━━━━\n\nWhat details would you like to retrieve today?",
        "km": "🏠 *ម៉ឺនុយចម្បង*\n━━━━━━━━━━━━━━━━━━━━\n{class_line}📅 ថ្ងៃនេះ៖  {date}\n━━━━━━━━━━━━━━━━━━━━\n\nតើអ្នកចង់មើលព័ត៌មានអ្វីខ្លះថ្ងៃនេះ?",
    },
    "menu_class_line": {
        "en": "🏫 Class:  *{code}*\n",
        "km": "🏫 ថ្នាក់រៀន៖  *{code}*\n",
=======
        "en": "👋 *Welcome back, {name}!*\n\n────────────────────────────\n🏫  Class:  *{code}*\n📅  Today:  {date}\n────────────────────────────\n\nHow can I help you today?",
        "km": "👋 *សូមស្វាគមន៍មកវិញ, {name}!*\n\n────────────────────────────\n🏫  ថ្នាក់:  *{code}*\n📅  ថ្ងៃនេះ:  {date}\n────────────────────────────\n\nខ្ញុំអាចជួយអ្នកអ្វីបានថ្ងៃនេះ?",
    },
    "menu_main": {
        "en": "🏠 *Main Menu*\n\n────────────────────────────\n{class_line}📅  Today:  {date}\n────────────────────────────\n\nHow can I help you today?",
        "km": "🏠 *ម៉ឺនុយចម្បង*\n\n────────────────────────────\n{class_line}📅  ថ្ងៃនេះ:  {date}\n────────────────────────────\n\nខ្ញុំអាចជួយអ្នកអ្វីបានថ្ងៃនេះ?",
    },
    "menu_class_line": {
        "en": "🏫  Class:  *{code}*\n",
        "km": "🏫  ថ្នាក់:  *{code}*\n",
>>>>>>> 0107596f5457f0bb1b3a42df5df7b8180e7999da
    },

    # ── Menu buttons ─────────────────────────────────────────────────────────
    "btn_homework": {
        "en": "📚  Homework",
        "km": "📚  កិច្ចការផ្ទះ",
    },
    "btn_holidays": {
        "en": "🗓  Upcoming Holidays",
        "km": "🗓  វិស្សមកាលខាងមុខ",
    },
    "btn_change_class": {
        "en": "✏️  Change Class",
        "km": "✏️  ប្តូរថ្នាក់រៀន",
    },
    "btn_about": {
        "en": "ℹ️  About",
        "km": "ℹ️  អំពី",
    },
    "btn_back": {
        "en": "‹  Back to Menu",
        "km": "‹  ត្រឡប់ទៅម៉ឺនុយ",
    },
    "btn_change_lang": {
        "en": "🌐  Change Language",
        "km": "🌐  ប្តូរភាសា",
    },

    # ── Homework ─────────────────────────────────────────────────────────────
    "hw_fetching": {
<<<<<<< HEAD
        "en": "⏳ Fetching today's assignments, please wait…",
        "km": "⏳ កំពុងទាញយកកិច្ចការផ្ទះ សូមរង់ចាំ…",
    },
    "hw_class_not_found": {
        "en": "❌ *Class Not Found*\n━━━━━━━━━━━━━━━━━━━━\nYour registered class was not found in the database. Please tap *Change Class* to register a valid class code.",
        "km": "❌ *រកមិនឃើញថ្នាក់រៀនទេ*\n━━━━━━━━━━━━━━━━━━━━\nថ្នាក់រៀនដែលបានចុះឈ្មោះរកមិនឃើញក្នុងប្រព័ន្ធទេ។ សូមចុចលើប៊ូតុង *ប្តូរថ្នាក់រៀន* ដើម្បីចុះឈ្មោះឡើងវិញ។",
    },
    "hw_none_today": {
        "en": "📚 *Homework Assignments*\n━━━━━━━━━━━━━━━━━━━━\n🏫 Class:  `{code}`\n📅 Date:   {date}\n━━━━━━━━━━━━━━━━━━━━\n\n🎉 *No homework has been assigned today!*\n\n_Enjoy your evening!_",
        "km": "📚 *កិច្ចការផ្ទះរបស់សិស្ស*\n━━━━━━━━━━━━━━━━━━━━\n🏫 ថ្នាក់រៀន៖  `{code}`\n📅 ថ្ងៃទី៖     {date}\n━━━━━━━━━━━━━━━━━━━━\n\n🎉 *មិនទាន់មានកិច្ចការផ្ទះសម្រាប់ថ្ងៃនេះទេ!*\n\nសូមរីករាយជាមួយពេលវេលាសម្រាករបស់កូនៗ!",
    },
    "hw_header": {
        "en": "📚 *Homework Assignments*\n━━━━━━━━━━━━━━━━━━━━\n🏫 Class:  `{code}`\n📅 Date:   {date}\n📋 Found:  *{count}* assignment{plural}\n━━━━━━━━━━━━━━━━━━━━\n\n",
        "km": "📚 *កិច្ចការផ្ទះរបស់សិស្ស*\n━━━━━━━━━━━━━━━━━━━━\n🏫 ថ្នាក់រៀន៖  `{code}`\n📅 ថ្ងៃទី៖     {date}\n📋 រកឃើញ៖  *{count}* កិច្ចការ\n━━━━━━━━━━━━━━━━━━━━\n\n",
    },
    "hw_due": {
        "en": "⏰ Due Date: *{date}*",
        "km": "⏰ កាលបរិច្ឆេទកំណត់៖ *{date}*",
    },
    "hw_teacher": {
        "en": "👤 Instructor:  {name}",
        "km": "👤 គ្រូបង្រៀន៖      {name}",
    },
    "hw_attachment": {
        "en": "📎 _Attachment attached below_ ↓",
        "km": "📎 មានឯកសារភ្ជាប់ខាងក្រោម ↓",
    },
    "hw_footer": {
        "en": "━━━━━━━━━━━━━━━━━━━━\n📥 _Download and review attachment files below._",
        "km": "━━━━━━━━━━━━━━━━━━━━\n📥 សូមទាញយក និងពិនិត្យមើលឯកសារភ្ជាប់ខាងក្រោម។",
=======
        "en": "⏳ Fetching homework, please wait…",
        "km": "⏳ កំពុងទាញយកកិច្ចការផ្ទះ សូមរង់ចាំ…",
    },
    "hw_class_not_found": {
        "en": "❌ *Class Not Found*\n\nYour class could not be found in the system.\nPlease tap *Change Class* from the menu to update it.",
        "km": "❌ *រកមិនឃើញថ្នាក់រៀន*\n\nថ្នាក់រៀនរបស់អ្នករកមិនឃើញក្នុងប្រព័ន្ធ។\nសូមចុច *ប្តូរថ្នាក់រៀន* ពីម៉ឺនុយ។",
    },
    "hw_none_today": {
        "en": "📚 *Homework — Class {code}*\n\n────────────────────────────\n📅  {date}\n────────────────────────────\n\n✅  No homework has been assigned yet today.\n\n_Check back later or contact your teacher._",
        "km": "📚 *កិច្ចការផ្ទះ — ថ្នាក់ {code}*\n\n────────────────────────────\n📅  {date}\n────────────────────────────\n\n✅  មិនទាន់មានកិច្ចការផ្ទះថ្ងៃនេះទេ។\n\n_សូមពិនិត្យម្តងទៀតនៅពេលក្រោយ ឬទាក់ទងគ្រូ។_",
    },
    "hw_header": {
        "en": "📚 *Homework — Class {code}*\n────────────────────────────\n📅  {date}\n📋  {count} assignment{plural} found\n────────────────────────────\n",
        "km": "📚 *កិច្ចការផ្ទះ — ថ្នាក់ {code}*\n────────────────────────────\n📅  {date}\n📋  រកឃើញ {count} កិច្ចការ\n────────────────────────────\n",
    },
    "hw_due": {
        "en": "📅  Due: *{date}*",
        "km": "📅  កំណត់ថ្ងៃ: *{date}*",
    },
    "hw_teacher": {
        "en": "👩‍🏫  Teacher: {name}",
        "km": "👩‍🏫  គ្រូ: {name}",
    },
    "hw_attachment": {
        "en": "📎  Attachment included ↓",
        "km": "📎  មានឯកសារភ្ជាប់ ↓",
    },
    "hw_footer": {
        "en": "────────────────────────────\n_Tap any attachment below to download it._",
        "km": "────────────────────────────\n_ចុចលើឯកសារភ្ជាប់ខាងក្រោមដើម្បីទាញយក។_",
>>>>>>> 0107596f5457f0bb1b3a42df5df7b8180e7999da
    },

    # ── Holidays ─────────────────────────────────────────────────────────────
    "hol_none": {
<<<<<<< HEAD
        "en": "🗓 *School Holidays*\n━━━━━━━━━━━━━━━━━━━━\n\n🌴 *No upcoming holidays are currently scheduled.*\n\n_Any scheduled closures will be posted here._",
        "km": "🗓 *វិស្សមកាលសាលា*\n━━━━━━━━━━━━━━━━━━━━\n\n🌴 *មិនទាន់មានថ្ងៃឈប់សម្រាកខាងមុខនៅឡើយទេ។*\n\nរាល់កាលវិភាគឈប់សម្រាក នឹងត្រូវបានបង្ហាញនៅទីនេះ។",
    },
    "hol_header": {
        "en": "🗓 *Upcoming Holidays*\n━━━━━━━━━━━━━━━━━━━━\n📅 Current Date:  {date}\n━━━━━━━━━━━━━━━━━━━━\n\n",
        "km": "🗓 *វិស្សមកាលខាងមុខ*\n━━━━━━━━━━━━━━━━━━━━\n📅 ថ្ងៃនេះ៖        {date}\n━━━━━━━━━━━━━━━━━━━━\n\n",
    },
    "hol_date_single": {
        "en": "📅 Date:  *{date}*",
        "km": "📅 ថ្ងៃឈប់សម្រាក៖  *{date}*",
    },
    "hol_date_from": {
        "en": "📅 Start: *{date}*",
        "km": "📅 ចាប់ផ្តើម៖       *{date}*",
    },
    "hol_date_to": {
        "en": "📅 End:   *{date}*",
        "km": "📅 បញ្ចប់៖          *{date}*",
    },
    "hol_footer": {
        "en": "━━━━━━━━━━━━━━━━━━━━\n_All dates are subject to official confirmation._",
        "km": "━━━━━━━━━━━━━━━━━━━━\nកាលបរិច្ឆេទទាំងអស់អាចផ្លាស់ប្តូរតាមការកំណត់ជាក់ស្តែង។",
=======
        "en": "🗓 *Upcoming Holidays*\n\n────────────────────────────\n\nNo upcoming holidays are scheduled at this time.\n\n_Check back later for updates._",
        "km": "🗓 *វិស្សមកាលខាងមុខ*\n\n────────────────────────────\n\nមិនមានវិស្សមកាលខាងមុខណាមួយទេ។\n\n_សូមពិនិត្យម្តងទៀតនៅពេលក្រោយ។_",
    },
    "hol_header": {
        "en": "🗓 *Upcoming Holidays*\n────────────────────────────\n📅  {date}\n────────────────────────────\n",
        "km": "🗓 *វិស្សមកាលខាងមុខ*\n────────────────────────────\n📅  {date}\n────────────────────────────\n",
    },
    "hol_date_single": {
        "en": "📅  Date: *{date}*",
        "km": "📅  ថ្ងៃ: *{date}*",
    },
    "hol_date_from": {
        "en": "📅  From: *{date}*",
        "km": "📅  ចាប់ពី: *{date}*",
    },
    "hol_date_to": {
        "en": "📅  To:      *{date}*",
        "km": "📅  ដល់:      *{date}*",
    },
    "hol_footer": {
        "en": "────────────────────────────\n_All dates are subject to change._",
        "km": "────────────────────────────\n_កាលបរិច្ឆេទទាំងអស់អាចផ្លាស់ប្តូរបាន។_",
>>>>>>> 0107596f5457f0bb1b3a42df5df7b8180e7999da
    },

    # ── About ────────────────────────────────────────────────────────────────
    "about": {
<<<<<<< HEAD
        "en": "ℹ️ *About This Assistant*\n━━━━━━━━━━━━━━━━━━━━\n🏫 *{school}*\n━━━━━━━━━━━━━━━━━━━━\n\nThis helper bot keeps parents connected with real-time academic resources directly on Telegram:\n\n📚  *Homework:* Instantly fetch daily tasks and files.\n🗓  *Holidays:* View up-to-date academic calendars.\n📢  *Broadcasts:* Receive urgent school announcements.\n\n━━━━━━━━━━━━━━━━━━━━\n📞 Need assistance? Please reach out to the school office.",
        "km": "ℹ️ *អំពីជំនួយការនេះ*\n━━━━━━━━━━━━━━━━━━━━\n🏫 *{school}*\n━━━━━━━━━━━━━━━━━━━━\n\nបូតនេះជួយផ្តល់ភាពងាយស្រួលដល់ឪពុកម្តាយក្នុងការទទួលព័ត៌មានពីសាលារបស់កូនៗផ្ទាល់នៅលើ Telegram៖\n\n📚  *កិច្ចការផ្ទះ៖* មើលកិច្ចការផ្ទះប្រចាំថ្ងៃ និងទាញយកឯកសារមេរៀន\n🗓  *វិស្សមកាល៖* ពិនិត្យមើលកាលបរិច្ឆេទឈប់សម្រាកសាលា\n📢  *សេចក្តីប្រកាស៖* ទទួលបានសារដំណឹងបន្ទាន់ៗពីសាលា\n\n━━━━━━━━━━━━━━━━━━━━\n📞 ត្រូវការជំនួយបន្ថែម? សូមទាក់ទងមកកាន់ការិយាល័យសាលា។",
=======
        "en": "ℹ️ *About This Bot*\n\n────────────────────────────\n🏫  *{school}*\n────────────────────────────\n\nThis bot helps parents stay informed about:\n\n📚  Daily homework assignments\n🗓  Upcoming school holidays\n📢  Important school announcements\n\n────────────────────────────\nFor support, please contact the school office.",
        "km": "ℹ️ *អំពីបូតនេះ*\n\n────────────────────────────\n🏫  *{school}*\n────────────────────────────\n\nបូតនេះជួយឪពុកម្តាយឱ្យដឹងអំពី:\n\n📚  កិច្ចការផ្ទះប្រចាំថ្ងៃ\n🗓  វិស្សមកាលសាលាខាងមុខ\n📢  សេចក្តីប្រកាសសាលាសំខាន់ៗ\n\n────────────────────────────\nសម្រាប់ជំនួយ សូមទាក់ទងការិយាល័យសាលា។",
>>>>>>> 0107596f5457f0bb1b3a42df5df7b8180e7999da
    },

    # ── Misc ─────────────────────────────────────────────────────────────────
    "cancelled": {
<<<<<<< HEAD
        "en": "🛑 Operation cancelled. Returning to main menu:",
        "km": "🛑 ប្រតិបត្តិការត្រូវបានបោះបង់។ ត្រឡប់ទៅម៉ឺនុយចម្បងវិញ៖",
    },
    "use_menu": {
        "en": "👉 Please use the interactive menu buttons below to proceed:",
        "km": "👉 សូមប្រើប្រាស់ប៊ូតុងបញ្ជាខាងក្រោមដើម្បីបន្ត៖",
    },
    "hw_title": {
        "en": "📌 *Assignment {num}: {subject}*",
        "km": "📌 *កិច្ចការទី {num}៖ {subject}*",
    },
    "hol_title": {
        "en": "🌴 *Holiday {num}: {title}*",
        "km": "🌴 *ថ្ងៃឈប់សម្រាក {num}៖ {title}*",
    },
    "alert_no_class": {
        "en": "⚠️ You do not have a class registered yet. Please select a class.",
        "km": "⚠️ អ្នកមិនទាន់បានចុះឈ្មោះថ្នាក់រៀននៅឡើយទេ។ សូមជ្រើសរើសថ្នាក់រៀន។",
=======
        "en": "Cancelled. Use the menu below:",
        "km": "បានបោះបង់។ ប្រើម៉ឺនុយខាងក្រោម:",
    },
    "use_menu": {
        "en": "Please use the menu below to navigate:",
        "km": "សូមប្រើម៉ឺនុយខាងក្រោមដើម្បីរុករក:",
>>>>>>> 0107596f5457f0bb1b3a42df5df7b8180e7999da
    },
}

def t(key: str, lang: str, **kwargs) -> str:
    """Return the translated string for key in lang, with optional format args."""
    lang = lang if lang in ("en", "km") else "en"
    text = STRINGS.get(key, {}).get(lang, STRINGS.get(key, {}).get("en", key))
    if kwargs:
        text = text.format(**kwargs)
    return text
