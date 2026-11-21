import math
import shutil
import xml.etree.ElementTree as ET

def build_perfect_er_svg():
    width = 3200
    height = 2100

    PALETTE = {
        'BRANCHES': {'bg': '#E8F5E9', 'border': '#2E7D32', 'attr_bg': '#F1F8E9', 'attr_b': '#33691E', 'text': '#1B5E20'},
        'SUBJECTS': {'bg': '#E0F2F1', 'border': '#00695C', 'attr_bg': '#E0F7FA', 'attr_b': '#00838F', 'text': '#004D40'},
        'GENRES': {'bg': '#F3E5F5', 'border': '#6A1B9A', 'attr_bg': '#F8BBD0', 'attr_b': '#880E4F', 'text': '#4A148C'},
        'PUBLISHERS': {'bg': '#FCE4EC', 'border': '#AD1457', 'attr_bg': '#F8BBD0', 'attr_b': '#C2185B', 'text': '#880E4F'},
        'AUTHORS': {'bg': '#E1F5FE', 'border': '#0277BD', 'attr_bg': '#E0F7FA', 'attr_b': '#0288D1', 'text': '#01579B'},
        'BOOKS': {'bg': '#FFEBEE', 'border': '#C62828', 'attr_bg': '#FFCDD2', 'attr_b': '#D32F2F', 'text': '#B71C1C'},
        'BOOK_COPIES': {'bg': '#EDE7F6', 'border': '#4527A0', 'attr_bg': '#D1C4E9', 'attr_b': '#512DA8', 'text': '#311B92'},
        'BOOK_REQUESTS': {'bg': '#E8F8F5', 'border': '#117A65', 'attr_bg': '#D5F5E3', 'attr_b': '#1E8449', 'text': '#0E6251'},
        'USERS': {'bg': '#FFF8E1', 'border': '#F57F17', 'attr_bg': '#FFFDE7', 'attr_b': '#FBC02D', 'text': '#E65100'},
        'RESERVATIONS': {'bg': '#FFF3E0', 'border': '#E65100', 'attr_bg': '#FFE0B2', 'attr_b': '#F57C00', 'text': '#BF360C'},
        'LOANS': {'bg': '#FBE9E7', 'border': '#BF360C', 'attr_bg': '#FFCCBC', 'attr_b': '#D84315', 'text': '#870000'},
        'FINES': {'bg': '#FFEBEE', 'border': '#B71C1C', 'attr_bg': '#FFCDD2', 'attr_b': '#C62828', 'text': '#7F0000'},
        'FINE_COLLECTIONS': {'bg': '#EFEBE9', 'border': '#4E342E', 'attr_bg': '#D7CCC8', 'attr_b': '#5D4037', 'text': '#3E2723'},
        'AUDIT_LOGS': {'bg': '#ECEFF1', 'border': '#37474F', 'attr_bg': '#CFD8DC', 'attr_b': '#455A64', 'text': '#263238'}
    }

    entities = {}
    relationships = {}
    attributes = []
    connections = []
    cardinalities = []

    def add_entity(key, name, cx, cy, w, h, is_weak=False):
        entities[key] = {
            'key': key, 'name': name, 'cx': cx, 'cy': cy, 'w': w, 'h': h,
            'is_weak': is_weak, 'colors': PALETTE[key]
        }

    def add_relationship(key, name, cx, cy, rx, ry, is_identifying=False):
        relationships[key] = {
            'key': key, 'name': name, 'cx': cx, 'cy': cy, 'rx': rx, 'ry': ry,
            'is_identifying': is_identifying
        }

    def add_attr(entity_key, name, cx, cy, w=105, h=34, is_pk=False):
        attributes.append({
            'entity_key': entity_key, 'name': name, 'cx': cx, 'cy': cy,
            'w': w, 'h': h, 'is_pk': is_pk, 'colors': PALETTE[entity_key]
        })

    def add_rel_attr(rel_key, name, cx, cy, w=100, h=32):
        attributes.append({
            'rel_key': rel_key, 'name': name, 'cx': cx, 'cy': cy,
            'w': w, 'h': h, 'is_pk': False, 'colors': PALETTE['BOOK_REQUESTS']
        })

    def connect(p1, p2, is_double=False, polyline=None, has_jump=False, jump_pt=None):
        connections.append({
            'p1': p1, 'p2': p2, 'is_double': is_double, 'polyline': polyline,
            'has_jump': has_jump, 'jump_pt': jump_pt
        })

    def add_cardinality(label, cx, cy):
        cardinalities.append({'label': label, 'cx': cx, 'cy': cy})

    # 1. ENTITIES DEFINITION
    # Top Tier
    add_entity('BRANCHES', 'BRANCHES', 400, 240, 160, 56)
    add_entity('SUBJECTS', 'SUBJECTS', 1060, 240, 160, 56)
    add_entity('GENRES', 'GENRES', 1660, 240, 150, 56)
    add_entity('PUBLISHERS', 'PUBLISHERS', 2260, 240, 160, 56)

    # Middle-Right
    add_entity('AUTHORS', 'AUTHORS', 2820, 480, 150, 56)
    add_entity('BOOKS', 'BOOKS', 1950, 640, 180, 64)
    add_entity('BOOK_COPIES', 'BOOK_COPIES', 1950, 1020, 180, 60, is_weak=True)
    add_entity('AUDIT_LOGS', 'AUDIT_LOGS', 2820, 1020, 170, 60)

    # Middle-Left
    add_entity('BOOK_REQUESTS', 'BOOK_REQUESTS', 400, 720, 180, 60)
    add_entity('USERS', 'USERS', 900, 1160, 180, 64)

    # Bottom Tier
    add_entity('RESERVATIONS', 'RESERVATIONS', 650, 1750, 180, 60)
    add_entity('LOANS', 'LOANS', 1420, 1750, 170, 60)
    add_entity('FINES', 'FINES', 2050, 1750, 160, 60)
    add_entity('FINE_COLLECTIONS', 'FINE_COLLECTIONS', 2680, 1750, 190, 60)

    # 2. ATTRIBUTES DEFINITION
    # BRANCHES Attributes
    add_attr('BRANCHES', 'branch_id', 230, 140, 100, 34, is_pk=True)
    add_attr('BRANCHES', 'branch_code', 350, 120, 110, 34)
    add_attr('BRANCHES', 'branch_name', 475, 120, 115, 34)
    add_attr('BRANCHES', 'hod_name', 595, 140, 100, 34)

    # SUBJECTS Attributes
    add_attr('SUBJECTS', 'subject_id', 890, 140, 100, 34, is_pk=True)
    add_attr('SUBJECTS', 'subject_code', 1010, 120, 115, 34)
    add_attr('SUBJECTS', 'subject_name', 1140, 120, 120, 34)
    add_attr('SUBJECTS', 'semester', 1260, 140, 95, 34)

    # GENRES Attributes
    add_attr('GENRES', 'genre_id', 1580, 135, 95, 34, is_pk=True)
    add_attr('GENRES', 'genre_name', 1740, 135, 110, 34)

    # PUBLISHERS Attributes (No legend box anywhere nearby!)
    add_attr('PUBLISHERS', 'publisher_id', 2160, 135, 110, 34, is_pk=True)
    add_attr('PUBLISHERS', 'publisher_name', 2360, 135, 125, 34)

    # AUTHORS Attributes
    add_attr('AUTHORS', 'author_id', 3010, 420, 100, 34, is_pk=True)
    add_attr('AUTHORS', 'author_name', 3040, 480, 115, 34)
    add_attr('AUTHORS', 'country', 3010, 540, 100, 34)

    # BOOKS Attributes (Fan strictly to LEFT and LOWER-LEFT, 60px clearance from HAS_COPIES!)
    add_attr('BOOKS', 'book_id', 1670, 530, 95, 34, is_pk=True)
    add_attr('BOOKS', 'title', 1640, 585, 90, 34)
    add_attr('BOOKS', 'isbn', 1630, 640, 90, 34)
    add_attr('BOOKS', 'edition', 1630, 690, 90, 34)
    add_attr('BOOKS', 'pub_year', 1650, 740, 95, 34)
    add_attr('BOOKS', 'rating', 1700, 790, 90, 34)
    add_attr('BOOKS', 'description', 1770, 835, 105, 34)

    # BOOK_COPIES Attributes
    add_attr('BOOK_COPIES', 'copy_id', 2180, 940, 100, 34, is_pk=True)
    add_attr('BOOK_COPIES', 'copy_code', 2210, 995, 110, 34)
    add_attr('BOOK_COPIES', 'status', 2210, 1050, 90, 34)
    add_attr('BOOK_COPIES', 'rack_location', 2180, 1105, 120, 34)

    # BOOK_REQUESTS Attributes (Fan strictly to LEFT, clear of vertical line down to VOTES_ON)
    add_attr('BOOK_REQUESTS', 'request_id', 220, 600, 105, 34, is_pk=True)
    add_attr('BOOK_REQUESTS', 'title', 190, 650, 90, 34)
    add_attr('BOOK_REQUESTS', 'author', 180, 700, 90, 34)
    add_attr('BOOK_REQUESTS', 'votes_count', 180, 750, 110, 34)
    add_attr('BOOK_REQUESTS', 'status', 200, 800, 90, 34)
    add_attr('BOOK_REQUESTS', 'created_at', 230, 850, 105, 34)

    # USERS Attributes (Arc fan across top, clear of SUGGESTED_BY path)
    add_attr('USERS', 'user_id', 680, 1030, 95, 34, is_pk=True)
    add_attr('USERS', 'usn', 790, 990, 90, 34)
    add_attr('USERS', 'name', 900, 975, 90, 34)
    add_attr('USERS', 'email', 1010, 990, 90, 34)
    add_attr('USERS', 'password', 1120, 1030, 100, 34)
    add_attr('USERS', 'role', 1145, 1105, 85, 34)
    add_attr('USERS', 'semester', 1155, 1165, 95, 34)
    add_attr('USERS', 'phone', 1145, 1225, 90, 34)
    add_attr('USERS', 'reservation_blocked_until', 840, 1330, 175, 34)
    add_attr('USERS', 'created_at', 980, 1260, 105, 34)

    # RESERVATIONS Attributes
    add_attr('RESERVATIONS', 'reservation_id', 450, 1860, 125, 34, is_pk=True)
    add_attr('RESERVATIONS', 'reserved_at', 585, 1895, 110, 34)
    add_attr('RESERVATIONS', 'expires_at', 715, 1895, 105, 34)
    add_attr('RESERVATIONS', 'status', 845, 1860, 90, 34)

    # LOANS Attributes
    add_attr('LOANS', 'loan_id', 1230, 1860, 95, 34, is_pk=True)
    add_attr('LOANS', 'borrow_date', 1360, 1895, 110, 34)
    add_attr('LOANS', 'due_date', 1480, 1895, 105, 34)
    add_attr('LOANS', 'return_date', 1610, 1860, 110, 34)

    # FINES Attributes
    add_attr('FINES', 'fine_id', 1870, 1860, 95, 34, is_pk=True)
    add_attr('FINES', 'amount', 1980, 1900, 90, 34)
    add_attr('FINES', 'assessed_at', 2070, 1960, 110, 34)
    add_attr('FINES', 'days_overdue', 2160, 1900, 115, 34)
    add_attr('FINES', 'status', 2270, 1860, 90, 34)

    # FINE_COLLECTIONS Attributes
    add_attr('FINE_COLLECTIONS', 'collection_id', 2520, 1860, 115, 34, is_pk=True)
    add_attr('FINE_COLLECTIONS', 'amount_paid', 2680, 1895, 115, 34)
    add_attr('FINE_COLLECTIONS', 'collection_date', 2840, 1860, 130, 34)

    # AUDIT_LOGS Attributes
    add_attr('AUDIT_LOGS', 'log_id', 2680, 930, 90, 34, is_pk=True)
    add_attr('AUDIT_LOGS', 'action', 2820, 910, 90, 34)
    add_attr('AUDIT_LOGS', 'query_executed', 2970, 930, 130, 34)
    add_attr('AUDIT_LOGS', 'performed_by', 3000, 1020, 125, 34)
    add_attr('AUDIT_LOGS', 'log_time', 2960, 1110, 100, 34)

    # 3. RELATIONSHIPS DEFINITION
    # 1. BRANCHES - OFFERS - SUBJECTS
    add_relationship('OFFERS', 'OFFERS', 730, 240, 52, 30)
    connect((400, 240), (730, 240))
    add_cardinality('(1,1)', 530, 218)
    connect((730, 240), (1060, 240))
    add_cardinality('(0,N)', 930, 218)

    # 2. SUBJECTS - BELONGS_TO - BOOKS
    add_relationship('BELONGS_TO', 'BELONGS TO', 1480, 420, 62, 32)
    connect((1060, 240), (1480, 420))
    add_cardinality('(0,N)', 1220, 310)
    connect((1480, 420), (1950, 640))
    add_cardinality('(1,1)', 1820, 540)

    # 3. GENRES - CATEGORIZED - BOOKS
    add_relationship('CATEGORIZED', 'CATEGORIZED', 1820, 420, 65, 32)
    connect((1660, 240), (1820, 420))
    add_cardinality('(0,N)', 1715, 320)
    connect((1820, 420), (1950, 640))
    add_cardinality('(1,1)', 1920, 510)

    # 4. PUBLISHERS - PUBLISHED_BY - BOOKS
    add_relationship('PUBLISHED_BY', 'PUBLISHED BY', 2140, 420, 65, 32)
    connect((2260, 240), (2140, 420))
    add_cardinality('(0,N)', 2235, 320)
    connect((2140, 420), (1950, 640))
    add_cardinality('(1,1)', 2035, 510)

    # 5. AUTHORS - WRITTEN_BY - BOOKS
    add_relationship('WRITTEN_BY', 'WRITTEN BY', 2420, 560, 60, 32)
    connect((2820, 480), (2420, 560))
    add_cardinality('(0,N)', 2670, 500)
    connect((2420, 560), (1950, 640))
    add_cardinality('(1,1)', 2140, 620)

    # 6. BOOKS - HAS_COPIES - BOOK_COPIES (Identifying Relationship)
    add_relationship('HAS_COPIES', 'HAS COPIES', 1950, 830, 62, 34, is_identifying=True)
    connect((1950, 640), (1950, 830))
    add_cardinality('(1,1)', 1985, 735)
    connect((1950, 830), (1950, 1020), is_double=True)
    add_cardinality('(1,N)', 1990, 925)

    # 7. BRANCHES - ASSOCIATED_WITH - USERS (Direct connection on left side)
    add_relationship('ASSOCIATED_WITH', 'ASSOCIATED WITH', 400, 480, 72, 34)
    connect((400, 240), (400, 480))
    add_cardinality('(1,1)', 435, 360)
    connect((400, 480), (900, 1160))
    add_cardinality('(0,N)', 600, 780)

    # 8. USERS - SUGGESTED_BY - BOOK_REQUESTS
    add_relationship('SUGGESTED_BY', 'SUGGESTED BY', 620, 920, 65, 32)
    connect((400, 720), (620, 920))
    add_cardinality('(0,N)', 470, 810)
    connect((620, 920), (900, 1160))
    add_cardinality('(1,1)', 790, 1070)

    # 9. USERS - VOTES_ON - BOOK_REQUESTS (with voted_at attribute)
    add_relationship('VOTES_ON', 'VOTES ON', 400, 1000, 55, 30)
    connect((400, 720), (400, 1000))
    add_cardinality('(0,N)', 435, 870)
    connect((400, 1000), (900, 1160))
    add_cardinality('(0,N)', 620, 1100)
    add_rel_attr('VOTES_ON', 'voted_at', 400, 1100, 95, 32)

    # 10. USERS - RESERVES_USER - RESERVATIONS
    add_relationship('RESERVES_USER', 'RESERVES USER', 650, 1450, 65, 32)
    connect((900, 1160), (650, 1450))
    add_cardinality('(0,N)', 740, 1370)
    connect((650, 1450), (650, 1750))
    add_cardinality('(1,1)', 685, 1600)

    # 11. RESERVATIONS - RESERVES_COPY - BOOK_COPIES
    add_relationship('RESERVES_COPY', 'RESERVES COPY', 1150, 1360, 65, 32)
    connect((650, 1750), (1150, 1360), has_jump=True, jump_pt=(1072, 1421))
    add_cardinality('(1,1)', 880, 1570)
    connect((1150, 1360), (1950, 1020))
    add_cardinality('(0,N)', 1600, 1170)

    # 12. USERS - BORROWS_USER - LOANS
    add_relationship('BORROWS_USER', 'BORROWS USER', 1150, 1540, 65, 32)
    connect((900, 1160), (1150, 1540))
    add_cardinality('(0,N)', 1030, 1360)
    connect((1150, 1540), (1420, 1750))
    add_cardinality('(1,1)', 1320, 1660)

    # 13. LOANS - BORROWS_COPY - BOOK_COPIES
    add_relationship('BORROWS_COPY', 'BORROWS COPY', 1680, 1380, 65, 32)
    connect((1420, 1750), (1680, 1380))
    add_cardinality('(1,1)', 1520, 1580)
    connect((1680, 1380), (1950, 1020))
    add_cardinality('(0,N)', 1840, 1180)

    # 14. LOANS - INCURRED_BY - FINES
    add_relationship('INCURRED_BY', 'INCURRED BY', 1735, 1750, 58, 30)
    connect((1420, 1750), (1735, 1750))
    add_cardinality('(0,1)', 1570, 1728)
    connect((1735, 1750), (2050, 1750))
    add_cardinality('(1,1)', 1890, 1728)

    # 15. USERS - OWED_BY - FINES
    add_relationship('OWED_BY', 'OWED BY', 1550, 1260, 55, 30)
    connect((900, 1160), (1550, 1260))
    add_cardinality('(0,N)', 1280, 1205)
    connect((1550, 1260), (2050, 1750))
    add_cardinality('(1,1)', 1880, 1560)

    # 16. FINES - SETTLED_IN - FINE_COLLECTIONS
    add_relationship('SETTLED_IN', 'SETTLED IN', 2365, 1750, 58, 30)
    connect((2050, 1750), (2365, 1750))
    add_cardinality('(0,1)', 2200, 1728)
    connect((2365, 1750), (2680, 1750))
    add_cardinality('(1,1)', 2530, 1728)

    # 17. FINE_COLLECTIONS - COLLECTED_BY - USERS (Librarian)
    add_relationship('COLLECTED_BY', 'COLLECTED BY', 2380, 1450, 65, 32)
    connect((2680, 1750), (2380, 1450))
    add_cardinality('(1,1)', 2570, 1610)
    connect(None, None, polyline=[(2380, 1450), (1800, 1340), (900, 1160)])
    add_cardinality('(0,N)', 1400, 1315)

    # Assemble into clean valid SVG
    svg_parts = []
    svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
<defs>
    <filter id="shadow" x="-8%" y="-8%" width="116%" height="116%" filterUnits="userSpaceOnUse">
        <feDropShadow dx="1.5" dy="2.5" stdDeviation="2.5" flood-color="#0F172A" flood-opacity="0.14" />
    </filter>
    <filter id="shadow-sm" x="-8%" y="-8%" width="116%" height="116%" filterUnits="userSpaceOnUse">
        <feDropShadow dx="1.0" dy="1.5" stdDeviation="1.5" flood-color="#0F172A" flood-opacity="0.08" />
    </filter>
</defs>

<!-- Pure White Architectural Canvas -->
<rect width="{width}" height="{height}" fill="#FFFFFF" />

<!-- Outer Border -->
<rect x="20" y="20" width="{width - 40}" height="{height - 40}" rx="12" fill="none" stroke="#E2E8F0" stroke-width="2" />

<!-- Clean Simple Centered Title (Exact match to original image style) -->
<text x="{width / 2}" y="75" font-family="'Segoe UI', Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" fill="#0F172A" text-anchor="middle" letter-spacing="1.5">
    E-LIBRARY DBMS - ENTITY-RELATIONSHIP DIAGRAM
</text>
''')

    # 1. CONNECTIONS LAYER (Drawn first so opaque shapes cover interior, guaranteeing 0 gaps)
    svg_parts.append('<!-- 1. Connections Layer -->\n<g id="connections-layer">')
    for conn in connections:
        p1 = conn['p1']
        p2 = conn['p2']
        is_double = conn['is_double']
        poly = conn['polyline']
        has_jump = conn['has_jump']
        jump_pt = conn['jump_pt']

        if poly:
            pts_str = " ".join([f"{x},{y}" for x, y in poly])
            svg_parts.append(f'    <polyline points="{pts_str}" fill="none" stroke="#475569" stroke-width="2.0" stroke-linejoin="round" />')
        elif has_jump and jump_pt:
            svg_parts.append(f'    <path d="M {p1[0]},{p1[1]} L 1060,1430 A 15,15 0 0,1 1084,1412 L {p2[0]},{p2[1]}" fill="none" stroke="#475569" stroke-width="2.0" />')
        elif is_double:
            x1, y1 = p1
            x2, y2 = p2
            dx = x2 - x1
            dy = y2 - y1
            dist = math.sqrt(dx*dx + dy*dy)
            ox = -dy / dist * 3.0
            oy = dx / dist * 3.0
            svg_parts.append(f'    <line x1="{x1+ox:.1f}" y1="{y1+oy:.1f}" x2="{x2+ox:.1f}" y2="{y2+oy:.1f}" stroke="#475569" stroke-width="1.8" />')
            svg_parts.append(f'    <line x1="{x1-ox:.1f}" y1="{y1-oy:.1f}" x2="{x2-ox:.1f}" y2="{y2-oy:.1f}" stroke="#475569" stroke-width="1.8" />')
        else:
            svg_parts.append(f'    <line x1="{p1[0]}" y1="{p1[1]}" x2="{p2[0]}" y2="{p2[1]}" stroke="#475569" stroke-width="2.0" />')

    # Entity to Attribute Lines
    for a in attributes:
        if 'entity_key' in a:
            e = entities[a['entity_key']]
            svg_parts.append(f'    <line x1="{e["cx"]}" y1="{e["cy"]}" x2="{a["cx"]}" y2="{a["cy"]}" stroke="#64748B" stroke-width="1.4" />')
        elif 'rel_key' in a:
            r = relationships[a['rel_key']]
            svg_parts.append(f'    <line x1="{r["cx"]}" y1="{r["cy"]}" x2="{a["cx"]}" y2="{a["cy"]}" stroke="#64748B" stroke-width="1.4" />')

    svg_parts.append('</g>\n')

    # 2. RELATIONSHIPS LAYER (Solid opaque diamonds)
    svg_parts.append('<!-- 2. Relationships Layer -->\n<g id="relationships-layer">')
    for k, r in relationships.items():
        x, y, rx, ry = r['cx'], r['cy'], r['rx'], r['ry']
        is_id = r['is_identifying']
        pts = f"{x},{y - ry} {x + rx},{y} {x},{y + ry} {x - rx},{y}"
        if is_id:
            pts_out = f"{x},{y - ry - 5} {x + rx + 6},{y} {x},{y + ry + 5} {x - rx - 6},{y}"
            svg_parts.append(f'    <polygon points="{pts_out}" fill="#FEF3C7" stroke="#B45309" stroke-width="1.6" filter="url(#shadow)" />')
            svg_parts.append(f'    <polygon points="{pts}" fill="#FEF3C7" stroke="#D97706" stroke-width="2.0" />')
        else:
            svg_parts.append(f'    <polygon points="{pts}" fill="#FEF3C7" stroke="#D97706" stroke-width="2.0" filter="url(#shadow)" />')

        words = r['name'].split()
        if len(words) > 1:
            svg_parts.append(f'    <text x="{x}" y="{y - 3}" font-family="\'Segoe UI\', Arial, sans-serif" font-size="10.5" font-weight="bold" fill="#92400E" text-anchor="middle">{words[0]}</text>')
            svg_parts.append(f'    <text x="{x}" y="{y + 11}" font-family="\'Segoe UI\', Arial, sans-serif" font-size="10.5" font-weight="bold" fill="#92400E" text-anchor="middle">{words[1]}</text>')
        else:
            svg_parts.append(f'    <text x="{x}" y="{y + 4}" font-family="\'Segoe UI\', Arial, sans-serif" font-size="11" font-weight="bold" fill="#92400E" text-anchor="middle">{r["name"]}</text>')

    svg_parts.append('</g>\n')

    # 3. ENTITIES LAYER (Solid opaque rectangles)
    svg_parts.append('<!-- 3. Entities Layer -->\n<g id="entities-layer">')
    for k, e in entities.items():
        x, y, w, h = e['cx'], e['cy'], e['w'], e['h']
        c = e['colors']
        if e['is_weak']:
            svg_parts.append(f'    <rect x="{x - w/2 - 5}" y="{y - h/2 - 5}" width="{w + 10}" height="{h + 10}" rx="8" fill="{c["bg"]}" stroke="{c["border"]}" stroke-width="1.6" filter="url(#shadow)" />')
            svg_parts.append(f'    <rect x="{x - w/2}" y="{y - h/2}" width="{w}" height="{h}" rx="6" fill="{c["bg"]}" stroke="{c["border"]}" stroke-width="2.2" />')
        else:
            svg_parts.append(f'    <rect x="{x - w/2}" y="{y - h/2}" width="{w}" height="{h}" rx="6" fill="{c["bg"]}" stroke="{c["border"]}" stroke-width="2.4" filter="url(#shadow)" />')

        svg_parts.append(f'    <text x="{x}" y="{y + 5}" font-family="\'Segoe UI\', Arial, sans-serif" font-size="13.5" font-weight="bold" fill="{c["text"]}" text-anchor="middle" letter-spacing="0.6">{e["name"]}</text>')

    svg_parts.append('</g>\n')

    # 4. ATTRIBUTES LAYER (Solid opaque ellipses)
    svg_parts.append('<!-- 4. Attributes Layer -->\n<g id="attributes-layer">')
    for a in attributes:
        x, y, w, h = a['cx'], a['cy'], a['w'], a['h']
        c = a['colors']
        is_pk = a['is_pk']
        svg_parts.append(f'    <ellipse cx="{x}" cy="{y}" rx="{w/2}" ry="{h/2}" fill="{c["attr_bg"]}" stroke="{c["attr_b"]}" stroke-width="1.6" filter="url(#shadow-sm)" />')
        weight = "bold" if is_pk else "normal"
        svg_parts.append(f'    <text x="{x}" y="{y + 4}" font-family="\'Segoe UI\', Arial, sans-serif" font-size="11" font-weight="{weight}" fill="#0F172A" text-anchor="middle">{a["name"]}</text>')
        if is_pk:
            tw = len(a['name']) * 3.4
            svg_parts.append(f'    <line x1="{x - tw}" y1="{y + 6.5}" x2="{x + tw}" y2="{y + 6.5}" stroke="#0F172A" stroke-width="1.3" />')

    svg_parts.append('</g>\n')

    # 5. CARDINALITY BADGES (Topmost layer, clean white pill boxes)
    svg_parts.append('<!-- 5. Cardinality Badges Layer -->\n<g id="cardinalities-layer">')
    for card in cardinalities:
        x, y, label = card['cx'], card['cy'], card['label']
        svg_parts.append(f'    <rect x="{x - 18}" y="{y - 10}" width="36" height="20" rx="4" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.0" filter="url(#shadow-sm)" />')
        svg_parts.append(f'    <text x="{x}" y="{y + 4}" font-family="\'Segoe UI\', Arial, sans-serif" font-size="11" font-weight="bold" fill="#1E40AF" text-anchor="middle">{label}</text>')

    svg_parts.append('</g>\n')

    svg_parts.append('</svg>')

    svg_full = "\n".join(svg_parts)

    # Validate XML
    ET.fromstring(svg_full)
    print("SVG XML is 100% valid!")

    # Write to target files
    with open('report_assets/e_library_er_diagram.svg', 'w') as f:
        f.write(svg_full)

    with open('e_library_er_diagram.svg', 'w') as f:
        f.write(svg_full)

    shutil.copyfile('report_assets/e_library_er_diagram.svg', '/home/pink/.gemini/antigravity/brain/878b7045-e7c3-4cdf-99f5-5590ac2d6140/e_library_er_diagram.svg')
    print("Files successfully generated and copied to artifact directory!")

if __name__ == '__main__':
    build_perfect_er_svg()
