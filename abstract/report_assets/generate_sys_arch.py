import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Color palette
client_color = '#3B82F6'      # vibrant blue
client_light = '#EFF6FF'
app_color = '#F59E0B'         # amber/orange
app_light = '#FFFBEB'
db_color = '#10B981'          # emerald green
db_light = '#ECFDF5'
box_bg = '#FFFFFF'
text_dark = '#1E293B'

# Layer 1: Client Layer
rect1 = patches.FancyBboxPatch((10, 70), 80, 24, boxstyle="round,pad=0.8,rounding_size=2",
                               linewidth=2, edgecolor=client_color, facecolor=client_light)
ax.add_patch(rect1)
ax.text(50, 90.5, "PRESENTATION / CLIENT LAYER", fontsize=13, fontweight='bold', ha='center', color=client_color)
ax.text(50, 87.5, "(HTML5, CSS3, JavaScript ES6+ — Modern Responsive Web Portal)", fontsize=9.5, ha='center', color='#475569', fontstyle='italic')

# Client sub-boxes
c_boxes = [
    ("Student Portal\n(Catalog & Search)", 14, 73, 16, 11),
    ("12h Reservation\nDashboard & Timer", 33, 73, 16, 11),
    ("Librarian Desk\n(Counter Issue/Return)", 52, 73, 16, 11),
    ("Acquisition Requests\n& Voting Portal", 71, 73, 16, 11)
]
for text, x, y, w, h in c_boxes:
    sub = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1",
                                linewidth=1.2, edgecolor='#93C5FD', facecolor=box_bg)
    ax.add_patch(sub)
    ax.text(x + w/2, y + h/2, text, fontsize=8, ha='center', va='center', color=text_dark, fontweight='bold')

# Arrow 1 -> 2
ax.annotate('', xy=(50, 62.5), xytext=(50, 69.5),
            arrowprops=dict(facecolor='#64748B', edgecolor='#475569', width=3, headwidth=10, shrink=0.05))
ax.text(52, 66, "HTTP / REST API (JSON)", fontsize=8, color='#334155', fontweight='semibold')

# Layer 2: Application Layer
rect2 = patches.FancyBboxPatch((10, 36), 80, 24, boxstyle="round,pad=0.8,rounding_size=2",
                               linewidth=2, edgecolor=app_color, facecolor=app_light)
ax.add_patch(rect2)
ax.text(50, 56.5, "APPLICATION / BUSINESS LOGIC LAYER", fontsize=13, fontweight='bold', ha='center', color='#D97706')
ax.text(50, 53.5, "(Java HTTP Server — Business Rules, REST Engine & Transaction Logger)", fontsize=9.5, ha='center', color='#475569', fontstyle='italic')

# App sub-boxes
a_boxes = [
    ("Authentication\n& Session Mgr", 13, 39, 14, 11),
    ("Circulation &\nLoan Controller", 29, 39, 14, 11),
    ("12h Expiry &\nSuspension Logic", 45, 39, 14, 11),
    ("Fine Assessment\n(₹1/Day Engine)", 61, 39, 14, 11),
    ("Live DBMS\nTransaction Logger", 77, 39, 14, 11)
]
for text, x, y, w, h in a_boxes:
    sub = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1",
                                linewidth=1.2, edgecolor='#FCD34D', facecolor=box_bg)
    ax.add_patch(sub)
    ax.text(x + w/2, y + h/2, text, fontsize=7.5, ha='center', va='center', color=text_dark, fontweight='bold')

# Arrow 2 -> 3
ax.annotate('', xy=(50, 28.5), xytext=(50, 35.5),
            arrowprops=dict(facecolor='#64748B', edgecolor='#475569', width=3, headwidth=10, shrink=0.05))
ax.text(52, 32, "JDBC / SQL (Port 3307)", fontsize=8, color='#334155', fontweight='semibold')

# Layer 3: Database Layer
rect3 = patches.FancyBboxPatch((10, 3), 80, 24, boxstyle="round,pad=0.8,rounding_size=2",
                               linewidth=2, edgecolor=db_color, facecolor=db_light)
ax.add_patch(rect3)
ax.text(50, 23.5, "DATABASE / PERSISTENCE LAYER", fontsize=13, fontweight='bold', ha='center', color=db_color)
ax.text(50, 20.5, "(MySQL 8.0 Server — Schema: elibrary_db | 14 Normalized 3NF Tables)", fontsize=9.5, ha='center', color='#475569', fontstyle='italic')

# DB sub-boxes
d_boxes = [
    ("Core Relational Tables\n(users, books, book_copies,\nloans, reservations, fines)", 14, 6, 23, 11),
    ("DBMS Triggers\n(PreventBorrowOverLimit,\nPreventBorrowIfOverdue,\nUpdateCopyStatus)", 40, 6, 23, 11),
    ("Database Views\n(OverdueLoansView,\nHighDemandBooksView,\nBranchFineSummaryView)", 66, 6, 23, 11)
]
for text, x, y, w, h in d_boxes:
    sub = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1",
                                linewidth=1.2, edgecolor='#6EE7B7', facecolor=box_bg)
    ax.add_patch(sub)
    ax.text(x + w/2, y + h/2, text, fontsize=7.5, ha='center', va='center', color=text_dark, fontweight='bold')

plt.tight_layout()
plt.savefig('/home/pink/e-libraryDB/report_assets/system_architecture.png', dpi=300, bbox_inches='tight')
print("system_architecture.png created successfully!")
