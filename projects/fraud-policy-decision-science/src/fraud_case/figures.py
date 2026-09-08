"""A consistent editorial chart system: exact data, high-contrast visual hierarchy."""

from io import BytesIO

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

BG = "#080f20"
PANEL = "#111d33"
FG = "#edf4ff"
MUTED = "#9caec8"
CYAN = "#34e4d4"
CORAL = "#ff796b"
PURPLE = "#af91ff"
GOLD = "#ffd075"
BLUE = "#539bff"
COLORS = [CYAN, CORAL, PURPLE, GOLD, BLUE]


def style():
    plt.rcParams.update(
        {
            "figure.facecolor": BG,
            "axes.facecolor": PANEL,
            "savefig.facecolor": BG,
            "text.color": FG,
            "axes.labelcolor": MUTED,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "axes.edgecolor": "#32435f",
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titleweight": "bold",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "svg.fonttype": "none",
            "svg.hashsalt": "fraud-v2",
            "axes.grid": False,
        }
    )


def canvas(title, subtitle, nrows=1, ncols=1, size=(13, 6)):
    fig, axes = plt.subplots(nrows, ncols, figsize=size, squeeze=False)
    fig.suptitle(title, x=0.06, y=0.97, ha="left", fontsize=23, fontweight="bold")
    fig.text(0.06, 0.89, subtitle, color=MUTED, fontsize=10)
    fig.subplots_adjust(
        left=0.08, right=0.96, bottom=0.16, top=0.79, wspace=0.40, hspace=0.60
    )
    return fig, axes


def save(fig, root, name):
    # Buffer complete images before writing, including on remote-backed filesystems.
    for ext in ["svg", "png"]:
        buffer = BytesIO()
        fig.savefig(
            buffer, format=ext, dpi=170, metadata={"Date": None} if ext == "svg" else {}
        )
        (root / f"{name}.{ext}").write_bytes(buffer.getvalue())
    plt.close(fig)


def generate(root, tables):
    style()
    root.mkdir(parents=True, exist_ok=True)
    inputs = root.parent.parent / "data/case_inputs"
    case_itt = pd.read_csv(inputs / "3ds_itt.csv")
    case_displacement = pd.read_csv(inputs / "displacement.csv")
    accounting = pd.read_csv(inputs / "accounting.csv")
    fig, ax = canvas(
        "WHEN FRAUD BECOMES A SYSTEM PROBLEM",
        "Decision Science / two connected mechanisms / supplied synthetic case evidence",
        size=(13, 5),
    )
    a = ax[0, 0]
    a.axis("off")
    for x, big, label, col in [
        (0, "+47%", "Reported portfolio loss rate", CORAL),
        (0.34, "−40.1%", "3DS experiment · net loss rate", CYAN),
        (0.68, "−53% / −7%", "Week 3 · channel / portfolio", PURPLE),
    ]:
        a.add_patch(
            FancyBboxPatch(
                (x, 0),
                0.30,
                0.95,
                boxstyle="round,pad=.015",
                clip_on=False,
                transform=a.transAxes,
                facecolor=PANEL,
                edgecolor=col,
                linewidth=1.5,
            )
        )
        a.text(
            x + 0.02,
            0.55,
            big,
            fontsize=29,
            color=col,
            fontweight="bold",
            transform=a.transAxes,
        )
        a.text(x + 0.02, 0.25, label, fontsize=10, transform=a.transAxes)
    fig.text(
        0.08,
        0.06,
        "Diagnose the mechanism. Change the estimand. Evaluate the decision.",
        fontsize=14,
        fontweight="bold",
    )
    save(fig, root, "00_hero")

    fig, axs = canvas(
        "Two investigations. One economic decision.",
        "Conceptual structure · the target expands from transaction effects to policy value",
        size=(13, 7),
    )
    a = axs[0, 0]
    a.axis("off")
    nodes = [
        (0.02, 0.76, "CNP deterioration", CORAL),
        (0.34, 0.76, "Routing × observability", CORAL),
        (0.68, 0.76, "3DS → displacement", CORAL),
        (0.02, 0.38, "Gross → liability", CYAN),
        (0.34, 0.38, "Evidence × capacity", CYAN),
        (0.68, 0.38, "Recovery → net loss", CYAN),
        (0.34, 0.02, "Joint adaptive policy", PURPLE),
    ]
    for x, y, label, c in nodes:
        a.add_patch(
            FancyBboxPatch(
                (x, y),
                0.27,
                0.17,
                boxstyle="round,pad=.02",
                facecolor=PANEL,
                edgecolor=c,
                linewidth=2,
                transform=a.transAxes,
            )
        )
        a.text(
            x + 0.135,
            y + 0.085,
            label,
            ha="center",
            va="center",
            fontsize=12,
            transform=a.transAxes,
        )
    for start, end in [
        ((0.29, 0.845), (0.34, 0.845)),
        ((0.61, 0.845), (0.68, 0.845)),
        ((0.29, 0.465), (0.34, 0.465)),
        ((0.61, 0.465), (0.68, 0.465)),
        ((0.815, 0.74), (0.48, 0.21)),
        ((0.815, 0.36), (0.55, 0.21)),
        ((0.475, 0.74), (0.475, 0.58)),
    ]:
        a.add_patch(
            FancyArrowPatch(
                start,
                end,
                arrowstyle="-|>",
                mutation_scale=17,
                color=MUTED,
                transform=a.transAxes,
                connectionstyle="arc3,rad=0.05",
            )
        )
    save(fig, root, "01_system_map")

    f, axs = canvas(
        "A merchant label can hide two different mechanisms.",
        "Generated reconstruction · standardized to the same pre-routing geography/CNP mix",
        ncols=2,
    )
    d = tables["merchant"]
    a = axs[0, 0]
    x = np.arange(len(d))
    a.bar(x - 0.17, d.raw_relative, 0.32, color=CORAL, label="Raw")
    a.bar(x + 0.17, d.standardized_relative, 0.32, color=CYAN, label="Standardized")
    a.set_xticks(x, d.merchant)
    a.set_ylabel("Fraud incidence relative to Peer")
    a.axhline(1, color=MUTED, ls=":")
    a.legend(frameon=False)
    a = axs[0, 1]
    a.axis("off")
    a.text(0.04, 0.78, "Merchant A", fontsize=20, color=CORAL, fontweight="bold")
    a.text(
        0.04,
        0.55,
        "Routing creates an additional\npath into weak authentication.",
        fontsize=13,
        linespacing=1.7,
    )
    a.text(0.04, 0.30, "Merchant B", fontsize=20, color=CYAN, fontweight="bold")
    a.text(
        0.04,
        0.07,
        "Risk concentration largely follows\nthe transaction mix.",
        fontsize=13,
        linespacing=1.7,
    )
    save(f, root, "02_merchants")

    f, axs = canvas(
        "The intervention creates a trade-off.",
        "Supplied scenario evidence · percentage-point changes; distinct denominators",
        ncols=3,
    )
    for a, title, vals, col, unit in zip(
        axs[0],
        ["Gross fraud loss", "Net company loss", "Payment completion"],
        [tuple(case_itt.iloc[i][["control_pct", "treatment_pct"]]) for i in [1, 2, 0]],
        [CORAL, CYAN, PURPLE],
        ["% attempted value", "% attempted value", "% attempted transactions"],
    ):
        a.bar(["Control", "Forced 3DS"], vals, color=[MUTED, col], width=0.55)
        a.set_title(title, pad=15)
        a.set_ylabel(unit)
        a.set_ylim(0, max(vals) * 1.35)
        for i, v in enumerate(vals):
            a.text(
                i,
                v + max(vals) * 0.04,
                f"{v:.2f}%",
                ha="center",
                fontsize=15,
                fontweight="bold",
            )
        a.text(
            0.5,
            0.92,
            f"{vals[1] - vals[0]:+.2f} pp",
            ha="center",
            transform=a.transAxes,
            color=col,
            fontsize=19,
            fontweight="bold",
        )
    save(f, root, "03_3ds_tradeoff")

    f, axs = canvas(
        "A selected population can reverse the apparent verdict.",
        "Left: original teaching example, 1,000 attempts per arm. Right: separate supplied experiment.",
        ncols=2,
    )
    a = axs[0, 0]
    vals = [20 / 918 * 100, 21 / 889 * 100]
    a.bar(
        ["Control completers", "3DS completers"], vals, color=[MUTED, CORAL], width=0.5
    )
    a.set_ylabel("Fraud count / completed transactions (%)")
    a.set_ylim(0, 3.2)
    a.set_title("Completed-only view")
    for i, v in enumerate(vals):
        a.text(i, v + 0.12, f"{v:.2f}%", ha="center", fontsize=20, color=CORAL)
    a = axs[0, 1]
    a.bar(
        ["Control attempts", "3DS attempts"],
        [2.72, 1.63],
        color=[MUTED, CYAN],
        width=0.5,
    )
    a.set_ylabel("Net loss / attempted value (%)")
    a.set_ylim(0, 3.5)
    a.set_title("Assigned-population view")
    for i, v in enumerate([2.72, 1.63]):
        a.text(i, v + 0.12, f"{v:.2f}%", ha="center", fontsize=20, color=CYAN)
    save(f, root, "04_selection")

    f, axs = canvas(
        "What improves when the information changes?",
        "Generated temporal holdout · empirical diagnostics, not a theoretical information bound",
        ncols=2,
        size=(14, 7),
    )
    f.subplots_adjust(left=0.19, wspace=0.48)
    d = tables["models"]
    a = axs[0, 0]
    low = d[(d.population == "Low") & (d.model != "Remaining-information diagnostic")]
    a.barh(np.arange(len(low)), low.roc_auc, color=[MUTED, CORAL, CYAN, PURPLE])
    a.set_yticks(
        np.arange(len(low)),
        ["Production proxy", "Same information", "Add PSP signal", "Specialized"],
    )
    a.set_xlim(0.45, 1)
    a.set_xlabel("ROC-AUC · natural low observability")
    for i, v in enumerate(low.roc_auc):
        a.text(v + 0.01, i, f"{v:.3f}", va="center")
    a = axs[0, 1]
    diag = d[d.model == "Remaining-information diagnostic"]
    a.bar(diag.population, diag.roc_auc, color=[BLUE, CORAL])
    a.set_ylim(0, 1)
    a.set_ylabel("ROC-AUC")
    a.set_title("Same remaining columns\nDifferent generating populations")
    save(f, root, "05_information")

    f, axs = canvas(
        "Local suppression. Delayed displacement.",
        "Supplied indexed losses · baseline 100 in each channel group; combined baseline 200",
        size=(13, 6),
    )
    a = axs[0, 0]
    x = np.arange(5)
    treated = case_displacement.treated.to_numpy()
    other = case_displacement.other.to_numpy()
    total = treated + other
    a.stackplot(
        x,
        treated,
        other,
        colors=[CYAN, CORAL],
        alpha=0.60,
        labels=["Treated channel", "Other channels"],
    )
    a.plot(x, total, color=FG, lw=3, marker="o", ms=7, label="Portfolio total")
    a.axhline(200, color=MUTED, ls="--", lw=1)
    a.set_ylim(0, 245)
    a.set_ylabel("Common indexed loss units")
    a.set_xticks(x, ["Baseline", "Week 1", "Week 2", "Week 3", "2 weeks after removal"])
    for i, v in enumerate(total):
        a.text(i, v + 10, str(v), ha="center", fontweight="bold")
    a.annotate(
        "Week 3: channel −53%\nportfolio only −7%",
        xy=(3, 186),
        xytext=(1.8, 225),
        color=GOLD,
        fontsize=13,
        arrowprops={"arrowstyle": "->", "color": GOLD},
    )
    a.legend(loc="lower left", frameon=False, ncol=3)
    save(f, root, "06_displacement")

    f, axs = canvas(
        "More fraud. A larger fraction becomes company loss.",
        "Exact supplied accounting · liability allocation and recovery are distinct deductions",
        ncols=2,
    )
    for a, title, gross, liable, recovery in [
        (axs[0, i], row.period, row.gross, row.company_liability, row.recovery)
        for i, row in accounting.iterrows()
    ]:
        vals = [gross, gross - liable, recovery, liable - recovery]
        bottom = [0, liable, liable - recovery, 0]
        a.bar(
            range(4),
            vals,
            bottom=bottom,
            color=[MUTED, PURPLE, CYAN, CORAL],
            width=0.65,
        )
        a.set_xticks(range(4), ["Gross", "Other liability", "Recovered", "Net"])
        a.set_ylim(0, 150)
        a.set_title(title)
        a.set_ylabel("Indexed monetary amount")
        for i, v in enumerate(vals):
            a.text(
                i,
                bottom[i] + v + 4,
                f"{'−' if i in [1, 2] else ''}{v}",
                ha="center",
                fontsize=17,
                fontweight="bold",
            )
    save(f, root, "07_waterfall")

    f, axs = canvas(
        "Policy value depends on the path through the queue.",
        "Generated low-arrival scenario · representative seed; terminal outstanding liability retained",
        nrows=3,
        size=(13, 10),
    )
    paths = tables["trajectories"]
    if "scenario" in paths:
        paths = paths[paths.scenario == "Low arrivals"]
    for i, policy in enumerate(["fixed_0.5", "adaptive", "delayed"]):
        d = paths[paths.policy == policy]
        for j, col in enumerate(["backlog", "saturation", "value"]):
            y = d[col].cumsum() / 1000 if col == "value" else d[col]
            axs[j, 0].plot(d.day, y, label=policy, color=[MUTED, CYAN, PURPLE][i], lw=2)
    axs[0, 0].axhline(1200, color=CORAL, ls=":", alpha=0.8)
    axs[0, 0].axhline(800, color=CYAN, ls=":", alpha=0.6)
    for a, label in zip(
        axs[:, 0], ["Open cases", "3DS saturation", "Cumulative value ($K)"]
    ):
        a.set_ylabel(label)
    axs[0, 0].legend(frameon=False, ncol=3)
    axs[2, 0].set_xlabel("Day")
    save(f, root, "08_policy_paths")

    f, axs = canvas(
        "Which policy wins when assumptions change?",
        "Generated sensitivity analysis · mean incremental value vs fixed medium, paired seeds",
        size=(13, 7),
    )
    f.subplots_adjust(left=0.20)
    d = tables["policies"]
    wide = d.pivot(index=["scenario", "seed"], columns="policy", values="value")
    delta = wide.sub(wide["fixed_0.5"], axis=0) / 1000
    summary = delta.groupby("scenario").mean()[
        ["fixed_0.2", "fixed_0.5", "fixed_0.8", "adaptive", "delayed"]
    ]
    a = axs[0, 0]
    bound = max(1, np.max(np.abs(summary.values)))
    im = a.imshow(summary, cmap="RdBu", vmin=-bound, vmax=bound, aspect="auto")
    a.set_xticks(
        range(5), ["Fixed low", "Fixed medium", "Fixed high", "Adaptive", "Delayed"]
    )
    a.set_yticks(range(len(summary)), summary.index)
    for i in range(len(summary)):
        for j in range(5):
            a.text(
                j,
                i,
                f"{summary.iloc[i, j]:+.1f}K",
                ha="center",
                va="center",
                color="black" if abs(summary.iloc[i, j]) < 0.5 * bound else "white",
                fontsize=14,
                fontweight="bold",
            )
    f.colorbar(im, ax=a, label="Incremental value ($K)", shrink=0.8)
    save(f, root, "09_policy_sensitivity")

    f, axs = canvas(
        "Immature cohorts can conceal deterioration.",
        "Generated settled history · fixed 42-day labels; dashed section uses future truth for diagnosis",
        size=(13, 6),
    )
    d = tables["cohorts"]
    a = axs[0, 0]
    a.plot(d.week, d.naive_rate * 100, color=CORAL, label="Observed by extraction")
    a.plot(
        d.week,
        d.recognition_rate * 100,
        color=PURPLE,
        alpha=0.7,
        label="Recognition dashboard",
    )
    mature = d.mature == 1
    a.plot(
        d.loc[mature, "week"],
        d.loc[mature, "fixed_window_rate"] * 100,
        color=CYAN,
        lw=2.5,
        label="Mature 42-day cohorts",
    )
    a.plot(
        d.loc[~mature, "week"],
        d.loc[~mature, "fixed_window_rate"] * 100,
        color=CYAN,
        ls="--",
        label="Future labels (simulator only)",
    )
    a.set_ylabel("Net loss / settled value (%)")
    a.set_xlabel("Transaction / reporting week")
    a.legend(frameon=False, fontsize=9)
    save(f, root, "10_cohorts")

    f, axs = canvas(
        "Recovery interventions can share the same benefit.",
        "Generated equal-dose factorial · 12 paired seeds · +450 weekly units and 70% automation",
        ncols=2,
    )
    fac = pd.read_csv(root.parent / "tables/factorial.csv")
    wide = fac.pivot(index="seed", columns="intervention", values="value")
    a = axs[0, 0]
    changes = (
        wide[["Capacity", "Automation", "Combined"]].sub(wide.Baseline, axis=0) / 1000
    )
    vals = changes.mean()
    err = 2.201 * changes.std() / np.sqrt(len(changes))
    a.bar(range(3), vals, yerr=err, color=[CORAL, CYAN, PURPLE], capsize=5)
    a.set_xticks(range(3), vals.index)
    a.set_ylabel("Incremental value ($K)")
    a = axs[0, 1]
    interaction = wide.Interaction / 1000
    a.axhline(0, color=MUTED, lw=1)
    a.scatter(range(len(interaction)), interaction, color=GOLD, s=45)
    a.set_xlabel("Paired simulation seed")
    a.set_ylabel("Factorial interaction ($K)")
    a.set_title("Combined − capacity − automation + baseline", fontsize=10)
    save(f, root, "11_operations_factorial")

    f, axs = canvas(
        "Ranking gains need a probability check.",
        "Generated temporal holdout · low-observability population · six equal-count calibration bins",
        size=(13, 6),
    )
    cal = pd.read_csv(root.parent / "tables/calibration.csv")
    a = axs[0, 0]
    for i, (name, g) in enumerate(
        cal[cal.population == "Low"].groupby("model", sort=False)
    ):
        a.plot(g.predicted, g.observed, marker="o", lw=2, color=COLORS[i], label=name)
    a.plot([0, 0.8], [0, 0.8], color=MUTED, ls="--", label="Perfect calibration")
    a.set_xlim(0, 0.8)
    a.set_ylim(0, 0.8)
    a.set_xlabel("Mean predicted probability")
    a.set_ylabel("Observed fraud incidence")
    a.legend(frameon=False, fontsize=9)
    save(f, root, "12_calibration")
