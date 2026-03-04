import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Wedge, Circle, FancyBboxPatch

score = 72
label = "Medium"
dims = {"Match": 76, "Strategy": 68, "Practical": 64}
risks = [
    ("Late Apply Window", -8),
    ("No Referral", -6),
    ("Out-of-State", -5),
]
reco = [
    "Mirror top JD keywords in first 1/3 of resume",
    "Prioritize jobs posted within last 72 hours",
    "Add 3 warm-intro targets before applying",
]
outcomes = {"No Reply": 48, "Interview": 28, "Final Round": 14, "Offer": 10}

fig = plt.figure(figsize=(14, 8), dpi=160)
fig.patch.set_facecolor("#f8fafc")

# Title
fig.text(0.04, 0.95, "Interview Probability Score - Sample Report", fontsize=20, weight='bold', color="#0f172a")
fig.text(0.04, 0.92, "Application Strategy Score | Generated Sample", fontsize=10, color="#475569")

# Score gauge
ax_g = fig.add_axes([0.04, 0.55, 0.28, 0.32])
ax_g.set_aspect('equal')
ax_g.axis('off')
base = Wedge((0, 0), 1.0, 180, 360, width=0.22, facecolor="#e2e8f0", edgecolor='none')
ax_g.add_patch(base)
end_angle = 180 + 180 * (score / 100)
color = "#10b981" if score >= 75 else "#f59e0b" if score >= 50 else "#f43f5e"
val = Wedge((0, 0), 1.0, 180, end_angle, width=0.22, facecolor=color, edgecolor='none')
ax_g.add_patch(val)
ax_g.add_patch(Circle((0,0), 0.68, color="#ffffff", ec="#e2e8f0", lw=1))
ax_g.text(0, -0.03, f"{score}", ha='center', va='center', fontsize=34, weight='bold', color="#0f172a")
ax_g.text(0, -0.22, f"{label}", ha='center', va='center', fontsize=12, weight='bold', color=color)
ax_g.text(-1.05, -0.02, "0", fontsize=9, color="#64748b")
ax_g.text(1.0, -0.02, "100", fontsize=9, color="#64748b")
ax_g.set_xlim(-1.2, 1.2)
ax_g.set_ylim(-1.1, 1.1)

# Dimensions bar
ax_d = fig.add_axes([0.36, 0.57, 0.28, 0.26])
ax_d.set_facecolor("#ffffff")
for s in ax_d.spines.values():
    s.set_visible(False)
ax_d.set_title("Dimension Breakdown", fontsize=12, weight='bold', color="#0f172a", loc='left', pad=10)
keys = list(dims.keys())
vals = list(dims.values())
y = np.arange(len(keys))
ax_d.barh(y, [100]*len(keys), color="#f1f5f9", height=0.5)
ax_d.barh(y, vals, color="#0f172a", height=0.5)
ax_d.set_yticks(y, keys)
ax_d.set_xlim(0, 100)
ax_d.invert_yaxis()
ax_d.tick_params(axis='x', colors="#94a3b8")
ax_d.tick_params(axis='y', colors="#334155")
for i, v in enumerate(vals):
    ax_d.text(v + 2, i, f"{v}%", va='center', fontsize=9, color="#334155")

# Risk factors
ax_r = fig.add_axes([0.67, 0.52, 0.29, 0.34])
ax_r.set_facecolor("#ffffff")
for s in ax_r.spines.values():
    s.set_visible(False)
ax_r.set_title("Top Risk Factors (Score Down)", fontsize=12, weight='bold', color="#0f172a", loc='left', pad=10)
rx = [r[1] for r in risks]
rl = [r[0] for r in risks]
y2 = np.arange(len(rl))
ax_r.barh(y2, rx, color="#fb7185", height=0.55)
ax_r.set_yticks(y2, rl)
ax_r.set_xlim(-10, 0)
ax_r.invert_yaxis()
ax_r.tick_params(axis='x', colors="#94a3b8")
ax_r.tick_params(axis='y', colors="#334155", labelsize=9)
for i, v in enumerate(rx):
    ax_r.text(v - 0.3, i, str(v), va='center', ha='right', fontsize=9, color="#9f1239", weight='bold')

# Recommendations card
ax_t = fig.add_axes([0.04, 0.08, 0.60, 0.36])
ax_t.axis('off')
bg = FancyBboxPatch((0,0), 1, 1, boxstyle="round,pad=0.012,rounding_size=0.02", fc="#ffffff", ec="#dbe3ee")
ax_t.add_patch(bg)
ax_t.text(0.03, 0.9, "3 Actionable Recommendations", fontsize=12, weight='bold', color="#0f172a")
for i, t in enumerate(reco, start=1):
    y0 = 0.75 - (i-1)*0.24
    row = FancyBboxPatch((0.03, y0-0.09), 0.94, 0.16, boxstyle="round,pad=0.01,rounding_size=0.015", fc="#f8fafc", ec="#e2e8f0")
    ax_t.add_patch(row)
    ax_t.text(0.06, y0, f"{i}. {t}", fontsize=10, color="#334155", va='center')

# Outcome donut
ax_o = fig.add_axes([0.68, 0.10, 0.28, 0.32])
ax_o.set_facecolor("#ffffff")
for s in ax_o.spines.values():
    s.set_visible(False)
ax_o.set_title("Outcome Tracking (Sample)", fontsize=12, weight='bold', color="#0f172a", loc='left', pad=10)
labels = list(outcomes.keys())
values = list(outcomes.values())
colors = ["#64748b", "#0ea5e9", "#8b5cf6", "#10b981"]
wedges, _ = ax_o.pie(values, colors=colors, startangle=90, wedgeprops=dict(width=0.35, edgecolor='white'))
ax_o.text(0, 0, "100\nApplications", ha='center', va='center', fontsize=10, color="#334155")
ax_o.legend(wedges, [f"{k}: {v}%" for k,v in zip(labels, values)], loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=2, frameon=False, fontsize=8)

fig.text(0.04, 0.03, "Decision: Apply with optimization first | Confidence: 74%", fontsize=10, color="#475569")

out = "/Users/sirao/interview-probability-score-tool-page/report-samples/interview-score-report-sample.png"
plt.savefig(out, bbox_inches='tight', facecolor=fig.get_facecolor())
print(out)
