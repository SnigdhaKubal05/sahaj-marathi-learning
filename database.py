import sqlite3
import os

DB_NAME = "sahaj.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def _db_needs_reset():
    """
    Returns True if sahaj.db exists but has the OLD schema
    (sentences table has 'english' column instead of just 'marathi' + 'category').
    This lets the app auto-fix itself without the user manually deleting the DB.
    """
    if not os.path.exists(DB_NAME):
        return False
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(sentences)")
        columns = [row[1] for row in cursor.fetchall()]
        conn.close()
        # Old schema had 'english' column — new schema does NOT
        if "english" in columns:
            return True
        # Also reset if category column is missing entirely
        if "category" not in columns:
            return True
        return False
    except Exception:
        return True


def create_tables():
    # ✅ Auto-delete old DB if schema is outdated
    if _db_needs_reset():
        os.remove(DB_NAME)
        print("⚠️  Old sahaj.db detected — deleted and rebuilding with new schema.")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mulakshare (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            letter TEXT NOT NULL,
            pronunciation TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            english TEXT NOT NULL,
            marathi TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sentences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marathi TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def insert_default_data():
    conn = connect_db()
    cursor = conn.cursor()

    # --- Mulakshare ---
    cursor.execute("SELECT COUNT(*) FROM mulakshare")
    if cursor.fetchone()[0] == 0:
        letters = [
            ("अ", "a"),  ("आ", "aa"), ("इ", "i"),  ("ई", "ee"),
            ("उ", "u"),  ("ऊ", "oo"), ("ए", "e"),  ("ऐ", "ai"),
            ("ओ", "o"),  ("औ", "au")
        ]
        cursor.executemany(
            "INSERT INTO mulakshare (letter, pronunciation) VALUES (?, ?)", letters
        )

    # --- Words ---
    cursor.execute("SELECT COUNT(*) FROM words")
    if cursor.fetchone()[0] == 0:
        words = [
            ("Hello",      "नमस्कार"), ("Thank You", "धन्यवाद"),
            ("Yes",        "हो"),       ("No",        "नाही"),
            ("Water",      "पाणी"),     ("Food",      "जेवण"),
            ("Home",       "घर"),       ("School",    "शाळा"),
            ("Mother",     "आई"),       ("Father",    "वडील"),
            ("Medicine",   "औषध"),      ("Doctor",    "डॉक्टर"),
            ("Help",       "मदत"),      ("Bus",       "बस"),
            ("Milk",       "दूध"),
        ]
        cursor.executemany(
            "INSERT INTO words (english, marathi) VALUES (?, ?)", words
        )

    # --- Sentences ---
    cursor.execute("SELECT COUNT(*) FROM sentences")
    if cursor.fetchone()[0] == 0:
        sentences = [

            # ============================================
            # घरगुती  →  category = "gharguti"
            
            ("तुम्ही कसे आहात?",                      "gharguti"),
            ("मला भूक लागली आहे.",                    "gharguti"),
            ("पाणी द्या.",                      "gharguti"),
            ("दरवाजा उघडा.",                    "gharguti"),
            ("मी घरी आहे.",                           "gharguti"),
            ("जेवण तयार आहे.",                        "gharguti"),
            ("झोपायची वेळ झाली.",                     "gharguti"),
            ("दिवा लावा.",                       "gharguti"),
            ("चहा करा.",                        "gharguti"),
            ("औषध घ्यायची वेळ झाली.",                 "gharguti"),
            ("खिडकी बंद कर.",                   "gharguti"),
            ("टीव्ही बंद कर.",                        "gharguti"),
            ("मला थकवा लागला आहे.",                     "gharguti"),
            ("आंघोळीचे पाणी गरम कर.",                 "gharguti"),
            ("मला चादर आण.",                    "gharguti"),
            ("घर स्वच्छ कर.",                         "gharguti"),
            ("फोन कुठे आहे?",                         "gharguti"),

            # ============================================
            #  रुग्णालय category = "hospital"    
          
            ("मला डॉक्टरकडे जायचे आहे.",              "hospital"),
            ("माझ्या पोटात दुखत आहे.",                "hospital"),
            ("मला ताप आहे.",                          "hospital"),
            ("औषध कधी घ्यायचे?",                     "hospital"),
            ("रुग्णालय कुठे आहे?",                    "hospital"),
            ("मला श्वास घ्यायला त्रास होत आहे.",          "hospital"),
            ("कृपया नर्सला बोलवा.",                   "hospital"),
            ("माझा रक्तदाब तपासा.",                   "hospital"),
            ("मला चक्कर येत आहे.",                    "hospital"),
            ("माझ्या छातीत दुखत आहे.",                "hospital"),
            ("मला उलटी होत आहे.",                     "hospital"),
            ("माझा पाय दुखत आहे.",                    "hospital"),
            ("कृपया रुग्णवाहिका बोलवा.",              "hospital"),
            ("मला ऍलर्जी आहे.",                      "hospital"),
            ("किती दिवस औषध घ्यायचे?",               "hospital"),
            ("तपासणी कधी आहे?",                      "hospital"),
            ("मला झोप येत नाही.",                     "hospital"),

            # ============================================
            # 🛒 बाजार  →  category = "market"
    
            ("हे किती रुपयांना आहे?",                 "market"),
            ("मला भाज्या हव्या आहेत.",                "market"),
            ("दूध आहे का?",                           "market"),
            ("एक किलो टोमॅटो द्या.",                  "market"),
            ("कृपया पिशवी द्या.",                     "market"),
            ("सुट्टे पैसे आहेत का?",                  "market"),
            ("हे ताजे आहे का?",                       "market"),
            ("मला साखर हवी आहे.",                     "market"),
            ("अर्धा किलो कांदे द्या.",                "market"),
            ("आंबे किती रुपयांना आहेत?",              "market"),
            ("हे महाग आहे.",                          "market"),
            ("थोडी कमी करा किंमत.",                   "market"),
            ("मला तांदूळ हवे आहेत.",                   "market"),
            ("दोन लिटर दूध द्या.",                    "market"),
            ("चहाची पाने आहेत का?",                   "market"),
            ("बिल किती झाले?",                        "market"),
            ("UPI ने पैसे देता येतील का?",            "market"),

            # ============================================
            # 🆘 मदत  →  category = "help"
           
            ("मला मदत करा.",                          "help"),
            ("कृपया रुग्णवाहिका बोलवा.",              "help"),
            ("मी हरवलो आहे.",                         "help"),
            ("पोलिसांना बोलवा.",                      "help"),
            ("मला एकटे वाटत आहे.",                    "help"),
            ("कृपया माझ्याशी बोला.",                  "help"),
            ("मला घरी पोहोचवा.",                      "help"),
            ("माझ्या घरचा नंबर लिहून घ्या.",          "help"),
            ("मला खूप भीती वाटत आहे.",                "help"),
            ("कृपया माझ्या मुलाला फोन करा.",          "help"),
            ("कृपया माझ्या मुलीला फोन करा.",          "help"),
            ("मी पडलो आहे, मला उठता येत नाही.",          "help"),
            ("इथे कोणी आहे का?",                     "help"),
            ("माझ्याजवळ पैसे नाहीत.",                "help"),
            ("कृपया जवळ बसा.",                       "help"),
            ("मला दवाखाना दाखवा.",                    "help"),
            ("माझे नाव लिहून घ्या.",                  "help"),
            ("मला पाणी हवे आहे.",                     "help"),
        ]
        cursor.executemany(
            "INSERT INTO sentences (marathi, category) VALUES (?, ?)", sentences
        )

    conn.commit()
    conn.close()


def get_mulakshare():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT letter, pronunciation FROM mulakshare")
    data = cursor.fetchall()
    conn.close()
    return data


def get_words():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT english, marathi FROM words")
    data = cursor.fetchall()
    conn.close()
    return data


def get_sentences_by_category(category):
    """
    Called by app.py with keys: 'gharguti', 'hospital', 'market', 'help'
    Returns a plain list of Marathi sentence strings.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT marathi FROM sentences WHERE category = ?", (category,)
    )
    data = [row[0] for row in cursor.fetchall()]
    conn.close()

    return data


