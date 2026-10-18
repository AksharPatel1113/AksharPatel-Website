# UAS Avionics Enclosure — Requirements, Environments & Analysis Report

| Field | Value |
|---|---|
| Project | Virtual environmental qualification of a machined avionics enclosure |
| Platform | 7 in class long-range multirotor UAS, 6S LiPo |
| Material | 6061-T6 aluminium, CNC machined |
| Author | Akshar Patel |
| Revision | **D — random vibration, fatigue, thermal network, Phase 5 redesign, mass and envelope closed** |

Rev D supersedes Rev C. Changes are listed in Sec 8.

---

## 1. Scope

Defines the design requirements and environmental load cases for an avionics enclosure housing the flight
control, propulsion control, and communications stack of a 7 in class multirotor UAS.

Verification is by analysis only. No physical test article is produced. All requirements trace to a
manufacturer-published limit, a published military standard, or a platform-derived excitation condition.

**In scope:** structural dynamics (modal, random vibration, fatigue), thermal (conduction, free and forced
convection, radiation), mass, and envelope.

**Out of scope:** shock, EMI/EMC, ingress protection, altitude, humidity, and any form of physical test
verification.

---

## 2. Component Stack

| ID | Component | Part | Mass (g) | Footprint (mm) | Height (mm) | Diss. (W) | Location |
|---|---|---|---|---|---|---|---|
| C1 | Flight controller | Matek H743-SLIM | 7.0 | 36 x 36 | 5.0 | 2.00 (A1) | Internal |
| C2 | 4-in-1 ESC | Holybro Tekko32 F4 65A | 15.8 | 46 x 44 | 6.0 | 0.90 hover / 1.44 cruise (A2) | Internal |
| C3 | Video transmitter | RushFPV Tank, 1.6 W class | 12.0 | 37 x 24 | 6.7 | 7.90 | Internal |
| C4 | GPS / compass | Matek M10Q-5883 | 8.0 | 20 x 20 | 12.4 | 0.07 | External |
| C5 | RC receiver | Happymodel EP2 ELRS | 0.4 | 10 x 10 | 6.0 | 0.20 | External |
| C6 | Bulk capacitor | Rubycon 35PK1000MEFCT810X20 | 2.75 | dia 11.25 | 25.0 | 0.05 (ripple) | Internal |

C4 and C5 are mounted externally. An aluminium enclosure forms a Faraday cage; the M10Q-5883 uses an
internal patch antenna and the EP2 an integrated SMD ceramic antenna. Neither would acquire signal if
enclosed.

**Internal heat load (C1 + C2 + C3):** 10.80 W hover / 11.34 W cruise.
**Binding internal component allowable:** 85 degC (C6).

### 2.1 Temperature limits

| ID | Max ambient (degC) | Max component (degC) | Notes |
|---|---|---|---|
| C1 | 40 (A4) | ~100 | Basis of the 40 degC figure not found in Matek documentation (open item) |
| C2 | — | 150 (MOSFET junction) | Device rating, not a board rating |
| C3 | — | 90 | Case temperature |
| C4 | — | 80 | External — excluded from internal thermal model |
| C5 | — | 80 | External — excluded from internal thermal model |
| C6 | — | **85** | PK series is an 85 degC part. Rev C's 105 degC was the generic electrolytic value. |

### 2.2 Interface notes

- C1 and C2 share a 30.5 x 30.5 mm mounting pattern. C2 is the larger outline and sets the minimum
  internal footprint.
- C2 has no output BEC. All 5 V loads are supplied by C1 onboard regulation; conversion losses dissipate
  on C1.
- C3 runs from VBAT: the RushFPV Tank family is specified for 7–36 V DC input (2–8S). **Closed.**
- C6 is required for 6S operation and is packaged upright inside the enclosure.

---

## 3. Environments

### 3.1 Vibration — MIL-STD-810H Method 514.8

**Profile selected:** Annex E, Category 24 — General Minimum Integrity Exposure (Figure 514.8E-1).

**Rationale:** No measured flight vibration data exists for this airframe, and no Annex D category
represents a small electric multirotor — the rotary-wing categories are built around helicopter main- and
tail-rotor sine tones. The minimum-integrity curve is the standard's own default when the environment is
unknown. Its 20–2000 Hz band covers the prop-passing range of Sec 3.2. The standard states that this
profile is a minimum-integrity screen and cannot by itself qualify hardware. That caveat is carried
forward: the results below show the design is robust, not that it is qualified for a measured flight
environment.

| Frequency (Hz) | PSD (g^2/Hz) |
|---|---|
| 20 | 0.04 |
| 1000 | 0.04 |
| 1000 – 2000 | -6 dB/oct |
| 2000 | 0.01 |

**Overall level:** 7.7 g_rms (integrated 7.69). **Duration:** 1 h per axis, 3 axes sequentially.

### 3.2 Platform excitation — prop passing frequency

`f_pp = (RPM / 60) x N_blades`

| Parameter | Value |
|---|---|
| Motor | T-Motor F90 2806.5, 1500 KV |
| Propeller | 7 in, 2 blades |
| RPM range | 2,600 (idle) to 17,200 (max) |

| Harmonic | Freq at idle (Hz) | Freq at max (Hz) |
|---|---|---|
| 1x | 87 | 573 |
| 2x | 173 | 1147 |
| 3x | 260 | 1720 |
| 4x | 347 | 2293 |

**Excitation band to avoid: 87 to 2,293 Hz.**

**Separation factor:** 1.5x applied to the highest harmonic of concern gives a REQ-STR-001 target of
3,440 Hz. A 2.0x factor would raise the target to 4,587 Hz and the design would not close. Noted as a
sensitivity rather than a failure, because the bonded-contact assumption (A6) already over-predicts
stiffness.

### 3.3 Thermal conditions

| Case | Freestream (m/s) | Ambient (degC) | ESC current | ESC loss | Notes |
|---|---|---|---|---|---|
| Hover | ~0 (prop wash neglected) | 35 | 3.5 A/motor | 0.90 W | Worst-case convection, low ESC load |
| Cruise | 18 | 35 | 6.0 A/motor | 1.44 W | Good convection, higher ESC load |

**Current basis (A2, A8):** a 1,000 g AUW needs 250 g of thrust per motor at hover. At ~6.8 g/W for the
F90 family on a 7 in prop, that is about 37 W, or 1.9 A per motor at 22.2 V. Cruise at 18 m/s adds
parasite power D·V ~ 34 W at 50 % propulsive efficiency, about 2.7 A per motor. The analysis carries
3.5 A and 6.0 A, roughly 1.8x and 2.2x those estimates, to cover the missing 1500 KV thrust table and
battery sag.

**ESC loss model:** P = 0.48 W (MCU, gate drive, LDO) + 4 x (I^2 x 4 mOhm + 0.016 W/A x I).

---

## 4. Requirements

### 4.1 Structural

| ID | Requirement | Source | Verification |
|---|---|---|---|
| REQ-STR-001 | First natural frequency shall exceed 3,440 Hz. | Sec 3.2, 1.5x separation | Modal FEA |
| REQ-STR-002 | No mode shall fall within 87 to 2,293 Hz. | Sec 3.2 excitation band | Modal FEA |
| REQ-STR-003 | MS under 3-sigma random vibration shall be positive against 6061-T6 yield (241 MPa, MMPDS A-basis). | MIL-STD-810H 514.8 | Miles' equation + plate / cantilever stress |
| REQ-STR-004 | Mounting interface shall survive 1,000 hours cumulative exposure without fatigue failure (Miner damage < 1). | 6061-T6 S-N data; service life (A9) | Steinberg three-band + Miner |

### 4.2 Thermal

| ID | Requirement | Source | Verification |
|---|---|---|---|
| REQ-THM-001 | Internal air temperature shall not exceed 40 degC in any flight condition. | C1 max ambient (A4) | Thermal network |
| REQ-THM-002 | C1 component temperature shall not exceed 100 degC. | C1 spec | Thermal network |
| REQ-THM-003 | C2 MOSFET junction temperature shall not exceed 150 degC. | C2 spec | Thermal network + R_th(j-board) |
| REQ-THM-004 | C3 case temperature shall not exceed 90 degC. | C3 spec | Thermal network |
| REQ-THM-005 | C6 capacitor temperature shall not exceed 85 degC. | C6 rating (Rubycon PK) | Thermal network |

### 4.3 Mass and envelope

| ID | Requirement | Source | Verification |
|---|---|---|---|
| REQ-MAS-001 | Enclosure mass (excluding avionics) shall not exceed 100 g. | 10 % of 1,000 g AUW (A10) | CAD mass properties |
| REQ-ENV-001 | Internal volume shall accommodate C1, C2, C3 and C6 with no interference and at least 1.0 mm clearance. | Sec 2 | CAD interference + min distance |
| REQ-ENV-002 | Enclosure shall accept the 30.5 x 30.5 mm stack mounting pattern. | C1, C2 interface | CAD |
| REQ-ENV-003 | Enclosure shall provide a cable penetration for the external C4 and C5 harness. | RF integration | CAD |

---

## 5. Analysis Results

### 5.1 Margin Table

MS = (Allowable / Predicted) − 1 for upper limits; MS = (Predicted / Allowable) − 1 for the frequency floor.

| Req ID | Condition | Predicted | Allowable | Margin | Status |
|---|---|---|---|---|---|
| REQ-STR-001 | Modal | 3,984 Hz | 3,440 Hz | +0.16 | **PASS** |
| REQ-STR-002 | Modal | f1 = 3,984 Hz | 87–2,293 Hz band | No mode in band | **PASS** |
| REQ-STR-003 | Random vib, Q = sqrt(fn) | 13.5 MPa (tab) | 241 MPa | +16.8 | **PASS** |
| REQ-STR-004 | Fatigue, 1,000 h | D = 2.3e-7 | D < 1 | Life 4.3e9 h | **PASS** |
| REQ-THM-001 | Hover, anodised, v1 | 73.0 degC | 40 degC | -0.45 | **FAIL** |
| REQ-THM-001 | Cruise, anodised, v1 | 48.4 degC | 40 degC | -0.17 | **FAIL** |
| REQ-THM-001 | Hover, Phase 5 R4 | 39.4 degC | 40 degC | +0.02 | **PASS (marginal)** |
| REQ-THM-001 | Cruise, Phase 5 R4 | 37.4 degC | 40 degC | +0.07 | **PASS** |
| REQ-THM-002 | Hover, anodised, v1 | 89.7 degC | 100 degC | +0.11 | **PASS** |
| REQ-THM-003 | Hover, anodised, v1 | 79.4 degC | 150 degC | +0.89 | **PASS** |
| REQ-THM-004 | Hover, anodised, v1 | 73.4 degC | 90 degC | +0.23 | **PASS** |
| REQ-THM-005 | Hover, anodised, v1 | 70.9 degC | 85 degC | +0.20 | **PASS** |
| REQ-MAS-001 | v1 (base + lid + 8 M3) | 69.7 g | 100 g | +0.43 | **PASS** |
| REQ-MAS-001 | Phase 5 R4 (fins + 2 fans) | 99.3 g | 100 g | +0.01 | **PASS (marginal)** |
| REQ-ENV-001 | CAD | 0 interferences, min 1.00 mm | 1.0 mm | 0.00 | **PASS (at limit)** |
| REQ-ENV-002 | CAD | 30.5 x 30.5 mm, 4 x M3 bosses | 30.5 x 30.5 mm | — | **PASS** |
| REQ-ENV-003 | CAD | dia 8.0 mm, +X wall | Present | — | **PASS** |

**Bare aluminium is not acceptable.** At hover, bare v1 fails REQ-THM-002 (110.6 degC), REQ-THM-004
(90.9 degC) and REQ-THM-005 (88.9 degC). An external **and** internal anodise (eps ~ 0.85) is a design
requirement.

### 5.2 Modal Results — enclosure_v1

Solver: Fusion 360 (Nastran). Fixed on four mounting tab underside faces, bonded at all interfaces (A6),
10 modes extracted. No mode falls within the excitation band; the first mode (finest mesh, 3,984 Hz)
clears the fourth harmonic at maximum RPM by a factor of 1.74.

| Mode | Freq, 10 % mesh (Hz) | Description |
|---|---|---|
| 1 | 4286.5 | Lid drumming, first bending. Centre antinode decaying to zero at the four corner bolts. |
| 2 | 4690.0 | Second lid mode. Lid deforms; base floor does not participate. |
| 3 | 5882.3 | Board stack responds about Y. VTX and capacitor stationary. |
| 4 | 6071.6 | Small coupled lid and floor bending. Stack bends about X. |
| 5 | 6955.8 | Capacitor and partial VTX response. Lid deforms out of plane over the stack. |
| 6 | 7130.9 | Capacitor-side wall deforms inward with the VTX. Lid and floor in opposition. |
| 7 | 9520.8 | Capacitor fully coupled into the adjacent wall. Lid and floor anti-phase diagonal. |
| 8 | 9847.4 | Coupled lid and long-wall response. Capacitor nodal. |
| 9 | 10081.1 | Long-wall out-of-plane bending. Two lid antinodes either side of the cable penetration. |
| 10 | 10591.3 | Three-antinode side-wall mode. Lid bows up while stack bows down. |

### 5.3 Mesh Convergence

| Mode | 10 % mesh | 7 % mesh | Δ 10→7 | 5 % mesh | Δ 7→5 |
|---|---|---|---|---|---|
| 1 | 4286.5 | 4147.9 | −3.23 % | 3983.7 | −3.96 % |
| 2 | 4690.0 | 4352.5 | −7.20 % | 4249.4 | −2.37 % |
| 3 | 5882.3 | 5826.4 | −0.95 % | 5779.2 | −0.81 % |
| 4 | 6071.6 | 6038.9 | −0.54 % | 6028.6 | −0.17 % |
| 5 | 6955.8 | 6574.2 | −5.49 % | 6271.9 | −4.60 % |
| 6 | 7130.9 | 6793.3 | −4.73 % | 6705.6 | −1.29 % |
| 7 | 9520.8 | 9284.6 | −2.48 % | 9163.3 | −1.31 % |
| 8 | 9847.4 | 9601.5 | −2.50 % | 9249.5 | −3.67 % |
| 9 | 10081.1 | 9769.5 | −3.09 % | 9730.2 | −0.40 % |
| 10 | 10591.3 | 10156.3 | −4.11 % | 9812.7 | −3.38 % |

Mode 1 does not meet the 2 % criterion. The shift grew from 3.23 % to 3.96 % across successive
refinements, and Richardson extrapolation returns a negative observed order. Modes 3 and 4 converge
cleanly; both are dominated by the single-body base. The poorly converging modes (1, 2, 5, 8, 10) all
involve the lid or capacitor, which depend on bonded contact between separately meshed bodies. The
reported 3,984 Hz is the lowest of three meshes and therefore the most conservative available.

**Sensitivity:** at ~4 % per refinement, REQ-STR-001 would still hold for about three more halvings
(3,984 → 3,440 Hz is a 13.6 % drop). Random-vibration margin is insensitive to f1 because Miles' response
scales as sqrt(fn).

### 5.4 Random Vibration and Fatigue

f1 lies above the 2 kHz profile limit, so the PSD is extrapolated at −6 dB/oct to f1 (0.00252 g^2/Hz). The
profile has no energy there, so this is conservative. The response is taken as the larger of Miles'
equation and the quasi-static input (7.69 g_rms).

| Case | g_rms | 3σ (g) | Lid plate σ (MPa) | Tab root σ, Kt 2.5 (MPa) | MS vs 241 MPa |
|---|---|---|---|---|---|
| Q = 10 (nominal) | 12.6 | 37.7 | 0.44 | 5.39 | +43.7 |
| Q = sqrt(fn) = 63 (Steinberg bound) | 31.6 | 94.7 | 1.11 | 13.54 | **+16.8** |

- Lid: Roark Table 11.4 case 1a, simply supported 90.5 x 60.5 x 4.0 mm plate under 3σ inertial pressure.
- Tabs: 105 g assembly on four 12 x 3 mm cantilevers, 4 mm moment arm, Kt = 2.5.
- Fatigue (governing tab, Q = sqrt(fn)): 1σ = 4.51 MPa. Steinberg three-band cycle counts over 1,000 h at
  3,984 Hz give Miner damage 2.3e-7. The 3σ peak (13.5 MPa) is below the 96.5 MPa endurance strength at
  5e8 cycles, so life is effectively unlimited.
- Not covered: bolt preload loss and fretting at the bonded interfaces (A6), and board-level solder
  fatigue (A7).

### 5.5 Thermal Network

Six-node steady-state network (shell, internal air, C1, C2, C3, C6), geometry from the Fusion model. It
agrees with the lumped scoping calc: shell 68.8 vs 69.3 degC at hover anodised, inside the 30 % cross-check
criterion.

Key conductances: C3 → shell 0.59 K/W (0.5 mm, 3 W/m·K gap pad on the 666 mm^2 machined pad plus floor
spreading); C2 → shell 3.94 K/W (four M3 bosses); C1 → C2 8.21 K/W (four aluminium standoffs). Internal
h = 3 W/m^2·K still air, 15 W/m^2·K with fans.

**Baseline, enclosure_v1 (degC, 35 degC ambient)**

| Case | Q (W) | Shell | Air | C1 | C2 | FET j | C3 | C6 |
|---|---|---|---|---|---|---|---|---|
| Hover, bare Al | 10.85 | 86.2 | 91.1 | 110.6 | 96.2 | 98.3 | 90.9 | 88.9 |
| Hover, anodised | 10.85 | 68.8 | 73.0 | 89.7 | 77.3 | 79.4 | 73.4 | 70.9 |
| Cruise, bare Al | 11.39 | 44.4 | 49.8 | 70.8 | 56.4 | 61.2 | 49.0 | 47.2 |
| Cruise, anodised | 11.39 | 43.6 | 48.4 | 66.7 | 54.2 | 59.0 | 48.2 | 45.8 |

Hover governs every requirement. The low hover ESC load is outweighed by the loss of forced convection.

### 5.6 Phase 5 Thermal Redesign

REQ-THM-001 allows 5 K of air rise for ~11 W, needing an air-to-ambient conductance of ~2.2 W/K. The
sealed v1 box provides ~0.32 W/K at hover; closing the gap with surface area alone would take ~6.9x the
external area. The redesign stacks four measures.

| Option | Change | Mass Δ |
|---|---|---|
| R1 | Anodise inside and out (baseline above) | 0 |
| R2 | 9 longitudinal lid fins, 1.0 mm x 10 mm tall, 7 mm pitch, machined integral (+0.0167 m^2) | +22.6 g |
| R3 | VTX operated at the 800 mW level (published draw 380 mA @ 12 V = 4.56 W) | 0 |
| R4 | Two 25 mm 5 V fans, push-pull through filtered ducts (~0.47 L/s each, 0.8 W motor heat) | +7 g |

| Case | Q (W) | Shell | Air | C1 | C2 | FET j | C3 | C6 |
|---|---|---|---|---|---|---|---|---|
| Hover, R1 no TIM | 10.85 | 68.8 | 73.4 | 89.7 | 77.3 | 79.4 | 79.1 | 70.9 |
| Hover, R2 + fins | 10.85 | 62.0 | 66.2 | 83.1 | 70.6 | 72.7 | 66.6 | 64.1 |
| Hover, R3 + VTX 800 mW | 7.51 | 54.8 | 59.0 | 76.1 | 63.5 | 65.6 | 57.5 | 56.9 |
| **Hover, R4 + 2 fans** | 8.31 | 45.9 | **39.4** | 57.7 | 49.9 | 52.0 | 48.5 | 44.8 |
| Cruise, R1 no TIM | 11.39 | 43.6 | 48.8 | 66.8 | 54.2 | 59.0 | 54.0 | 45.9 |
| Cruise, R2 + fins | 11.39 | 40.7 | 45.5 | 63.9 | 51.3 | 56.1 | 45.3 | 42.9 |
| Cruise, R3 + VTX 800 mW | 8.05 | 39.0 | 43.7 | 62.3 | 49.7 | 54.5 | 41.7 | 41.3 |
| **Cruise, R4 + 2 fans** | 8.85 | 38.1 | **37.4** | 53.5 | 45.2 | 50.0 | 40.8 | 39.1 |

**Findings**

1. All component requirements (REQ-THM-002 to 005) close on the anodised v1 with a gap pad under the VTX.
   Without the pad, C3 rises 5.7 K at hover; a gap pad on the machined VTX pad is a design requirement.
2. REQ-THM-001 closes only with the full R2–R4 stack, and at hover only marginally (39.4 degC, 0.6 K
   margin). It is not robust to the network assumptions (internal h, fan delivered flow, A4).
3. R3 costs video range (1.6 W → 800 mW, roughly −30 % range at equal link margin). R4 breaks the
   sealed-box concept; ingress protection is out of scope, but the inlet needs a filter.
4. **Recommendation:** close open item A4 before committing to R2–R4. If the 40 degC figure is not a real
   C1 ambient rating, REQ-THM-001 should be restated to the most limiting internal-component ambient. The
   STM32H743 is rated −40 to +85 degC ambient, and the C6 rating is 85 degC. On that basis the anodised v1
   with a gap pad passes with MS >= +0.11 at hover and needs no fans, fins or VTX derating. If the 40 degC
   is confirmed, adopt R2 + R3 + R4 as enclosure_v2.

### 5.7 Mass and Envelope (Fusion API)

| Item | Value |
|---|---|
| Base (Body60) | 54.26 g |
| Lid (Body61) | 11.87 g |
| Enclosure, base + lid | 66.13 g |
| + 8 x M3 steel screws (est.) | 69.7 g |
| Assembly incl. component stand-ins | 101.34 g, CoG (−0.69, 0.02, 12.90) mm |
| Interferences (10 bodies) | 0 |
| Minimum clearances | C6–lid 1.00, C6–C3 1.38, C2–C3 2.00, C1–lid 3.00 mm |
| Stack pattern | Bosses at x = −32.25 / −1.75, y = ±15.25 → 30.5 x 30.5 mm |
| Cable penetration | dia 8.0 mm, +X wall at y = −15, z = 18 mm |

The C1 and C2 stand-in masses (8.43 g, 10.93 g) differ from the published values (7.0 g, 15.8 g). Net
assembly error is −3.4 g (−3 %), which raises the modal frequencies slightly. Open item.

### 5.8 Fusion Procedures

The Fusion adsk.sim scripting API returns no simulation object in the installed build, and its
documentation limits scripted solves to Linear Static Stress. These studies are run interactively and
recorded against the hand calcs.

- **P-STR-1 (done, Rev C):** Modal, 10 modes, fixed tab undersides, bonded contacts, 10 / 7 / 5 % mesh.
- **P-STR-2 (to run):** Linear Static Stress. Gravity load of 94.7 g applied separately in X, Y and Z.
  Compare max von Mises in tabs and lid against 13.5 MPa / 1.1 MPa.
- **P-THM-1 (to run):** Thermal study, hover anodised. C1 2.00 W, C2 0.90 W, C3 7.90 W, C6 0.05 W.
  Convection 8.0 W/m^2·K, radiation eps 0.85 at 35 degC. Thermal contact 1,670 W/m^2·K at the VTX–pad
  interface. Compare shell and C3 against 68.8 / 73.4 degC; divergence above 30 % needs explanation.
- **P-THM-2 (to run):** As P-THM-1 with 54.6 W/m^2·K, C2 1.44 W (cruise).

---

## 6. Assumptions Log

| # | Assumption | Justification | Impact if wrong |
|---|---|---|---|
| A1 | C1 dissipation 2.00 W | Published static power 1.0 W; rounded up to bound BEC losses | Over-predicts by ~0.6 W. Conservative. |
| A2 | C2 0.90 W hover (3.5 A/motor), 1.44 W cruise (6.0 A/motor) | Loss model of Sec 3.3, calibrated to 0.90 W at 3.5 A | Conduction term scales with I^2. C2 is 8–13 % of the load; low sensitivity. |
| A3 | Ambient 35 degC | Hot-day condition | Offsets every temperature 1:1 |
| A4 | C1 40 degC limit interpreted as max ambient | Distinct from ~100 degC component rating. No Matek source found. | Drives the entire Phase 5 redesign. |
| A5 | Standoffs modelled as aluminium | Stiffer than nylon | Nylon lowers stack modes and raises C1 temperature. Non-conservative. |
| A6 | All interfaces bonded | Fully preloaded joints | Over-predicts stiffness. NON-CONSERVATIVE for REQ-STR-001. |
| A7 | Components as homogeneous solids | Correct mass and envelope | Board-level modes and solder fatigue not represented |
| A8 | AUW 1,000 g; currents from F90 KV1300 efficiency data | No published F90 1500 KV / 7 in thrust table found | Carried at ~2x the estimate; low thermal sensitivity |
| A9 | Service life 1,000 flight hours | Typical airframe life for a long-range FPV platform | Fatigue damage 2.3e-7 per 1,000 h; insensitive |
| A10 | Enclosure mass budget 100 g (10 % of AUW) | Allocation, not a sourced limit | v1 has 30 g margin; Phase 5 R4 has 0.7 g |
| A11 | Network conductances (gap pad 3 W/m·K, 15 K/W per PCB-to-boss joint, internal h 3 W/m^2·K) | Handbook values | C1 and C2 most sensitive. Verify with P-THM-1. |
| A12 | MIL-STD-810H Cat. 24 minimum-integrity profile | No measured flight data | Screening-level only; not a qualification environment |
| A13 | Response Q = sqrt(fn) ~ 63 (Steinberg upper bound) | Conservative vs typical Q = 10–20 for bolted Al | Over-predicts stress ~2.5x. Conservative. |

---

## 7. Open Items

- **Confirm what the C1 40 degC figure refers to (ambient vs component). This decides whether R2–R4 are
  needed.**
- Confirm C1 board revision (BEC rating differs by revision).
- Obtain the F90 1500 KV / 7 in manufacturer thrust table to replace A8.
- Obtain the Rubycon PK datasheet to confirm 85 degC (currently distributor listings).
- Correct the C1 / C2 stand-in masses in CAD and re-run modal.
- Run Fusion procedures P-STR-2, P-THM-1 and P-THM-2 and record against the hand calcs.
- Contact modelling: replace the bonded lid contact with a bolted/separation contact to investigate mode 1
  non-convergence (A6).
- Complete modal descriptions for modes 8–10.

---

## 8. Revision History

| Rev | Change |
|---|---|
| A | Initial requirements |
| B | Modal results incorporated |
| C | C4/C5 moved external; mesh convergence; motor/prop and separation factor set |
| D | Vibration profile selected; REQ-STR-003/004 closed by analysis; thermal network added (component temperatures); ESC currents stated; C6 rating corrected 105 → 85 degC; Phase 5 redesign sized; mass budget, envelope, stack pattern and penetration verified from Fusion CAD; Fusion procedures defined |
