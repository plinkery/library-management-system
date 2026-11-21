from PIL import Image

im = Image.open('report_assets/er_diagram_preview_rendered.png')
w, h = im.size
print('Preview size:', w, h)

# Scale factors (canvas is 3200 x 2100)
sx = w / 3200.0
sy = h / 2100.0

def crop_box(name, cx, cy, rx, ry):
    x1 = max(0, int((cx - rx) * sx))
    y1 = max(0, int((cy - ry) * sy))
    x2 = min(w, int((cx + rx) * sx))
    y2 = min(h, int((cy + ry) * sy))
    im.crop((x1, y1, x2, y2)).save(f'report_assets/check_{name}.png')
    print(f'Saved report_assets/check_{name}.png ({x2-x1}x{y2-y1})')

# 1. BOOKS & HAS_COPIES & Attributes
crop_box('books_has_copies', 1850, 720, 350, 250)

# 2. Top-right PUBLISHERS (No legend, clean)
crop_box('publishers_top_right', 2300, 220, 350, 180)

# 3. USERS & SUGGESTED_BY & reservation_blocked_until
crop_box('users_suggested', 800, 1150, 350, 280)

# 4. BOOK_REQUESTS & VOTES_ON
crop_box('requests_votes', 400, 850, 300, 300)

# 5. RESERVES_COPY & BORROWS_USER separation
crop_box('reserves_borrows_separation', 1150, 1450, 300, 250)

# 6. BOOK_COPIES & FINE_COLLECTIONS separation
crop_box('copies_collections_separation', 2300, 1380, 500, 450)

