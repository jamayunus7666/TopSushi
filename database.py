import sqlite3
from config import DB_NAME

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            language TEXT DEFAULT 'uz'
        )''')
        
        cur.execute('''CREATE TABLE IF NOT EXISTS sushis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kategoriya TEXT,
            nomi TEXT,
            tavsif TEXT,
            narxi INTEGER,
            rasm_url TEXT
        )''')
        
        cur.execute('''CREATE TABLE IF NOT EXISTS basket (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            sushi_id INTEGER,
            miqdor INTEGER DEFAULT 1
        )''')

        cur.execute("SELECT COUNT(*) FROM sushis")
        if cur.fetchone()[0] == 0:
            sushilar = [
                ('Klassik', 'Filadelfiya', 'Losos, pishloq, bodring', 45000, 'https://yandex.uz/images/search?from=tabbar&img_url=https%3A%2F%2Fimg.vkusvill.ru%2Fpim%2Fimages%2Fsite%2Fsite_LargeWebP%2F77332e0f-a311-4ef5-875f-d1c5b72f12a6.webp&lr=10339&pos=9&rpt=simage&text=Filadelfiya%20sushi'),
                ('Klassik', 'Kaliforniya', 'Krab, tobiko, avokado', 42000, 'https://yandex.uz/images/search?from=tabbar&img_url=https%3A%2F%2Fstatic.1000.menu%2Fimg%2Fcontent-v2%2F1d%2Ffa%2F2494%2Frolly-kaliforniya-v-domashnix-usloviyax_1703322188_12_max.jpg&lr=10339&pos=2&rpt=simage&text=Kaliforniya%20sushi'),
                ('Issiq rollar', 'Hot Salmon', 'Tempura losos va pishloq', 48000, 'https://yandex.uz/images/search?from=tabbar&img_url=https%3A%2F%2Ft3.ftcdn.net%2Fjpg%2F06%2F98%2F12%2F86%2F360_F_698128630_UuoHFrjREsop5YmSAMCyXP6NJOxMlLK4.jpg&lr=10339&pos=1&rpt=simage&text=Hot%20Salmon%20sushi'),
                ('Setlar', 'Samuray Set', '32 dona turli xil rollar', 180000, 'https://yandex.uz/images/search?from=tabbar&img_url=https%3A%2F%2Fx100-venus-sm-by.gumlet.io%2Fsm-by%2Fproducts%2F0001-set_samuraj.jpg%3F%26amp%3Bw%3D300%26amp%3Bh%3D300%26amp%3Bformat%3Dauto%26amp%3Bmode%3Dfit%26amp%3Bq%3D80&lr=10339&pos=1&rpt=simage&text=Samuray%20Set%20sushi'),
                ('Vegetarian', 'Kappa Maki', 'Guruch va yangi bodring', 25000, 'https://yandex.uz/images/search?from=tabbar&img_url=https%3A%2F%2Fcafesemya.ru%2Fuploads%2Fs%2Fm%2F1%2Fk%2Fm1kaos4vtcyw%2Fimg%2Ffull_cNYXEdsM.jpg&lr=10339&pos=6&rpt=simage&text=Kappa%20Maki%20sushi'),
            ]
            cur.executemany("INSERT INTO sushis (kategoriya, nomi, tavsif, narxi, rasm_url) VALUES (?,?,?,?,?)", sushilar)
        conn.commit()

def get_user_lang(user_id: int) -> str:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        return row[0] if row else None  # None qaytarsa — yangi foydalanuvchi

def set_user_lang(user_id: int, lang: str):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO users (user_id, language) VALUES (?, ?)",
            (user_id, lang)
        )
        conn.commit()

def get_categories():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT kategoriya FROM sushis")
        return [row[0] for row in cur.fetchall()]

def get_sushis_by_category(cat: str):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, nomi FROM sushis WHERE kategoriya=?", (cat,))
        return cur.fetchall()

def get_sushi_by_id(s_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM sushis WHERE id=?", (s_id,))
        return cur.fetchone()

def add_to_basket(user_id: int, sushi_id: int, miqdor: int = 1):
    with get_connection() as conn:
        cur = conn.cursor()
        
        # Bir xil mahsulot bor-yo'qligini tekshirib, yangilash yoki qo'shish
        cur.execute("""
            SELECT miqdor FROM basket 
            WHERE user_id = ? AND sushi_id = ?
        """, (user_id, sushi_id))
        
        existing = cur.fetchone()
        
        if existing:
            new_miqdor = existing[0] + miqdor
            cur.execute("""
                UPDATE basket SET miqdor = ? 
                WHERE user_id = ? AND sushi_id = ?
            """, (new_miqdor, user_id, sushi_id))
        else:
            cur.execute("""
                INSERT INTO basket (user_id, sushi_id, miqdor) 
                VALUES (?, ?, ?)
            """, (user_id, sushi_id, miqdor))
        
        conn.commit()



def get_basket_items(user_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT s.nomi, s.narxi, b.miqdor 
            FROM basket b 
            JOIN sushis s ON b.sushi_id = s.id 
            WHERE b.user_id=?
        """, (user_id,))
        return cur.fetchall()

def clear_basket(user_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM basket WHERE user_id=?", (user_id,))
        conn.commit()

def get_basket_total(user_id: int) -> int:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT SUM(s.narxi * b.miqdor) FROM basket b JOIN sushis s ON b.sushi_id = s.id WHERE b.user_id=?", (user_id,))
        result = cur.fetchone()[0]
        return result or 0

def add_sushi(category: str, name: str, description: str, price: int, photo_url: str):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO sushis (kategoriya, nomi, tavsif, narxi, rasm_url)
            VALUES (?, ?, ?, ?, ?)
        """, (category, name, description, price, photo_url))
        conn.commit()