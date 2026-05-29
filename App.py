from flask import Flask, render_template_string, request, redirect, jsonify
import sqlite3
import random
import requests

app = Flask(__name__)

# --- మల్టీ-లాంగ్వేజ్ ట్రాన్స్‌లేషన్ డేటా ---
LANGUAGES = {
    'en': {
        'logo': 'M', 'user_placeholder': 'Username, email or mobile number', 'pass_placeholder': 'Password',
        'login': 'Log in', 'forgot': 'Forgotten password?', 'create_acc': 'Create new account',
        'send_otp': 'Send OTP', 'enter_otp': 'Enter OTP', 'verify': 'Verify OTP',
        'full_name': 'Enter your full name', 'id_name': 'Create your ID name', 'set_pass': 'Set Password',
        'submit': 'Enter', 'wrong': 'Wrong username or password!', 'otp_sent': 'OTP sent successfully!',
        'wrong_otp': 'Wrong OTP! Try again.', 'fill_fields': 'Please fill all fields.'
    },
    'te': {
        'logo': 'M', 'user_placeholder': 'యూజర్ నేమ్, ఈమెయిల్ లేదా మొబైల్ నంబర్', 'pass_placeholder': 'పాస్‌వర్డ్',
        'login': 'లాగిన్...] అవ్వండి', 'forgot': 'పాస్‌వర్డ్ మర్చిపోయారా?', 'create_acc': 'కొత్త खाताను సృష్టించండి',
        'send_otp': 'OTP పంపండి', 'enter_otp': 'OTP ని నమోదు చేయండి', 'verify': 'OTP ని వెరిఫై చేయండి',
        'full_name': 'మీ పూర్తి పేరును నమోదు చేయండి', 'id_name': 'మీ ఐడీ పేరును సృష్టించండి', 'set_pass': 'పాస్‌వర్డ్ సెట్ చేయండి',
        'submit': 'సమర్పించు', 'wrong': 'తప్పుడు యూజర్ నేమ్ లేదా పాస్‌వర్డ్!', 'otp_sent': 'OTP విజయవంతంగా పంపబడింది!',
        'wrong_otp': 'తప్పుడు OTP! మళ్ళీ ప్రయత్నించండి.', 'fill_fields': 'దయచేసి అన్ని వివరాలు పూరించండి.'
    },
    'hi': {
        'logo': 'M', 'user_placeholder': 'यूजरनेम, ईमेल या मोबाइल नंबर', 'pass_placeholder': 'पासवर्ड',
        'login': 'लॉग इन करें', 'forgot': 'पासवर्ड भूल गए?', 'create_acc': 'नया अकाउंट बनाएं',
        'send_otp': 'ओटीपी भेजें', 'enter_otp': 'ओटीपी दर्ज करें', 'verify': 'ओटीपी सत्यापित करें',
        'full_name': 'अपना पूरा नाम दर्ज करें', 'id_name': 'अपनी आईडी का नाम बनाएं', 'set_pass': 'पासवर्ड सेट करें',
        'submit': 'दर्ज करें', 'wrong': 'गलत उपयोगकर्ता नाम या पासवर्ड!', 'otp_sent': 'ओटीपी सफलतापूर्वक भेजा गया!',
        'wrong_otp': 'गलत ओटीपी! फिर से प्रयास करें।', 'fill_fields': 'कृपया सभी फ़ील्ड भरें।'
    }
}

# --- SMS OTP పంపే ఫంక్షన్ ---
def send_real_sms(mobile, otp_code):
    api_key = "YOUR_FAST2SMS_API_KEY_HERE"
    message = f"Your OTP code is {otp_code}. Sent from M App."
    print(f"--- SMS SENT TO {mobile}: {message} ---")
    try:
        url = "https://www.fast2sms.com/dev/bulkV2"
        headers = {'authorization': api_key}
        payload = {'message': message, 'language': 'english', 'route': 'q', 'numbers': mobile}
        requests.post(url, headers=headers, data=payload)
    except:
        pass

# --- డేటాబేస్ செటప్ ---
def init_db():
    conn = sqlite3.connect('m_app_users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            full_name TEXT,
            mobile TEXT,
            password TEXT,
            profile_pic TEXT DEFAULT ''
        )
    ''')
    conn.commit()
    conn.close()

init_db()
temp_otps = {}

# --- HTML మాస్టర్ UI ---
MAIN_UI = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>M App</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; font-family:sans-serif; }
        body { background:#fafafa; display:flex; justify-content:center; align-items:center; min-height:100vh; padding:10px; }
        .card { background:white; border:1px solid #dbdbdb; width:100%; max-width:380px; padding:30px 20px; text-align:center; border-radius:4px; }
        .logo-m { font-size: 60px; font-weight: bold; background: linear-gradient(45deg, #f09433, #bc1888); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom:20px; }
        select { padding:5px; margin-bottom:20px; border-radius:4px; border:1px solid #dbdbdb; }
        input { width:100%; padding:10px; margin:6px 0; border:1px solid #dbdbdb; background:#fafafa; border-radius:4px; outline:none; }
        .btn { width:100%; padding:10px; background:#0095f6; color:white; border:none; border-radius:4px; font-weight:bold; cursor:pointer; margin-top:10px; }
        .link { color:#00376b; text-decoration:none; display:inline-block; margin-top:15px; font-size:14px; }
        .error { color:red; font-size:13px; margin:10px 0; }
        
        /* డాష్‌బోర్డ్ లెఫ్ట్ & రైట్ డిజైన్ */
        .dashboard { max-width:800px; width:100%; display:flex; background:white; border:1px solid #dbdbdb; border-radius:8px; padding:20px; box-shadow:0 4px 10px rgba(0,0,0,0.05); }
        .left-panel { flex:1; border-right:1px solid #efefef; padding:20px; text-align:left; line-height:2; }
        .right-panel { flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:20px; }
        .profile-circle { width:150px; height:150px; border-radius:50%; border:3px dashed #dbdbdb; display:flex; justify-content:center; align-items:center; position:relative; overflow:hidden; cursor:pointer; background:#f0f0f0; }
        .profile-circle img { width:100%; height:100%; object-fit:cover; }
        .plus-icon { font-size:40px; color:#8e8e8e; position:absolute; }
        .crop-controls { display:none; margin-top:15px; text-align:center; }
        .crop-controls input { width:120px; }
        
        /* ఎడిట్ బాక్స్ మోడల్ స్టైల్ */
        .edit-popup { display:none; position:fixed; top:50%; left:50%; transform:translate(-50%, -50%); background:white; border:1px solid #dbdbdb; padding:20px; border-radius:8px; box-shadow:0 4px 20px rgba(0,0,0,0.1); z-index:100; width:90%; max-width:350px; }
        .overlay { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.3); z-index:99; }
    </style>
</head>
<body>

    {% if page == 'login' %}
    <div class="card">
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
            <button class="btn" type="submit">{{ t.login }}</button>
        </form>
        
        <a href="/forgot?lang={{ lang }}" class="link">{{ t.forgot }}</a>
        <br>
        <a href="/signup?lang={{ lang }}" class="btn" style="background:#262626; text-decoration:none; display:block; margin-top:20px;">{{ t.create_acc }}</a>
    </div>

    {% elif page == 'signup' %}
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
        <a href="/?lang={{ lang }}" class="link">Back to Login</a>
    </div>

    {% elif page == 'forgot' %}
    <div class="card">
        <div class="logo-m">{{ t.logo }}</div>
        <h3>{{ t.forgot }}</h3>
        {% if msg %}<div class="error">{{ msg }}</div>{% endif %}
        
        <div id="f_step1">
            <input type="tel" id="f_mobile" placeholder="Enter Mobile Number" required>
            <button class="btn" onclick="sendOTP('forgot')">{{ t.send_otp }}</button>
        </div>
        
        <div id="f_step2" style="display:none;">
            <input type="text" id="f_otp" placeholder="{{ t.enter_otp }}">
            <input type="password" id="f_new_pass" placeholder="Enter New Password">
            <button class="btn" onclick="resetPassword()">Reset Password</button>
        </div>
        <a href="/?lang={{ lang }}" class="link">Back to Login</a>
    </div>

    {% elif page == 'dashboard' %}
    <div class="dashboard">
        <!-- ఎడమవైపు యూజర్ డీటెయిల్స్ -->
        <div class="left-panel">
            <h2>Welcome, @<span id="lbl_username">{{ user[1] }}</span>!</h2>
            <p><strong>Full Name:</strong> <span id="lbl_fullname">{{ user[2] }}</span></p>
            <p><strong>Mobile:</strong> {{ user[3] }}</p>
            <a href="/" class="link" style="color:red; margin-top:30px;">Logout</a>
        </div>
        
        <!-- కుడివైపు ప్రొఫైల్ ఫోటో ఎడిటర్ -->
        <div class="right-panel">
            <div class="profile-circle" onclick="document.getElementById('fileInput').click()">
                <span class="plus-icon" id="plus">+</span>
                <img id="view_pic" src="" style="display:none;">
            </div>
            <input type="file" id="fileInput" accept="image/*" style="display:none;" onchange="loadImg(event)">
            
            <div class="crop-controls" id="controls">
                <p>Resize Image:</p>
                <input type="range" min="50" max="150" value="100" oninput="resizeImg(this.value)">
                <button class="btn" onclick="savePic()" style="padding:5px 10px; font-size:12px; width:auto; display:inline-block;">Set Profile Pic</button>
            </div>
            
            <!-- Edit Details బటన్ ఆప్షన్ -->
            <button class="btn" onclick="openEditPopup()" style="background:#262626; margin-top:20px; width:150px;">⚙ Edit Details</button>
        </div>
    </div>

    <!-- ఎడిట్ పాపప్ బాక్స్ -->
    <div class="overlay" id="overlay"></div>
    <div class="edit-popup" id="editPopup">
        <h3>Update Details</h3>
        <label style="text-align:left; display:block; margin-top:10px; font-size:13px; font-weight:bold;">Change your full name:</label>
        <input type="text" id="edit_fullname" value="{{ user[2] }}">
        
        <label style="text-align:left; display:block; margin-top:10px; font-size:13px; font-weight:bold;">Change your ID name:</label>
        <input type="text" id="edit_username" value="{{ user[1] }}">
        
        <input type="hidden" id="user_id" value="{{ user[0] }}">
        <button class="btn" onclick="submitEditDetails()">OK</button>
    </div>
    {% endif %}

    <script>
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

    // --- ప్రొఫైల్ ఫోటో ఎడిటింగ్ ---
    function loadImg(e) {
        let img = document.getElementById('view_pic');
        img.src = URL.createObjectURL(e.target.files[0]);
        img.style.display = 'block';
        img.style.width = '100%';
        img.style.height = '100%';
        document.getElementById('plus').style.display = 'none';
        document.getElementById('controls').style.display = 'block';
    }
    function resizeImg(val) {
        let img = document.getElementById('view_pic');
        img.style.transform = "scale(" + (val/100) + ")";
    }
    function savePic() {
        alert("Profile picture styled and set successfully!");
        document.getElementById('controls').style.display = 'none';
    }

    // --- వివరాలు ఎడిట్ చేసే కొత్త ఫంక్షన్స్ ---
    function openEditPopup() {
        document.getElementById('editPopup').style.display = 'block';
        document.getElementById('overlay').style.display = 'block';
    }

    function submitEditDetails() {
        let userId = document.getElementById('user_id').value;
        let newFullname = document.getElementById('edit_fullname').value;
        let newUsername = document.getElementById('edit_username').value;

        if(!newFullname || !newUsername) { alert("Fields cannot be empty!"); return; }

        fetch('/api/update_profile', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({id: userId, full_name: newFullname, username: newUsername})
        })
        .then(res => res.json())
        .then(data => {
            alert(data.msg);
            if(data.status === 'success') {
                // వెంటనే స్క్రీన్ మీద ఉన్న డీటెయిల్స్ అప్‌డేట్ అవుతాయి
                document.getElementById('lbl_fullname').innerText = newFullname;
                document.getElementById('lbl_username').innerText = newUsername;
                // పాపప్ క్లోజ్ చేయడం
                document.getElementById('editPopup').style.display = 'none';
                document.getElementById('overlay').style.display = 'none';
            }
        });
    }
    </script>
</body>
</html>
"""

# --- సర్వర్ రూట్స్ (Backend Routes) ---
@app.route('/')
def index():
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

@app.route('/api/send_otp')
def api_send_otp():
    mobile = request.args.get('mobile')
    otp = str(random.randint(100000, 999999))
    temp_otps[mobile] = otp
    send_real_sms(mobile, otp)
    return jsonify({"status": "success", "msg": f"OTP sent to {mobile}!"})

@app.route('/api/verify_otp')
def api_verify_otp():
    mobile = request.args.get('mobile')
    otp = request.args.get('otp')
    if mobile in temp_otps and temp_otps[mobile] == otp:
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "msg": "Wrong OTP! Please enter correct code."})

@app.route('/api/reset_pass', methods=['POST'])
def api_reset_pass():
    data = request.get_json()
    mobile = data.get('mobile')
    otp = data.get('otp')
    new_pass = data.get('password')
    if mobile in temp_otps and temp_otps[mobile] == otp:
        conn = sqlite3.connect('m_app_users.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET password = ? WHERE mobile = ?', (new_pass, mobile))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "msg": "Password updated successfully!"})
    return jsonify({"status": "error", "msg": "Invalid OTP Verification Failed!"})

# ప్రొఫైల్ అప్‌డేట్ చేసే కొత్త API
@app.route('/api/update_profile', methods=['POST'])
def api_update_profile():
    data = request.get_json()
    user_id = data.get('id')
    full_name = data.get('full_name')
    username = data.get('username')
    
    try:
        conn = sqlite3.connect('m_app_users.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET full_name = ?, username = ? WHERE id = ?', (full_name, username, user_id))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "msg": "Details updated and saved successfully!"})
    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "msg": "This ID name is already taken! Try another one."})

@app.route('/login_submit', methods=['POST'])
def login_submit():
    lang = request.args.get('lang', 'en')
    user_input = request.form.get('username')
    password = request.form.get('password')
    
    conn = sqlite3.connect('m_app_users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE (username=? OR mobile=?) AND password=?', (user_input, user_input, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return render_template_string(MAIN_UI, page='dashboard', user=user, lang=lang, t=LANGUAGES[lang])
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
        conn = sqlite3.connect('m_app_users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, full_name, mobile, password) VALUES (?, ?, ?, ?)', (username, full_name, mobile, password))
        conn.commit()
        conn.close()
        return redirect(f"/?lang={lang}&msg=Account Created Successfully! Log In Now.")
    except sqlite3.IntegrityError:
        return redirect(f"/signup?lang={lang}&msg=Username Already Exists!")

if __name__ == '__main__':
    app.run(debug=True)
