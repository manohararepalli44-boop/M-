<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Manohar Arepalli | Portfolio</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        body {
            background-color: #0f172a;
            color: #f8fafc;
            line-height: 1.6;
        }
        header {
            background-color: #1e293b;
            padding: 20px;
            text-align: center;
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 2px solid #3b82f6; /* Modern Blue Accent */
        }
        header h1 {
            color: #3b82f6;
            font-size: 24px;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }
        .hero {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
            border-radius: 12px;
            margin-bottom: 40px;
        }
        .profile-container {
            position: relative;
            margin-bottom: 20px;
        }
        .profile-img {
            width: 220px;
            height: 220px;
            border-radius: 50%;
            object-fit: cover;
            border: 4px solid #3b82f6; /* Blue Border */
            box-shadow: 0 0 25px rgba(59, 130, 246, 0.4);
        }
        /* Image Upload Styling */
        .upload-btn-wrapper {
            margin-top: 10px;
            position: relative;
            overflow: hidden;
            display: inline-block;
        }
        .upload-btn {
            border: 2px dashed #3b82f6;
            color: #60a5fa;
            background-color: transparent;
            padding: 6px 15px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        .upload-btn:hover {
            background-color: #3b82f6;
            color: white;
        }
        .upload-btn-wrapper input[type=file] {
            font-size: 100px;
            position: absolute;
            left: 0;
            top: 0;
            opacity: 0;
            cursor: pointer;
        }
        .hero h2 {
            font-size: 32px;
            margin-bottom: 10px;
        }
        .hero p {
            color: #94a3b8;
            font-size: 18px;
            max-width: 600px;
        }
        .section {
            background-color: #1e293b;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            border-left: 5px solid #3b82f6; /* Blue Section Line */
        }
        .section h3 {
            color: #3b82f6;
            font-size: 22px;
            margin-bottom: 15px;
        }
        .skills-list {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            list-style: none;
            margin-top: 10px;
        }
        .skills-list li {
            background-color: #3b82f6;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
        }
        .btn {
            display: inline-block;
            background-color: #3b82f6;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            margin-top: 15px;
            transition: background 0.3s;
        }
        .btn:hover {
            background-color: #2563eb;
        }
        .contact-links {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 15px;
        }
        .contact-links p {
            font-size: 18px;
        }
        .contact-links a {
            color: #60a5fa;
            text-decoration: none;
            font-weight: bold;
        }
        .contact-links a:hover {
            text-decoration: underline;
        }
        footer {
            text-align: center;
            padding: 20px;
            color: #64748b;
            font-size: 14px;
        }
        @media (min-width: 768px) {
            .hero {
                flex-direction: row;
                text-align: left;
                justify-content: space-around;
                padding: 60px;
            }
            .hero-content {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .hero-text {
                max-width: 550px;
            }
        }
    </style>
</head>
<body>

    <header>
        <h1>Manohar Arepalli Portfolio</h1>
    </header>

    <div class="container">
        <!-- Hero Section -->
        <section class="hero">
            <div class="hero-content">
                <!-- Mee crop photo primary ga load avvuthundi -->
                <img id="profile-pic" src="https://weserv.nl" alt="Manohar Arepalli" class="profile-img">
                
                <!-- Image Upload Option -->
                <div class="upload-btn-wrapper">
                  <button class="upload-btn">📸 Change Photo</button>
                  <input type="file" id="image-loader" accept="image/*" />
                </div>
            </div>
            
            <div class="hero-text">
                <h2>Hi, I'm Manohar Arepalli 👋</h2>
                <p>B.Tech Student & Tech Enthusiast. Building a digital presence and learning to create innovative tech solutions.</p>
                <a href="#contact" class="btn">Connect With Me</a>
            </div>
        </section>

        <!-- About Section -->
        <section class="section">
            <h3>About Me</h3>
            <p>Nenu prastutam B.Tech chaduvuthunnanu. Technology ante naku chala aasakti. Kotha skills nerchukuntu, modern projects tayaru cheyadame na lakshyam. I love styling my work and keeping things creative.</p>
        </section>

        <!-- Education & Skills Section -->
        <section class="section">
            <h3>Education & Skills</h3>
            <p><strong>Degree:</strong> Bachelor of Technology (B.Tech)</p>
            <p style="margin-top: 10px;"><strong>My Skills:</strong></p>
            <ul class="skills-list">
                <li>Web Development</li>
                <li>Python / Java</li>
                <li>Problem Solving</li>
                <li>Creative Styling</li>
            </ul>
        </section>

        <!-- Contact Section -->
        <section class="section" id="contact">
            <h3>Contact Me</h3>
            <p>Natho matladalani unna leda collaborate avvalani unna kinda unna links dvaara nannu contact cheyachhu:</p>
            <div class="contact-links">
                <p>📞 <strong>Mobile:</strong> +91 9030783435</p>
                <p>📸 <strong>Instagram:</strong> <a href="https://instagram.com" target="_blank">@self_style_manohar</a></p>
            </div>
        </section>
    </div>

    <footer>
        <p>&copy; 2026 Manohar Arepalli. All Rights Reserved.</p>
    </footer>

    <!-- Image upload functional JavaScript -->
    <script>
        const imageLoader = document.getElementById('image-loader');
        const profilePic = document.getElementById('profile-pic');

        imageLoader.addEventListener('change', function(e) {
            const reader = new FileReader();
            reader.onload = function(event) {
                profilePic.src = event.target.result;
            }
            reader.readAsDataURL(e.target.files[0]);
        });
    </script>

</body>
</html>
