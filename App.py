from flask import Flask, render_template_string, request, redirect, jsonify, session
import psycopg2
from psycopg2.extras import DictCursor
import random
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'm_app_super_secret_key_2026'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)

DB_URL = "postgresql://postgres.ksooqeaoeihmcpwxlyeh:mano%219133584715@aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres?sslmode=require"

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
        'login': 'లాగిన్ అవ్వండి', 'forgot': 'పాస్‌వర్డ్ మర్చిపోయారా?', 'create_acc': 'కొత్త खाताను సృష్టించండి',
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
        'edit_msg': 'संदेश संशोधित करें', 'chats_title': 'आपकी चैट'
    }
}

def init_db():
    try:
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE,
                full_name TEXT,
                mobile TEXT,
                password TEXT,
                profile_pic TEXT DEFAULT '',
                about_me TEXT DEFAULT ''
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                sender_id INTEGER,
                receiver_id INTEGER,
                message_text TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("Error:", e)

init_db()
temp_otps = {}

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
        .app-container { width:100%; max-width:420px; height:100vh; background:white; display:flex; flex-direction:column; position:relative; border-left:1px solid #dbdbdb; border-right:1px solid #dbdbdb; }
        .blue-header { background: #0095f6; color: white; padding: 15px; font-size: 18px; font-weight: bold; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .blue-header a { color: white; text-decoration: none; font-size: 14px; }
        .green-footer { background: #2ecc71; height: 60px; display: flex; justify-content: space-around; align-items: center; position: absolute; bottom: 0; width: 100%; box-shadow: 0 -2px 5px rgba(0,0,0,0.1); z-index: 10; }
        .footer-icon { font-size: 24px; color: white; cursor: pointer; text-decoration: none; background: none; border: none; }
        .content-area { flex: 1; padding: 20px; overflow-y: auto; margin-bottom: 60px; }
        .card { background:white; padding:20px; text-align:center; border-radius:4px; width: 100%; }
        .logo-m { font-size: 55px; font-weight: bold; background: linear-gradient(45deg, #f09433, #bc1888); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom:20px; }
        input, select, textarea { width:100%; padding:10px; margin:8px 0; border:1px solid #dbdbdb; background:#fafafa; border-radius:4px; outline:none; }
        .btn { width:100%; padding:10px; background:#0095f6; color:white; border:none; border-radius:4px; font-weight:bold; cursor:pointer; }
        .error { color:red; font-size:13px; margin:10px 0; }
        .profile-section { display: flex; margin-top: 15px; border-bottom: 1px solid #efefef; padding-bottom: 20px; text-align: left;}
        .p-left { flex: 1.2; line-height: 1.8; font-size: 15px; }
        .about-display { background: #f7f9fa; border-left: 4px solid #0095f6; padding: 10px; margin-top: 15px; border-radius: 4px; text-align: left; }
        .chat-container { display: flex; flex-direction: column; height: 100%; }
        .chat-messages { flex: 1; overflow-y: auto; padding: 10px; display: flex; flex-direction: column; }
        .msg-bubble { max-width: 75%; padding: 10px; margin: 5px 0; border-radius: 15px; font-size: 14px; position: relative; word-wrap: break-word; }
        .msg-sender { background: #e1ffc7; align-self: flex-end; border-bottom-right-radius: 0; text-align: right; }
        .msg-receiver { background: #f1f0f0; align-self: flex-start; border-bottom-left-radius: 0; }
        .chat-input-area { display: flex; padding: 8px; border-top: 1px solid #efefef; background: white; align-items: center; }
        .chat-input-area input { flex: 1; padding: 8px 12px; margin: 0; border-radius: 20px; border: 1px solid #dbdbdb; }
        .chat-input-area button { background: none; border: none; color: #0095f6; font-weight: bold; margin-left: 10px; cursor: pointer; font-size: 15px; }
        .item-row { display: flex; align-items: center; padding: 12px; border-bottom: 1px solid #f1f1f1; cursor: pointer; text-decoration: none; color: black; }
        .item-avatar { width: 40px; height: 40px; border-radius: 50%; background: #ddd; margin-right: 12px; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; }
    </style>
</head>
<body>
    <div class="app-container">
        {% if page not in ['login', 'signup', 'forgot'] %}
        <div class="blue-header">
            <span>
                {% if page == 'chat_window' %} @{{ target_user[1] }} {% else %} {{ t.logo }} App {% endif %}
            </span>
            <div>
                {% if page == 'dashboard' %}
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

        <div class="content-area">
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
                <a href="/forgot?lang={{ lang }}" style="display:inline-block; margin-top:15px; color:#00376b; text-decoration:none;">{{ t.forgot }}</a>
                <a href="/signup?lang={{ lang }}" class="btn" style="background:#262626; text-decoration:none; display:block; margin-top:25px; text-align:center;">{{ t.create_acc }}</a>
            </div>

            {% elif page == 'signup' %}
            <div class="card">
                <div class="logo-m">{{ t.logo }}</div>
                <h3>{{ t.create_acc }}</h3>
                {% if msg %}<div class="error">{{ msg }}</div>{% endif %}
                <div id="step1">
                    <input type="tel" id="mobile" placeholder="Mobile Number" required>
                    <button class="btn" onclick="sendOTP()">{{ t.send_otp }}</button>
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

            {% elif page == 'dashboard' %}
            <div class="profile-section">
                <div class="p-left">
                    <h3 style="font-size:20px; font-family: cursive;">{{ t.welcome }},</h3>
                    <h2 style="color:#0095f6; font-size:22px; margin-bottom:10px;">@{{ user[1] }}</h2>
                    <p><strong>{{ t.lbl_fullname }}:</strong> <br>{{ user[2] }}</p>
                    <p><strong>{{ t.lbl_mobile }}:</strong> <br>{{ user[3] }}</p>
                </div>
            </div>
            <div class="about-display">
                <strong>About me:-</strong>
                <p style="color:#555; white-space: pre-wrap; margin-top:5px;">{{ user[6] if user[6] else 'No about text added yet.' }}</p>
            </div>

            {% elif page == 'search' %}
            <h3>{{ t.search_title }}</h3>
            <form method="POST" action="/search_user?lang={{ lang }}" style="display:flex; margin-top:10px;">
                <input type="text" name="search_username" placeholder="Enter ID Name..." required>
                <button type="submit" class="btn" style="width:auto;">{{ t.search_btn }}</button>
            </form>
            {% if msg %}<div class="error" style="margin-top:20px;">{{ msg }}</div>{% endif %}

            {% elif page == 'view_profile' %}
            <div class="profile-section">
                <div class="p-left">
                    <h2 style="color:#0095f6;">@{{ target_user[1] }}</h2>
                    <p><strong>{{ t.lbl_fullname }}:</strong> <br>{{ target_user[2] }}</p>
                </div>
            </div>
            <a href="/chat/{{ target_user[0] }}?lang={{ lang }}" class="btn" style="margin-top:25px; display:block; text-align:center; background:#2ecc71; text-decoration:none;">💬 {{ t.message_btn }}</a>

            {% elif page == 'chat_window' %}
            <div class="chat-container">
                <div class="chat-messages">
                    {% for msg in chat_messages %}
                        <div class="msg-bubble {% if msg[1] == session['user_id'] %}msg-sender{% else %}msg-receiver{% endif %}">
                            {{ msg[3] }}
                        </div>
                    {% endfor %}
                </div>
                <form method="POST" action="/send_message/{{ target_user[0] }}?lang={{ lang }}" class="chat-input-area">
                    <input type="text" name="msg_text" placeholder="Type a message..." autocomplete="off" required>
                    <button type="submit">{{ t.send_btn }}</button>
                </form>
            </div>

            {% elif page == 'chats_list' %}
            <h3>{{ t.chats_title }}</h3>
            <div style="margin-top:15px;">
                {% for chat in dynamic_chats %}
                <a href="/chat/{{ chat.id }}?lang={{ lang }}" class="item-row">
                    <div class="item-avatar" style="background:#0095f6;">{{ chat.username[0]|upper }}</div>
                    <div>
                        <strong>@{{ chat.username }}</strong>
                        <div style="font-size:12px; color:#888;">Click to open conversation</div>
                    </div>
                </a>
                {% else %}
                    <p style="color:#888;">No active chats.</p>
                {% endfor %}
            </div>
            {% endif %}
        </div>

        {% if page not in ['login', 'signup', 'forgot'] %}
        <div class="green-footer">
            <a href="/dashboard?lang={{ lang }}" class="footer-icon">🏠</a>
            <a href="/search?lang={{ lang }}" class="footer-icon">🔍</a>
            <a href="/chats?lang={{ lang }}" class="footer-icon">💬</a>
        </div>
        {% endif %}
    </div>

    <script>
        function sendOTP() {
            var mobile = document.getElementById('mobile').value;
            if(!mobile) { alert('Enter Mobile'); return; }
            fetch('/send_otp_ajax?mobile=' + mobile).then(r => r.json()).then(data => {
                alert("TEST OTP is: " + data.otp);
                document.getElementById('step1').style.display = 'none';
                document.getElementById('step2').style.display = 'block';
                window.current_mobile = mobile;
            });
        }
        function verifyOTP() {
            var otp = document.getElementById('otp').value;
            fetch('/verify_otp_ajax?mobile=' + window.current_mobile + '&otp=' + otp).then(r => r.json()).then(data => {
                if(data.success) {
                    document.getElementById('step2').style.display = 'none';
                    document.getElementById('step3').style.display = 'block';
                    document.getElementById('final_mobile').value = window.current_mobile;
                } else { alert('Wrong OTP'); }
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    lang = request.args.get('lang', 'en')
    if 'user_id' in session:
        return redirect(f'/dashboard?lang={lang}')
    return render_template_string(MAIN_UI, page='login', lang=lang, t=LANGUAGES[lang], msg=request.args.get('msg'))

@app.route('/login_submit', methods=['POST'])
def login_submit():
    lang = request.args.get('lang', 'en')
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username = %s OR mobile = %s", (username, username))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user and user[1] == password:
        session.permanent = True  
        session['user_id'] = user[0]
        return redirect(f'/dashboard?lang={lang}')
    return redirect(f'/?lang={lang}&msg=' + LANGUAGES[lang]['wrong'])

@app.route('/signup')
def signup():
    lang = request.args.get('lang', 'en')
    return render_template_string(MAIN_UI, page='signup', lang=lang, t=LANGUAGES[lang])

@app.route('/send_otp_ajax')
def send_otp_ajax():
    mobile = request.args.get('mobile')
    otp = str(random.randint(1000, 9999))
    temp_otps[mobile] = otp
    return jsonify({'success': True, 'otp': otp})

@app.route('/verify_otp_ajax')
def verify_otp_ajax():
    mobile = request.args.get('mobile')
    otp = request.args.get('otp')
    if temp_otps.get(mobile) == otp:
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/signup_finish', methods=['POST'])
def signup_finish():
    lang = request.args.get('lang', 'en')
    mobile = request.form.get('final_mobile')
    full_name = request.form.get('full_name')
    username = request.form.get('username')
    password = request.form.get('password')
    
    try:
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, full_name, mobile, password) VALUES (%s, %s, %s, %s) RETURNING id", 
                       (username, full_name, mobile, password))
        new_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        session.permanent = True  
        session['user_id'] = new_id
    /dashboard?lang={lang}')
    except Exception as e:
        return redirect(f'/signup?lang={lang}&msg=Username already exists!')

@app.route('/dashboard')
def dashboard():
    lang = request.args.get('lang', 'en')
    if 'user_id' not in session: return redirect(f'/?lang={lang}')
    
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template_string(MAIN_UI, page='dashboard', lang=lang, t=LANGUAGES[lang], user=user)

@app.route('/search')
def search():
    lang = request.args.get('lang', 'en')
    if 'user_id' not in session: return redirect(f'/?lang={lang}')
    return render_template_string(MAIN_UI, page='search', lang=lang, t=LANGUAGES[lang], msg=request.args.get('msg'))

@app.route('/search_user', methods=['POST'])
def search_user():
    lang = request.args.get('lang', 'en')
    search_username = request.form.get('search_username')
    
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (search_username,))
    target = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if target:
        return redirect(f'/profile/{target[0]}?lang={lang}')
    return redirect(f'/search?lang={lang}&msg=' + LANGUAGES[lang]['not_found'])

@app.route('/profile/<int:user_id>')
def profile(user_id):
    lang = request.args.get('lang', 'en')
    if 'user_id' not in session: return redirect(f'/?lang={lang}')
    
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    target_user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template_string(MAIN_UI, page='view_profile', lang=lang, t=LANGUAGES[lang], target_user=target_user)

@app.route('/chat/<int:target_id>')
def chat_window(target_id):
    lang = request.args.get('lang', 'en')
    if 'user_id' not in session: return redirect(f'/?lang={lang}')
    my_id = session['user_id']
    
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (target_id,))
    target_user = cursor.fetchone()
    
    cursor.execute("""
        SELECT * FROM messages 
        WHERE (sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s)
        ORDER BY timestamp ASC
    """, (my_id, target_id, target_id, my_id))
    chat_messages = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template_string(MAIN_UI, page='chat_window', lang=lang, t=LANGUAGES[lang], target_user=target_user, chat_messages=chat_messages)

@app.route('/send_message/<int:target_id>', methods=['POST'])
def send_message(target_id):
    lang = request.args.get('lang', 'en')
    if 'user_id' not in session: return redirect(f'/?lang={lang}')
    msg_text = request.form.get('msg_text')
    my_id = session['user_id']
    
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (sender_id, receiver_id, message_text) VALUES (%s, %s, %s)", (my_id, target_id, msg_text))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(f'/chat/{target_id}?lang={lang}')

@app.route('/chats')
def chats_list():
    lang = request.args.get('lang', 'en')
    if 'user_id' not in session: return redirect(f'/?lang={lang}')
    my_id = session['user_id']
    
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("""
        SELECT DISTINCT u.id, u.username FROM users u
        JOIN messages m ON (u.id = m.sender_id OR u.id = m.receiver_id)
        WHERE (m.sender_id = %s OR m.receiver_id = %s) AND u.id != %s
    """, (my_id, my_id, my_id))
    dynamic_chats = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template_string(MAIN_UI, page='chats_list', lang=lang, t=LANGUAGES[lang], dynamic_chats=dynamic_chats)

@app.route('/logout')
def logout():
    lang = request.args.get('lang', 'en')
    session.clear()
    return redirect(f'/?lang={lang}')

if __name__ == '__main__':
    app.run(debug=True)
    
