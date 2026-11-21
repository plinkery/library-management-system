import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(9, 13), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 140)
ax.axis('off')

# Box styles
box_color = '#F0FDFA'
box_border = '#0D9488'
decision_color = '#FEF3C7'
decision_border = '#D97706'
arrow_color = '#334155'

def draw_box(x, y, w, h, text, color=box_color, border=box_border):
    rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.3,rounding_size=1",
                                linewidth=1.5, edgecolor=border, facecolor=color, zorder=3)
    ax.add_patch(rect)
    ax.text(x, y, text, fontsize=8, ha='center', va='center', color='#0F172A', fontweight='medium', zorder=4)

def draw_decision(x, y, r, text):
    pts = [[x, y + r], [x + r*1.6, y], [x, y - r], [x - r*1.6, y]]
    poly = patches.Polygon(pts, linewidth=1.5, edgecolor=decision_border, facecolor=decision_color, zorder=3)
    ax.add_patch(poly)
    ax.text(x, y, text, fontsize=7.5, ha='center', va='center', color='#92400E', fontweight='bold', zorder=4)

def draw_arrow(x1, y1, x2, y2, label=None, lx=None, ly=None):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(facecolor=arrow_color, edgecolor=arrow_color, width=1.5, headwidth=6, shrink=0.05), zorder=2)
    if label and lx is not None and ly is not None:
        ax.text(lx, ly, label, fontsize=7.5, fontweight='bold', color='#1E40AF', zorder=5)

# 1. Login
draw_box(50, 134, 40, 6, "User Login (USN & Password)\nRole: Student / Chief Librarian")

# Arrow to catalog
draw_arrow(50, 131, 50, 122)

# 2. Browse catalog
draw_box(50, 119, 44, 6, "Browse Catalog & Filter by Branch / Genre\nSelect Desired Book & Physical Copy")

# Arrow to reserve
draw_arrow(50, 116, 50, 108)

# 3. Reserve 12h
draw_box(50, 105, 48, 6, "Click 'Reserve (12h)' -> Copy='RESERVED'\nLive 12-Hour Countdown Timer Commences")

# Arrow to decision: pickup within 12h?
draw_arrow(50, 102, 50, 93)

# 4. Decision: Pickup within 12h?
draw_decision(50, 88, 5, "Pickup at Counter\nwithin 12 Hours?")

# No branch -> Expiry & 1-day block
draw_arrow(60, 88, 80, 88, "No", 66, 90)
draw_arrow(80, 88, 80, 77)
draw_box(80, 74, 32, 6, "Reservation EXPIRED\nCopy Released to 'AVAILABLE'\nStudent Suspended for 24h", '#FEE2E2', '#EF4444')

# Yes branch -> Librarian Counter
draw_arrow(50, 83, 50, 74, "Yes", 53, 80)

# 5. Librarian Counter Checkout & Trigger check
draw_decision(50, 68, 5.5, "Database Triggers Check:\n1. Active Loans < 5?\n2. No Overdue / Unpaid Fines?")

# Trigger fails branch
draw_arrow(61, 68, 80, 68, "Fails", 67, 70)
draw_arrow(80, 68, 80, 58)
draw_box(80, 55, 32, 6, "Borrowing BLOCKED by Trigger\n(SIGNAL SQLSTATE '45000')\nError Displayed on Counter", '#FEE2E2', '#EF4444')

# Trigger passes -> Issue book
draw_arrow(50, 62.5, 50, 52, "Passes", 53, 58)
draw_box(50, 49, 46, 6, "Issue Book -> Loan Created (30-Day Due Date)\nCopy='BORROWED' via Trigger UpdateCopyOnLoan")

# Arrow to return
draw_arrow(50, 46, 50, 37)
draw_box(50, 34, 44, 6, "Student Uses Book (Active Loan Period)\nReturns Physical Copy to Circulation Desk")

# Arrow to Overdue Check
draw_arrow(50, 31, 50, 23)
draw_decision(50, 18, 5, "Returned After\n30-Day Due Date?")

# Overdue Yes -> Fine
draw_arrow(60, 18, 78, 18, "Yes", 66, 20)
draw_box(80, 18, 30, 6, "Assess Fine: ₹1/day overdue\nLibrarian Collects Revenue\nRecord logged in fine_collections", '#FEF3C7', '#D97706')
draw_arrow(80, 15, 80, 6)
draw_arrow(80, 6, 65, 6)

# Overdue No -> Reset copy
draw_arrow(50, 13, 50, 6, "No", 53, 10)
draw_box(50, 4, 46, 6, "Trigger UpdateCopyOnReturn Fires:\nCopy Status Reset to 'AVAILABLE' in Catalog")

# Title on top
ax.text(50, 139, "College E-Library System — Complete Operational Workflow",
        fontsize=11.5, fontweight='bold', ha='center', color='#0F766E')

plt.tight_layout()
plt.savefig('/home/pink/e-libraryDB/report_assets/system_flowchart.png', dpi=300, bbox_inches='tight')
print("system_flowchart.png created successfully!")
