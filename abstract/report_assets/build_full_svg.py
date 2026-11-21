import math
import xml.etree.ElementTree as ET
from generate_er_svg_v2 import generate_svg

entities, relationships, attributes, connections, cardinalities = generate_svg()

width = 3200
height = 2100

svg_parts = []

# SVG Header & Defs
svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
<defs>
    <filter id="shadow" x="-8%" y="-8%" width="116%" height="116%" filterUnits="userSpaceOnUse">
        <feDropShadow dx="1.5" dy="2.5" stdDeviation="2.5" flood-color="#0F172A" flood-opacity="0.14" />
    </filter>
    <filter id="shadow-sm" x="-8%" y="-8%" width="116%" height="116%" filterUnits="userSpaceOnUse">
        <feDropShadow dx="1.0" dy="1.5" stdDeviation="1.5" flood-color="#0F172A" flood-opacity="0.08" />
    </filter>
</defs>

<!-- Architectural Pure White Canvas -->
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
        # Route p1 to p2 with jump arc over jump_pt
        # Line from p1=(650, 1750) to p2=(1150, 1360). Jump at (1072, 1421).
        # Normal vector to line to make arc jump upward
        svg_parts.append(f'    <path d="M {p1[0]},{p1[1]} L 1060,1430 A 15,15 0 0,1 1084,1412 L {p2[0]},{p2[1]}" fill="none" stroke="#475569" stroke-width="2.0" />')
    elif is_double:
        # Offset parallel lines by 3px
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

    # Relationship Name Text
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

# Validate XML structure
try:
    ET.fromstring(svg_full)
    print("SVG is valid XML!")
except Exception as e:
    print("XML Error:", e)

# Save to destination paths
with open('report_assets/e_library_er_diagram.svg', 'w') as f:
    f.write(svg_full)

with open('e_library_er_diagram.svg', 'w') as f:
    f.write(svg_full)

import shutil
shutil.copyfile('report_assets/e_library_er_diagram.svg', '/home/pink/.gemini/antigravity/brain/878b7045-e7c3-4cdf-99f5-5590ac2d6140/e_library_er_diagram.svg')

print("All SVG files saved and updated successfully!")
