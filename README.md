# U.S. Income Inequality Visualization Suite

A 6-chart Python data visualization suite exploring systemic income inequality
across race, gender, and wealth distribution using U.S. Census Bureau data
spanning 1963–2023.

---

## Project Overview

This project visualizes income inequality across three primary dimensions:
- **Gender** — wage gap trends and workforce participation over time
- **Race** — income bracket distribution and high/low earner trends by racial group
- **Wealth Distribution** — Gini, Atkinson, percentile ratios, and quintile metrics

Data sourced from the U.S. Census Bureau:
https://www.census.gov/data/tables/2024/demo/income-poverty/p60-282.html

---

## Scripts

| File | Description |
|------|-------------|
| `wageGapOverTime.py` | Bar chart of female-to-male earnings ratio over time with a 1:1 equality baseline |
| `genderedWorkforceStats.py` | Bubble chart encoding median earnings, workforce size, and M/F discrepancy simultaneously |
| `racialIncomeBracketDisparityHeatmap.py` | Heatmap of average income bracket distribution by race, ordered by mean income |
| `racialBracketsOverTime.py` | 4-panel line chart with interactive brushing and cross-subplot highlight by race |
| `percentileInequitiesMapped.py` | Dual panel: income quintiles over time + 90th/50th/10th percentile CPI-adjusted ratios |
| `incomeInequalityMetrics.py` | Gini index, Mean Log Deviation, and Atkinson measures charted over time |

---

## Setup & Dependencies

Install required packages:

```bash
pip install pandas matplotlib seaborn numpy
```

All scripts use only these four libraries plus Python's standard `textwrap` module.

---

## Data Wrangling

The raw Census files required significant cleaning before visualization was possible:

- **Type coercion** — most numeric columns were stored as strings; commas stripped,
  `'N'` placeholders replaced with `NaN`, and values cast to `float` throughout
- **Schema pruning** — Census tables ship with multi-row headers, footnote rows,
  subgroup categories, and mixed sources; irrelevant rows and columns were dropped
  before any analysis
- **Inconsistent formatting** — column names contained embedded newlines and
  irregular spacing, requiring careful exact-match selection
- **File format** — raw Excel exports were re-saved as clean CSVs to resolve
  pandas/matplotlib read compatibility issues
- **Deduplication & filtering** — race subcategories (e.g. "in combination" groups)
  and `"All Races"` aggregate rows were explicitly excluded to avoid double-counting

---

## Data Location

Place the following CSV files in a `Formatted/` directory one level above the
scripts (i.e. `../Formatted/`), or update the `file_path` variable at the top
of each script to an absolute path on your machine:

| File | Used By |
|------|---------|
| `tableA2.csv` | `racialIncomeBracketDisparityHeatmap.py`, `racialBracketsOverTime.py` |
| `tableA5(form)2.csv` | `incomeInequalityMetrics.py`, `percentileInequitiesMapped.py` |
| `tableA7.csv` | `wageGapOverTime.py`, `genderedWorkforceStats.py` |

Each script also contains a commented-out absolute path at the top for
reference — swap that in if relative paths aren't resolving.

---

## Interactivity

All charts include hover tooltips showing exact values at each data point.
`racialBracketsOverTime.py` additionally supports:
- **Hover** — temporarily highlights the hovered line and dims others
- **Click** — locks a line (or set of lines) as persistently highlighted
- **Click background** — resets all highlights

---

## Key Findings

- The gender pay gap has narrowed consistently since the 1960s but has not closed
- Racial income inequality has contracted at low income brackets but stagnated at high ones
- Wealth inequality by every metric — Gini, Atkinson, percentile ratios — is rising
- Growth is concentrated at the top: the 90th percentile has accelerated far beyond the 10th

---

## Author

Caden Eckman
Data sourced from the U.S. Census Bureau Current Population Survey (CPS)
[Income in the United States: 2023](https://www.census.gov/data/tables/2024/demo/income-poverty/p60-282.html)
