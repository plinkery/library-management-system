import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(13, 10), dpi=300)
ax.set_xlim(0, 130)
ax.set_ylim(0, 100)
ax.axis('off')

# Color styling
ent_bg = '#F8FAFC'
ent_border = '#1E3A8A'
rel_bg = '#FEF3C7'
rel_border = '#D97706'
attr_bg = '#F0FDFA'
attr_border = '#0D9488'
line_color = '#475569'

def draw_entity(x, y, w, h, name):
    rect = patches.Rectangle((x - w/2, y - h/2), w, h,
                             linewidth=1.8, edgecolor=ent_border, facecolor=ent_bg, zorder=3)
    ax.add_patch(rect)
    ax.text(x, y, name, fontsize=10, fontweight='bold', ha='center', va='center', color='#1E293B', zorder=4)

def draw_relationship(x, y, r, name):
    pts = [[x, y + r], [x + r*1.3, y], [x, y - r], [x - r*1.3, y]]
    poly = patches.Polygon(pts, linewidth=1.5, edgecolor=rel_border, facecolor=rel_bg, zorder=3)
    ax.add_patch(poly)
    ax.text(x, y, name, fontsize=8, fontweight='bold', ha='center', va='center', color='#92400E', zorder=4)

def draw_attribute(x, y, w, h, name, is_pk=False):
    ellipse = patches.Ellipse((x, y), w, h, linewidth=1.2, edgecolor=attr_border, facecolor=attr_bg, zorder=3)
    ax.add_patch(ellipse)
    txt = ax.text(x, y, name, fontsize=7.5, ha='center', va='center', color='#0F172A', zorder=4)
    if is_pk:
        # Underline text for PK
        txt.set_fontweight('bold')
        ax.plot([x - len(name)*1.3, x + len(name)*1.3], [y - 1.2, y - 1.2], color='#0F172A', lw=1.2, zorder=5)

def draw_line(x1, y1, x2, y2, label=None, lx=None, ly=None):
    ax.plot([x1, x2], [y1, y2], color=line_color, lw=1.3, zorder=2)
    if label and lx is not None and ly is not None:
        ax.text(lx, ly, label, fontsize=8.5, fontweight='bold', color='#1E40AF', zorder=5)

# 1. ENTITY: Users (x=30, y=75)
draw_entity(30, 75, 18, 7, "Users")
# Attributes of Users
u_attrs = [
    (14, 88, 14, 5, "user_id", True),
    (30, 90, 13, 5, "usn"),
    (46, 88, 14, 5, "name"),
    (14, 75, 13, 5, "role"),
    (14, 62, 14, 5, "email"),
    (46, 62, 14, 5, "password")
]
for ax_pos, ay_pos, aw, ah, aname, *pk in u_attrs:
    is_p = pk[0] if pk else False
    draw_attribute(ax_pos, ay_pos, aw, ah, aname, is_p)
    draw_line(30, 75, ax_pos, ay_pos)

# 2. ENTITY: BookCopies (x=80, y=75)
draw_entity(80, 75, 20, 7, "Book_Copies")
# Attributes of BookCopies
bc_attrs = [
    (70, 89, 14, 5, "copy_id", True),
    (90, 89, 16, 5, "copy_code"),
    (100, 75, 14, 5, "status"),
    (80, 63, 16, 5, "rack_location")
]
for ax_pos, ay_pos, aw, ah, aname, *pk in bc_attrs:
    is_p = pk[0] if pk else False
    draw_attribute(ax_pos, ay_pos, aw, ah, aname, is_p)
    draw_line(80, 75, ax_pos, ay_pos)

# Relationship: Users - BORROWS - BookCopies (via Loans)
draw_relationship(55, 75, 5.5, "BORROWS")
draw_line(39, 75, 48, 75, "1", 42, 77)
draw_line(62, 75, 70, 75, "N", 67, 77)

# Relationship: Users - RESERVES - BookCopies
draw_relationship(55, 87, 5, "RESERVES")
draw_line(35, 78.5, 48.5, 87, "1", 38, 85)
draw_line(61.5, 87, 75, 78.5, "N", 70, 85)

# 3. ENTITY: Books (x=112, y=45)
draw_entity(112, 45, 18, 7, "Books")
b_attrs = [
    (112, 60, 14, 5, "book_id", True),
    (124, 53, 12, 5, "title"),
    (124, 38, 12, 5, "isbn"),
    (112, 30, 13, 5, "rating")
]
for ax_pos, ay_pos, aw, ah, aname, *pk in b_attrs:
    is_p = pk[0] if pk else False
    draw_attribute(ax_pos, ay_pos, aw, ah, aname, is_p)
    draw_line(112, 45, ax_pos, ay_pos)

# Relationship: Books - HAS - BookCopies
draw_relationship(96, 60, 5, "HAS")
draw_line(112, 48.5, 96, 55, "1", 107, 53)
draw_line(96, 65, 85, 71.5, "N", 91, 70)

# 4. ENTITY: Loans (Transaction Entity) (x=55, y=45)
draw_entity(55, 45, 18, 7, "Loans")
l_attrs = [
    (40, 53, 14, 5, "loan_id", True),
    (38, 42, 15, 5, "borrow_date"),
    (40, 32, 14, 5, "due_date"),
    (55, 32, 14, 5, "status")
]
for ax_pos, ay_pos, aw, ah, aname, *pk in l_attrs:
    is_p = pk[0] if pk else False
    draw_attribute(ax_pos, ay_pos, aw, ah, aname, is_p)
    draw_line(55, 45, ax_pos, ay_pos)

# Link Loans to BORROWS
draw_line(55, 69.5, 55, 48.5)

# 5. ENTITY: Fines (x=20, y=20)
draw_entity(20, 20, 16, 7, "Fines")
f_attrs = [
    (10, 31, 13, 5, "fine_id", True),
    (10, 10, 14, 5, "amount"),
    (24, 8, 16, 5, "days_overdue"),
    (32, 18, 13, 5, "status")
]
for ax_pos, ay_pos, aw, ah, aname, *pk in f_attrs:
    is_p = pk[0] if pk else False
    draw_attribute(ax_pos, ay_pos, aw, ah, aname, is_p)
    draw_line(20, 20, ax_pos, ay_pos)

# Relationship: Loans - INCURS - Fines
draw_relationship(38, 25, 4.5, "INCURS")
draw_line(49, 41.5, 43, 28, "1", 48, 33)
draw_line(33, 23, 28, 21, "0..1", 31, 18)

# 6. ENTITY: BookRequests (x=80, y=20)
draw_entity(80, 20, 20, 7, "Book_Requests")
br_attrs = [
    (67, 9, 15, 5, "request_id", True),
    (83, 8, 13, 5, "title"),
    (96, 12, 14, 5, "author"),
    (98, 23, 16, 5, "votes_count")
]
for ax_pos, ay_pos, aw, ah, aname, *pk in br_attrs:
    is_p = pk[0] if pk else False
    draw_attribute(ax_pos, ay_pos, aw, ah, aname, is_p)
    draw_line(80, 20, ax_pos, ay_pos)

# Relationship: Users - SUGGESTS - BookRequests
draw_relationship(70, 35, 5, "SUGGESTS")
draw_line(30, 71.5, 65, 38, "1", 38, 56)
draw_line(74, 32, 78, 23.5, "N", 78, 29)

# Title box on top
ax.text(65, 96, "College E-Library Management System — Entity-Relationship (ER) Diagram",
        fontsize=13, fontweight='bold', ha='center', color='#1E3A8A')

plt.tight_layout()
plt.savefig('/home/pink/e-libraryDB/report_assets/er_diagram.png', dpi=300, bbox_inches='tight')
print("er_diagram.png created successfully!")
