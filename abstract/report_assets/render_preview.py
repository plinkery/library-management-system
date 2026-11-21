import matplotlib.pyplot as plt
import matplotlib.patches as patches
from generate_er_svg_v2 import generate_svg

entities, relationships, attributes, connections, cardinalities = generate_svg()

fig, ax = plt.subplots(figsize=(32, 21), dpi=100)
ax.set_xlim(0, 3200)
ax.set_ylim(2100, 0) # Inverted Y to match SVG coordinate system
ax.axis('off')

# Title
ax.text(1600, 75, "E-LIBRARY DBMS - ENTITY-RELATIONSHIP DIAGRAM", fontsize=28, fontweight='bold', ha='center', va='center', color='#0F172A')

# 1. Connections
for conn in connections:
    p1 = conn['p1']
    p2 = conn['p2']
    is_double = conn['is_double']
    poly = conn['polyline']
    has_jump = conn['has_jump']

    if poly:
        xs = [p[0] for p in poly]
        ys = [p[1] for p in poly]
        ax.plot(xs, ys, color='#475569', lw=2.0, zorder=1)
    elif is_double:
        ax.plot([p1[0]-3, p2[0]-3], [p1[1], p2[1]], color='#475569', lw=1.8, zorder=1)
        ax.plot([p1[0]+3, p2[0]+3], [p1[1], p2[1]], color='#475569', lw=1.8, zorder=1)
    else:
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='#475569', lw=2.0, zorder=1)

# Attribute connections
for a in attributes:
    if 'entity_key' in a:
        e = entities[a['entity_key']]
        ax.plot([e['cx'], a['cx']], [e['cy'], a['cy']], color='#64748B', lw=1.4, zorder=1)
    elif 'rel_key' in a:
        r = relationships[a['rel_key']]
        ax.plot([r['cx'], a['cx']], [r['cy'], a['cy']], color='#64748B', lw=1.4, zorder=1)

# 2. Relationships (Diamonds)
for k, r in relationships.items():
    x, y, rx, ry = r['cx'], r['cy'], r['rx'], r['ry']
    pts = [[x, y - ry], [x + rx, y], [x, y + ry], [x - rx, y]]
    if r['is_identifying']:
        pts_out = [[x, y - ry - 5], [x + rx + 6, y], [x, y + ry + 5], [x - rx - 6, y]]
        poly_out = patches.Polygon(pts_out, facecolor='#FEF3C7', edgecolor='#B45309', lw=1.6, zorder=2)
        ax.add_patch(poly_out)
    poly = patches.Polygon(pts, facecolor='#FEF3C7', edgecolor='#D97706', lw=2.0, zorder=3)
    ax.add_patch(poly)

    words = r['name'].split()
    if len(words) > 1:
        ax.text(x, y - 5, words[0], fontsize=10.5, fontweight='bold', color='#92400E', ha='center', va='center', zorder=5)
        ax.text(x, y + 8, words[1], fontsize=10.5, fontweight='bold', color='#92400E', ha='center', va='center', zorder=5)
    else:
        ax.text(x, y, r['name'], fontsize=11, fontweight='bold', color='#92400E', ha='center', va='center', zorder=5)

# 3. Entities (Rectangles)
for k, e in entities.items():
    x, y, w, h = e['cx'], e['cy'], e['w'], e['h']
    c = e['colors']
    if e['is_weak']:
        rect_out = patches.FancyBboxPatch((x - w/2 - 5, y - h/2 - 5), w + 10, h + 10, boxstyle="round,pad=0,rounding_size=8",
                                          facecolor=c['bg'], edgecolor=c['border'], lw=1.6, zorder=2)
        ax.add_patch(rect_out)
    rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0,rounding_size=6",
                                  facecolor=c['bg'], edgecolor=c['border'], lw=2.4, zorder=3)
    ax.add_patch(rect)
    ax.text(x, y, e['name'], fontsize=13, fontweight='bold', color=c['text'], ha='center', va='center', zorder=5)

# 4. Attributes (Ellipses)
for a in attributes:
    x, y, w, h = a['cx'], a['cy'], a['w'], a['h']
    c = a['colors']
    ellipse = patches.Ellipse((x, y), w, h, facecolor=c['attr_bg'], edgecolor=c['attr_b'], lw=1.6, zorder=3)
    ax.add_patch(ellipse)
    weight = 'bold' if a['is_pk'] else 'normal'
    txt = ax.text(x, y, a['name'], fontsize=10.5, fontweight=weight, color='#0F172A', ha='center', va='center', zorder=5)
    if a['is_pk']:
        tw = len(a['name']) * 3.4
        ax.plot([x - tw, x + tw], [y + 7, y + 7], color='#0F172A', lw=1.4, zorder=6)

# 5. Cardinalities
for card in cardinalities:
    x, y, label = card['cx'], card['cy'], card['label']
    box = patches.FancyBboxPatch((x - 18, y - 10), 36, 20, boxstyle="round,pad=0,rounding_size=4",
                                facecolor='#FFFFFF', edgecolor='#94A3B8', lw=1.0, zorder=4)
    ax.add_patch(box)
    ax.text(x, y, label, fontsize=10.5, fontweight='bold', color='#1E40AF', ha='center', va='center', zorder=5)

plt.tight_layout()
plt.savefig('report_assets/er_diagram_preview_rendered.png', dpi=100)
print("Preview rendered successfully to report_assets/er_diagram_preview_rendered.png!")
