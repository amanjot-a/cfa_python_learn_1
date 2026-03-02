"""
╔══════════════════════════════════════════════════════════════════╗
║          TVM — TIME VALUE OF MONEY CALCULATOR                    ║
║          Solve for any one of 5 financial variables              ║
╠══════════════════════════════════════════════════════════════════╣
║  Variables:                                                      ║
║    PV  — Present Value   (initial investment)                    ║
║    FV  — Future Value    (end balance)                           ║
║    N   — Number of Periods  (years × compounding freq)           ║
║    I   — Interest Rate per Period  (annual % ÷ periods/year)     ║
║    PMT — Payment per Period  (regular contribution)              ║
║                                                                  ║
║  Core Formula (Ordinary Annuity):                                ║
║    FV = PV·(1+i)^n  +  PMT·[ ((1+i)^n − 1) / i ]               ║
╚══════════════════════════════════════════════════════════════════╝
"""

import math

# ─────────────────────────────────────────────────────────────────
#  Optional plotting (gracefully disabled if matplotlib absent)
# ─────────────────────────────────────────────────────────────────
try:
    import matplotlib
    matplotlib.use("Agg")          # non-interactive backend (saves to file)
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    import numpy as np
    PLOTTING_AVAILABLE = True
except ImportError:
    PLOTTING_AVAILABLE = False

# ─────────────────────────────────────────────────────────────────
#  Constants
# ─────────────────────────────────────────────────────────────────

VARIABLES = {
    "FV":  "Future Value          (how much you'll have)",
    "PV":  "Present Value         (initial investment)",
    "N":   "Number of Periods     (total compounding periods)",
    "I":   "Interest Rate / Period(annual rate ÷ periods per year, as %)",
    "PMT": "Payment per Period    (regular contribution each period)",
}

DIVIDER     = "─" * 64
DBL_DIVIDER = "═" * 64

COMPOUNDING_OPTIONS = {
    "1":  ("Annually",      1),
    "2":  ("Semi-Annually", 2),
    "4":  ("Quarterly",     4),
    "12": ("Monthly",       12),
    "365":("Daily",         365),
}

# ─────────────────────────────────────────────────────────────────
#  Input Helpers
# ─────────────────────────────────────────────────────────────────

def get_float(prompt: str, allow_negative: bool = False, allow_zero: bool = True) -> float:
    while True:
        try:
            val = float(input(prompt).strip().replace(",", ""))
            if not allow_negative and val < 0:
                print("  ⚠  Value must be non-negative.\n")
                continue
            if not allow_zero and val == 0:
                print("  ⚠  Value cannot be zero.\n")
                continue
            return val
        except ValueError:
            print("  ⚠  Invalid input. Please enter a number.\n")


def get_positive_float(prompt: str) -> float:
    return get_float(prompt, allow_negative=False, allow_zero=False)


def get_choice(prompt: str, valid: list[str]) -> str:
    valid_lower = [v.lower() for v in valid]
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_lower:
            return choice
        print(f"  ⚠  Choose one of: {', '.join(valid)}\n")


# ─────────────────────────────────────────────────────────────────
#  TVM Solvers
# ─────────────────────────────────────────────────────────────────

def solve_fv(pv: float, n: float, i: float, pmt: float) -> float:
    """FV = PV·(1+i)^n + PMT·[((1+i)^n − 1) / i]"""
    if i == 0:
        return pv + pmt * n
    factor = (1 + i) ** n
    return pv * factor + pmt * ((factor - 1) / i)


def solve_pv(fv: float, n: float, i: float, pmt: float) -> float:
    """PV = [FV − PMT·(((1+i)^n − 1) / i)] / (1+i)^n"""
    if i == 0:
        return fv - pmt * n
    factor = (1 + i) ** n
    return (fv - pmt * ((factor - 1) / i)) / factor


def solve_pmt(fv: float, pv: float, n: float, i: float) -> float:
    """PMT = (FV − PV·(1+i)^n) · i / ((1+i)^n − 1)"""
    if i == 0:
        if n == 0:
            raise ValueError("N cannot be 0 when I = 0.")
        return (fv - pv) / n
    factor = (1 + i) ** n
    denom = factor - 1
    if denom == 0:
        raise ValueError("Cannot solve PMT: ((1+i)^n − 1) equals zero.")
    return (fv - pv * factor) * i / denom


def solve_n(fv: float, pv: float, i: float, pmt: float) -> float:
    """Solve for N numerically (Newton-Raphson)."""
    if i == 0:
        total = pmt
        if total == 0:
            raise ValueError("Cannot solve N when I = 0 and PMT = 0.")
        return (fv - pv) / total

    if pmt == 0:
        if pv == 0:
            raise ValueError("PV cannot be 0 when PMT = 0.")
        if fv / pv <= 0:
            raise ValueError("FV/PV must be positive to solve N.")
        return math.log(fv / pv) / math.log(1 + i)

    n = 10.0
    for _ in range(1000):
        fn  = pv * (1 + i) ** n + pmt * ((1 + i) ** n - 1) / i - fv
        dfn = pv * math.log(1 + i) * (1 + i) ** n + pmt * math.log(1 + i) * (1 + i) ** n / i
        if abs(dfn) < 1e-15:
            break
        n_new = n - fn / dfn
        if abs(n_new - n) < 1e-10:
            n = n_new
            break
        n = n_new
    if n <= 0:
        raise ValueError("No valid positive N found. Check your inputs.")
    return n


def solve_i(fv: float, pv: float, n: float, pmt: float) -> float:
    """Solve for I (rate per period) numerically (Newton-Raphson)."""
    if pmt == 0:
        if pv == 0:
            raise ValueError("PV cannot be 0 when PMT = 0.")
        if fv / pv <= 0:
            raise ValueError("FV/PV must be positive to solve I.")
        return (fv / pv) ** (1 / n) - 1

    i = 0.05 / 12
    for _ in range(2000):
        factor = (1 + i) ** n
        fi     = pv * factor + pmt * ((factor - 1) / i) - fv
        d_factor = n * (1 + i) ** (n - 1)
        dfi = (pv * d_factor
               + pmt * (d_factor * i - (factor - 1)) / (i ** 2))
        if abs(dfi) < 1e-20:
            break
        i_new = i - fi / dfi
        if i_new <= -1:
            i_new = i / 2
        if abs(i_new - i) < 1e-12:
            i = i_new
            break
        i = i_new
    if i <= -1:
        raise ValueError("No valid interest rate found. Check your inputs.")
    return i


# ─────────────────────────────────────────────────────────────────
#  Display Helpers
# ─────────────────────────────────────────────────────────────────

def fmt_currency(v: float) -> str:
    return f"${v:,.4f}"


def fmt_pct(v: float) -> str:
    return f"{v:.6f}%"


def print_header():
    print("\n" + DBL_DIVIDER)
    print("      💹  TVM — TIME VALUE OF MONEY CALCULATOR  💹")
    print(DBL_DIVIDER)


def print_variable_menu():
    print("\n  The 5 TVM variables are:\n")
    for key, desc in VARIABLES.items():
        print(f"    [{key:3}]  {desc}")


def print_known_values(known: dict, solve_for: str, n_per_year: int):
    print("\n" + DIVIDER)
    print("  📥  YOUR INPUTS")
    print(DIVIDER)
    labels = {
        "PV":  ("Present Value",    "currency"),
        "FV":  ("Future Value",     "currency"),
        "N":   ("Total Periods",    "periods"),
        "I":   ("Rate / Period",    "percent"),
        "PMT": ("Payment / Period", "currency"),
    }
    for var, (label, kind) in labels.items():
        if var == solve_for:
            continue
        val = known.get(var)
        if var == "I":
            annual = val * n_per_year * 100
            display = f"{val * 100:.6f}%  (= {annual:.4f}% per year)"
        elif var == "N":
            display = f"{val:,.4f} periods"
        else:
            display = fmt_currency(val)
        print(f"  {label:<26}  {display}")
    print(DIVIDER)


def print_result(solve_for: str, value: float, known: dict, n_per_year: int):
    labels = {
        "PV":  "Present Value",
        "FV":  "Future Value",
        "N":   "Number of Periods",
        "I":   "Interest Rate / Period",
        "PMT": "Payment per Period",
    }
    print(f"\n  {'✅  SOLVED':}")
    print(DIVIDER)
    label = labels[solve_for]
    if solve_for == "I":
        annual = value * n_per_year * 100
        print(f"  {label:<30}  {value * 100:.6f}%  per period")
        print(f"  {'Annual Rate (nominal)':<30}  {annual:.6f}%")
    elif solve_for == "N":
        years = value / n_per_year
        print(f"  {label:<30}  {value:,.4f}  periods")
        print(f"  {'Equivalent years':<30}  {years:,.4f}  years")
    else:
        print(f"  {label:<30}  {fmt_currency(value)}")

    pv  = known.get("PV",  value if solve_for == "PV"  else 0)
    fv  = known.get("FV",  value if solve_for == "FV"  else 0)
    n   = known.get("N",   value if solve_for == "N"   else 0)
    i   = known.get("I",   value if solve_for == "I"   else 0)
    pmt = known.get("PMT", value if solve_for == "PMT" else 0)

    total_contributed = pv + pmt * n
    total_interest    = fv - total_contributed
    roi = (fv / total_contributed - 1) * 100 if total_contributed > 0 else 0

    print(DIVIDER)
    print("  📊  SUMMARY")
    print(DIVIDER)
    print(f"  {'Total Amount Invested':<30}  {fmt_currency(total_contributed)}")
    print(f"  {'Total Interest Earned':<30}  {fmt_currency(total_interest)}")
    print(f"  {'Overall ROI':<30}  {roi:.4f}%")
    print(DIVIDER)


# ─────────────────────────────────────────────────────────────────
#  Plotting Module
# ─────────────────────────────────────────────────────────────────

# ── Shared style ──────────────────────────────────────────────────
PALETTE = {
    "principal":   "#2563EB",   # blue
    "interest":    "#16A34A",   # green
    "fv":          "#7C3AED",   # purple
    "pmt":         "#EA580C",   # orange
    "grid":        "#E5E7EB",   # light grey
    "accent":      "#F59E0B",   # amber
    "bg":          "#FAFAFA",
    "text":        "#1F2937",
}

def _apply_style(ax, title: str, xlabel: str, ylabel: str):
    """Apply consistent professional styling to an axes object."""
    ax.set_facecolor(PALETTE["bg"])
    ax.set_title(title, fontsize=13, fontweight="bold", color=PALETTE["text"], pad=12)
    ax.set_xlabel(xlabel, fontsize=10, color=PALETTE["text"])
    ax.set_ylabel(ylabel, fontsize=10, color=PALETTE["text"])
    ax.tick_params(colors=PALETTE["text"], labelsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    for spine in ax.spines.values():
        spine.set_edgecolor("#D1D5DB")
    ax.grid(axis="y", color=PALETTE["grid"], linewidth=0.8, linestyle="--")
    ax.set_axisbelow(True)


def _build_growth_series(pv, n, i, pmt):
    """Return (periods, principal_list, interest_list, balance_list)."""
    periods = list(range(0, int(n) + 1))
    principal_list, interest_list, balance_list = [], [], []
    for t in periods:
        bal   = solve_fv(pv, t, i, pmt)
        princ = pv + pmt * t
        intr  = bal - princ
        principal_list.append(princ)
        interest_list.append(intr)
        balance_list.append(bal)
    return periods, principal_list, interest_list, balance_list


# ── Plot 1: Investment Growth Curve ──────────────────────────────
def plot_growth_curve(ax, pv, n, i, pmt, n_per_year):
    periods, principal_list, interest_list, balance_list = _build_growth_series(pv, n, i, pmt)
    years = [t / n_per_year for t in periods]

    ax.stackplot(years, principal_list, interest_list,
                 labels=["Principal + Contributions", "Interest Earned"],
                 colors=[PALETTE["principal"], PALETTE["interest"]], alpha=0.85)
    ax.plot(years, balance_list, color=PALETTE["fv"], linewidth=2.2,
            linestyle="--", label="Total Balance", zorder=5)

    _apply_style(ax, "Investment Growth Over Time",
                 "Time (years)", "Portfolio Value ($)")
    ax.legend(fontsize=8, loc="upper left", framealpha=0.9)


# ── Plot 2: Breakdown Pie Chart ───────────────────────────────────
def plot_pie_breakdown(ax, pv, n, i, pmt):
    fv            = solve_fv(pv, n, i, pmt)
    total_contrib = pv + pmt * n
    interest      = fv - total_contrib

    if pmt > 0:
        sizes  = [pv, pmt * n, max(interest, 0)]
        labels = ["Initial Investment", "Total Contributions", "Interest Earned"]
        colors = [PALETTE["principal"], PALETTE["accent"], PALETTE["interest"]]
    else:
        sizes  = [pv, max(interest, 0)]
        labels = ["Initial Investment", "Interest Earned"]
        colors = [PALETTE["principal"], PALETTE["interest"]]

    sizes  = [s for s in sizes  if s > 0]
    labels = [l for l, s in zip(labels, [pv, pmt * n if pmt > 0 else 0, max(interest, 0)]) if s > 0]
    colors = colors[:len(sizes)]

    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors,
        autopct="%1.1f%%", startangle=140,
        wedgeprops=dict(edgecolor="white", linewidth=1.5),
        textprops=dict(color=PALETTE["text"], fontsize=9),
    )
    for at in autotexts:
        at.set_fontsize(9)
    ax.set_title("Final Value Composition", fontsize=13, fontweight="bold",
                 color=PALETTE["text"], pad=12)


# ── Plot 3: Amortization Schedule (PMT solve) ────────────────────
def plot_amortization(ax, pv, n, i):
    """Bar chart of per-period principal vs. interest payment for a loan."""
    periods = list(range(1, int(n) + 1))
    pmt     = solve_pmt(0, pv, n, i)   # FV = 0 (loan paid off)
    balance = pv
    princ_parts, int_parts = [], []

    for _ in periods:
        interest_payment   = balance * i
        principal_payment  = pmt - interest_payment
        balance           -= principal_payment
        int_parts.append(interest_payment)
        princ_parts.append(principal_payment)

    # Downsample if too many periods
    MAX_BARS = 60
    if len(periods) > MAX_BARS:
        step = len(periods) // MAX_BARS
        periods     = periods[::step]
        princ_parts = princ_parts[::step]
        int_parts   = int_parts[::step]

    ax.bar(periods, int_parts, label="Interest",  color=PALETTE["interest"],  alpha=0.85)
    ax.bar(periods, princ_parts, bottom=int_parts,
           label="Principal", color=PALETTE["principal"], alpha=0.85)

    _apply_style(ax, "Amortization Schedule", "Period", "Payment ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.legend(fontsize=8, framealpha=0.9)


# ── Plot 4: FV Sensitivity to Interest Rate ──────────────────────
def plot_rate_sensitivity(ax, pv, n, i, pmt, n_per_year):
    base_annual_pct = i * n_per_year * 100
    rates_annual    = np.linspace(max(0.1, base_annual_pct * 0.3),
                                  base_annual_pct * 2.0, 200)
    fv_values = [solve_fv(pv, n, r / 100 / n_per_year, pmt) for r in rates_annual]

    ax.plot(rates_annual, fv_values, color=PALETTE["fv"], linewidth=2.2)
    ax.axvline(base_annual_pct, color=PALETTE["pmt"], linewidth=1.5,
               linestyle="--", label=f"Your rate: {base_annual_pct:.2f}%")
    current_fv = solve_fv(pv, n, i, pmt)
    ax.scatter([base_annual_pct], [current_fv],
               color=PALETTE["pmt"], s=60, zorder=6)

    _apply_style(ax, "Future Value vs. Annual Interest Rate",
                 "Annual Rate (%)", "Future Value ($)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.1f}%"))
    ax.legend(fontsize=8, framealpha=0.9)


# ── Plot 5: Compounding Frequency Comparison ─────────────────────
def plot_compounding_comparison(ax, pv, n_years, annual_rate_pct, pmt_annual):
    freq_options = [
        ("Annually",      1),
        ("Semi-Annually", 2),
        ("Quarterly",     4),
        ("Monthly",       12),
        ("Daily",         365),
    ]
    colors = ["#1D4ED8", "#2563EB", "#3B82F6", "#60A5FA", "#93C5FD"]
    years  = np.linspace(0, n_years, 200)

    for (label, freq), color in zip(freq_options, colors):
        i_period   = (annual_rate_pct / 100) / freq
        pmt_period = pmt_annual / freq
        fv_vals    = [solve_fv(pv, t * freq, i_period, pmt_period) for t in years]
        ax.plot(years, fv_vals, label=label, color=color, linewidth=2)

    _apply_style(ax, "Effect of Compounding Frequency",
                 "Years", "Future Value ($)")
    ax.legend(fontsize=8, framealpha=0.9, loc="upper left")


# ── Plot 6: Loan Balance Remaining Over Time ─────────────────────
def plot_loan_balance(ax, pv, n, i):
    pmt     = solve_pmt(0, pv, n, i)
    balance = pv
    periods = [0]
    balances = [pv]

    for t in range(1, int(n) + 1):
        balance -= (pmt - balance * i)
        periods.append(t)
        balances.append(max(balance, 0))

    ax.fill_between(periods, balances, alpha=0.25, color=PALETTE["principal"])
    ax.plot(periods, balances, color=PALETTE["principal"], linewidth=2.2)
    ax.axhline(0, color="#9CA3AF", linewidth=0.8, linestyle="--")

    _apply_style(ax, "Loan Balance Remaining Over Time",
                 "Period", "Outstanding Balance ($)")


# ── Master plot dispatcher ────────────────────────────────────────
def generate_plots(solve_for: str, result: float, known: dict, n_per_year: int):
    """
    Select and render the most relevant charts for the solved variable,
    then save to tvm_charts.png.
    """
    if not PLOTTING_AVAILABLE:
        print("\n  ⚠  matplotlib / numpy not installed — skipping charts.")
        print("      Run:  pip install matplotlib numpy")
        return

    pv  = known.get("PV",  result if solve_for == "PV"  else 0)
    fv  = known.get("FV",  result if solve_for == "FV"  else 0)
    n   = known.get("N",   result if solve_for == "N"   else 0)
    i   = known.get("I",   result if solve_for == "I"   else 0)
    pmt = known.get("PMT", result if solve_for == "PMT" else 0)

    # Guard: need at least some periods and a non-zero rate
    if n <= 0:
        print("\n  ⚠  N = 0: not enough data to plot.")
        return

    fig = plt.figure(figsize=(16, 10), facecolor="white")
    fig.suptitle("TVM Analysis — Professional Charts",
                 fontsize=16, fontweight="bold", color=PALETTE["text"], y=0.98)

    # ── Layout: 2 rows × 3 cols ──────────────────────────────────
    axes = fig.subplots(2, 3)

    annual_rate_pct = i * n_per_year * 100
    n_years         = n / n_per_year
    pmt_annual      = pmt * n_per_year

    # ── Row 1 ─────────────────────────────────────────────────────

    # Chart 1 — always shown: growth curve
    plot_growth_curve(axes[0, 0], pv, n, i, pmt, n_per_year)

    # Chart 2 — always shown: pie breakdown
    plot_pie_breakdown(axes[0, 1], pv, n, i, pmt)

    # Chart 3 — rate sensitivity (always useful)
    if i > 0:
        plot_rate_sensitivity(axes[0, 2], pv, n, i, pmt, n_per_year)
    else:
        axes[0, 2].set_visible(False)

    # ── Row 2 ─────────────────────────────────────────────────────

    # Chart 4 — compounding frequency comparison
    if i > 0 and n_years >= 1:
        plot_compounding_comparison(axes[1, 0], pv, n_years, annual_rate_pct, pmt_annual)
    else:
        axes[1, 0].set_visible(False)

    # Chart 5 — amortization / loan balance (if PMT solve or pv > 0 and i > 0)
    if solve_for in ("PMT", "I", "N") and pv > 0 and i > 0 and n >= 2:
        plot_amortization(axes[1, 1], pv, n, i)
        plot_loan_balance(axes[1, 2], pv, n, i)
    else:
        # Generic: show cumulative interest earned over time
        periods, _, interest_list, _ = _build_growth_series(pv, n, i, pmt)
        years = [t / n_per_year for t in periods]
        axes[1, 1].plot(years, interest_list, color=PALETTE["interest"], linewidth=2.2)
        _apply_style(axes[1, 1], "Cumulative Interest Earned Over Time",
                     "Years", "Interest ($)")

        # Balance across different PMT values
        if pmt > 0:
            for mult, alpha in [(0.5, 0.5), (1.0, 1.0), (1.5, 0.7), (2.0, 0.5)]:
                fv_series = [solve_fv(pv, t, i, pmt * mult) for t in range(0, int(n) + 1)]
                yrs       = [t / n_per_year for t in range(0, int(n) + 1)]
                axes[1, 2].plot(yrs, fv_series, alpha=alpha,
                                label=f"PMT × {mult:.1f}", linewidth=2)
            _apply_style(axes[1, 2], "FV Sensitivity to PMT Variation",
                         "Years", "Future Value ($)")
            axes[1, 2].legend(fontsize=8, framealpha=0.9)
        else:
            axes[1, 2].set_visible(False)

    plt.tight_layout(rect=[0, 0, 1, 0.96])

    outfile = "tvm_charts.png"
    plt.savefig(outfile, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\n  📈  Charts saved to → {outfile}")


# ─────────────────────────────────────────────────────────────────
#  Compounding Frequency Helper
# ─────────────────────────────────────────────────────────────────

def ask_compounding_freq() -> int:
    print("\n  Compounding / Payment Frequency:")
    for key, (label, _) in COMPOUNDING_OPTIONS.items():
        print(f"    [{key:>3}]  {label}")
    while True:
        choice = input("  Enter periods per year: ").strip()
        if choice in COMPOUNDING_OPTIONS:
            label, n = COMPOUNDING_OPTIONS[choice]
            print(f"  → {label} selected  ({n} period(s) per year)")
            return n
        print(f"  ⚠  Choose from: {', '.join(COMPOUNDING_OPTIONS.keys())}\n")


# ─────────────────────────────────────────────────────────────────
#  Main Calculator Flow
# ─────────────────────────────────────────────────────────────────

def collect_known_values(solve_for: str, n_per_year: int) -> dict:
    known: dict = {}

    prompts = {
        "PV":  ("  PV  — Present Value ($): ",           False),
        "FV":  ("  FV  — Future Value  ($): ",           False),
        "PMT": ("  PMT — Payment per Period ($, 0 if none): ", False),
    }

    print(f"\n  Enter values for the 4 known variables (solving for {solve_for}):\n")

    for var in ["PV", "FV", "N", "I", "PMT"]:
        if var == solve_for:
            continue

        if var == "N":
            print(f"  N can be entered as total periods OR as years.\n"
                  f"  (If you enter years, multiply by {n_per_year} periods/year = total periods)")
            mode = get_choice("  Enter N as [periods] or [years]? ", ["periods", "years"])
            raw  = get_positive_float("  N value: ")
            known["N"] = raw if mode == "periods" else raw * n_per_year

        elif var == "I":
            print(f"  I — Enter the ANNUAL interest rate (%).")
            annual_pct = get_float("  Annual Interest Rate (%): ", allow_negative=False, allow_zero=True)
            known["I"] = (annual_pct / 100) / n_per_year

        elif var in prompts:
            prompt, _ = prompts[var]
            known[var] = get_float(prompt, allow_negative=False, allow_zero=True)

    return known


def run_calculator():
    print_header()
    print_variable_menu()

    print(f"\n  Which variable do you want to SOLVE FOR?")
    print(f"  Options: {' | '.join(VARIABLES.keys())}")
    solve_for = get_choice("  Solve for: ", list(VARIABLES.keys())).upper()

    n_per_year = ask_compounding_freq()
    known = collect_known_values(solve_for, n_per_year)
    print_known_values(known, solve_for, n_per_year)

    try:
        pv  = known.get("PV",  0.0)
        fv  = known.get("FV",  0.0)
        n   = known.get("N",   0.0)
        i   = known.get("I",   0.0)
        pmt = known.get("PMT", 0.0)

        if solve_for == "FV":
            result = solve_fv(pv, n, i, pmt)
        elif solve_for == "PV":
            result = solve_pv(fv, n, i, pmt)
        elif solve_for == "PMT":
            result = solve_pmt(fv, pv, n, i)
        elif solve_for == "N":
            result = solve_n(fv, pv, i, pmt)
        elif solve_for == "I":
            result = solve_i(fv, pv, n, pmt)
        else:
            raise ValueError(f"Unknown variable: {solve_for}")

        print_result(solve_for, result, known, n_per_year)

        # ── Offer to generate charts ───────────────────────────────
        if PLOTTING_AVAILABLE:
            print()
            plot_choice = get_choice("  📈  Generate professional charts? (yes / no): ",
                                     ["yes", "no"])
            if plot_choice == "yes":
                generate_plots(solve_for, result, known, n_per_year)
        else:
            print("\n  ℹ  Install matplotlib & numpy for chart generation:")
            print("      pip install matplotlib numpy")

    except (ValueError, ZeroDivisionError, OverflowError) as exc:
        print(f"\n  ❌  Could not solve: {exc}")
        print("      Please check your inputs and try again.\n")


# ─────────────────────────────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────────────────────────────

def main():
    while True:
        run_calculator()
        print()
        again = get_choice("  Run another calculation? (yes / no): ", ["yes", "no"])
        if again == "no":
            print("\n  Thank you for using the TVM Calculator. Goodbye! 👋\n")
            break


if __name__ == "__main__":
    main()
