import math

class ERDiagramSVG:
    def __init__(self, width=2800, height=2100):
        self.width = width
        self.height = height
        self.elements = []
        self.lines = []
        self.front_elements = []

    def add_line(self, x1, y1, x2, y2, color="#475569", width=1.8, dashed=False, label=None, lx=None, ly=None):
        dash_str = ' stroke-dasharray="6,4"' if dashed else ''
        self.lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{dash_str} />')
        if label and lx is not None and ly is not None:
            self.lines.append(f'<rect x="{lx-18}" y="{ly-11}" width="36" height="20" rx="4" fill="#FFFFFF" fill-opacity="0.92" stroke="#CBD5E1" stroke-width="0.8" />')
            self.lines.append(f'<text x="{lx}" y="{ly+4}" font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="bold" fill="#1E40AF" text-anchor="middle">{label}</text>')

    def add_polyline(self, pts, color="#475569", width=1.8, label=None, lx=None, ly=None):
        pts_str = " ".join([f"{x},{y}" for x, y in pts])
        self.lines.append(f'<polyline points="{pts_str}" fill="none" stroke="{color}" stroke-width="{width}" />')
        if label and lx is not None and ly is not None:
            self.lines.append(f'<rect x="{lx-18}" y="{ly-11}" width="36" height="20" rx="4" fill="#FFFFFF" fill-opacity="0.92" stroke="#CBD5E1" stroke-width="0.8" />')
            self.lines.append(f'<text x="{lx}" y="{ly+4}" font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="bold" fill="#1E40AF" text-anchor="middle">{label}</text>')

    def add_entity(self, x, y, w, h, name, bg="#F8FAFC", border="#1E3A8A", is_weak=False):
        if is_weak:
            # Double rectangle for weak/associative entity
            self.elements.append(f'<rect x="{x - w/2 - 4}" y="{y - h/2 - 4}" width="{w + 8}" height="{h + 8}" rx="8" fill="none" stroke="{border}" stroke-width="1.4" />')
        self.elements.append(f'<rect x="{x - w/2}" y="{y - h/2}" width="{w}" height="{h}" rx="6" fill="{bg}" stroke="{border}" stroke-width="2.2" filter="url(#shadow)" />')
        self.elements.append(f'<text x="{x}" y="{y + 5}" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="bold" fill="{border}" text-anchor="middle" letter-spacing="0.5">{name}</text>')

    def add_relationship(self, x, y, rx, ry, name, bg="#FEF9E7", border="#D4AC0D", is_identifying=False):
        pts = f"{x},{y - ry} {x + rx},{y} {x},{y + ry} {x - rx},{y}"
        if is_identifying:
            pts_outer = f"{x},{y - ry - 4} {x + rx + 5},{y} {x},{y + ry + 4} {x - rx - 5},{y}"
            self.elements.append(f'<polygon points="{pts_outer}" fill="none" stroke="{border}" stroke-width="1.3" />')
        self.elements.append(f'<polygon points="{pts}" fill="{bg}" stroke="{border}" stroke-width="2" filter="url(#shadow)" />')
        
        # Word wrap name if contains space
        parts = name.split()
        if len(parts) > 1:
            self.elements.append(f'<text x="{x}" y="{y - 3}" font-family="Arial, Helvetica, sans-serif" font-size="10.5" font-weight="bold" fill="#7D6608" text-anchor="middle">{parts[0]}</text>')
            self.elements.append(f'<text x="{x}" y="{y + 11}" font-family="Arial, Helvetica, sans-serif" font-size="10.5" font-weight="bold" fill="#7D6608" text-anchor="middle">{parts[1]}</text>')
        else:
            self.elements.append(f'<text x="{x}" y="{y + 4}" font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="bold" fill="#7D6608" text-anchor="middle">{name}</text>')

    def add_attribute(self, x, y, w, h, name, is_pk=False, bg="#F0FDFA", border="#0D9488"):
        self.elements.append(f'<ellipse cx="{x}" cy="{y}" rx="{w/2}" ry="{h/2}" fill="{bg}" stroke="{border}" stroke-width="1.6" filter="url(#shadow-sm)" />')
        weight = "bold" if is_pk else "normal"
        self.elements.append(f'<text x="{x}" y="{y + 4}" font-family="Arial, Helvetica, sans-serif" font-size="10.5" font-weight="{weight}" fill="#0F172A" text-anchor="middle">{name}</text>')
        if is_pk:
            # Draw underline for PK
            tw = len(name) * 3.4
            self.elements.append(f'<line x1="{x - tw}" y1="{y + 6.5}" x2="{x + tw}" y2="{y + 6.5}" stroke="#0F172A" stroke-width="1.3" />')

    def save(self, filepath):
        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="100%" height="100%">
<defs>
    <filter id="shadow" x="-5%" y="-5%" width="115%" height="115%" filterUnits="userSpaceOnUse">
        <feDropShadow dx="1.5" dy="2" stdDeviation="2.5" flood-color="#0F172A" flood-opacity="0.12" />
    </filter>
    <filter id="shadow-sm" x="-5%" y="-5%" width="115%" height="115%" filterUnits="userSpaceOnUse">
        <feDropShadow dx="1" dy="1.5" stdDeviation="1.5" flood-color="#0F172A" flood-opacity="0.08" />
    </filter>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#1E3A8A" />
        <stop offset="100%" stop-color="#0F172A" />
    </linearGradient>
</defs>

<!-- Background -->
<rect width="{self.width}" height="{self.height}" fill="#F8FAFC" />

<!-- Header Banner -->
<rect x="50" y="30" width="{self.width - 100}" height="75" rx="10" fill="url(#headerGrad)" filter="url(#shadow)" />
<text x="{self.width / 2}" y="65" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="bold" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">
    COLLEGE E-LIBRARY DATABASE MANAGEMENT SYSTEM (DBMS) — ENTITY-RELATIONSHIP (ER) DIAGRAM
</text>
<text x="{self.width / 2}" y="90" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="#93C5FD" text-anchor="middle">
    Course Code: 24CS520 &amp; 24CS561 | 3NF Normalized Relational Schema | Chen ER Notation with Min-Max Participation Cardinalities
</text>

<!-- Legend Box -->
<g transform="translate(1850, 115)">
    <rect x="0" y="0" width="850" height="45" rx="6" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1" />
    <!-- Regular Entity -->
    <rect x="15" y="12" width="70" height="22" rx="3" fill="#F8FAFC" stroke="#1E3A8A" stroke-width="1.5" />
    <text x="50" y="27" font-family="Arial" font-size="9" font-weight="bold" fill="#1E3A8A" text-anchor="middle">Entity</text>
    <!-- Weak/Associative Entity -->
    <rect x="105" y="10" width="75" height="26" rx="4" fill="none" stroke="#512DA8" stroke-width="1" />
    <rect x="108" y="13" width="69" height="20" rx="3" fill="#EDE7F6" stroke="#512DA8" stroke-width="1.5" />
    <text x="142" y="27" font-family="Arial" font-size="9" font-weight="bold" fill="#512DA8" text-anchor="middle">Weak Entity</text>
    <!-- Relationship -->
    <polygon points="220,13 235,23 220,33 205,23" fill="#FEF9E7" stroke="#D4AC0D" stroke-width="1.5" />
    <text x="255" y="27" font-family="Arial" font-size="9" font-weight="bold" fill="#7D6608">Relationship</text>
    <!-- Attribute -->
    <ellipse cx="340" cy="23" rx="32" ry="11" fill="#F0FDFA" stroke="#0D9488" stroke-width="1.3" />
    <text x="340" y="27" font-family="Arial" font-size="9" fill="#0F172A" text-anchor="middle">Attribute</text>
    <!-- Primary Key -->
    <ellipse cx="440" cy="23" rx="32" ry="11" fill="#F0FDFA" stroke="#0D9488" stroke-width="1.3" />
    <text x="440" y="27" font-family="Arial" font-size="9" font-weight="bold" fill="#0F172A" text-anchor="middle"><u>PK Attribute</u></text>
    <!-- Cardinality info -->
    <text x="500" y="27" font-family="Arial" font-size="9" font-weight="bold" fill="#1E40AF">Cardinality: (min, max)</text>
    <text x="650" y="27" font-family="Arial" font-size="9" fill="#64748B">[Double Line = Total Participation]</text>
</g>

<!-- Lines Layer -->
{"".join(self.lines)}

<!-- Entities, Relationships, and Attributes Layer -->
{"".join(self.elements)}

</svg>'''
        with open(filepath, 'w') as f:
            f.write(svg_content)
        print(f"Successfully generated {filepath}")

