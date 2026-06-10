from flask import Flask, render_template_string, request, redirect, jsonify, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'm_app_super_secret_key_2026'

# --- మల్టీ-లాంగ్వేజ్ ట్రాన్స్‌లేషన్ డేటా ---
LANGUAGES = {
    'en': {
        'logo': 'M', 'user_placeholder': 'Username, email or mobile number', 'pass_placeholder': 'Password',
        'login': 'Log in', 'forgot': 'Forgotten password?', 'create_acc': 'Create new account',
        'send_otp': 'Send OTP', 'enter_otp': 'Enter OTP', 'verify': 'Verify OTP',
        'full_name': 'Enter your full name', 'id_name': 'Create your ID name', 'set_pass': 'Set Password',
        'submit': 'Enter', 'wrong': 'Wrong username or password!', 'otp_sent': 'OTP sent successfully!',
        'wrong_otp': 'Wrong OTP! Try again.', 'fill_fields': 'Please fill all fields.',
        'welcome': 'Welcome', 'lbl_fullname': 'Full Name', 'lbl_mobile': 'Mobile', 'logout': 'Logout',
        'edit_btn': '⚙ Edit Details', 'edit_title': 'Update Details', 
        'chg_fullname': 'Change your full name:', 'chg_id': 'Change your ID name:', 'ok': 'OK',
        'about_me': 'About Me', 'save_about': 'Save About Me', 'search_title': 'Search Users',
        'search_btn': 'Search', 'not_found': 'User not found!', 'message_btn': 'Message',
        'send_btn': 'Send', 'call_alert': 'Call Feature coming soon in next update!',
        'edit_msg': 'Edit Message', 'chats_title': 'Your Chats'
    },
    'te': {
        'logo': 'M', 'user_placeholder': 'యూజర్ నేమ్, ఈమెయిల్ లేదా మొబైల్ నంబర్', 'pass_placeholder': 'పాస్‌వర్డ్',
        'login': 'లాగిన్ అవ్వండి', 'forgot': 'పాస్‌వర్డ్ మర్చిపోయారా?', 'create_acc': 'కొత్త ఖాతాను సృష్టించండి',
        'send_otp': 'OTP పంపండి', 'enter_otp': 'OTP ని నమోదు చేయండి', 'verify': 'OTP ని వెరిఫై చేయండి',
        'full_name': 'మీ పూర్తి పేరును నమోదు చేయండి', 'id_name': 'మీ ఐడీ పేరును సృష్టించండి', 'set_pass': 'పాస్‌వర్డ్ సెట్ చేయండి',
        'submit': 'సమర్పించు', 'wrong': 'తప్పుడు యూజర్ నేమ్ లేదా పాస్‌వర్డ్!', 'otp_sent': 'OTP విజయవంతంగా పంపబడింది!',
        'wrong_otp': 'తప్పుడు OTP! మళ్ళీ ప్రయత్నించండి.', 'fill_fields': 'దయచేసి అన్ని వివరాలు పూరించండి.',
        'welcome': 'స్వాగతం', 'lbl_fullname': 'పూర్తి పేరు', 'lbl_mobile': 'మొబైల్', 'logout': 'లాగౌట్',
        'edit_btn': '⚙ వివరాలను సవరించు', 'edit_title': 'వివరాలను నవీకరించండి', 
        'chg_fullname': 'మీ పూర్తి పేరును మార్చండి:', 'chg_id': 'మీ ఐడీ పేరును మార్చండి:', 'ok': 'సరే',
        'about_me': 'నా గురించి (About Me)', 'save_about': 'సేవ్ చేయి', 'search_title': 'ఐడీ కోసం వెతకండి',
        'search_btn': 'వెతుకు', 'not_found': 'ఈ ఐడీ పేరుతో ఎవరూ లేరు!', 'message_btn': 'మెసేజ్ చేయి',
        'send_btn': 'పంపు', 'call_alert': 'కాల్ ఫీచర్ తదుపరి అప్‌డేట్‌లో వస్తుంది!',
        'edit_msg': 'మెసేజ్ సవరించు', 'chats_title': 'మీ చాట్స్'
    },
    'hi': {
        'logo': 'M', 'user_placeholder': 'यूजरनेम, ईमेल या मोबाइल नंबर', 'pass_placeholder': 'पासवर्ड',
        'login': 'लॉग इन करें', 'forgot': 'पासवर्ड भूल गए?', 'create_acc': 'नया अकाउंट बनाएं',
        'send_otp': 'ओटीपी भेजें', 'enter_otp': 'ओटीपी दर्ज करें', 'verify': 'ओटीपी सत्यापित करें',
        'full_name': 'अपना पूरा नाम दर्ज करें', 'id_name': 'अपनी आईडी का नाम बनाएं', 'set_pass': 'पासवर्ड सेट करें',
        'submit': 'दर्ज करें', 'wrong': 'गलत उपयोगकर्ता नाम या पासवर्ड!', 'otp_sent': 'ओटीपी सफलतापूर्वक भेजा गया!',
        'wrong_otp': 'गलत ओटीपी! फिर से प्रयास करें।', 'fill_fields': 'कृपया सभी फ़ील्ड भरें.',
        'welcome': 'स्वागत हे', 'lbl_fullname': 'पूरा नाम', 'lbl_mobile': 'मोबाइल', 'logout': 'लॉगआउट',
        'edit_btn': '⚙ विवरण संपादित करें', 'edit_title': 'विवरण अपडेट करें', 
        'chg_fullname': 'अपना पूरा नाम बदलें:', 'chg_id': 'अपनी आईडी का नाम बदलें:', 'ok': 'ठीक है',
        'about_me': 'मेरे बारे में', 'save_about': 'सहेजें', 'search_title': 'यूज़र खोजें',
        'search_btn': 'खोजें', 'not_found': 'यूज़र नहीं मिला!', 'message_btn': 'संदेश भेजें',
        'send_btn': 'भेजें', 'call_alert': 'कॉल फीचर अगले अपडेट में आ रहा है!',
        'edit_msg': 'संदेश संपादित करें', 'chats_title': 'आपकी चैट'
    }
}

# --- పర్మనెంట్ డేటాబేస్ సెటప్ ---
def init_db():
    with sqlite3.connect('m_app_users.db') as conn:
        cursor = conn.cursor()
        # యూజర్స్ టేబుల్ (About Me యాడ్ అయింది)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                full_name TEXT,
                mobile TEXT,
                password TEXT,
                profile_pic TEXT DEFAULT '',
                about_me TEXT DEFAULT ''
            )
        ''')
        # మెసేజ్ స్టోరేజ్ టేబుల్ (Instagram లాంటి రియల్-టైమ్ స్టోరేజ్)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER,
                receiver_id INTEGER,
                message_text TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

init_db()
temp_otps = {}

# --- HTML/CSS/JavaScript మాస్టర్ UI ---
MAIN_UI = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>M App</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; font-family:sans-serif; }
        body { background:#fafafa; display:flex; justify-content:center; align-items:center; min-height:100vh; padding:0; }
        
        /* కంటైనర్ & మొబైల్ ఫ్రెండ్లీ థీమ్ */
        .app-container { width:100%; max-width:420px; height:100vh; background:white; display:flex; flex-direction:column; position:relative; border-left:1px solid #dbdbdb; border-right:1px solid #dbdbdb; }
        
        /* పైన బ్లూ కలర్ స్పేస్ / హెడర్ */
        .blue-header { background: #0095f6; color: white; padding: 15px; font-size: 18px; font-weight: bold; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .blue-header a { color: white; text-decoration: none; font-size: 14px; }
        
        /* కింద గ్రీన్ కలర్ స్పేస్ / నేవిగేషన్ బార్ */
        .green-footer { background: #2ecc71; height: 60px; display: flex; justify-content: space-around; align-items: center; position: absolute; bottom: 0; width: 100%; box-shadow: 0 -2px 5px rgba(0,0,0,0.1); }
        .footer-icon { font-size: 24px; color: white; cursor: pointer; text-decoration: none; background: none; border: none; }
        .footer-profile-pic { width: 32px; height: 32px; border-radius: 50%; object-fit: cover; border: 2px solid white; }
        
        /* మెయిన్ బాడీ కంటెంట్ */
        .content-area { flex: 1; padding: 20px; overflow-y: auto; margin-bottom: 60px; }
        
        .card { background:white; padding:20px; text-align:center; border-radius:4px; width: 100%; }
        .logo-m { font-size: 55px; font-weight: bold; background: linear-gradient(45deg, #f09433, #bc1888); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom:20px; }
        input, select, textarea { width:100%; padding:10px; margin:8px 0; border:1px solid #dbdbdb; background:#fafafa; border-radius:4px; outline:none; }
        .btn { width:100%; padding:10px; background:#0095f6; color:white; border:none; border-radius:4px; font-weight:bold; cursor:pointer; }
        .error { color:red; font-size:13px; margin:10px 0; }
        
        /* డాష్‌బోర్డ్ ప్రొఫైల్ స్టైలింగ్ (Image 1000162373.jpg లాగా) */
        .profile-section { display: flex; margin-top: 15px; border-bottom: 1px solid #efefef; padding-bottom: 20px; text-align: left;}
        .p-left { flex: 1.2; line-height: 1.8; font-size: 15px; }
        .p-right { flex: 0.8; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .profile-circle { width:110px; height:110px; border-radius:50%; border:2px dashed #dbdbdb; display:flex; justify-content:center; align-items:center; position:relative; overflow:hidden; cursor:pointer; background:#f0f0f0; }
        .profile-circle img { width:100%; height:100%; object-fit:cover; }
        .plus-icon { font-size:30px; color:#8e8e8e; position:absolute; }
        
        /* అబౌట్ మీ బాక్స్ డిజైన్ */
        .about-display { background: #f7f9fa; border-left: 4px solid #0095f6; padding: 10px; margin-top: 15px; border-radius: 4px; text-align: left; }
        
        /* చాట్ విండో (ఇన్‌స్టాగ్రామ్ లాంటి స్టైల్) */
        .chat-container { display: flex; flex-direction: column; height: 100%; }
        .chat-messages { flex: 1; overflow-y: auto; padding: 10px; display: flex; flex-direction: column; }
        .msg-bubble { max-width: 75%; padding: 10px; margin: 5px 0; border-radius: 15px; font-size: 14px; position: relative; word-wrap: break-word; cursor: pointer; }
        .msg-sender { background: #e1ffc7; align-self: flex-end; border-bottom-right-radius: 0; text-align: right; }
        .msg-receiver { background: #f1f0f0; align-self: flex-start; border-bottom-left-radius: 0; }
        
        /* సన్నటి మొబైల్ మెసేజ్ బాక్స్ */
        .chat-input-area { display: flex; padding: 8px; border-top: 1px solid #efefef; background: white; align-items: center; }
        .chat-input-area input { flex: 1; padding: 8px 12px; margin: 0; border-radius: 20px; border: 1px solid #dbdbdb; }
        .chat-input-area button { background: none; border: none; color: #0095f6; font-weight: bold; margin-left: 10px; cursor: pointer; font-size: 15px; }
        
        /* లిస్ట్ వ్యూస్ */
        .item-row { display: flex; align-items: center; padding: 12px; border-bottom: 1px solid #f1f1f1; cursor: pointer; text-decoration: none; color: black; }
        .item-avatar { width: 40px; height: 40px; border-radius: 50%; background: #ddd; margin-right: 12px; object-fit: cover; }
        
        /* పాపప్ మోడల్స్ */
        .popup-modal { display:none; position:fixed; top:50%; left:50%; transform:translate(-50%, -50%); background:white; border:1px solid #dbdbdb; padding:20px; border-radius:8px; box-shadow:0 4px 20px rgba(0,0,0,0.15); z-index:100; width:90%; max-width:360px; }
        .overlay { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.4); z-index:99; }
    </style>
</head>
<body>

    <div class="app-container">
        
        <!-- లాగిన్/సైన్అప్/ఫర్గాట్ పేజీలు తప్ప మిగిలిన వాటికి టాప్ హెడర్ ఉంటుంది -->
        {% if page not in ['login', 'signup', 'forgot'] %}
        <div class="blue-header">
            <span>
                {% if page == 'chat_window' %}
                    @{{ target_user[1] }}
                {% else %}
                    {{ t.logo }} App
                {% endif %}
            </span>
            <div>
                {% if page == 'dashboard' %}
                    <a href="javascript:void(0)" onclick="openAboutPopup()" style="margin-right:15px; text-decoration:underline;">{{ t.about_me }}</a>
                    <a href="/logout?lang={{ lang }}">{{ t.logout }}</a>
                {% elif page == 'chat_window' %}
                    <span onclick="alert('{{ t.call_alert }}')" style="cursor:pointer; font-size:18px; margin-right:10px;">📞</span>
                    <a href="/chats?lang={{ lang }}">✕</a>
                {% elif page == 'view_profile' %}
                    <a href="/search?lang={{ lang }}">← Back</a>
                {% endif %}
            </div>
        </div>
        {% endif %}

        <!-- మెయిన్ కంటెంట్ ఏరియా -->
        <div class="content-area">
            
            <!-- 1. లాగిన్ పేజీ -->
            {% if page == 'login' %}
            <div class="card" style="margin-top: 40px;">
                <form method="GET" action="/">
                    <select name="lang" onchange="this.form.submit()">
                        <option value="en" {% if lang=='en' %}selected{% endif %}>English (UK)</option>
                        <option value="te" {% if lang=='te' %}selected{% endif %}>తెలుగు</option>
                        <option value="hi" {% if lang=='hi' %}selected{% endif %}>हिंदी</option>
                    </select>
                </form>
                <div class="logo-m">{{ t.logo }}</div>
                {% if msg %}<div class="error">{{ msg }}</div>{% endif %}
                <form method="POST" action="/login_submit?lang={{ lang }}">
                    <input type="text" name="username" placeholder="{{ t.user_placeholder }}" required>
                    <input type="password" name="password" placeholder="{{ t.pass_placeholder }}" required>
                    <button class="btn" type="submit" style="margin-top:10px;">{{ t.login }}</button>
                </form>
                <a href="/forgot?lang={{ lang }}" class="link" style="display:inline-block; margin-top:15px; color:#00376b; text-decoration:none;">{{ t.forgot }}</a>
                <a href="/signup?lang={{ lang }}" class="btn" style="background:#262626; text-decoration:none; display:block; margin-top:25px; text-align:center;">{{ t.create_acc }}</a>
            </div>

            <!-- 2. సైన్ అప్ పేజీ -->
            {% if page == 'signup' %}
            <!-- (పాత సైన్అప్ కోడ్ యథాతథంగా ఇక్కడ రన్ అవుతుంది) -->
            <div class="card">
                <div class="logo-m">{{ t.logo }}</div>
                <h3>{{ t.create_acc }}</h3>
                {% if msg %}<div class="error">{{ msg }}</div>{% endif %}
                <div id="step1">
                    <input type="tel" id="mobile" placeholder="Mobile Number" required>
                    <button class="btn" onclick="sendOTP('signup')">{{ t.send_otp }}</button>
                </div>
                <div id="step2" style="display:none; margin-top:10px;">
                    <input type="text" id="otp" placeholder="{{ t.enter_otp }}">
                    <button class="btn" onclick="verifyOTP()">{{ t.verify }}</button>
                </div>
                <div id="step3" style="display:none;">
                    <form method="POST" action="/signup_finish?lang={{ lang }}">
                        <input type="hidden" name="final_mobile" id="final_mobile">
                        <input type="text" name="full_name" placeholder="{{ t.full_name }}" required>
                        <input type="text" name="username" placeholder="{{ t.id_name }}" required>
                        <input type="password" name="password" placeholder="{{ t.set_pass }}" required>
                        <button class="btn" type="submit">{{ t.submit }}</button>
                    </form>
                </div>
                <a href="/?lang={{ lang }}" style="display:block; margin-top:15px;">Back to Login</a>
            </div>
            {% endif %}

            <!-- 3. పాస్‌వర్డ్ రీసెట్ పేజీ -->
            {% if page == 'forgot' %}
            <div class="card">
                <div class="logo-m">{{ t.logo }}</div>
                <h3>{{ t.forgot }}</h3>
                <div id="f_step1">
                    <input type="tel" id="f_mobile" placeholder="Enter Mobile Number" required>
                    <button class="btn" onclick="sendOTP('forgot')">{{ t.send_otp }}</button>
                </div>
                <div id="f_step2" style="display:none;">
                    <input type="text" id="f_otp" placeholder="{{ t.enter_otp }}">
                    <input type="password" id="f_new_pass" placeholder="Enter New Password">
                    <button class="btn" onclick="resetPassword()">Reset Password</button>
                </div>
                <a href="/?lang={{ lang }}" style="display:block; margin-top:15px;">Back to Login</a>
            </div>
            {% endif %}

            <!-- 4. ప్రొఫైల్ డాష్‌బోర్డ్ పేజీ (Image 1000162373.jpg డిజైన్) -->
            {% elif page == 'dashboard' %}
            <div class="profile-section">
                <div class="p-left">
                    <h3 style="font-size:20px; font-family: cursive;">{{ t.welcome }},</h3>
                    <h2 style="color:#0095f6; font-size:22px; margin-bottom:10px;">@<span id="lbl_username">{{ user[1] }}</span></h2>
                    <p><strong>{{ t.lbl_fullname }}:</strong> <br><span id="lbl_fullname">{{ user[2] }}</span></p>
                    <p><strong>{{ t.lbl_mobile }}:</strong> <br>{{ user[3] }}</p>
                </div>
                <div class="p-right">
                    <div class="profile-circle" onclick="document.getElementById('fileInput').click()">
                        {% if user[5] %}
                            <img id="view_pic" src="{{ user[5] }}">
                        {% else %}
                            <span class="plus-icon" id="plus">+</span>
                            <img id="view_pic" src="" style="display:none;">
                        {% endif %}
                    </div>
                    <input type="file" id="fileInput" accept="image/*" style="display:none;" onchange="loadImg(event)">
                    <button class="btn" onclick="openEditPopup()" style="background:#262626; padding:6px; font-size:12px; margin-top:10px; width:110px;">{{ t.edit_btn }}</button>
                </div>
            </div>
            
            <!-- అబౌట్ మీ ప్రదర్శన స్పేస్ -->
            <div class="about-display">
                <strong>About me:-</strong>
                <p id="about_text_p" style="color:#555; white-space: pre-wrap; margin-top:5px;">{{ user[6] if user[6] else 'No about text added yet.' }}</p>
            </div>

            <!-- 5. యూజర్ సెర్చ్ పేజీ -->
            {% elif page == 'search' %}
            <h3>{{ t.search_title }}</h3>
            <form method="POST" action="/search_user?lang={{ lang }}" style="display:flex; margin-top:10px;">
                <input type="text" name="search_username" placeholder="Enter ID Name..." style="margin:0; border-radius:4px 0 0 4px;" required>
                <button type="submit" class="btn" style="width:auto; border-radius:0 4px 4px 0; padding:0 20px;">{{ t.search_btn }}</button>
            </form>
            {% if msg %}
                <div class="error" style="margin-top:20px; font-weight:bold;">{{ msg }}</div>
            {% endif %}

            <!-- 6. ఇతరుల ప్రొఫైల్ చూసే పేజీ (సెర్చ్ రిజల్ట్) -->
            {% elif page == 'view_profile' %}
            <div class="profile-section">
                <div class="p-left">
                    <h2 style="color:#0095f6;">@{{ target_user[1] }}</h2>
                    <p><strong>{{ t.lbl_fullname }}:</strong> <br>{{ target_user[2] }}</p>
                </div>
                <div class="p-right">
                    <div class="profile-circle" style="cursor:default;">
                        {% if target_user[5] %}
                            <img src="{{ target_user[5] }}">
                        {% else %}
                            <span style="font-size:40px; color:#ccc;">👤</span>
                        {% endif %}
                    </div>
                </div>
            </div>
            <div class="about-display">
                <strong>About me:-</strong>
                <p style="color:#555; white-space: pre-wrap; margin-top:5px;">{{ target_user[6] if target_user[6] else '' }}</p>
            </div>
            <!-- మొబైల్ ఆప్షన్ బదులు 'Message' బటన్ ఇక్కడ యాడ్ చేయబడింది -->
            <a href="/chat/{{ target_user[0] }}?lang={{ lang }}" class="btn" style="margin-top:25px; display:block; text-align:center; background:#2ecc71; text-decoration:none;">💬 {{ t.message_btn }}</a>

            <!-- 7. ఇన్‌స్టాగ్రామ్ లాంటి చాట్ విండో -->
            {% elif page == 'chat_window' %}
            <div class="chat-container">
                <div class="chat-messages" id="chat_msg_box">
                    {% for msg in chat_messages %}
                        <div class="msg-bubble {% if msg[1] == session['user_id'] %}msg-sender{% else %}msg-receiver{% endif %}" 
                             onclick="triggerEditMessage('{{ msg[0] }}', '{{ msg[3] }}', '{{ msg[1] }}')"
                            {{ msg[3] }}
                        </div>
                    {% endfor %}
                </div>
                <form method="POST" action="/send_message/{{ target_user[0] }}?lang={{ lang }}" class="chat-input-area">
                    <input type="text" name="msg_text" placeholder="Type a message..." autocomplete="off" required>
                    <button type="submit">{{ t.send_btn }}</button>
                </form>
            </div>

            <!-- 8. యాక్టివ్ చాట్స్ లిస్ట్ పేజీ -->
            {% elif page == 'chats_list' %}
            <h3>{{ t.chats_title }}</h3>
            <div style="margin-top:15px;">
                {% for chat in dynamic_chats %}
                <a href="/chat/{{ chat.id }}?lang={{ lang }}" class="item-row">
                    <div class="item-avatar" style="display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; background:#0095f6;">
                        {{ chat.username[0]|upper }}
                    </div>
                    <div>
                        <strong>@{{ chat.username }}</strong>
                        <div style="font-size:12px; color:#888;">Click to open conversation</div>
                    </div>
                </a>
                {% else %}
                    <p style="color:#888; text-align:center; margin-top:30px;">No active chats yet. Use Search to start a conversation!</p>
                {% endfor %}
            </div>
            {% endif %}

        </div>

        <!-- కింద గ్రీన్ కలర్ నేవిగేషన్ బార్ (లాగిన్ స్క్రీన్లలో రాదు) -->
        {% if page not in ['login', 'signup', 'forgot'] %}
        <div class="green-footer">
            <a href="/search?lang={{ lang }}" class="footer-icon">🔍</a>
            <a href="/chats?lang={{ lang }}" class="footer-icon">💬</a>
            <a href="/dashboard?lang={{ lang }}" class="footer-icon">
                <div class="footer-profile-pic" style="background:#fff; display:inline-block; text-align:center; line-height:28px; color:#2ecc71; font-weight:bold; font-size:12px;">M</div>
            </a>
        </div>
        {% endif %}

    </div>

    <!-- --- అన్ని పాపప్ విండోస్ (Modals) --- -->
    <div class="overlay" id="overlay" onclick="closeAllPopups()"></div>
    
    <!-- 1. అబౌట్ మీ ఎంటర్ చేసే పాపప్ బాక్స్ -->
    <div class="popup-modal" id="aboutPopup">
        <h3>{{ t.about_me }}</h3>
        <textarea id="about_input_text" rows="4" placeholder="Write something about yourself..."></textarea>
        <button class="btn" onclick="submitAboutMe()">{{ t.ok }}</button>
    </div>

    <!-- 2. ప్రొఫైల్ ఎడిట్ పాపప్ -->
    <div class="popup-modal" id="editPopup">
        <h3>{{ t.edit_title }}</h3>
        <label style="text-align:left; display:block; margin-top:10px; font-size:13px; font-weight:bold;">{{ t.chg_fullname }}</label>
        <input type="text" id="edit_fullname" value="{{ user[2] if user else '' }}">
        <label style="text-align:left; display:block; margin-top:10px; font-size:13px; font-weight:bold;">{{ t.chg_id }}</label>
        <input type="text" id="edit_username" value="{{ user[1] if user else '' }}">
        <button class="btn" onclick="submitEditDetails()">{{ t.ok }}</button>
    </div>

    <!-- 3. మెసేజ్ ఎడిట్ పాపప్ బాక్స్ -->
    <div class="popup-modal" id="msgEditPopup">
        <h3>{{ t.edit_msg }}</h3>
        <input type="hidden" id="edit_msg_id">
        <input type="text" id="edit_msg_text">
        <button class="btn" onclick="submitMessageEdit()">{{ t.ok }}</button>
    </div>

    <script>
    // చాట్ బాక్స్ ఆటోమేటిక్ గా కిందకు స్క్రోల్ అవ్వడానికి
    window.onload = function() {
        var box = document.getElementById('chat_msg_box');
        if(box) { box.scrollTop = box.scrollHeight; }
    }

    function openAboutPopup() {
        document.getElementById('aboutPopup').style.display = 'block';
        document.getElementById('overlay').style.display = 'block';
    }

    function openEditPopup() {
        document.getElementById('editPopup').style.display = 'block';
        document.getElementById('overlay').style.display = 'block';
    }

    function closeAllPopups() {
        document.getElementById('aboutPopup').style.display = 'none';
        document.getElementById('editPopup').style.display = 'none';
        document.getElementById('msgEditPopup').style.display = 'none';
        document.getElementById('overlay').style.display = 'none';
    }

    function submitAboutMe() {
        let txt = document.getElementById('about_input_text').value;
        fetch('/api/update_about', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({about_me: txt})
        })
        .then(res => res.json())
        .then(data => {
            if(data.status === 'success') {
                document.getElementById('about_text_p').innerText = txt;
                closeAllPopups();
            }
        });
    }

    function submitEditDetails() {
        let newFullname = document.getElementById('edit_fullname').value;
        let newUsername = document.getElementById('edit_username').value;
        fetch('/api/update_profile', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({full_name: newFullname, username: newUsername})
        })
        .then(res => res.json())
        .then(data => {
            alert(data.msg);
            if(data.status === 'success') {
                document.getElementById('lbl_fullname').innerText = newFullname;
                document.getElementById('lbl_username').innerText = newUsername;
                closeAllPopups();
            }
        });
    }

    function triggerEditMessage(msgId, oldText, senderId) {
        if (senderId !== "{{ session['user_id'] }}") return;
        document.getElementById('edit_msg_id').value = msgId;
        document.getElementById('edit_msg_text').value = oldText;
        document.getElementById('msgEditPopup').style.display = 'block';
        document.getElementById('overlay').style.display = 'block';
    }

    function submitMessageEdit() {
        let mId = document.getElementById('edit_msg_id').value;
        let mTxt = document.getElementById('edit_msg_text').value;
        fetch('/api/edit_message', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message_id: mId, message_text: mTxt})
        })
        .then(res => res.json())
        .then(data => {
            if(data.status === 'success') {
                window.location.reload();
            }
        });
    }

    function loadImg(e) {
        let img = document.getElementById('view_pic');
        img.src = URL.createObjectURL(e.target.files[0]);
        img.style.display = 'block';
        let plus = document.getElementById('plus');
        if(plus) plus.style.display = 'none';
        
        let reader = new FileReader();
        reader.onloadend = function() {
            fetch('/api/save_profile_pic', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({image_data: reader.result})
            });
        }
        reader.readAsDataURL(e.target.files[0]);
    }

    let userMobile = "";
    function sendOTP(type) {
        let num = type === 'signup' ? document.getElementById('mobile').value : document.getElementById('f_mobile').value;
        if(!num) { alert("Enter mobile number"); return; }
        userMobile = num;
        fetch('/api/send_otp?mobile=' + num)
        .then(res => res.json())
        .then(data => {
            alert(data.msg);
            if(type === 'signup') document.getElementById('step2').style.display = 'block';
            else document.getElementById('f_step2').style.display = 'block';
        });
    }
    function verifyOTP() {
        let code = document.getElementById('otp').value;
        fetch('/api/verify_otp?mobile=' + userMobile + '&otp=' + code)
        .then(res => res.json())
        .then(data => {
            if(data.status === 'success') {
                document.getElementById('step1').style.display = 'none';
                document.getElementById('step2').style.display = 'none';
                document.getElementById('step3').style.display = 'block';
                document.getElementById('final_mobile').value = userMobile;
            } else { alert(data.msg); }
        });
    }
    function resetPassword() {
        let code = document.getElementById('f_otp').value;
        let newPass = document.getElementById('f_new_pass').value;
        fetch('/api/reset_pass', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({mobile: userMobile, otp: code, password: newPass})
        }).then(res => res.json())
        .then(data => {
            alert(data.msg);
            if(data.status === 'success') window.location.href = '/';
        });
    }
    </script>
</body>
</html>
\"\"\"

# --- సర్వర్ బ్యాకెండ్ రూట్స్ ---
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    lang = request.args.get('lang', 'en')
    return render_template_string(MAIN_UI, page='login', lang=lang, t=LANGUAGES[lang], msg=request.args.get('msg', ''))

@app.route('/signup')
def signup():
    lang = request.args.get('lang', 'en')
    return render_template_string(MAIN_UI, page='signup', lang=lang, t=LANGUAGES[lang])

@app.route('/forgot')
def forgot():
    lang = request.args.get('lang', 'en')
    return render_template_string(MAIN_UI, page='forgot', lang=lang, t=LANGUAGES[lang])

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect('/')
    lang = request.args.get('lang', 'en')
    with sqlite3.connect('m_app_users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
        user = cursor.fetchone()
    return render_template_string(MAIN_UI, page='dashboard', user=user, lang=lang, t=LANGUAGES[lang])

@app.route('/search')
def search_page():
    if 'user_id' not in session: return redirect('/')
    lang = request.args.get('lang', 'en')
    return render_template_string(MAIN_UI, page='search', lang=lang, t=LANGUAGES[lang], msg=request.args.get('msg', ''))

@app.route('/search_user', methods=['POST'])
def search_user():
    lang = request.args.get('lang', 'en')
    search_name = request.form.get('search_username').strip()
    with sqlite3.connect('m_app_users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (search_name,))
        target_user = cursor.fetchone()
    
    if target_user:
        if target_user[0] == session['user_id']:
            return redirect(f'/dashboard?lang={lang}')
        return render_template_string(MAIN_UI, page='view_profile', target_user=target_user, lang=lang, t=LANGUAGES[lang])
    else:
        return redirect(f'/search?lang={lang}&msg=' + LANGUAGES[lang]['not_found'])

@app.route('/chat/<int:receiver_id>')
def chat_window(receiver_id):
    if 'user_id' not in session: return redirect('/')
    lang = request.args.get('lang', 'en')
    my_id = session['user_id']
    
    with sqlite3.connect('m_app_users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (receiver_id,))
        target_user = cursor.fetchone()
        cursor.execute('''
            SELECT * FROM messages 
            WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
            ORDER BY timestamp ASC
        ''', (my_id, receiver_id, receiver_id, my_id))
        chat_messages = cursor.fetchall()
        
    return render_template_string(MAIN_UI, page='chat_window', target_user=target_user, chat_messages=chat_messages, lang=lang, t=LANGUAGES[lang])

@app.route('/send_message/<int:receiver_id>', methods=['POST'])
def send_message(receiver_id):
    if 'user_id' not in session: return redirect('/')
    lang = request.args.get('lang', 'en')
    msg_text = request.form.get('msg_text')
    my_id = session['user_id']
    
    with sqlite3.connect('m_app_users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (sender_id, receiver_id, message_text) VALUES (?, ?, ?)', (my_id, receiver_id, msg_text))
        conn.commit()
    return redirect(f'/chat/{receiver_id}?lang={lang}')

@app.route('/chats')
def chats_list():
    if 'user_id' not in session: return redirect('/')
    lang = request.args.get('lang', 'en')
    my_id = session['user_id']
    
    with sqlite3.connect('m_app_users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT users.id, users.username FROM users
            JOIN messages ON (messages.sender_id = users.id OR messages.receiver_id = users.id)
            WHERE (messages.receiver_id = ? OR messages.sender_id = ?) AND users.id != ?
            ORDER BY messages.id ASC
        ''', (my_id, my_id, my_id))
        rows = cursor.fetchall()
        
    dynamic_chats = [{"id": row[0], "username": row[1]} for row in rows]
    return render_template_string(MAIN_UI, page='chats_list', dynamic_chats=dynamic_chats, lang=lang, t=LANGUAGES[lang])

# --- APIs ---
@app.route('/api/update_about', methods=['POST'])
def api_update_about():
    if 'user_id' not in session: return jsonify({"status": "error"})
    data = request.get_json()
    about_text = data.get('about_me')
    with sqlite3.connect('m_app_users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET about_me = ? WHERE id = ?', (about_text, session['user_id']))
        conn.commit()
    return jsonify({"status": "success"})

@app.route('/api/edit_message', methods=['POST'])
def api_edit_message():
    if 'user_id' not in session: return jsonify({"status": "error"})
    data = request.get_json()
    msg_id = data.get('message_id')
    new_text = data.get('message_text')
    with sqlite3.connect('m_app_users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE messages SET message_text = ? WHERE id = ? AND sender_id = ?', (new_text, msg_id, session['user_id']))
        conn.commit()
    return jsonify({"status": "success"})

@app.route('/api/save_profile_pic', methods=['POST'])
def api_save_profile_pic():
    if 'user_id' not in session: return jsonify({"status": "error"})
    data = request.get_json()
    img_data = data.get('image_data')
    with sqlite3.connect('m_app_users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET profile_pic = ? WHERE id = ?', (img_data, session['user_id']))
        conn.commit()
    return jsonify({"status": "success"})

@app.route('/api/update_profile', methods=['POST'])
def api_update_profile():
    if 'user_id' not in session: return jsonify({"status": "error"})
    data = request.get_json()
    full_name = data.get('full_name')
    username = data.get('username')
    try:
        with sqlite3.connect('m_app_users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET full_name = ?, username = ? WHERE id = ?', (full_name, username, session['user_id']))
            conn.commit()
        return jsonify({"status": "success", "msg": "Details saved successfully!"})
    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "msg": "Username already taken!"})

@app.route('/login_submit', methods=['POST'])
def login_submit():
    lang = request.args.get('lang', 'en')
    user_input = request.form.get('username')
    password = request.form.get('password')
    with sqlite3.connect('m_app_users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE (username=? OR mobile=?) AND password=?', (user_input, user_input, password))
        user = cursor.fetchone()
    if user:
        session['user_id'] = user[0]
        return redirect(f'/dashboard?lang={lang}')
    else:
        return redirect(f"/?lang={lang}&msg=" + LANGUAGES[lang]['wrong'])

@app.route('/signup_finish', methods=['POST'])
def signup_finish():
    lang = request.args.get('lang', 'en')
    mobile = request.form.get('final_mobile')
    full_name = request.form.get('full_name')
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        with sqlite3.connect('m_app_users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, full_name, mobile, password) VALUES (?, ?, ?, ?)', (username, full_name, mobile, password))
            conn.commit()
        return redirect(f"/?lang={lang}&msg=Account created successfully!")
    except sqlite3.IntegrityError:
        return redirect(f"/signup?lang={lang}&msg=Username already exists!")

@app.route('/api/send_otp')
def api_send_otp():
    mobile = request.args.get('mobile')
    otp = str(random.randint(100000, 999999))
    temp_otps[mobile] = otp
    return jsonify({"status": "success", "msg": f"OTP: {otp}"})

@app.route('/api/verify_otp')
def api_verify_otp():
    mobile = request.args.get('mobile')
    otp = request.args.get('otp')
    if mobile in temp_otps and temp_otps[mobile] == otp: return jsonify({"status": "success"})
    return jsonify({"status": "error", "msg": "Wrong OTP!"})

@app.route('/api/reset_pass', methods=['POST'])
def api_reset_pass():
    data = request.get_json()
    mobile = data.get('mobile'); otp = data.get('otp'); new_pass = data.get('password')
    if mobile in temp_otps and temp_otps[mobile] == otp:
        with sqlite3.connect('m_app_users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET password = ? WHERE mobile = ?', (new_pass, mobile))
            conn.commit()
        return jsonify({"status": "success", "msg": "Success!"})
    return jsonify({"status": "error", "msg": "Failed!"})

@app.route('/logout')
def logout():
    lang = request.args.get('lang', 'en')
    session.clear()
    return redirect(f'/?lang={lang}')

if __name__ == '__main__':
    app.run(debug=True)


