# UAS Avionics Enclosure — Requirements, Environments & Analysis Report

| Field | Value |
|---|---|
| Project | Virtual environmental qualification of a machined avionics enclosure |
| Platform | 7 in class long-range multirotor UAS, 6S LiPo |
| Material | 6061-T6 aluminium, CNC machined |
| Author | Akshar Patel |
| Revision | **C — modal results incorporated** |

---

## 1. Scope

This document defines the design requirements and environmental load cases for an avionics enclosure
housing the flight control, propulsion control, and communications stack of a 7 in class multirotor UAS.

Verification is by analysis only. No physical test article is produced. All requirements trace to either
a manufacturer-published limit, a published military standard, or a platform-derived excitation condition.

**In scope:** structural dynamics (modal, random vibration), thermal (conduction, free and forced
convection), mass, and envelope.

**Out of scope:** shock, EMI/EMC, ingress protection, altitude, humidity, and any form of physical test
verification.

---

## 2. Component Stack

Baseline selected via weighted trade study (`trade_study.xlsx`, Rev A).

| ID | Component | Part | Mass (g) | Footprint (mm) | Height (mm) | Diss. (W) | Location |
|---|---|---|---|---|---|---|---|
| C1 | Flight controller | Matek H743-SLIM | 7.0 | 36 x 36 | 5.0 | 2.00 (A1) | Internal |
| C2 | 4-in-1 ESC | Holybro Tekko32 F4 65A | 15.8 | 46 x 44 | 6.0 | 0.90 (A2) | Internal |
| C3 | Video transmitter | RushFPV Tank Ultimate | 12.0 | 37 x 24 | 6.7 | 7.90 | Internal |
| C4 | GPS / compass | Matek M10Q-5883 | 8.0 | 20 x 20 | 12.4 | 0.07 | External |
| C5 | RC receiver | Happymodel EP2 ELRS | 0.4 | 10 x 10 | 6.0 | 0.20 | External |
| C6 | Bulk capacitor | 35PK1000MEFCT810X20 | 2.75 | dia 11.25 | 25.0 | negligible | Internal |

C4 and C5 are mounted externally. An aluminium enclosure forms a Faraday cage; the M10Q-5883 uses an
internal patch antenna and the EP2 an integrated SMD ceramic antenna. Neither would acquire signal if
enclosed.

**Internal heat load (C1 + C2 + C3): 10.80 W. Binding internal component allowable: 90 degC (C3).**

### 2.1 Temperature limits

| ID | Max ambient (degC) | Max component (degC) | Notes |
|---|---|---|---|
| C1 | 40 | ~100 | Ambient limit binds inside a sealed enclosure |
| C2 | [TBD] | 150 (MOSFET) | Device rating, not a board rating |
| C3 | [TBD] | 90 | Binding internal allowable |
| C4 | [TBD] | 80 | External — excluded from internal thermal model |
| C5 | [TBD] | 80 | External — excluded from internal thermal model |
| C6 | [TBD] | 105 typical | Verify. Lifetime halves per ~10 degC above rating |

### 2.2 Interface notes

- C1 and C2 share a 30.5 x 30.5 mm mounting pattern. C2 is the larger outline and sets the minimum
  internal footprint.
- C2 has no output BEC. All 5 V loads are supplied by C1 onboard regulation; conversion losses dissipate
  on C1.
- C3 runs from VBAT, not the 5 V rail. Confirm before finalising the power budget.
- C6 is required for 6S operation and is packaged upright inside the enclosure.

---

## 3. Environments

### 3.1 Vibration — MIL-STD-810H Method 514.8

Profile selected: [ANNEX / TABLE / FIGURE]. Rationale: [WHY THIS PROFILE FITS A SMALL MULTIROTOR].
Overall level [TBD] g_rms, duration [TBD] per axis, 3 axes sequentially.

### 3.2 Platform excitation — prop passing frequency

`f_pp = (RPM / 60) x N_blades`

| Parameter | Value |
|---|---|
| Motor | T-Motor F90 2806.5, 1500 KV |
| Propeller | 7 in, 2 blades |
| RPM range | 2,600 (idle) to 17,200 (max) |
| Source | Manufacturer thrust table |

| Harmonic | Freq at idle (Hz) | Freq at max (Hz) |
|---|---|---|
| 1x | 87 | 573 |
| 2x | 173 | 1,147 |
| 3x | 260 | 1,720 |
| 4x | 347 | 2,293 |

**Excitation band to avoid: 87 to 2,293 Hz.**

Separation factor: 1.5x applied to the highest harmonic of concern (4x at maximum RPM), giving a
REQ-STR-001 target of 3,440 Hz. 1.5x is a common preliminary-design rule for avionics mounting structure.
A 2.0x factor would raise the target to 4,587 Hz and the design would not close; this is noted as a
sensitivity rather than a failure, because the bonded-contact assumption (A6) already over-predicts
stiffness.

### 3.3 Thermal conditions

| Case | Freestream (m/s) | Ambient (degC) | ESC current | Notes |
|---|---|---|---|---|
| Hover | ~0 (prop wash only) | 35 | [TBD] A/motor | Worst-case convection, low ESC load |
| Cruise | 18 | 35 | [TBD] A/motor | Good convection, higher ESC load |

The two cases trade against each other. Hover has the worst heat rejection but the lowest ESC
dissipation; cruise has better convection but higher I^2R loss. Both must be evaluated.

---

## 4. Requirements

### 4.1 Structural

| ID | Requirement | Source | Verification |
|---|---|---|---|
| REQ-STR-001 | First natural frequency of the loaded enclosure assembly shall exceed 3,440 Hz. | Sec 3.2, 1.5x separation | Modal FEA |
| REQ-STR-002 | No mode shall fall within 87 to 2,293 Hz. | Sec 3.2 excitation band | Modal FEA |
| REQ-STR-003 | Margin of safety under 3-sigma random vibration response shall be positive against 6061-T6 yield. | MIL-STD-810H | Miles' equation + static FEA |
| REQ-STR-004 | Mounting interface shall survive [TBD] hours cumulative exposure without fatigue failure. | 6061-T6 S-N data | Fatigue hand calc |

### 4.2 Thermal

| ID | Requirement | Source | Verification |
|---|---|---|---|
| REQ-THM-001 | Internal air temperature shall not exceed 40 degC in any flight condition. | C1 max ambient | Coupled CFD / thermal FEA |
| REQ-THM-002 | C1 component temperature shall not exceed 100 degC. | C1 spec | Thermal FEA |
| REQ-THM-003 | C2 MOSFET temperature shall not exceed 150 degC. | C2 spec | Thermal FEA |
| REQ-THM-004 | C3 case temperature shall not exceed 90 degC. | C3 spec | Thermal FEA |
| REQ-THM-005 | C6 capacitor temperature shall not exceed [TBD] degC. | C6 spec | Thermal FEA |

REQ-THM for C4 and C5 removed — both components are externally mounted and are not in the internal
thermal model.

### 4.3 Mass and envelope

| ID | Requirement | Source | Verification |
|---|---|---|---|
| REQ-MAS-001 | Enclosure mass shall not exceed [TBD] g. | Platform mass budget | CAD mass properties |
| REQ-ENV-001 | Internal volume shall accommodate C1, C2, C3 and C6 with clearance. | Sec 2 | CAD |
| REQ-ENV-002 | Enclosure shall accept the 30.5 x 30.5 mm stack mounting pattern. | C1, C2 interface | CAD |
| REQ-ENV-003 | Enclosure shall provide a cable penetration for the external C4 and C5 harness. | RF integration | CAD |

---

## 5. Analysis Results

### 5.1 Margin Table

| Req ID | Condition | Predicted | Allowable | Margin | Status |
|---|---|---|---|---|---|
| REQ-STR-001 | Modal | 3,984 Hz | 3,440 Hz | +0.16 | **PASS** |
| REQ-STR-002 | Modal | f1 = 3,984 Hz | 87–2,293 Hz band | No mode in band | **PASS** |
| REQ-STR-003 | Random vib | [TBD] MPa | [TBD] MPa | [TBD] | — |
| REQ-STR-004 | Fatigue | [TBD] | [TBD] | [TBD] | — |
| REQ-THM-001 | Hover, bare Al | 86.0 degC | 40 degC | -0.53 | **FAIL** |
| REQ-THM-001 | Hover, anodised | 69.4 degC | 40 degC | -0.42 | **FAIL** |
| REQ-THM-001 | Cruise, bare Al | 43.9 degC | 40 degC | -0.09 | **FAIL** |
| REQ-THM-001 | Cruise, anodised | 43.2 degC | 40 degC | -0.07 | **FAIL** |
| REQ-THM-002 | Hover | [TBD] degC | 100 degC | [TBD] | — |
| REQ-THM-003 | Cruise | [TBD] degC | 150 degC | [TBD] | — |
| REQ-THM-004 | Hover | [TBD] degC | 90 degC | [TBD] | — |
| REQ-MAS-001 | — | 96 g (base) | [TBD] g | [TBD] | — |

MS = (Allowable / Predicted) − 1. Thermal predictions are from the preliminary lumped-parameter
calculation (`thermal_scoping.py`), not from FEA. They are surface temperatures and therefore optimistic;
internal air will run hotter.

### 5.2 Modal Results — enclosure_v1

| Setting | Value |
|---|---|
| Solver | Autodesk Fusion 360 (Nastran) |
| Constraint | Fixed, four mounting tab underside faces |
| Contacts | Bonded at all interfaces (see A6) |
| Modes extracted | 10 |
| Excitation band | 87–2,293 Hz |

**No mode falls within the excitation band.**

Mode shapes (frequencies below are quoted at the 5% mesh, per section 5.3):

1. **3,983.7 Hz** — Lid drumming, first bending mode. Centre antinode, decaying to zero at the four
   corner bolts. Base and internal stack essentially rigid.
2. **4,249.4 Hz** — Second lid mode. Lid deforms; base floor does not participate. No significant motion
   of internal components.
3. **5,779.2 Hz** — Board stack responds about the Y axis. VTX and capacitor stationary. No lid or floor
   bending.
4. **6,028.6 Hz** — Small coupled lid and floor bending. Outer walls stationary. Board stack bends about
   the X axis.
5. **6,271.9 Hz** — Capacitor and partial VTX response. Lid deforms out of plane over the stack, opposite
   half deforms inward.
6. **6,705.6 Hz** — Capacitor-side wall deforms inward with the VTX. Stack largely unaffected. Lid and
   floor deform in opposition across the two halves.
7. **9,163.3 Hz** — Capacitor deformation fully coupled into the adjacent wall. Stack bending present.
   Lid and floor deform in an anti-phase diagonal pattern.
8. **9,249.5 Hz** — Coupled lid and long-wall response. Lid exhibits a single centre antinode in
   elevation; the internal stack shows a diagonal displacement pattern with peak amplitude at one ESC
   corner and a node at the capacitor, which remains near-stationary (min 0.028).
9. **9,730.2 Hz** — Long-wall out-of-plane bending. Two antinodes develop on the lid either side of the
   cable penetration, with a matching pair on the opposing side wall. The stack participates weakly; the
   base floor and mounting tabs are nodal.
10. **9,812.7 Hz** — Higher-order side-wall mode with three antinodes along the long wall. Lid and board
    stack deform in opposition — the lid bows upward while the stack bows downward beneath it. Standoffs
    act as the coupling path between the two.

### 5.3 Mesh Convergence

Mesh independence is established by re-solving with a reduced element size and comparing the first mode.
A shift below 2% is taken as converged.

| Mode | 10% Mesh (Baseline) | 7% Mesh (Refined) | Delta (10→7) | 5% Mesh (Further Refined) | Delta (7→5) |
|---|---|---|---|---|---|
| 1 | 4286.5 Hz | 4147.9 Hz | −138.6 Hz (3.23%) | 3983.7 Hz | −3.96% |
| 2 | 4690.0 Hz | 4352.5 Hz | −337.5 Hz (7.20%) | 4249.4 Hz | −2.37% |
| 3 | 5882.3 Hz | 5826.4 Hz | −55.9 Hz (0.95%) | 5779.2 Hz | −0.81% |
| 4 | 6071.6 Hz | 6038.9 Hz | −32.7 Hz (0.54%) | 6028.6 Hz | −0.17% |
| 5 | 6955.8 Hz | 6574.2 Hz | −381.6 Hz (5.49%) | 6271.9 Hz | −4.60% |
| 6 | 7130.9 Hz | 6793.3 Hz | −337.6 Hz (4.73%) | 6705.6 Hz | −1.29% |
| 7 | 9520.8 Hz | 9284.6 Hz | −236.2 Hz (2.48%) | 9163.3 Hz | −1.31% |
| 8 | 9847.4 Hz | 9601.5 Hz | −245.9 Hz (2.50%) | 9249.5 Hz | −3.67% |
| 9 | 10081.14 Hz | 9769.5 Hz | −311.6 Hz (3.09%) | 9730.2 Hz | −0.40% |
| 10 | 10591.3 Hz | 10156.3 Hz | −435.0 Hz (4.11%) | 9812.7 Hz | −3.38% |

Mode 1 does not meet the 2% criterion. The shift increased from 3.23% to 3.96% across successive
refinements rather than decreasing, and Richardson extrapolation returns a negative observed order of
convergence, indicating the discretisation error is not reducing monotonically. Modes 3 and 4 converge
cleanly at 0.81% and 0.17%; both are dominated by the base, a single solid body with no contact
dependence. The poorly converging modes — 1, 2, 5, 8, 10 — all involve the lid or the capacitor, both of
which depend on bonded contact between separately meshed bodies. Contact discretisation at these
interfaces is the probable cause. The reported first-mode frequency is the lowest of three meshes and is
therefore the most conservative available estimate.

---

## 6. Assumptions Log

| # | Assumption | Justification | Impact if wrong |
|---|---|---|---|
| A1 | C1 dissipation taken as 2.00 W | Published static power is 1.0 W (200 mA at 5 V, Betaflight). Rounded up to bound BEC conversion losses. | Over-predicts heat load by ~0.6 W. Conservative. |
| A2 | C2 dissipation taken as 0.90 W at hover | Conduction loss scales as I^2 x Rds(on). Corresponds to [TBD] A per motor. | Loss scales with the square of current. A 2x current error is a 4x dissipation error. |
| A3 | Ambient temperature 35 degC | Hot-day condition for the intended operating environment. | Directly offsets every predicted temperature. |
| A4 | C1 40 degC limit interpreted as max ambient | Distinct from the ~100 degC component rating. Inside a sealed enclosure the ambient limit governs internal air temperature. | If it is a component limit, REQ-THM-001 is over-conservative. |
| A5 | Standoffs modelled as aluminium | Stiffer than the nylon alternative commonly used in FPV builds. | Nylon would lower the board stack modes. **Non-conservative.** |
| A6 | All interfaces modelled as bonded | Represents fully preloaded bolted joints with no slip. | Over-predicts assembly stiffness and therefore natural frequencies. **Non-conservative for REQ-STR-001.** |
| A7 | Component blocks modelled as homogeneous solids | Correct mass and envelope; no PCB or component detail. FEA requires mass distribution, not layout. | Local stiffness of the boards is not represented. Affects board-level modes only. |

---

## 7. Open Items

- [ ] Confirm what the C1 40 degC figure refers to (ambient vs. component)
- [ ] State assumed ESC phase current for both hover and cruise
- [ ] Obtain MIL-STD-810H Method 514.8 and extract the PSD profile
- [ ] Define enclosure mass budget allocation
- [ ] Confirm C3 powered from VBAT, not the 5 V rail
- [ ] Confirm C6 temperature rating from the manufacturer datasheet
- [ ] Execute Phase 5 thermal redesign to close REQ-THM-001
