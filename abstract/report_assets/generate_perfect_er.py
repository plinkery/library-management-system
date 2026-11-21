import sys

def build_er_svg():
    width = 2850
    height = 2050
    
    lines = []
    entities = []
    relationships = []
    attributes = []

    # Helper styling
    COLOR_MAP = {
        'BRANCHES': {'bg': '#E8F5E9', 'border': '#2E7D32', 'attr_bg': '#F1F8E9', 'attr_b': '#33691E'},
        'SUBJECTS': {'bg': '#E0F2F1', 'border': '#00695C', 'attr_bg': '#E0F7FA', 'attr_b': '#00838F'},
        'GENRES': {'bg': '#F3E5F5', 'border': '#6A1B9A', 'attr_bg': '#F8BBD0', 'attr_b': '#880E4F'},
        'PUBLISHERS': {'bg': '#FCE4EC', 'border': '#AD1457', 'attr_bg': '#F8BBD0', 'attr_b': '#C2185B'},
        'AUTHORS': {'bg': '#E1F5FE', 'border': '#0277BD', 'attr_bg': '#E0F7FA', 'attr_b': '#0288D1'},
        'BOOKS': {'bg': '#FFEBEE', 'border': '#C62828', 'attr_bg': '#FFCDD2', 'attr_b': '#D32F2F'},
        'BOOK_COPIES': {'bg': '#EDE7F6', 'border': '#4527A0', 'attr_bg': '#D1C4E9', 'attr_b': '#512DA8'},
        'BOOK_REQUESTS': {'bg': '#E8F8F5', 'border': '#117A65', 'attr_bg': '#D5F5E3', 'attr_b': '#1E8449'},
        'USERS': {'bg': '#FFF8E1', 'border': '#F57F17', 'attr_bg': '#FFFDE7', 'attr_b': '#FBC02D'},
        'RESERVATIONS': {'bg': '#FFF3E0', 'border': '#E65100', 'attr_bg': '#FFE0B2', 'attr_b': '#F57C00'},
        'LOANS': {'bg': '#FBE9E7', 'border': '#BF360C', 'attr_bg': '#FFCCBC', 'attr_b': '#D84315'},
        'FINES': {'bg': '#FFEBEE', 'border': '#B71C1C', 'attr_bg': '#FFCDD2', 'attr_b': '#C62828'},
        'FINE_COLLECTIONS': {'bg': '#EFEBE9', 'border': '#4E342E', 'attr_bg': '#D7CCC8', 'attr_b': '#5D4037'},
        'AUDIT_LOGS': {'bg': '#ECEFF1', 'border': '#37474F', 'attr_bg': '#CFD8DC', 'attr_b': '#455A64'}
    }

    def draw_line(x1, y1, x2, y2, color="#475569", width=1.8, is_double=False, label=None, lx=None, ly=None):
        if is_double:
            # Total participation double line (offset by 2.5px)
            dx = x2 - x1
            dy = y2 - y1
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > 0:
                ox = -dy / dist * 2.5
                oy = dx / dist * 2.5
                lines.append(f'<line x1="{x1+ox:.1f}" y1="{y1+oy:.1f}" x2="{x2+ox:.1f}" y2="{y2+oy:.1f}" stroke="{color}" stroke-width="{width*0.85}" />')
                lines.append(f'<line x1="{x1-ox:.1f}" y1="{y1-oy:.1f}" x2="{x2-ox:.1f}" y2="{y2-oy:.1f}" stroke="{color}" stroke-width="{width*0.85}" />')
        else:
            lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" />')

        if label and lx is not None and ly is not None:
            lines.append(f'<rect x="{lx-20}" y="{ly-11}" width="40" height="20" rx="4" fill="#FFFFFF" fill-opacity="0.95" stroke="#94A3B8" stroke-width="0.9" />')
            lines.append(f'<text x="{lx}" y="{ly+4}" font-family="Arial, Helvetica, sans-serif" font-size="11.5" font-weight="bold" fill="#0F172A" text-anchor="middle">{label}</text>')

    def draw_polyline(pts, color="#475569", width=1.8, label=None, lx=None, ly=None):
        pts_str = " ".join([f"{x},{y}" for x, y in pts])
        lines.append(f'<polyline points="{pts_str}" fill="none" stroke="{color}" stroke-width="{width}" />')
        if label and lx is not None and ly is not None:
            lines.append(f'<rect x="{lx-20}" y="{ly-11}" width="40" height="20" rx="4" fill="#FFFFFF" fill-opacity="0.95" stroke="#94A3B8" stroke-width="0.9" />')
            lines.append(f'<text x="{lx}" y="{ly+4}" font-family="Arial, Helvetica, sans-serif" font-size="11.5" font-weight="bold" fill="#0F172A" text-anchor="middle">{label}</text>')

    def draw_entity(x, y, w, h, name, key, is_weak=False):
        c = COLOR_MAP[key]
        if is_weak:
            entities.append(f'<rect x="{x - w/2 - 5}" y="{y - h/2 - 5}" width="{w + 10}" height="{h + 10}" rx="8" fill="none" stroke="{c["border"]}" stroke-width="1.5" />')
        entities.append(f'<rect x="{x - w/2}" y="{y - h/2}" width="{w}" height="{h}" rx="6" fill="{c["bg"]}" stroke="{c["border"]}" stroke-width="2.4" filter="url(#shadow)" />')
        entities.append(f'<text x="{x}" y="{y + 5}" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="{c["border"]}" text-anchor="middle" letter-spacing="0.5">{name}</text>')

    def draw_relationship(x, y, rx, ry, name, is_identifying=False):
        pts = f"{x},{y - ry} {x + rx},{y} {x},{y + ry} {x - rx},{y}"
        if is_identifying:
            pts_out = f"{x},{y - ry - 4} {x + rx + 5},{y} {x},{y + ry + 4} {x - rx - 5},{y}"
            relationships.append(f'<polygon points="{pts_out}" fill="none" stroke="#B45309" stroke-width="1.4" />')
        relationships.append(f'<polygon points="{pts}" fill="#FEF3C7" stroke="#D97706" stroke-width="2" filter="url(#shadow)" />')
        
        words = name.split()
        if len(words) > 1:
            relationships.append(f'<text x="{x}" y="{y - 3}" font-family="Arial, Helvetica, sans-serif" font-size="10" font-weight="bold" fill="#92400E" text-anchor="middle">{words[0]}</text>')
            relationships.append(f'<text x="{x}" y="{y + 10}" font-family="Arial, Helvetica, sans-serif" font-size="10" font-weight="bold" fill="#92400E" text-anchor="middle">{words[1]}</text>')
        else:
            relationships.append(f'<text x="{x}" y="{y + 4}" font-family="Arial, Helvetica, sans-serif" font-size="10.5" font-weight="bold" fill="#92400E" text-anchor="middle">{name}</text>')

    def draw_attr(x, y, w, h, name, key, is_pk=False):
        c = COLOR_MAP[key]
        attributes.append(f'<ellipse cx="{x}" cy="{y}" rx="{w/2}" ry="{h/2}" fill="{c["attr_bg"]}" stroke="{c["attr_b"]}" stroke-width="1.6" filter="url(#shadow-sm)" />')
        weight = "bold" if is_pk else "normal"
        attributes.append(f'<text x="{x}" y="{y + 4}" font-family="Arial, Helvetica, sans-serif" font-size="10.5" font-weight="{weight}" fill="#0F172A" text-anchor="middle">{name}</text>')
        if is_pk:
            tw = len(name) * 3.3
            attributes.append(f'<line x1="{x - tw}" y1="{y + 6.5}" x2="{x + tw}" y2="{y + 6.5}" stroke="#0F172A" stroke-width="1.3" />')

    import math

    # =========================================================================
    # 1. TOP TIER ENTITIES & ATTRIBUTES (Y=260)
    # =========================================================================

    # BRANCHES (x=400, y=260)
    draw_entity(400, 260, 150, 52, "BRANCHES", "BRANCHES")
    b_attrs = [
        (300, 170, 105, 34, "branch_id", True),
        (400, 150, 115, 34, "branch_code"),
        (505, 170, 120, 34, "branch_name"),
        (525, 240, 105, 34, "hod_name")
    ]
    for ax, ay, aw, ah, aname, *pk in b_attrs:
        draw_line(400, 260, ax, ay, color="#64748B", width=1.3)
        draw_attr(ax, ay, aw, ah, aname, "BRANCHES", bool(pk and pk[0]))

    # SUBJECTS (x=950, y=260)
    draw_entity(950, 260, 150, 52, "SUBJECTS", "SUBJECTS")
    s_attrs = [
        (840, 170, 105, 34, "subject_id", True),
        (940, 150, 120, 34, "subject_code"),
        (1055, 170, 125, 34, "subject_name"),
        (1075, 240, 95, 34, "semester")
    ]
    for ax, ay, aw, ah, aname, *pk in s_attrs:
        draw_line(950, 260, ax, ay, color="#64748B", width=1.3)
        draw_attr(ax, ay, aw, ah, aname, "SUBJECTS", bool(pk and pk[0]))

    # Relationship: BRANCHES - OFFERS - SUBJECTS (1:N)
    draw_relationship(675, 260, 50, 30, "OFFERS")
    draw_line(475, 260, 625, 260, label="(1,1)", lx=540, ly=242)
    draw_line(725, 260, 875, 260, label="(0,N)", lx=810, ly=242)

    # GENRES (x=1480, y=260)
    draw_entity(1480, 260, 140, 52, "GENRES", "GENRES")
    g_attrs = [
        (1420, 170, 95, 34, "genre_id", True),
        (1540, 170, 115, 34, "genre_name")
    ]
    for ax, ay, aw, ah, aname, *pk in g_attrs:
        draw_line(1480, 260, ax, ay, color="#64748B", width=1.3)
        draw_attr(ax, ay, aw, ah, aname, "GENRES", bool(pk and pk[0]))

    # PUBLISHERS (x=1980, y=260)
    draw_entity(1980, 260, 160, 52, "PUBLISHERS", "PUBLISHERS")
    p_attrs = [
        (1910, 170, 115, 34, "publisher_id", True),
        (2050, 170, 130, 34, "publisher_name")
    ]
    for ax, ay, aw, ah, aname, *pk in p_attrs:
        draw_line(1980, 260, ax, ay, color="#64748B", width=1.3)
        draw_attr(ax, ay, aw, ah, aname, "PUBLISHERS", bool(pk and pk[0]))

    # AUTHORS (x=2460, y=420)
    draw_entity(2460, 420, 150, 52, "AUTHORS", "AUTHORS")
    a_attrs = [
        (2620, 360, 105, 34, "author_id", True),
        (2640, 420, 115, 34, "author_name"),
        (2620, 480, 100, 34, "country")
    ]
    for ax, ay, aw, ah, aname, *pk in a_attrs:
        draw_line(2460, 420, ax, ay, color="#64748B", width=1.3)
        draw_attr(ax, ay, aw, ah, aname, "AUTHORS", bool(pk and pk[0]))

    # =========================================================================
    # 2. CORE CATALOG ENTITY: BOOKS (x=1750, y=620)
    # =========================================================================
    draw_entity(1750, 620, 160, 60, "BOOKS", "BOOKS")
    bk_attrs = [
        (1530, 510, 100, 34, "book_id", True),
        (1510, 560, 95, 34, "title"),
        (1500, 610, 95, 34, "isbn"),
        (1510, 660, 95, 34, "edition"),
        (1530, 710, 100, 34, "pub_year"),
        (1580, 760, 95, 34, "rating"),
        (1670, 785, 110, 34, "description")
    ]
    for ax, ay, aw, ah, aname, *pk in bk_attrs:
        draw_line(1750, 620, ax, ay, color="#64748B", width=1.3)
        draw_attr(ax, ay, aw, ah, aname, "BOOKS", bool(pk and pk[0]))

    # Relationship: SUBJECTS - BELONGS_TO - BOOKS
    draw_relationship(1350, 440, 55, 30, "BELONGS TO")
    draw_line(980, 286, 1300, 430, label="(0,N)", lx=1100, ly=340)
    draw_line(1400, 450, 1680, 595, label="(1,1)", lx=1570, ly=510)

    # Relationship: BRANCHES - ASSOCIATED_WITH - BOOKS
    draw_relationship(1050, 520, 65, 30, "ASSOCIATED WITH")
    draw_polyline([(400, 286), (400, 520), (985, 520)], label="(0,N)", lx=430, ly=420)
    draw_line(1115, 520, 1670, 610, label="(1,1)", lx=1420, ly=580)

    # Relationship: GENRES - CATEGORIZED - BOOKS
    draw_relationship(1620, 440, 60, 30, "CATEGORIZED")
    draw_line(1500, 286, 1600, 415, label="(0,N)", lx=1530, ly=340)
    draw_line(1640, 465, 1720, 590, label="(1,1)", lx=1700, ly=520)

    # Relationship: PUBLISHERS - PUBLISHED_BY - BOOKS
    draw_relationship(1880, 440, 60, 30, "PUBLISHED BY")
    draw_line(1960, 286, 1900, 415, label="(0,N)", lx=1950, ly=340)
    draw_line(1860, 465, 1780, 590, label="(1,1)", lx=1800, ly=520)

    # Relationship: AUTHORS - WRITTEN_BY - BOOKS
    draw_relationship(2120, 520, 55, 30, "WRITTEN BY")
    draw_line(2400, 440, 2170, 510, label="(0,N)", lx=2300, ly=460)
    draw_line(2065, 530, 1830, 600, label="(1,1)", lx=1930, ly=580)

    # =========================================================================
    # 3. WEAK ENTITY: BOOK_COPIES (x=1750, y=980)
    # =========================================================================
    draw_entity(1750, 980, 160, 56, "BOOK_COPIES", "BOOK_COPIES", is_weak=True)
    bc_attrs = [
        (1970, 930, 105, 34, "copy_id", True),
        (1990, 980, 115, 34, "copy_code"),
        (1980, 1030, 95, 34, "status"),
        (1960, 1080, 120, 34, "rack_location")
    ]
    for ax, ay, aw, ah, aname, *pk in bc_attrs:
        draw_line(1750, 980, ax, ay, color="#64748B", width=1.3)
        draw_attr(ax, ay, aw, ah, aname, "BOOK_COPIES", bool(pk and pk[0]))

    # Relationship: BOOKS - HAS_COPIES - BOOK_COPIES (Identifying relationship)
    draw_relationship(1750, 800, 55, 30, "HAS COPIES", is_identifying=True)
    draw_line(1750, 650, 1750, 770, label="(1,1)", lx=1780, ly=710)
    draw_line(1750, 830, 1750, 952, is_double=True, label="(1,N)", lx=1785, ly=890)

    # =========================================================================
    # 4. BOOK_REQUESTS (x=360, y=720) - Zero overlap with lines!
    # =========================================================================
    draw_entity(360, 720, 170, 56, "BOOK_REQUESTS", "BOOK_REQUESTS")
    br_attrs = [
        (180, 600, 110, 34, "request_id", True),
        (160, 660, 95, 34, "title"),
        (150, 720, 95, 34, "author"),
        (160, 780, 115, 34, "votes_count"),
        (190, 840, 95, 34, "status"),
        (230, 900, 110, 34, "created_at")
    ]
    for ax, ay, aw, ah, aname, *pk in br_attrs:
        draw_line(360, 720, ax, ay, color="#64748B", width=1.3)
        draw_attr(ax, ay, aw, ah, aname, "BOOK_REQUESTS", bool(pk and pk[0]))

    # =========================================================================
    # 5. USER ENTITY & COMMUNITY RELATIONSHIPS (x=840, y=1180)
    # =========================================================================
    draw_entity(840, 1180, 160, 60, "USERS", "USERS")

    # Attributes of USERS neatly arranged on Top and Right (No collision with SUGGESTED_BY)
    u_attrs = [
        # Top-left and Top row
        (660, 1050, 100, 34, "user_id", True),
        (760, 1020, 95, 34, "usn"),
        (860, 1010, 95, 34, "name"),
        (960, 1020, 95, 34, "email"),
        (1060, 1050, 105, 34, "password"),
        # Left side
        (680, 1110, 90, 34, "role"),
        (670, 1170, 100, 34, "semester"),
        (680, 1230, 95, 34, "phone"),
        # Bottom side - cleanly isolated
        (840, 1310, 175, 34, "reservation_blocked_until"),
        (1010, 1270, 110, 34, "created_at")
    ]
    for ax, ay, aw, ah, aname, *pk in u_attrs:
        draw_line(840, 1180, ax, ay, color="#64748B", width=1.3)
        draw_attr(ax, ay, aw, ah, aname, "USERS", bool(pk and pk[0]))

    # Relationship: USERS - SUGGESTED_BY - BOOK_REQUESTS
    draw_relationship(560, 890, 60, 30, "SUGGESTED BY")
    draw_line(420, 748, 510, 870, label="(0,N)", lx=440, ly=815)
    draw_line(610, 910, 780, 1150, label="(1,1)", lx=725, ly=1010)

    # Relationship: USERS - VOTES_ON - BOOK_REQUESTS (M:N)
    draw_relationship(360, 1070, 55, 30, "VOTES ON")
    # Clean vertical line from BOOK_REQUESTS bottom (x=360) to VOTES_ON (x=360)
    draw_line(360, 748, 360, 1040, label="(0,N)", lx=320, ly=900)
    # Line from VOTES_ON to USERS
    draw_line(415, 1070, 760, 1170, label="(0,N)", lx=580, ly=1100)
    # Attribute of VOTES_ON relationship: voted_at
    draw_line(360, 1070, 360, 1160, color="#64748B", width=1.3)
    draw_attr(360, 1160, 95, 32, "voted_at", "BOOK_REQUESTS")

    # =========================================================================
    # 6. TRANSACTION ENTITIES (BOTTOM TIER) - WIDE SPACING, ZERO AMBIGUITY
    # =========================================================================

    # --- RESERVATIONS (x=700, y=1700) ---
    draw_entity(700, 1700, 170, 56, "RESERVATIONS", "RESERVATIONS")
    r_attrs = [
        (560, 1800, 125, 34, "reservation_id", True),
        (670, 1830, 115, 34, "reserved_at"),
        (780, 1830, 110, 34, "expires_at"),
        (880, 1800, 95, 34, "status")
    ]
    for ax, ay, aw, ah, aname, *pk in r_attrs:
        draw_line(700, 1700, ax, ay, color="#64748B", width=1.3)
        draw_attr(ax, ay, aw, ah, aname, "RESERVATIONS", bool(pk and pk[0]))

    # Relationship: USERS - RESERVES_USER - RESERVATIONS
    draw_relationship(700, 1480, 60, 30, "RESERVES USER")
    draw_line(800, 1210, 730, 1455, label="(0,N)", lx=790, ly=1320)
    draw_line(700, 1510, 700, 1672, label="(1,1)", lx=660, ly=1580)

    # Relationship: RESERVATIONS - RESERVES_COPY - BOOK_COPIES
    draw_relationship(1200, 1380, 60, 30, "RESERVES COPY")
    draw_line(760, 1675, 1150, 1400, label="(1,1)", lx=920, ly=1560)
    draw_line(1250, 1360, 1680, 1005, label="(0,N)", lx=1460, ly=1160)

    # --- LOANS (x=1440, y=1700) ---
    draw_entity(1440, 1700, 160, 56, "LOANS", "LOANS")
    l_attrs = [
        (1280, 1800, 100, 34, "loan_id", True),
        (1380, 1830, 115, 34, "borrow_date"),
        (1490, 1830, 110, 34, "due_date"),
        (1600, 1800, 115, 34, "return_date")
    ]
    for ax, ay, aw, ah, aname, *pk in l_attrs:
        draw_line(1440, 1700, ax, ay, color="#64748B", width=1.3)
        draw_attr(ax, ay, aw, ah, aname, "LOANS", bool(pk and pk[0]))

    # Relationship: USERS - BORROWS_USER - LOANS
    draw_relationship(1050, 1480, 60, 30, "BORROWS USER")
    draw_line(860, 1210, 1010, 1455, label="(0,N)", lx=920, ly=1340)
    draw_line(1090, 1500, 1380, 1675, label="(1,1)", lx=1210, ly=1610)

    # Relationship: LOANS - BORROWS_COPY - BOOK_COPIES
    draw_relationship(1580, 1380, 60, 30, "BORROWS COPY")
    draw_line(1460, 1672, 1560, 1410, label="(1,1)", lx=1470, ly=1520)
    draw_line(1600, 1350, 1720, 1008, label="(0,N)", lx=1690, ly=1160)

    # --- FINES (x=1960, y=1700) ---
    draw_entity(1960, 1700, 150, 56, "FINES", "FINES")
    f_attrs = [
        (1820, 1800, 100, 34, "fine_id", True),
        (1910, 1830, 95, 34, "amount"),
        (2010, 1830, 120, 34, "days_overdue"),
        (2100, 1800, 95, 34, "status"),
        (1960, 1880, 115, 34, "assessed_at")
    ]
    for ax, ay, aw, ah, aname, *pk in f_attrs:
        draw_line(1960, 1700, ax, ay, color="#64748B", width=1.3)
        draw_attr(ax, ay, aw, ah, aname, "FINES", bool(pk and pk[0]))

    # Relationship: LOANS - INCURRED_BY - FINES
    draw_relationship(1700, 1700, 55, 30, "INCURRED BY")
    draw_line(1520, 1700, 1645, 1700, label="(0,1)", lx=1575, ly=1680)
    draw_line(1755, 1700, 1885, 1700, label="(1,1)", lx=1825, ly=1680)

    # Relationship: FINES - OWED_BY - USERS
    draw_relationship(1450, 1260, 55, 30, "OWED BY")
    draw_line(1940, 1672, 1490, 1280, label="(1,1)", lx=1750, ly=1460)
    draw_line(1395, 1260, 920, 1200, label="(0,N)", lx=1140, ly=1210)

    # --- FINE_COLLECTIONS (x=2480, y=1700) - CLEAR SEPARATION FROM BOOK_COPIES! ---
    draw_entity(2480, 1700, 170, 56, "FINE_COLLECTIONS", "FINE_COLLECTIONS")
    fc_attrs = [
        (2360, 1800, 120, 34, "collection_id", True),
        (2480, 1830, 115, 34, "amount_paid"),
        (2600, 1800, 130, 34, "collection_date")
    ]
    for ax, ay, aw, ah, aname, *pk in fc_attrs:
        draw_line(2480, 1700, ax, ay, color="#64748B", width=1.3)
        draw_attr(ax, ay, aw, ah, aname, "FINE_COLLECTIONS", bool(pk and pk[0]))

    # Relationship: FINES - SETTLED_IN - FINE_COLLECTIONS
    draw_relationship(2220, 1700, 55, 30, "SETTLED IN")
    draw_line(2035, 1700, 2165, 1700, label="(0,1)", lx=2095, ly=1680)
    draw_line(2275, 1700, 2395, 1700, label="(1,1)", lx=2340, ly=1680)

    # Relationship: FINE_COLLECTIONS - COLLECTED_BY - USERS (Librarian)
    draw_relationship(2200, 1450, 60, 30, "COLLECTED BY")
    draw_line(2430, 1672, 2240, 1475, label="(1,1)", lx=2370, ly=1580)
    draw_polyline([(2150, 1440), (1800, 1300), (920, 1195)], label="(0,N)", lx=1750, ly=1285)

    # =========================================================================
    # 7. AUDIT_LOGS (STANDALONE SYSTEM LOG ENTITY) (x=2460, y=1050)
    # =========================================================================
    draw_entity(2460, 1050, 160, 56, "AUDIT_LOGS", "AUDIT_LOGS")
    log_attrs = [
        (2320, 970, 95, 34, "log_id", True),
        (2460, 950, 95, 34, "action"),
        (2600, 970, 130, 34, "query_executed"),
        (2620, 1050, 125, 34, "performed_by"),
        (2580, 1130, 105, 34, "log_time")
    ]
    for ax, ay, aw, ah, aname, *pk in log_attrs:
        draw_line(2460, 1050, ax, ay, color="#64748B", width=1.3)
        draw_attr(ax, ay, aw, ah, aname, "AUDIT_LOGS", bool(pk and pk[0]))

    # Assembly into full SVG
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
<defs>
    <filter id="shadow" x="-5%" y="-5%" width="115%" height="115%" filterUnits="userSpaceOnUse">
        <feDropShadow dx="1.5" dy="2.5" stdDeviation="2.5" flood-color="#0F172A" flood-opacity="0.14" />
    </filter>
    <filter id="shadow-sm" x="-5%" y="-5%" width="115%" height="115%" filterUnits="userSpaceOnUse">
        <feDropShadow dx="1" dy="1.5" stdDeviation="1.5" flood-color="#0F172A" flood-opacity="0.08" />
    </filter>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#1E3A8A" />
        <stop offset="50%" stop-color="#0F172A" />
        <stop offset="100%" stop-color="#1E3A8A" />
    </linearGradient>
</defs>

<!-- Clean Architectural Canvas Background -->
<rect width="{width}" height="{height}" fill="#F8FAFC" />

<!-- Outer Decorative Border -->
<rect x="25" y="25" width="{width - 50}" height="{height - 50}" rx="14" fill="none" stroke="#E2E8F0" stroke-width="2" />

<!-- Header Banner -->
<rect x="50" y="45" width="{width - 100}" height="80" rx="10" fill="url(#headerGrad)" filter="url(#shadow)" />
<text x="{width / 2}" y="82" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">
    COLLEGE E-LIBRARY DATABASE SYSTEM — ENTITY-RELATIONSHIP (ER) DIAGRAM
</text>
<text x="{width / 2}" y="108" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#93C5FD" text-anchor="middle">
    DBMS Laboratory &amp; Presentation Specification (Course Code: 24CS520) | 3NF Normalized Relational Schema | Chen Notation with Structural Cardinalities
</text>

<!-- Legend Panel -->
<g transform="translate(1930, 135)">
    <rect x="0" y="0" width="870" height="48" rx="6" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2" filter="url(#shadow-sm)" />
    <!-- Regular Entity -->
    <rect x="18" y="13" width="70" height="22" rx="3" fill="#F8FAFC" stroke="#1E3A8A" stroke-width="1.6" />
    <text x="53" y="28" font-family="Arial" font-size="9.5" font-weight="bold" fill="#1E3A8A" text-anchor="middle">Entity</text>
    <!-- Weak Entity -->
    <rect x="106" y="10" width="84" height="28" rx="4" fill="none" stroke="#512DA8" stroke-width="1.2" />
    <rect x="109" y="13" width="78" height="22" rx="3" fill="#EDE7F6" stroke="#512DA8" stroke-width="1.6" />
    <text x="148" y="28" font-family="Arial" font-size="9.5" font-weight="bold" fill="#512DA8" text-anchor="middle">Weak Entity</text>
    <!-- Relationship -->
    <polygon points="230,12 248,24 230,36 212,24" fill="#FEF3C7" stroke="#D97706" stroke-width="1.6" />
    <text x="260" y="28" font-family="Arial" font-size="9.5" font-weight="bold" fill="#92400E">Relationship</text>
    <!-- Attribute -->
    <ellipse cx="370" cy="24" rx="35" ry="11" fill="#F0FDFA" stroke="#0D9488" stroke-width="1.4" />
    <text x="370" y="28" font-family="Arial" font-size="9" fill="#0F172A" text-anchor="middle">Attribute</text>
    <!-- PK -->
    <ellipse cx="465" cy="24" rx="35" ry="11" fill="#F0FDFA" stroke="#0D9488" stroke-width="1.4" />
    <text x="465" y="28" font-family="Arial" font-size="9" font-weight="bold" fill="#0F172A" text-anchor="middle"><u>PK Attribute</u></text>
    <!-- Cardinality -->
    <text x="525" y="28" font-family="Arial" font-size="9.5" font-weight="bold" fill="#1E40AF">Cardinality: (min, max)</text>
    <text x="695" y="28" font-family="Arial" font-size="9" fill="#64748B">[Double Line = Total Participation]</text>
</g>

<!-- 1. Connections Layer -->
{''.join(lines)}

<!-- 2. Relationships Layer -->
{''.join(relationships)}

<!-- 3. Entities Layer -->
{''.join(entities)}

<!-- 4. Attributes Layer -->
{''.join(attributes)}

</svg>'''
    
    with open('report_assets/e_library_er_diagram.svg', 'w') as f:
        f.write(svg_content)
    print("report_assets/e_library_er_diagram.svg generated successfully!")

if __name__ == '__main__':
    build_er_svg()
