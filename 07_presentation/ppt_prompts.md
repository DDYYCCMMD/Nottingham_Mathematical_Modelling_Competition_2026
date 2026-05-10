# PPT 生成提示词
## 适用于 Gamma / Beautiful.ai / Canva AI / MindShow / 或 ChatGPT + DALL·E

---

## 方式A：一键生成完整PPT（推荐用 Gamma.app 或 MindShow）

将以下提示词粘贴到 Gamma.app 的"Generate Deck"输入框：

```
Create a professional academic presentation with 9 slides for a mathematical modelling competition.

Title: "Modelling Antimicrobial Resistance Dynamics in a Hospital Network"
Subtitle: Nottingham Mathematical Modelling Competition 2026
Theme: Clean white academic style, blue and teal accent colors, minimal text per slide

Slide 1 – Title Slide
Title: Modelling Antimicrobial Resistance Dynamics in a Hospital Network
Subtitle: A Coupled SIS+HCW Compartmental Model
Visual: Simple network diagram showing 4 hospital wards (GM, GS, ICU, GW) connected by patient transfer arrows

Slide 2 – Problem & Motivation
Title: Why Hospital AMR Matters
Content: 4-column table showing ward name, beds, average stay (days), antibiotic use (%)
General Medicine: 60 beds, 5 days, 40%
General Surgery: 40 beds, 7 days, 60%
ICU: 15 beds, 12 days, 80%
Geriatric Ward: 30 beds, 14 days, 50%
Key message callout box: "Patient transfers couple the wards — ICU drives the whole network"

Slide 3 – Model Structure
Title: SIS + HCW Compartmental Model
Visual: Flow diagram with boxes S_i (green) → C_i (red) → S_i (green), with HCW contamination loop H_i (orange)
Two ODE equations displayed:
dC_i/dt = β_i(C_i/N_i)S_i + λ_i H_i S_i + α_i μ_i N_i − (γ_i+μ_i)C_i ± transfers
dH_i/dt = η_i(C_i/N_i)(1−H_i) − δ_i H_i
Three justification bullets: "SIS not SIR: no immunity from colonisation" | "HCW compartment: 21-29% of ICU transmission via HCW hands" | "Antibiotic pressure modulates β and γ per ward"

Slide 4 – R₀ Analysis
Title: Basic Reproduction Number R₀ = 0.96
Large centered number: R₀ = 0.96
Formula box: R₀ = ρ(F·V⁻¹) where ρ = spectral radius
Two key insights:
"R₀ < 1 → in-hospital transmission alone cannot sustain AMR"
"Endemic persistence is driven by admission colonisation forcing (α·μ·N) — eliminating this is the necessary condition for eradication (Scenario B)"

Slide 5 – Baseline Simulation
Title: 12-Month Colonisation Dynamics
Insert image placeholder labeled "Figure 1: baseline.png"
Results table:
Ward | Day-365 Prevalence
GM | 5.1%
GS | 6.0%
ICU | 15.6%
GW | 9.3%
Key finding: "ICU 15.6% — consistent with Bootsma et al. literature range 15–26%"

Slide 6 – Intervention Results
Title: Which Intervention Works Best?
Insert image placeholder labeled "Figure 2: interventions.png"
Comparison table 5 rows:
Scenario | R₀ | System Prevalence
Baseline | 0.96 | 7.3%
A: Hand Hygiene 80% | 0.95 | 7.2%
B: Admission Screening | 0.70 | 1.0% ← HIGHLIGHT THIS ROW in green
C: Antibiotic Stewardship | 0.90 | 6.4%
D: Combined A+C | 0.88 | 6.3%
Callout: "Scenario B: 86% prevalence reduction — eliminates the admission colonisation forcing term"

Slide 7 – Sensitivity Analysis
Title: R₀ vs Prevalence — Different Drivers
Insert image placeholder labeled "Figure 3: sensitivity.png"
Two-column comparison:
Left: "Strongest drivers of R₀" → β (+0.99), γ (−0.97), δ hand hygiene (−0.49)
Right: "Strongest drivers of Prevalence" → β (+0.95), α admission rate (+0.92), γ (−0.88)
Key insight box: "α has PRCC ≈ 0 for R₀ but +0.92 for prevalence; β dominates both → Scenario B targets the two top prevalence drivers simultaneously"

Slide 8 – Critical Evaluation
Title: Honest Model Assessment
Three limitation cards side by side:
Card 1: Homogeneous Mixing — "Real transmission is spatially structured by bed proximity and nursing teams"
Card 2: Stochastic Extinction — "ICU has only 15 beds — deterministic ODE cannot model random fade-out"
Card 3: Static Parameters — "Real compliance improvements decay over time without reinforcement"
Bottom banner: "Scope: steady-state endemic planning tool — NOT for acute outbreak prediction"

Slide 9 – Conclusion & Recommendation
Title: Recommendation to the Hospital Board
Three action items with priority labels:
🔴 IMMEDIATE: Universal admission screening + contact precautions → reduces system prevalence 7.3% → 1.0%
🟡 MEDIUM-TERM: Antibiotic stewardship programme → reduces ICU prevalence by 21%
🟢 SUSTAINED: Maintain 80% hand hygiene compliance → keeps R₀ low, reduces outbreak amplification risk
Key takeaway box: "R₀ and endemic prevalence have different sensitivity profiles — optimise for the right target"
```

---

## 方式B：逐张幻灯片生成（用于 Canva AI 或 PowerPoint Designer）

### 幻灯片1 — 标题页
```
Design a title slide for an academic mathematical modelling presentation.
Title text: "Modelling Antimicrobial Resistance Dynamics in a Hospital Network"
Subtitle: "Nottingham Mathematical Modelling Competition 2026 | A Coupled SIS+HCW Model"
Visual element: a clean network diagram of 4 colored hospital ward boxes (blue=GM, orange=GS, red=ICU, green=GW) connected by directional arrows labeled with transfer percentages (5%, 10%). White background, professional academic style, no decorative elements.
Color scheme: navy blue #1B3A6B, teal #2A9D8F, white background.
```

### 幻灯片2 — 问题背景
```
Design an information slide for a mathematical biology presentation.
Title: "A Four-Ward Hospital Network with Coupled AMR Dynamics"
Main visual: a clean 4-row data table with headers: Ward | Beds | Avg Stay | Antibiotic Use
Data rows: General Medicine 60 5d 40% | General Surgery 40 7d 60% | ICU 15 12d 80% | Geriatric Ward 30 14d 50%
Highlight the ICU row in light red to indicate highest risk.
Right side: a small network connectivity diagram showing patient transfer arrows between wards.
Style: clean white slide, minimal text, academic blue color theme.
```

### 幻灯片3 — 模型结构
```
Design a scientific diagram slide for a mathematical modelling presentation.
Title: "The SIS + HCW Compartmental Model"
Main visual: a compartment flow diagram with:
- Green rounded rectangle labeled "S_i (Susceptible patients)"
- Red rounded rectangle labeled "C_i (Colonised patients)"
- Bidirectional arrows between them labeled with ODE terms
- Orange hexagon labeled "H_i (HCW contamination)" connected to both patient compartments
- Blue arrows showing inter-ward patient transfers between 4 copies of this diagram
Below the diagram: two mathematical equations in a grey box (LaTeX-style typography):
dC_i/dt equation and dH_i/dt equation
Style: white background, color-coded compartments, clean sans-serif font.
```

### 幻灯片4 — R₀
```
Design a results announcement slide for a mathematical presentation.
Title: "Basic Reproduction Number"
Center: a very large bold number "R₀ = 0.96" in navy blue, font size equivalent to 120pt
Below it: the formula "R₀ = ρ(F · V⁻¹)" in a light grey formula box
Two insight bullet points:
• "R₀ < 1 → in-hospital transmission alone cannot sustain AMR"  
• "Endemic persistence driven by admission colonisation forcing (α·μ·N) — Scenario B eliminates this"
Visual accent: a subtle threshold line graphic showing 1.0, with R₀ = 0.96 marked below it.
Style: minimalist white slide, single focal point on the number, academic typography.
```

### 幻灯片5 — 基线结果
```
Design a results slide for a scientific presentation with a figure and data table.
Title: "Baseline 12-Month Colonisation Dynamics"
Left half: image placeholder box labeled "[Figure 1: 4-panel ward prevalence trajectories]" with a light grey border
Right half: a small results table:
Ward | Prevalence at Day 365
General Medicine | 5.1%
General Surgery | 6.0%
ICU | 15.6% ← bold
Geriatric Ward | 9.3%
Below table: a green checkmark callout "ICU 15.6% ✓ consistent with literature (15–26%)"
Style: split layout, clean academic design, data-first presentation.
```

### 幻灯片6 — 干预结果
```
Design a comparison results slide for a scientific presentation.
Title: "Intervention Scenario Comparison"
Top half: image placeholder box labeled "[Figure 2: 5-scenario colonisation comparison]"
Bottom half: a 5-row comparison table:
Scenario | R₀ | System Prevalence
Baseline | 0.96 | 7.3%
A: Hand Hygiene | 0.95 | 7.2%
B: Admission Screening | 0.70 | 1.0% ← highlight this row with green background
C: Antibiotic Stewardship | 0.90 | 6.4%
D: Combined A+C | 0.88 | 6.3%
Right side callout box in green: "Scenario B: 86% prevalence reduction"
Style: data-focused, clear visual hierarchy, highlight the key finding.
```

### 幻灯片7 — 敏感性分析
```
Design a sensitivity analysis results slide for a mathematical biology presentation.
Title: "R₀ and Prevalence Have Different Drivers"
Left panel: vertical bar chart or list showing PRCC vs R₀:
β transmission: +0.99 (dark green bar)
γ decolonisation: -0.97 (dark red bar)
δ hand hygiene: -0.49 (medium red bar)
α admission: -0.03 (barely visible, grey)
Right panel: vertical bar chart showing PRCC vs 12-month prevalence:
β transmission: +0.95 (green)
α admission: +0.92 (dark green — prominent)
γ decolonisation: -0.88 (red)
δ hand hygiene: -0.14 (light red — small)
Center callout box: "Key asymmetry: α negligible for R₀ but +0.92 for prevalence → β and α jointly dominate"
Style: two symmetric panels, PRCC scale -1 to +1, color-coded bars.
```

### 幻灯片8 — 批判性评估
```
Design a limitations slide for a scientific presentation using a 3-card layout.
Title: "Critical Evaluation — Model Limitations"
Three equal-width cards side by side:
Card 1 (blue border): 
Icon: network/graph symbol
Title: "Homogeneous Mixing"
Text: "Real transmission structured by bed proximity and nursing teams — cohorting unmodellable"

Card 2 (orange border):
Icon: dice/probability symbol  
Title: "Stochastic Extinction"
Text: "ICU has only 15 beds — deterministic ODE cannot represent random fade-out when R₀ ≈ 1"

Card 3 (grey border):
Icon: clock/decay symbol
Title: "Static Parameters"  
Text: "Compliance improvements decay; winter surge increases β — unmodelled dynamics"

Bottom full-width banner (light yellow background):
"⚠ Scope: steady-state endemic planning tool — NOT for acute outbreak prediction"
Style: clean card layout, icon-driven, honest self-assessment tone.
```

### 幻灯片9 — 结论
```
Design a conclusion and recommendation slide for a policy-oriented scientific presentation.
Title: "Recommendation to the Hospital Board"
Three stacked action items with priority color coding:
🔴 IMMEDIATE PRIORITY (red left border):
"Universal admission screening + contact precautions"
"Result: system prevalence 7.3% → 1.0% (86% reduction)"

🟡 MEDIUM-TERM (amber left border):
"Antibiotic stewardship programme (−30% unnecessary use)"
"Result: ICU prevalence 15.6% → 12.3%"

🟢 SUSTAINED BASELINE (green left border):
"Maintain 80% hand hygiene compliance"
"Result: R₀ 0.96 → 0.95, maintains low transmission baseline"

Bottom takeaway box (navy background, white text):
"R₀ and endemic prevalence require different interventions — target both metrics"
Style: priority-coded action items, policy brief aesthetic, clear visual hierarchy.
```

---

## 方式C：图片生成提示词（用于每张幻灯片的配图，适用DALL·E / Midjourney）

### 封面配图
```
Minimalist scientific illustration of a hospital network: four colored rectangular nodes labeled GM, GS, ICU, GW connected by directional arrows. Clean white background, navy blue and teal color scheme, no text in image. Professional academic diagram style, vector art aesthetic.
```

### 模型结构配图
```
Scientific compartment flow diagram: three shapes connected by arrows. Left green rectangle labeled S (susceptible), right red rectangle labeled C (colonised), top orange circle labeled H (HCW). Curved arrows form a cycle. Additional small blue arrows on the right represent inter-ward transfers. Clean white background, academic vector illustration style, no photographic elements.
```

### 干预结果配图（如果无法插入真实图表）
```
Five overlapping line charts on a single panel. Lines in different colors: black (baseline), blue (solid), orange (dashed), green (dash-dot), red (solid thick). Y-axis labeled "Colonisation Prevalence 0-40%", X-axis labeled "Days 0-365". Grey horizontal dashed reference line at 5%. Clean white background, academic data visualization style.
```
