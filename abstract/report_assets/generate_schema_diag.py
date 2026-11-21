import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
ax.set_xlim(0, 140)
ax.set_ylim(0, 100)
ax.axis('off')

# Table drawing helper
def draw_table(x, y, title, cols, col_widths, header_color='#1E40AF'):
    total_w = sum(col_widths)
    # Header title
    ax.text(x, y + 5.5, title, fontsize=10, fontweight='bold', color=header_color)
    
    # Cells
    cur_x = x
    h = 5.0
    for i, (cname, w) in enumerate(zip(cols, col_widths)):
        rect = patches.Rectangle((cur_x, y), w, h, linewidth=1.2, edgecolor='#334155', facecolor='#F8FAFC')
        ax.add_patch(rect)
        is_pk = '(PK)' in cname
        is_fk = '(FK)' in cname
        txt = ax.text(cur_x + w/2, y + h/2, cname, fontsize=7.5, ha='center', va='center',
                      fontweight='bold' if (is_pk or is_fk) else 'normal',
                      color='#1E3A8A' if is_pk else ('#B45309' if is_fk else '#0F172A'))
        cur_x += w
    return total_w

# 1. USERS
draw_table(5, 85, "Users",
           ["user_id (PK)", "usn", "name", "role", "branch_id (FK)", "password"],
           [16, 14, 16, 12, 18, 14])

# 2. BOOKS
draw_table(85, 85, "Books",
           ["book_id (PK)", "title", "isbn", "branch_id (FK)", "rating"],
           [15, 13, 11, 15, 9])

# 3. BOOK_COPIES
draw_table(45, 65, "Book_Copies",
           ["copy_id (PK)", "book_id (FK)", "copy_code", "status", "rack_loc"],
           [16, 15, 14, 12, 13])

# 4. RESERVATIONS
draw_table(5, 45, "Reservations",
           ["reservation_id (PK)", "user_id (FK)", "copy_id (FK)", "reserved_at", "expires_at", "status"],
           [22, 16, 16, 16, 16, 12])

# 5. LOANS
draw_table(5, 25, "Loans",
           ["loan_id (PK)", "user_id (FK)", "copy_id (FK)", "borrow_date", "due_date", "return_date", "status"],
           [16, 15, 15, 16, 15, 16, 12])

# 6. FINES
draw_table(5, 5, "Fines",
           ["fine_id (PK)", "loan_id (FK)", "user_id (FK)", "days_overdue", "amount", "status"],
           [15, 15, 15, 16, 12, 12])

# 7. BOOK_REQUESTS
draw_table(82, 45, "Book_Requests",
           ["request_id (PK)", "title", "author", "suggested_by (FK)", "votes_count", "status"],
           [18, 11, 11, 19, 13, 10])

# FK Arrows
# Books -> Book_Copies (book_id)
ax.annotate('', xy=(67.5, 70), xytext=(92.5, 85),
            arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.5,
                            connectionstyle="arc3,rad=-0.2"))

# Users -> Reservations (user_id)
ax.annotate('', xy=(35, 50), xytext=(13, 85),
            arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.5,
                            connectionstyle="arc3,rad=0.2"))

# Book_Copies -> Reservations (copy_id)
ax.annotate('', xy=(51, 50), xytext=(53, 65),
            arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.5,
                            connectionstyle="arc3,rad=-0.1"))

# Users -> Loans (user_id)
ax.annotate('', xy=(28, 30), xytext=(13, 85),
            arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.5,
                            connectionstyle="arc3,rad=0.35"))

# Book_Copies -> Loans (copy_id)
ax.annotate('', xy=(43, 30), xytext=(53, 65),
            arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.5,
                            connectionstyle="arc3,rad=-0.3"))

# Loans -> Fines (loan_id)
ax.annotate('', xy=(27.5, 10), xytext=(13, 25),
            arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.5,
                            connectionstyle="arc3,rad=0.15"))

# Users -> Fines (user_id)
ax.annotate('', xy=(42.5, 10), xytext=(13, 85),
            arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.5,
                            connectionstyle="arc3,rad=0.45"))

# Users -> Book_Requests (suggested_by -> user_id)
ax.annotate('', xy=(131.5, 50), xytext=(13, 85),
            arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.5,
                            connectionstyle="arc3,rad=-0.2"))

# Title
ax.text(70, 97, "College E-Library Database Management System — Relational Schema Diagram",
        fontsize=13, fontweight='bold', ha='center', color='#1E3A8A')

plt.tight_layout()
plt.savefig('/home/pink/e-libraryDB/report_assets/schema_diagram.png', dpi=300, bbox_inches='tight')
print("schema_diagram.png created successfully!")
