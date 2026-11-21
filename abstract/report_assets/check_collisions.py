import math
from generate_er_svg_v2 import generate_svg

entities, relationships, attributes, connections, cardinalities = generate_svg()

# Collect bounding boxes: (name, min_x, min_y, max_x, max_y)
boxes = []

for k, e in entities.items():
    boxes.append((f"Entity:{e['name']}", e['cx'] - e['w']/2, e['cy'] - e['h']/2, e['cx'] + e['w']/2, e['cy'] + e['h']/2))

for k, r in relationships.items():
    boxes.append((f"Rel:{r['name']}", r['cx'] - r['rx'], r['cy'] - r['ry'], r['cx'] + r['rx'], r['cy'] + r['ry']))

for a in attributes:
    boxes.append((f"Attr:{a['name']}", a['cx'] - a['w']/2, a['cy'] - a['h']/2, a['cx'] + a['w']/2, a['cy'] + a['h']/2))

for c in cardinalities:
    boxes.append((f"Card:{c['label']}@({c['cx']},{c['cy']})", c['cx'] - 18, c['cy'] - 10, c['cx'] + 18, c['cy'] + 10))

print(f"Total shapes checked: {len(boxes)}")

overlaps = []
for i in range(len(boxes)):
    for j in range(i + 1, len(boxes)):
        name1, x1_min, y1_min, x1_max, y1_max = boxes[i]
        name2, x2_min, y2_min, x2_max, y2_max = boxes[j]

        # Check AABB overlap with padding of 6px
        if (x1_min - 6 < x2_max and x1_max + 6 > x2_min and
            y1_min - 6 < y2_max and y1_max + 6 > y2_min):
            overlaps.append((name1, name2))

if overlaps:
    print(f"Found {len(overlaps)} overlaps:")
    for o1, o2 in overlaps:
        print(f"  Overlap between {o1} and {o2}")
else:
    print("SUCCESS: 0 overlaps found! Every element has perfect clearance!")
