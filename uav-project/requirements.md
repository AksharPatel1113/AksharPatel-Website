# UAS Avionics Enclosure — Requirements & Environments

**Project:** Virtual environmental qualification of a machined avionics enclosure   
**Platform:** 7" class long-range multirotor UAS, 6S LiPo   
**Enclosure material:** 6061-T6 aluminum, CNC machined   
**Author:** Akshar Patel

---

## 1\. Scope

This document defines the design requirements and environmental load cases for an avionics enclosure housing the flight control, propulsion control, and communications stack of a 7" class multirotor UAS.

Verification is by analysis only. No physical test article is produced. All requirements trace to either a manufacturer-published limit, a published military standard, or a platform-derived excitation condition.

**In scope:** structural dynamics (modal, random vibration), thermal (conduction, free and forced convection), mass, and envelope.

**Out of scope:** shock, EMI/EMC, ingress protection, altitude, humidity, and any form of physical test verification.

---

## 2\. Component Stack

Baseline selected via weighted trade study (`docs/trade_study.xlsx`, Rev A).

| ID | Component | Part | Mass (g) | Footprint (mm) | Height (mm) | Dissipation (W) | Source |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| C1 | Flight controller | Matek H743-SLIM | 7.0 | 36 x 36 | 5 | 2.00 (see A1) | Mfr. spec |
| C2 | 4-in-1 ESC | Holybro Tekko32 F4 Metal 65A | 15.8 | 43 x 44 | \[TBD\] | 0.90 (see A2) | Mfr. spec |
| C3 | Video transmitter | RushFPV Tank Ultimate 5.8G 1.6W | 12.0 | \[TBD\] | \[TBD\] | 7.90 | Mfr. spec |
| C4 | GPS / compass | Matek M10Q-5883 | 8.0 | \[TBD\] | \[TBD\] | 0.07 | Mfr. spec |
| C5 | RC receiver | Happymodel EP2 ELRS 2.4 GHz | 0.4 | \[TBD\] | \[TBD\] | 0.20 | Mfr. spec |
| C6 | Bulk capacitor | 1000 uF 35 V electrolytic | \[TBD\] | \[TBD\] | \[TBD\] | negligible | Supplied with C2 |

**Total stack mass (C1–C5):** 43.2 g — C6 not yet included **Total dissipation:** 11.07 W

### 2.1 Temperature limits

Two distinct limits apply and must not be conflated.

| ID | Max ambient (degC) | Max component / junction (degC) | Notes |
| :---- | :---- | :---- | :---- |
| C1 | 40 | \~100 | Ambient limit is binding inside a sealed enclosure |
| C2 | \[TBD\] | 150 (MOSFET) | 150 is a device rating, not a board rating |
| C3 | \[TBD\] | 90 |  |
| C4 | \[TBD\] | 80 |  |
| C5 | \[TBD\] | 80 |  |
| C6 | \[TBD\] | 105 (typical electrolytic) | Verify. Lifetime halves per \~10 degC above rating |

**Binding ambient allowable:** 40 degC (C1) **Binding component allowable:** 80 degC (C4, C5)

### 2.2 Interface notes

- C1 and C2 share a 30.5 x 30.5 mm mounting pattern. C2 is the larger outline (43 x 44 mm) and therefore sets the minimum internal footprint.  
- C2 has **no output BEC**. All 5 V loads are supplied by C1's onboard regulator (5 V @ 2.0–2.5 A depending on board revision). BEC conversion losses dissipate on C1.  
- C3 runs from VBAT, not the 5 V rail. Confirm before finalizing the power budget.  
- C6 is required for 6S operation and must be packaged inside the enclosure.

---

## 3\. Environments

### 3.1 Vibration — MIL-STD-810H Method 514.8

**Profile selected:** \[ANNEX / TABLE / FIGURE\] **Rationale for selection:** \[WHY THIS PROFILE FITS A SMALL MULTIROTOR\]

| Frequency (Hz) | PSD (g^2/Hz) |
| :---- | :---- |
| \[TBD\] | \[TBD\] |
| \[TBD\] | \[TBD\] |
| \[TBD\] | \[TBD\] |
| \[TBD\] | \[TBD\] |

**Overall level:** \[TBD\] g\_rms **Duration:** \[TBD\] per axis, 3 axes sequentially

### 3.2 Platform excitation — prop passing frequency

f\_pp \= (RPM / 60\) x N\_blades

**Motor/prop combination:** \[SELECTED FROM TRADE STUDY\] **RPM range:** \[TBD\] (idle) to \[TBD\] (max) **Source:** \[MANUFACTURER THRUST TABLE\]

| Harmonic | Freq at idle (Hz) | Freq at max (Hz) |
| :---- | :---- | :---- |
| 1x | 87 | 573 |
| 2x | 173 | 1147 |
| 3x | 260 | 1720 |
| 4x | 347 | 2293 |

**Excitation band to avoid:** \[TBD\] to \[TBD\] Hz

### 3.3 Thermal conditions

| Case | Freestream (m/s) | Ambient (degC) | ESC current | Notes |
| :---- | :---- | :---- | :---- | :---- |
| Hover | \~0 (prop wash only) | 35 | \[TBD\] A/motor | Worst case convection, low ESC load |
| Cruise | 18 | 35 | \[TBD\] A/motor | Good convection, higher ESC load |

**Ambient basis:** 35 degC selected as a hot-day condition representative of the intended operating environment. \[CONFIRM AND CITE\]

**Note:** the two cases trade against each other. Hover has the worst heat rejection but the lowest ESC dissipation; cruise has better convection but higher I^2R loss. Both must be evaluated — neither is obviously binding a priori.

---

## 4\. Requirements

### 4.1 Structural

| ID | Requirement | Source | Verification |
| :---- | :---- | :---- | :---- |
| REQ-STR-001 | First natural frequency of the loaded enclosure assembly shall exceed 3,440 Hz. | Sec 3.2, separation factor \[TBD\] | Modal FEA |
| REQ-STR-002 | No mode shall fall within \[TBD\] to \[TBD\] Hz. | Sec 3.2 excitation band | Modal FEA |
| REQ-STR-003 | Margin of safety under 3-sigma random vibration response shall be positive against 6061-T6 yield. | MIL-STD-810H | Miles' equation \+ static FEA |
| REQ-STR-004 | Mounting interface shall survive \[TBD\] hours cumulative exposure without fatigue failure. | 6061-T6 S-N data | Fatigue hand calc |

### 4.2 Thermal

Split into ambient and component requirements per Sec 2.1.

| ID | Requirement | Source | Verification |
| :---- | :---- | :---- | :---- |
| REQ-THM-001 | Internal air temperature shall not exceed 40 degC in any flight condition. | C1 max ambient | Coupled CFD / thermal FEA |
| REQ-THM-002 | C1 component temperature shall not exceed 100 degC. | C1 spec | Thermal FEA |
| REQ-THM-003 | C2 MOSFET temperature shall not exceed 150 degC. | C2 spec | Thermal FEA |
| REQ-THM-004 | C3 case temperature shall not exceed 90 degC. | C3 spec | Thermal FEA |
| REQ-THM-005 | C4 temperature shall not exceed 80 degC. | C4 spec | Thermal FEA |
| REQ-THM-006 | C5 temperature shall not exceed 80 degC. | C5 spec | Thermal FEA |
| REQ-THM-007 | C6 capacitor temperature shall not exceed \[TBD\] degC. | C6 spec | Thermal FEA |

### 4.3 Mass and envelope

| ID | Requirement | Source | Verification |
| :---- | :---- | :---- | :---- |
| REQ-MAS-001 | Enclosure mass shall not exceed \[TBD\] g. | Platform mass budget | CAD mass properties |
| REQ-ENV-001 | Internal volume shall accommodate C1–C6 with \[TBD\] mm clearance. | Sec 2 | CAD |
| REQ-ENV-002 | Enclosure shall accept the 30.5 x 30.5 mm stack mounting pattern. | C1, C2 interface | CAD |
| REQ-ENV-003 | Enclosure shall provide antenna penetrations for C3 (5.8 GHz) and C5 (2.4 GHz). | RF integration | CAD |

---

## 5\. Margin Table

| Req ID | Condition | Predicted | Allowable | Margin | Status |
| :---- | :---- | :---- | :---- | :---- | :---- |
| REQ-STR-001 | Modal | 4211 Hz | 3440 Hz | +-0.22 | PASS |
| REQ-STR-002 | Modal | 4211 Hz (f1) | 87-2293 Hz band | No mode in band | PASS |
| REQ-STR-003 | Random vib | \[TBD\] MPa | \[TBD\] MPa | \[TBD\] | \[ \] |
| REQ-STR-004 | Fatigue | \[TBD\] | \[TBD\] | \[TBD\] | \[ \] |
| REQ-THM-001 | Hover | \[TBD\] degC | 40 | \[TBD\] | \[ \] |
| REQ-THM-001 | Cruise, anodized | 69.4 degC | 40 | -0.42 | FAIL |
| REQ-THM-002 | Hover | \[TBD\] degC | 100 | \[TBD\] | \[ \] |
| REQ-THM-003 | Cruise | \[TBD\] degC | 150 | \[TBD\] | \[ \] |
| REQ-THM-004 | Hover | \[TBD\] degC | 90 | \[TBD\] | \[ \] |
| REQ-THM-005 | Hover | \[TBD\] degC | 80 | \[TBD\] | \[ \] |
| REQ-THM-006 | Hover | \[TBD\] degC | 80 | \[TBD\] | \[ \] |
| REQ-THM-007 | Hover | \[TBD\] degC | \[TBD\] | \[TBD\] | \[ \] |
| REQ-MAS-001 | — | \[TBD\] g | \[TBD\] g | \[TBD\] | \[ \] |

MS \= (Allowable / Predicted) \- 1

## 5.1 Modal Results — enclosure_v1

Solver: Fusion 360 (Nastran). 10 modes extracted.
Constraint: fixed on four mounting tab underside faces.
Contacts: bonded at all interfaces (see A6).

| Mode | Freq (Hz) | Description |
|------|-----------|-------------|
| 1 | 4211.3 | Lid drumming, first bending, centre antinode |
| 2 | 4474.6 | Top lid deformation, bottom doesn't bend, no bending of internal components |
| 3 | 5771.8 | Stack is effected about y, but VTX & Capacitor aren't, no lid and bottom bending |
| 4 | 6003.3 | Small top bottom bending,No outside bending, Stack bends about x |
| 5 | 6786.6 | Capacitor and a little of VTX bends, top half of lid (stack) deforms up, other half of lid bends down |
| 6 | 6882.3 | Capacitor side bends inwards w VTX, Stack isn't majorly effected, stack side lid deforms up, Capacitor side lid and bottom deforms down |
| 7 | 9248.7 | Capacitor deformation completely effecting wall, stack bending, stack side lid/capacitor side bottom inwards, stack side bottom/capacitor side lid outwards |
| 8 | 9728.9 | [TBD] |
| 9 | [TBD] | [TBD] |
| 10 | [TBD] | [TBD] |

Excitation band: 87–2293 Hz (Sec 3.2). No mode falls within the band.

---

## 6\. Assumptions Log

| \# | Assumption | Justification | Impact if wrong |
| :---- | :---- | :---- | :---- |
| A1 | C1 dissipation taken as 2.00 W | Published static power is 1.0 W (200 mA @ 5 V, Betaflight). Rounded up to bound BEC conversion losses for downstream 5 V loads. Conservative. | Over-predicts internal heat load by \~0.6 W (5% of total). Conservative direction — a design that closes at 2.00 W closes at 1.4 W. |
| A2 | C2 dissipation taken as 0.90 W at hover | Conduction loss scales as I^2 x Rds(on). Figure corresponds to \[TBD\] A per motor. | Loss scales with the square of current. A 2x current error is a 4x dissipation error. Must be restated for the cruise case. |
| A3 | Ambient temperature 35 degC | Hot-day condition for intended operating environment. | Directly offsets every predicted temperature. A 5 degC error is a 5 degC margin error. |
| A4 | C1 40 degC limit interpreted as max ambient | Distinct from the \~100 degC component rating. Inside a sealed enclosure the ambient limit governs internal air temperature. | If 40 degC is actually a component limit, REQ-THM-001 is over-conservative and the design is easier than modeled. If it is an ambient limit and is ignored, the design is unqualified. |
| A5 | \[TBD\] |  |  |

---

## 7\. Open Items

- [ ] Confirm what the C1 40 degC figure refers to (ambient vs. component)  
- [ ] Obtain footprint and height for C3, C4, C5, C6  
- [ ] Determine C6 mass and temperature rating  
- [ ] State assumed ESC phase current for both flight conditions  
- [ ] Obtain MIL-STD-810H Method 514.8 and extract PSD profile  
- [ ] Select motor/prop and determine RPM range  
- [ ] Set and justify modal separation factor  
- [ ] Define enclosure mass budget allocation  
- [ ] Confirm C3 powered from VBAT, not 5 V rail  
- [ ] Confirm C1 board revision (BEC rating differs by revision)

