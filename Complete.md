# Technical Report – Point D

### Demonstration of Detection and Avoidance Architectures

### for Safe Integration of Unmanned Aircraft System (UAS) in

### Non-Segregated Airspace

### SIMUA Project – Safe Integration of Manned and Unmanned Aircrafts

```
Brazil-Sweden Strategic Partnership | Air Domain Study (ADS)
```
### March 2026

```
Abstract
This report documents the technical results of Point D of the Work Plan for
the SIMUA project (Safe Integration of different Manned and Unmanned Aircraft
into non-segregated airspace), a research initiative developed within the strategic
partnership between Instituto Tecnológico de Aeronáutica (ITA) and Instituto de
Controle do Espaço Aéreo (ICEA) under the Brazil–Sweden Air Domain Study (ADS)
program. Formulated as a technical evidence package for DECEA/ICEA authorities,
the document explores the architectural feasibility of Detect and Avoid (DAA)
systems in non-segregated airspaces, structured around the international Remain
Well Clear (RWC)/Collision Avoidance (CA) layered framework (RTCA DO-365B,
ASTM F3442). The investigation is organized into five complementary research
threads: (i) pre-tactical sensor infrastructure optimization (SCOPAS) generating
cost-versus-coverage boundaries for regional surveillance; (ii) strategic microclimate
forecasting (WRF/UCM) integrating localized atmospheric risk as a foundational
UTM/U-space layer; (iii) Macro-Scale Strategic Layering Analysis (MSLA)
stress-testing fleet-scale capacity and conflict trade-offs between strategic reservation
tubes and tactical self-separation; (iv) High-Fidelity Tactical Logic Validation (HTLV)
evaluating the 10 Hz kinematic execution of NASA’s DAIDALUS logic under high-
density alert saturation; and (v) a synchronized multi-sensor simulation benchmark
empirically investigating the "sense" layer (Radar, LiDAR, Electro-Optical) under
diverse lighting and encounter geometries. The experimental campaign indicates
that while reactive-only guidance faces O(N^2) scalability bottlenecks at extreme
```

```
fleet densities (N > 300), the hybrid xTM+DAA layering ensures sustainable
safety margins. Furthermore, the findings identify the ABDAA architecture —
combining mmWave Radar for lighting-invariant cueing and Electro-Optical vision for
semantic classification, managed by standard-aligned RWC logic—as the preferred
research pathway for safe UAS integration within Brazilian Airspace Control
System (SISCEAB) airspace classes. All studies represent ongoing research efforts;
their primary value is the technical understanding and capability consolidation
developed to guide future development and regulatory decisions, rather than providing
a finalized operational delivery.
```
**Keywords:** Detect and Avoid (DAA); Remain Well Clear (RWC); UAS Traffic Manage-
ment (UTM); Advanced Air Mobility (AAM); DAIDALUS; mmWave Radar; Computer
Vision; SISCEAB; OSED; Microclimate Forecasting; SCOPAS; MSLA; HTLV; Brazil-
Sweden ADS; RTCA DO-365B; ASTM F3442.


## Contents


- List of Acronyms and Abbreviations
- 1 Technical Foundation and Requirements
   - 1.1 Strategic Alignment and Partnership
      - 1.1.1 Context and Motivation
      - 1.1.2 Milestone Identification – Point D
      - 1.1.3 Partners and Responsibilities
   - 1.2 Architecture Definition: Strategy and Sensors
      - 1.2.1 DAA Layered Architecture: RWC and CA
      - 1.2.2 Operational Services and Environment Definition (OSED)
      - 1.2.3 Sensor Trade-off Study: Motivation and Criteria
      - 1.2.4 LiDAR: Evaluation and Infeasibility on Micro-UAS
      - 1.2.5 Millimeter Wave Radar (mmWave)
      - 1.2.6 Computer Vision with Edge AI
      - 1.2.7 Passive Acoustic Array
      - 1.2.8 Sensor Comparison Table
      - 1.2.9 Operational Envelopes and Detection Probability
- 2 Strategic Foundation and Experimental Campaign
   - 2.1 Sensor Coverage Optimization for Protected Air Space (SCOPAS)
      - 2.1.1 Operational Context and Role Within Point D
      - 2.1.2 What SCOPAS Measures: Surveillance Performance Metrics
      - 2.1.3 Sensor Types and Infrastructure Parameters
      - 2.1.4 Three Strategic Planning Profiles
      - 2.1.5 Experimental Results
      - 2.1.6 Key Findings and Possible Operational Impacts
   - 2.2 Microclimate Forecasting as an Operational UTM/U-space Layer
      - 2.2.1 Operational Motivation
      - 2.2.2 International Reference Context
      - 2.2.3 Current Research State and Prototype Results
      - 2.2.4 Evolution Roadmap
      - 2.2.5 Implications for UTM Governance and BVLOS Operations
   - 2.3 Macro-Scale Strategic Layering Analysis (MSLA)
      - 2.3.1 Nominal traffic and safety parameters
      - 2.3.2 Scenario 1 — Baseline: Blind Flight
      - 2.3.3 Scenario 2 — DAA Only (Reactive)
      - 2.3.4 Scenario 3 — xTM Only (Strategic)
      - 2.3.5 Scenario 4A — Optimized xTM + DAA
         - counter Model Validation) 2.3.6 Scenario 4B — xTM + Intelligent DAA + Stochastic Wind (En-
      - 2.3.7 Summary of Experiments
      - 2.3.8 Parity with High-Fidelity Tactical Engine
   - 2.4 High-Fidelity Tactical Logic Validation (HTLV)
      - 2.4.1 HTLV Architecture and Execution Engine
      - 2.4.2 Methodological Comparison: Macro-Scale vs. High-Fidelity
      - 2.4.3 Complementary Strengths and Integration Path
      - 2.4.4 DAIDALUS Core Logic
      - 2.4.5 Scenario 2: DAIDALUS Scalability Evaluation
      - 2.4.6 Key Finding: The xTM Imperative
      - 2.4.7 Future Integration Directions
      - 2.4.8 Summary for DECEA Evaluation
   - 2.5 Multi-Sensor Simulation Campaign for Method Development
      - 2.5.1 Objective and Evaluation Questions
      - 2.5.2 Experimental Setup and Architecture
      - 2.5.3 Electro-Optical (EO) Tracking and Classification Performance
      - 2.5.4 Cross-Sensor Detection by Operational Distance Band
      - 2.5.5 Condition-Level Performance (Day/Dawn/Dusk/Night)
      - 2.5.6 Earliest Detection and Warning Relevance
      - 2.5.7 Simulation Strengths and Current Limitations
      - 2.5.8 Implications for the ABDAA Architecture
- 3 Operational Impact and Regulatory Alignment
   - 3.1 Alignment with CONOPS and SISCEAB
      - 3.1.1 Validation of Operational Premises
      - 3.1.2 Link to SISCEAB Strategic Objectives
      - 3.1.3 Compliance with SISCEAB and Federated Management
      - 3.1.4 Convergence of UTM and UAM (eVTOL) Operations
      - 3.1.5 Integration with Digital Flight Rules (DFR)
      - 3.1.6 ASTM Interoperability and Ecosystem Architecture
      - 3.1.7 Mitigation of Identified Risks
- 4 Conclusions and Strategic Vision
   - 4.1 Conclusions and Deliverables Summary
      - 4.1.1 Research Nature and Overall Assessment
      - 4.1.2 Research Maturity and Identified Limitations
      - 4.1.3 Contribution to the SIMUA Project and Future Vision


## List of Acronyms and Abbreviations

**AAM** Advanced Air Mobility.

**ABDAA** Airborne Detect and Avoid.

**ADS-B** Automatic Dependent Surveillance-Broadcast.

**ANAC** Agência Nacional de Aviação Civil.

**ATC** Air Traffic Control.

**BVLOS** Beyond Visual Line of Sight.

**CA** Collision Avoidance.

**CONOPS** Concept of Operations.

**CPA** Closest Point of Approach.

**DAA** Detect and Avoid.

**DECEA** Departamento de Controle do Espaço Aéreo.

**DFR** Digital Flight Rules.

**eVTOL** Electric Vertical Takeoff and Landing.

**HTLV** High-Fidelity Tactical Logic Validation.

**ICEA** Instituto de Controle do Espaço Aéreo.

**ITA** Instituto Tecnológico de Aeronáutica.

**MSLA** Macro-Scale Strategic Layering Analysis.

**NMAC** Near Mid-Air Collision.

**OSED** Operational Services and Environment Definition.

**PSU** Provider of Services for UAM.

**RPIC** Remote Pilot in Command.

**RWC** Remain Well Clear.


**SCOPAS** Sensor Coverage Optimization for Protected Air Space.

**SISCEAB** Brazilian Airspace Control System.

**sUAS** Small Unmanned Aircraft System.

**SUM** Sensor Uncertainty Mitigation.

**SWaP** Size, Weight and Power.

**UAM** Urban Air Mobility.

**UAS** Unmanned Aircraft System.

**USS** UAS Service Supplier.

**UTM** Unmanned Traffic Management.

**VISA** Virtual Intruder State Aggregation.

**xTM** UAS Traffic Management Extension.


## 1 Technical Foundation and Requirements

This section establishes the technical and strategic basis for the Point D milestone in the
Work Plan of the SIMUA ( _Safe Integration of different Manned and Unmanned Aircraft into
non-segregated airspace_ ) project, developed within the strategic partnership between ITA
and ICEA, formalized as the ITA-ICEA Detect and Avoid Project (DAA), in the context
of the Brazil-Sweden _Air Domain Study_ (ADS) program. It bridges the international
cooperation goals with the physical engineering requirements for safe UAS integration in
non-segregated airspace, covering the sensor architecture trade-offs and the operational
envelopes.

### 1.1 Strategic Alignment and Partnership

#### 1.1.1 Context and Motivation

The integration of Unmanned Aircraft Systems (UAS) into shared airspaces with manned
aviation is one of the fundamental milestones for the feasibility of Advanced Air Mobility
(Advanced Air Mobility (AAM)) and Unmanned Aircraft Systems Traffic Management
(Unmanned Traffic Management (UTM)). Within the scope of the strategic partnership
between ITA and ICEA, the ITA-ICEA DAA project establishes technical and financial
support for the research and development initiative of SIMUA in the context of the
Brazil–Sweden international cooperation, the ADS program.
The complexity of this initiative includes analyses of controlled airspace for AAM
flows, that requires a DAA architecture that is simultaneously resource-efficient and
highly reliable. The transition from cooperative, telemetry-based systems to hybrid
systems capable of detecting non-cooperative aircraft represents the core of challenges
addressed in the studies in this project. Additionally, scaling these operations safely
in urban environments requires integrating dynamic environmental constraints, such as
microclimate forecasting, into the operational decision-making process.
Within the ITA-ICEA DAA project as in SIMUA agreement, the Airborne Detect
and Avoid (ABDAA) architecture is defined as a methodological framework for evaluation
rather than a finalized hardware solution. This architecture serves as an investigative
baseline for exploring the feasibility of integrating UAS into non-segregated airspace,
providing a structured environment to test tactical logic against national and international
safety mandates.
While the ultimate goal of the Concept of Operations (CONOPS) includes the conver-
gence of both UTM and Urban Air Mobility (UAM), the scope of the empirical evaluations
in Point D is deliberately constrained to Small Unmanned Aircraft System (sUAS). This
provides a highly conservative baseline: if the architecture safely scales under the extreme
payload and computational limitations of a drone, it is inherently adaptable to the larger


payloads, higher-fidelity sensors, and aerodynamics of Electric Vertical Takeoff and Landing
(eVTOL) platforms in future roadmap initiatives.

#### 1.1.2 Milestone Identification – Point D

```
Point D of the ITA/ICEA Work Plan corresponds to the Architecture Demonstration
stage, equivalent to Milestone D in the Statement of Work (SoW) from the Brazil-Sweden
Agreement in the ADS context. This milestone closes the current project phase; its results
are not intended as immediately operational deliveries to Departamento de Controle do
Espaço Aéreo (DECEA), but rather as a structured body of technical understanding
to support the consolidation of alternative approaches and guide future investment and
development decisions. The main research contributions of Point D are:
```
1. The investigation of drone integration in non-segregated airspace through DAA tech-
    nologies, with explicit RWC and CA layers, documenting the conceptual feasibility
    and the principal trade-offs involved;
2. The exploration of pre-tactical sensing infrastructure optimization to support quan-
    tified cooperative and non-cooperative observability boundaries;
3. The assessment of candidate algorithms for an RWC function in cooperative scenarios
    (via Automatic Dependent Surveillance-Broadcast (ADS-B)/telemetry) and the
       investigation of alternative non-cooperative detection strategies (via onboard sensors);
4. The study of the hybrid ABDAA architecture as a scalable research baseline for
    high-density UTM environments, benchmarked against ASTM F3442 performance
    requirements for sUAS [1];
5. The development of a prototype for strategic microclimate forecasting (WRF/UCM)
    as a candidate operational layer for risk mitigation and dynamic airspace manage-
    ment.

#### 1.1.3 Partners and Responsibilities

```
The following institutional actors participate in the execution of Point D activities:
```
- **ITA** : Technical leadership in the development of simulations, sensors, algorithms
    and experiments.
- **ICEA** : Regulatory expertise (DECEA) and provision of the national operational
    scenario.


### 1.2 Architecture Definition: Strategy and Sensors

In this project, the ABDAA (Airborne Detect and Avoid) architecture is treated as a
multi-level strategic mitigation framework, rather than merely a collection of isolated
sensor hardware. This architecture serves as the foundation for safely integrating UAS
into non-segregated airspace, guided directly by the performance-based requirements and
operational constraints established in the developed CONOPS (Report Points E/F).
The architectural strategy evaluated in our simulation scenarios is based on a com-
prehensive three-layer, multi-fidelity approach that conceptually unifies the project’s five
research deliverables:

- **Strategic and Pre-Tactical Layer** : The outermost planning and flow management
    envelope. This layer investigates pre-flight infrastructure capacity limits via an
    optimization framework, analyzes traffic density scaling managed through a flow
    simulator, and presents the prototype of a dynamic environmental tool via mesoscale
    Microclimate forecasting.
- **Tactical Execution and Separation Layer** : The core active conflict management
    envelope. This addresses the interaction between operational airspace classes and the
    computational algorithms governing self-separation (RWC) and evasive maneuvering
(CA). It relies on the high-fidelity simulation evaluation of DAIDALUS-based solution.
- **Situational Awareness Layer (Sense** **_Ownship_** **)** : The foundational perception
    base embedded on the UAS. It provides the necessary real-time environmental
    awareness (distance, velocity, and angle of arrival) required by the tactical algorithms.
    This layer incorporates insights from the Multi-Sensor benchmark, exploring the
    operational trade-offs of Radar, Vision, and LiDAR under strict Size, Weight and
    Power (SWaP) constraints.

#### 1.2.1 DAA Layered Architecture: RWC and CA

In alignment with internationally accepted DAA standards [2, 1], this report adopts a
two-layer separation model:

- **RWC** : The tactical self-separation function that maintains the Well Clear volume
    between aircraft. This report presents simulated scenarios using different strategies
    and conditions to evaluate the capability to operate in _x_ TM airspace in safe and
    efficient conditions, including both simplified and DAIDALUS algorithm-based
    solutions as the RWC layer, providing alerting and maneuver guidance.
- **CA** : The emergency last-resort maneuver layer activated only when the RWC
    function has failed to prevent a loss of Well Clear. CA logic triggers aggressive
    escape maneuvers to prevent a Near Mid-Air Collision (NMAC).


Figure 1: Hierarchical structure of the ABDAA layered concept mapping the Point D
Deliverables.

#### 1.2.2 Operational Services and Environment Definition (OSED)

The Operational Services and Environment Definition (OSED) for this study maps simula-
tions to specific airspace classes as defined in the SISCEAB framework:

- **Class G** (Uncontrolled): Primary environment for initial Beyond Visual Line of
    Sight (BVLOS) UAS operations; no ATC separation service is provided. DAA
    self-separation is the sole barrier against collision.
- **Class E** (Controlled, IFR only): Transition environment where UAS must maintain
    self-separation from VFR traffic while complying with IFR clearances.
- **Classes C and D** (Controlled, IFR + VFR): High-complexity environments re-
    quiring full DAA capability with ADS-B cooperative surveillance, supplemented by
    onboard sensors for non-cooperative intruders.

The simulation campaigns (MSLA and HTLV) are proposed as an investigations tool
designed to, in future, to validate DAA performance across these operational envelopes,
with increasing complexity moving from Class G through Class C.
The remainder of this section focuses on the foundational “Sense” layer, beginning with
the sensor trade-off study and progressing to the empirically derived detection envelopes
that feed the ABDAA architecture.

#### 1.2.3 Sensor Trade-off Study: Motivation and Criteria

The selection of sensors for the ABDAA situational awareness layer is governed by SWaP
constraints and the performance framework defined in the CONOPS. These requirements
are particularly critical for small drones, such as commercial DJI platforms or custom


```
urban delivery vehicles, which represent the majority of operations in the high-density
urban corridors envisioned for the project. The core engineering challenge is to balance the
need for high spatial resolution and reliable detection with the limited payload capacity
and power budget of the ownship.
The criteria adopted for the trade-off study are:
```
- Power consumption (W);
- Module weight (g);
- Computational processing cost;
- Detection latency (ms);
- Resilience to adverse weather conditions;
- Typical detection range for UAS intruders.

#### 1.2.4 LiDAR: Evaluation and Infeasibility on Micro-UAS

While LiDAR (Light Detection and Ranging) is widely recognized for its centimeter-level
precision and ability to generate detailed 3D maps, its application as a primary DAA
sensor on micro- and small UAS faces significant physical and operational barriers. High-
performance units, such as the Ouster OS0, provide a 90 ◦vertical field of view with up
to 128 resolution channels, but consume 14–20 W in steady operation, with peak power
reaching 28 W during startup or under extreme temperature conditions [3].
For platforms whose flight autonomy is dictated by grams of battery, the mass of
approximately 430 g of the OS0 sensor, combined with the computational cost of processing
millions of points per second, renders the system impractical for micro-drones [4]. Further-
more, LiDAR performance degrades significantly in adverse atmospheric conditions such as
dense fog, smoke, or heavy rain, where laser pulses suffer from scattering and attenuation,
drastically reducing long-range detection probability of small intruder aircraft [5].
During project development a LiDAR sensor was acquired and evaluated in practical
experiments, mounted on a DJI Matrice 350, targeting detection of smaller cooperative
drones. The results confirmed limited performance, exacerbated by the sensor’s low
resolution (16 channels), indicating no practical applicability as an onboard DAA sensor
for the intended use case. Although LiDAR technology is becoming more compact and
efficient, at the time of project completion these limitations for detecting small, fast
intruders were still evident, rendering it infeasible for onboard deployment on micro-UAS.

#### 1.2.5 Millimeter Wave Radar (mmWave)

```
Millimeter-wave (mmWave) radar, exemplified by the Texas Instruments IWR6843 family,
operates in the 60–64 GHz band and provides an extremely compact, low-power solution
```

(typically 1.5–2.5 W, with transient peaks up to∼ 5 W) [6]. The FMCW (Frequency-
Modulated Continuous Wave) architecture enables simultaneous extraction of distance,
relative velocity, and angle of arrival (AoA) for multiple targets, with high immunity to
weather and lighting conditions [7].
This modality offers a trade-off of moderate spatial resolution against robust long-range
detection (on the order of 150–300 m) and strong resilience to rain, fog, and clutter, making
it particularly suitable for the early detection and cueing of small non-cooperative intruders
in urban and mixed VFR environments.

#### 1.2.6 Computer Vision with Edge AI

```
Computer vision leverages the ubiquity of lightweight cameras and recent advances in
hardware accelerators such as the NVIDIA Jetson Orin Nano and Google Coral Edge
TPU [8]. Neural networks such as YOLO enable real-time detection, though they incur
substantial computational cost [9, 10].
While the literature often reports visual detection ranges exceeding 1 km for large
aircraft (e.g., Alta 8), for small drones and lightweight visible-band cameras this capability
is significantly reduced. The small visual cross-section and limited signal-to-noise ratio
in outdoor conditions constrain the detection probability ( Pd ) at longer ranges. This
reinforces the need for mmWave radar as a primary early-cue sensor, while computer vision
handles higher-fidelity identification and precise tracking at closer ranges, where visual
conditions permit.
```
#### 1.2.7 Passive Acoustic Array

```
Passive acoustic systems, based on microphone arrays and spectral processing (e.g.,
YAMNet), offer low component cost but suffer from limited range and sensitivity to
background noise and self-noise from the ownship’s motors [11, 12]. While useful as a
supplementary modality in certain scenarios, acoustic sensing alone is not sufficient for
robust, timely DAA on small drones.
```
#### 1.2.8 Sensor Comparison Table

```
Table 1 consolidates both the physical hardware constraints (SWaP, latency) and the
operational detection envelopes ( Rmax , Twarn ) that underpin the selection of the hybrid
sensor architecture for Point D. These values reflect nominal baselines for micro-UAS
applications, where the absolute performance can vary depending on hardware variants,
algorithmic optimization, and environmental conditions.
```

```
Table 1: Consolidated Sensor Architecture: Physical Constraints and Operational En-
velopes
```
```
Modality SWaP (W – g) Latency Rmax Twarn Uncert. Critical
Degradation
Factor
ADS-B (Coop.) Ref. Standard < 10 ms > 9 km 90–120 s < 5 m MSO frequency
saturation
mmWave Radar 2 W – < 10 g 30 ms 150–300 m 15–30 s 2–5 m Ground clutter &
Low RCS
Comp. Vision 10 W – 50 g 30 ms 70–250 m 5–15 s 10–20 m Fog & Low
illumination
Acoustic Array 2 W – 100 g 150 ms 100–300 m 10–20 s > 20 m Wind & Ownship
motor noise
LiDAR (3D) 18 W – 430 g 10 ms 35–100 m < 5 s < 1 m Atmospheric
scattering (Rain)
```
```
As a research project, many different alternatives were studied and analyzed by the
team. Practical tests with LiDAR yielded weak results; image-based and acoustic solutions
were also evaluated as alternatives and remain subjects of ongoing research. Consequently,
this matrix supports a final consolidated view that a fusion between mmWave radar (for
robust early detection and proximity awareness) and computer vision (for identification
and tracking) is currently a prominent alternative. This approach discards LiDAR due to
its severe impact on the operational envelope and inefficiency with small drones, while
recognizing that acoustic solutions are still in their early experimental phases for practical
applications.
```
#### 1.2.9 Operational Envelopes and Detection Probability

The definition of input parameters for ABDAA simulations requires foundation in empirical
data. Detection envelopes establish the minimum safety distances and warning times
necessary for the system to execute effective evasive maneuvers [13], directly feeding the
operational thresholds mapped in Table 1.
For compatibility with air traffic control (Air Traffic Control (ATC)), the system must
initiate separation maintenance maneuvers ( _Well Clear_ ) with sufficient advance warning
to ensure safety margins before the closest point of approach (Closest Point of Approach
(CPA)) [14].
The probability of detection ( _Pd_ ) is a dynamic, stochastic factor that serves as the
bridge between the idealized sensor envelopes and operational reality. Rather than a static
distance threshold, _Pd_ is modeled by dynamic factors that affect each type of sensor. In
the low-altitude urban corridors analyzed in the project, this is particularly critical: the


Figure 2: Visual representation of the temporal DAA alerting envelopes around the
ownship.

probability of maintaining a firm radar track drops significantly due to ground clutter and
signal multipath in complex 3D environments. During the project execution, the multi-
sensor benchmark research (Section 2.5), become an interesting tool to allow to quantify,
at least in high fidelity simulations, how lighting and range degrade detectability, including
how computer vision models degrade in dark or non favorable wheather conditions. This
part of the reseach also aimming to, in future, support the Macro-Scale and High-Fidelity
simulations parameters definition.


## 2 Strategic Foundation and Experimental Campaign

This part presents the operational chronological flow of Point D research, from infrastructure
planning through to tactical kinematics. First, the strategic constraints are explored via
**pre-tactical infrastructure optimization** (Section 2.1) and **microclimate forecasting**
(Section 2.2) as an environmental layer. With the boundary conditions established, **MSLA**
(Section 2.3) stress-tests capacity and safety at fleet scale under strategic UAS Traffic
Management Extension (xTM) and tactical DAA layering. Next, **HTLV** (Section 2.4)
investigates the fundamental RWC capability in a high-fidelity continuous execution setup
using the standard-aligned NASA DAIDALUS algorithms. Finally, a **Multi-Sensor
Simulation Campaign** (Section 2.5) empirically investigates the “sense” side of ABDAA
to inform the tactical collision avoidance requirements. All studies in this part are ongoing
research contributions. Their central value is the _technical understanding and capability
consolidation_ they provide for future development phases, not final operational outputs.

### 2.1 Sensor Coverage Optimization for Protected Air Space (SCOPAS)

### PAS)

#### 2.1.1 Operational Context and Role Within Point D

```
Modern BVLOS drone operations in non-segregated airspace require two complementary
layers of safety infrastructure. The first layer is tactical : airborne logic that detects
approaching threats and computes avoidance maneuvers in real time, as described in
the HTLV campaign (Section 2.4). The second layer is pre-tactical : a carefully designed
ground-based sensor network that provides the surveillance picture on which all tactical
decisions ultimately depend.
Sensor Coverage Optimization for Protected Air Space (SCOPAS) addresses this second
layer. Before a single drone is authorized to fly a BVLOS route, airspace authorities and
operators must decide where to position radars, radio-frequency receivers, and electro-
optical cameras so that the protected volume is adequately monitored. A poorly designed
sensor network creates blind spots that cannot be compensated by onboard avoidance
systems alone. SCOPAS provides a reproducible methodology for support infrastructure
investment decisions, mapping every sensor layout to explicit coverage estimates and
financial cost.
Within the Point D scope, SCOPAS strategy, yet as an initial research study, aim to
acts as the infrastructure justification and planning layer : its outputs (coverage envelopes,
cost thresholds, and detectability margins) serve as the boundary conditions that define
possible operational scenarios for the tactical validation campaign. Section 3.1 describes
the cooperative and non-cooperative surveillance assumptions that SCOPAS directly
informs.
```

#### 2.1.2 What SCOPAS Measures: Surveillance Performance Metrics

To evaluate and compare sensor network designs in a consistent, operationally meaningful
way, SCOPAS employs a set of metrics specifically designed to reflect airspace authority
priorities.

**Cooperative vs. Non-Cooperative Surveillance.** SCOPAS distinguishes two funda-
mentally different surveillance regimes:

- **Cooperative traffic** comprises aircraft and UAS that actively broadcast their
    identity and position via telemetry or transponder signals (analogue to ADS-B or
    Radio Frequency (RF) remote identification). Coverage in this regime is measured
    as the fraction of the protected airspace volume in which at least one RF receiver
    can reliably decode those transmissions.
- **Non-cooperative traffic** comprises aircraft with no active broadcast — dark
    targets that must be detected kinematically using radar or electro-optical (EO)
    sensors. Coverage here reflects the fraction of airspace in which at least one radar or
    EO system achieves line-of-sight. This is substantially harder to achieve in urban
    environments due to building occlusion.

**Weighted Protection (** _Mwp_ **).** When critical assets are defined — such as an airport
terminal or a populated area — the metric assigns higher analytical weight to the airspace
volumes immediately above and around those assets. Formally:

```
Mwp =
```
```
∑
vw ( v )∑·^1 [covered( v )]
vw ( v )
```
##### , (1)

where _w_ ( _v_ ) is the threat weight of airspace cell _v_ and the indicator equals one when that
cell falls within at least one sensor’s surveillance envelope. An _Mwp_ of 1.0 means 100 %
of the threat-weighted airspace is covered; a value of 0.5 means half of the strategically
important volume has no surveillance. The complement, _vulnerabilityMvuln_ = 1− _Mwp_ ,
directly quantifies exposure to undetected intrusions.

**Fused Resilience.** For the highest-priority volumes, relying on a single sensing modality
is inherently fragile: an RF network alone cannot detect a non-broadcasting drone, and a
radar alone may lose track of cooperative traffic in busy environments. Fused resilience
measures the fraction of the threat-weighted airspace covered _simultaneously_ by both
cooperative and non-cooperative sensors, providing a dual-layer safety margin. Higher
fused resilience means the surveillance picture is maintained even if one modality is
degraded.


**Infrastructure Cost and Return on Investment.** Each sensor configuration has an
associated capital expenditure comprising hardware cost (per sensor type) and a fixed
site-activation cost per installation point. The _Asset Security ROI_ is defined as the total
investment divided by the weighted protection achieved, expressed in cost per unit of
protected airspace. This allows airspace planners to compare configurations not just by
technical performance but by economic efficiency.
Table 2 summarises the metrics and their operational interpretation.

Table 2: SCOPAS performance metrics and their operational meaning for airspace author-
ities.

```
Metric Symbol Operational meaning
Cooperative weighted protection Mwp,coop Fraction priority airspace detectable via RF/telemetry
Non-cooperative weighted protection Mwp,ncoop Fraction detectable by radar/EO (dark targets)
Vulnerability index Mvuln Unprotected fraction — direct exposure measure
Fused resilience – Airspace covered by both modalities simultaneously
Asset Security ROI – Investment per unit of protected airspace
```
#### 2.1.3 Sensor Types and Infrastructure Parameters

SCOPAS evaluates three ground-based sensor types, selected to reflect the equipment
families typically available to airspace authorities for counter-UAS or UTM surveillance
infrastructure (values are hypoteticals only to demonstrate the methodology):

- **Radar** — detects non-cooperative targets kinematically (shape, velocity). Effective
    surveillance range up to 3 km; limited vertical elevation angle (− 5 to +30 degress)
    constrains coverage of overhead corridors at very low altitudes. Unit cost: $50,000.
- **RF Receiver** — passively listens for telemetry, remote identification, and command-
    link transmissions from cooperative UAS. Wide vertical coverage (− 30 to +
    degress) makes it well suited to low-altitude urban corridors. Unit cost: $15,000.
- **Electro-Optical (EO)** — visual or near-infrared camera system for non-cooperative
    detection by line-of-sight. Useful in clear conditions; highly susceptible to occlusion.
    Unit cost: $25,000.

A fixed site-activation cost of $15,000 per installation point (representing civil works,
power, and communications) is added to the hardware cost, making sensor count and site
selection jointly important optimisation decisions.
The methodology evaluates thousands of candidate sensor placements — drawn from
candidate mounting locations such as rooftops, control towers, and perimeter fences
defined in the scenario — and identifies the combinations that deliver the best surveillance
performance at each investment level.


#### 2.1.4 Three Strategic Planning Profiles

SCOPAS supports three distinct planning modes, each targeting a different operational
requirement:

1. **Dual-Layer Safety** — simultaneously optimises cooperative and non-cooperative
    coverage alongside cost. Intended for mixed-airspace environments where both
    compliant and non-compliant traffic must be considered. Reports fused resilience
    and asset ROI.
2. **Cooperative Traffic Management** — optimises solely for compliant, broadcasting
    targets. Appropriate for UTM corridors where all participants are required to carry
    remote identification.
3. **Non-Cooperative Defense (Point Defense)** — optimises solely for radar and
    EO detectability of dark targets. Most demanding from an infrastructure standpoint;
    recommended for protection of critical assets such as airport terminals or restricted
    areas.

**Operational planning recommendation.** Analysing cooperative and non-cooperative
scenarios independently is strongly advised. Assuming that strong cooperative coverage
implies adequate non-cooperative protection is a common and dangerous planning error:
as the experimental results below demonstrate, a network that achieves 100 % cooperative
surveillance may simultaneously provide near-zero radar coverage of the same airspace.

#### 2.1.5 Experimental Results

Two experimental scenarios were evaluated to demonstrate the methodology at different
scales and operational contexts.

**Scenario 1 — Synthetic Dense Urban Environment.** The first scenario is a
synthetic 1 km× 1 kmurban grid comprising 196 building structures at realistic heights,
representing the airspace challenges of a high-density urban area. Three operational flight
altitudes were evaluated: 20 m, 45 m, and 65 m above ground level — the range typical for
BVLOS urban delivery and inspection operations.
The optimisation surveyed thousands of candidate sensor configurations, completing
the full search in approximately 8.0 hours of computational processing. The result is a set
of Pareto-optimal deployments that each represent a different balance between cost and
surveillance performance.
Figure 3 shows the obtained cost-versus-coverage trade-off front. Each point on
the curve is a valid sensor deployment; moving along the curve reveals how additional
investment, not necessarily, translates into better coverage.


```
Figure 3: Synthetic dense urban scenario ( 10 × 10 city grid, 196 buildings): Pareto-optimal
sensor deployments. Each point represents a sensor network configuration on the cost-
versus-performance frontier.
```
A representative high-performing configuration from this scenario achieved cooperative
protection of _Mwp,coop_ = 0_._ 928 across the entire threat-weighted volume at an infrastructure
cost of approximately $470,000 (13 sensor sites). The same deployment, however, delivered
only _Mwp,ncoop_ = 0_._ 139 for non-cooperative targets — meaning that more than 86 % of
the strategically important airspace remained invisible to radar and EO sensors despite
near-complete telemetry coverage. Fused resilience was 9.1 %, reinforcing that dual-layer
surveillance in dense urban terrain requires dedicated, significantly costlier infrastructure.
Figure 4 illustrates this contrast spatially: the coverage map at the lowest configuration
(8 % coverage, sparse deployment) versus the highest-investment solution (93 % coverage,
dense deployment). The progressive improvement in spatial coverage as more sensors are
added is evident.

```
(a) Low-budget configuration: 8 % aggregate
coverage.
```
```
(b) High-budget configuration: 93 % aggregate
coverage.
Figure 4: Urban scenario surveillance coverage maps. Green cells are monitored; dark cells
are blind spots. The progression illustrates the direct spatial impact of additional sensor
investment.
```
```
Scenario 2 — São José dos Campos Airport (Point-Defense). The second scenario
evaluates infrastructure at São José dos Campos Airport (SJK), using actual building
footprints and candidate sensor mounting locations derived from OpenStreetMap data.
```

```
The airport terminal was defined as the critical protected asset, receiving the highest threat
weight in the optimisation. Cooperative and non-cooperative planning were executed as
independent campaigns to reveal the full contrast between the two regimes.
```
**Cooperative surveillance — compliant UAS traffic.** The cooperative campaign
(RF-based surveillance) completed in approximately 69.5 minutes.
Figure 5 shows the cost-versus-coverage Pareto front for this profile.

```
Figure 5: SJC Airport — cooperative surveillance profile: trade-off curves for RF-based
detection of compliant UAS.
```
```
Example of Key findings that can be extarct from this sugested methodology:
```
- **Minimum viable network** : Just **three strategically placed RF receivers at a**
    **total investment of $90,000** are sufficient to achieve 99.9 % cooperative coverage
( _Mwp,coop_ = 0_._ 999 ) across all threat-weighted airspace. This represents the most
cost-efficient configuration on the Pareto front and a practical baseline for UTM
regulatory compliance.
- **Six-sensor configuration at $180,000** : delivers effectively complete (≈ 100 %)
    cooperative coverage with higher redundancy (each airspace cell monitored by an
    average of 5.4 sensors), providing resilience against individual sensor failures.
- **Full-redundancy ceiling** : Peak cooperative performance ( _Mwp,coop_ ≈ 1_._ 000 ) is
    achievable with 9 sensors at $290,000 — beyond which additional investment yields
    diminishing returns for the cooperative problem alone.

**Non-cooperative surveillance — dark targets.** The non-cooperative campaign
(radar and EO) completed in approximately 55.4 minutes.
This profile reveals the fundamental limitation of ground-based sensor infrastructure
for detecting aircraft that do not broadcast their position. Figure 6 shows the Pareto front
and cost-coverage threshold curve.
Key findings:


Figure 6: SJC Airport — non-cooperative (radar/EO) profile: trade-off curves for detection
of non-broadcasting targets. Note the hard coverage ceiling near 50 %.

- **A practical detectability ceiling exists near 50 %** : Even investing $520,000
    across eight radar/EO sites, the best achievable non-cooperative coverage for the
    airport scenario was 48.3 % ( _Mwp,ncoop_ = 0_._ 483 ). This is not a failure of the optimisa-
    tion — it is a physical consequence of building occlusion. Radar and EO sensors
    require line-of-sight, and urban structures create large persistent shadow zones that
    no feasible number of ground sensors can fully eliminate.
- **High cost, limited return** : Compared to the cooperative scenario (near-complete
    coverage for $90,000), non-cooperative surveillance of the same airspace demands
    six times the investment for roughly half the coverage. Figure 7 shows the spatial
    distribution of these blind spots.
- **Regulatory implication** : This result provides quantitative indications that ground-
    based radar/EO infrastructure alone is an insufficient safety barrier against non-
    cooperative UAS in structured airport environments. Effective detection of dark
    targets requires complementary airborne DAA systems onboard authorised aircraft,
    reinforcing the rationale for the tactical HTLV validation layer.

#### 2.1.6 Key Findings and Possible Operational Impacts

The SCOPAS experiments presented here, despite aimming to represnet actual scenarios,
should be considered hypotethical at this point. However, they are proposed alternatives
that can yield interesting conclusions for airspace authorities and UTM service providers
with a deeper consolidation in the futere, as examples we got:

1. **Cooperative surveillance is affordable and highly effective.** In our study,
    three RF receivers at a $90,000 investment would be sufficient for near-complete
    cooperative coverage of the SJC airport protected volume. This could establishes a
    reachable baseline for UTM corridor deployment and regulatory compliance.


(a) Coverage by flight level (non-cooperative). (b) Spatial coverage map — best
non-cooperative configuration.
Figure 7: SJC Airport — non-cooperative profile: altitude stratification and spatial
coverage map. Dark cells represent persistent radar blind spots caused by building
occlusion; these cannot be resolved by additional ground sensor investment.

2. **Non-cooperative surveillance has a hard physical ceiling in urban environ-**
    **ments.** Ground-based radar and EO systems cannot overcome building occlusion
    through investment alone. Authorities must not design safety cases for uncontrolled
    airspace that assume adequate radar coverage of dark targets — our examples shows
    this ceiling is approximately 50 % for the studied geometry.
3. **Cooperative and non-cooperative planning must be conducted indepen-**
    **dently.** A network designed for compliant traffic provides near-zero protection
    against non-broadcasting intrusions (in the SJC cooperative scenario, the 9-sensor,
    $290,000 RF network achieved only 4.8 % non-cooperative coverage). Planning both
    regimes simultaneously as a single requirement leads to under-designed infrastructure
    for at least one threat category.
4. **Onboard detect-and-avoid is a regulatory necessity, not an option.** Because
    no feasible ground infrastructure can guarantee full non-cooperative coverage in
    structured environments, the safety architecture must treat airborne DAA systems
    as a mandatory complement to ground surveillance. SCOPAS outputs provide the
    quantitative coverage gaps that define the residual risk that onboard systems must
    absorb.

```
Methodological scope and limitations. SCOPAS can provides reproducible, scenario-
portable infrastructure analysis at an appropriate level of planning maturity. The method-
ology still need furtehr consolidation, anyway, analysts and authorities should be aware of
the following for any similar solution:
```
- Results are sensitive to building data quality. Missing or inaccurate building heights
    cause coverage to be over-estimated, as the tool cannot model occlusion that it does
    not know exists.


- Sensor models are idealised: effects such as rain attenuation, multipath interference,
    and moving-clutter rejection are not captured. Field validation of final designs is
    required before operational deployment.

**Recommended practice for authorities.** Document the cooperative and non-cooperative
profiles separately in infrastructure procurement and safety case submissions. Use SCOPAS
similar strategies to define coverage envelopes and cost thresholds as justified boundary
conditions when specifying performance requirements for UTM service providers, and as
residual-risk quantification inputs for any onboard DAA system certification activity.


### 2.2 Microclimate Forecasting as an Operational UTM/U-space Layer

```
As UAS operations scale in complexity and duration, tactical collision avoidance provided
by the ABDAA architecture must be complemented by strategic environmental awareness.
Low-altitude urban airspace is not solely conditioned by traffic, obstacles, geography, and
administrative restrictions — it is also conditioned by microclimate. A given operational
sector may be free of geometric conflict and yet be entirely unsuitable for flight due to
excessive wind, persistent gusts, restrictive precipitation, pronounced thermal gradients,
or localized instability.
The project therefore incorporates microclimate forecasting as a foundational opera-
tional layer for UTM and U-Space integration. In this architecture, microclimate ceases
to be merely aerological background data and becomes an explicit airspace management
variable — one that directly influences pre-flight authorization, route selection, altitude
prioritization, and dynamic sector reclassification.
```
#### 2.2.1 Operational Motivation

For small-to-medium sUAS platforms, atmospheric variables impose immediate and mea-
surable effects on stability, energy consumption, navigation precision, route adherence, and
safety margins across all flight phases: take-off, transition, cruise, manoeuvre, and landing.
The central operational problem therefore extends beyond _who is flying where_ to include
_in what microclimatic environment is the flight occurring_ and _how is that environment
expected to evolve during the mission_.
This framing connects directly to the ABDAA detect-and-avoid concept. Detecting
and avoiding hazards cannot be limited to preventing geometric collisions or maintaining
separation from obstacles. The concept must also encompass the capacity to recognize
airspace volumes whose microclimate is incompatible with the mission — whether due
to risk of stability loss, battery drain acceleration, increased control effort, payload
compromise, or reduced safety margins in specific route sectors.
At the UTM governance level, the implication is equally significant. Mature airspace
services cannot rely solely on fixed rules or manual coordination. They require dynamic
restrictions, temporal windows, operational volumes, and replanning support. Microclimate
integrates naturally into this architecture because it acts directly on mission viability and
airspace safety. When treated operationally, meteorological data transforms from scientific
output into a management service.

#### 2.2.2 International Reference Context

```
International systems and research converge on a common conclusion: safe and scalable
low-altitude UAS operations depend on digital, distributed, service-based architectures.
```

```
These ecosystems — developed in North America, Europe, and across the Asia-Pacific
region — have been designed from the outset to accept supplementary data sources as
part of the operational decision process, creating direct space for operational microclimate
services.
In Europe, the U-Space regulatory environment explicitly treats atmospheric infor-
mation as operationally relevant, since it directly affects mission capability, safe window
definition, and the need for dynamic sector reclassification. The European approach
makes clear that operational data must be delivered as a service — with defined format,
frequency, reliability, and interoperability — not as a static product. Beyond visual line
of sight (BVLOS) operations, emergency response, and critical infrastructure missions
are explicitly named in European U-Space frameworks as scenarios where microclimate
services provide irreplaceable safety support.
The Brazilian context further reinforces this study’s relevance. The layered safety logic
of the BR-xTM CONOPS — strategic mission management, in-flight separation mainte-
nance, conformance monitoring, and disturbance response — is particularly compatible
with the concept of microclimate as an explicit decision variable capable of influencing
planning, dynamic restriction, and contingency management.
```
#### 2.2.3 Current Research State and Prototype Results

The research has established a functional mesoscale forecasting prototype. The operational
pipeline utilizes the Weather Research and Forecasting engine configured with a 3 km
horizontal resolution, ingesting global atmospheric data as initial and boundary conditions.
This architecture successfully extracts operationally critical variables — including air
temperature, wind vectors (speed and direction), surface pressure, and precipitation
— and disseminates these products in near-real-time via Message Queuing Telemetry
Transport (MQTT).

```
Operational Value at 3 km Resolution The prototype results confirm that 3 km
mesoscale resolution already delivers tangible operational value, even without resolving
the full urban microscale. Concretely, the system enables:
```
- **Wind gradient identification:** Regional wind fields at this resolution reveal
    speed and directional gradients across the operational area, identifying sectors with
    persistently unfavorable flow regimes versus calmer corridors.
- **Regional thermal differentiation:** Contrasts between open areas, built surfaces,
    and water bodies become identifiable, enabling preliminary classification of thermally
    unstable sectors.
- **Precipitation trend monitoring:** Precipitation onset and evolution can be tracked,
    informing mission window closure before conditions impose operational degradation.


- **Preliminary microclimatic risk assessment:** When forecast fields are cross-
    referenced with sUAS platform limits and mission geometry, the system generates a
    first-layer risk evaluation.

**Operational Decision Support** In practical operational terms, the current prototype
aims to support:

1. **Pre-flight Go/No-Go Decision:** Immediate assessment of whether atmospheric
    conditions are within safe operational envelopes at planned flight time.
2. **Preliminary Route Selection:** Identification of more favorable corridors and
    altitudes prior to departure.
3. **Sector Risk Flagging:** Marking of climatically challenging sectors along the
    planned route.
4. **Operational Window Monitoring:** Continuous tracking of atmospheric evolution
    to dynamically define safe mission windows.

**MQTT Integration Architecture** The system architecture is explicitly designed for
operational integration rather than isolated analysis. By publishing products over MQTT,
the microclimate layer enables consumption by operational dashboards, mission support
modules, flight management systems, and UTM service layers. This interoperability is
critical: it positions microclimate as a live, shared operational feed rather than a static
pre-flight consultation.

#### 2.2.4 Evolution Roadmap

The current 3 km layer represents the first operational stratum of a progressively more
capable urban microclimate service. Three complementary fronts define the evolution
roadmap:

- **Sub-kilometric Spatial Refinement:** Transitioning to grid resolutions between
    500 m and 900 m allows the system to begin differentiating open areas, densely
    built zones, thermally contrasting corridors, and persistent unfavorable wind bands.
    This spatial gain directly improves sector risk classification and mission corridor
    adherence.
- **Urban Canopy Model (UCM) Integration:** Utilizing WRF-UCM to represent
    the aggregate effect of the built environment on microclimate — including urban
    roughness, surface energy balance, and building-induced circulation — substantially
    improves adherence to real operational airspace. With greater fidelity to urban


```
roughness and thermal balance, the system provides more accurate risk identification
in the sectors and altitudes actually traversed by the platform.
```
- **Ground Sensor Network Integration:** Combining numerical forecasting with
    distributed ground-based sensors enables real-time validation, local bias correction,
    and hyper-local confidence enhancement, transforming the regional forecast into an
    urban microclimate service directly calibrated to operational conditions.

#### 2.2.5 Implications for UTM Governance and BVLOS Operations

From a UTM governance perspective, an operationally mature microclimate layer enables:

- Dynamic volumetric restrictions based on forecast atmospheric thresholds.
- Definition of preferred routing corridors via current and predicted wind analysis.
- Altitude prioritization reflecting stability forecasts across the urban canopy.
- Automated alert dispatch to service providers and operators in advance of deterio-
    rating conditions.

For BVLOS operations, this capability is particularly decisive. When the operator can-
not directly perceive the atmosphere along the route, the anticipatory value of operational
microclimate forecasting becomes especially critical. Knowing in advance that a specific
corridor is likely to degrade, that a particular altitude band is more favorable, or that a
sector should be avoided translates directly into safety and mission efficiency gains.
Ultimately, this capability positions microclimate as an explicit decision variable within
the U-Space service architecture — bridging strategic mission planning with tactical
execution, and ensuring that the low-altitude airspace ecosystem treats atmospheric risk
with the same operational rigor applied to traffic separation and obstacle avoidance.


### 2.3 Macro-Scale Strategic Layering Analysis (MSLA)

This section documents a series of large-scale computational evaluations to test the
conceptual layered model of conflict management. Operating downstream from the
theoretical surveillance coverage boundary established in the pre-tactical SCOPAS models
(Section 2.1), the MSLA explores the strategic interactions between UTM (xTM) pre-
departure reservations and tactical DAA (RWC) as complementary safety barriers.
**Methodological Note** : This macroscopic layer was developed to rapidly process 8
hours of high-density fleet logic across SJK/DCTA region. Because it focuses on thousands
of simultaneous interactions, it intentionally abstracts perception: detection is represented
by scenario rules and envelopes, while Section 2.5 proposes a structured study to deeper
understand the actual capabilities and limitations of diferent candidates for onboard DAA.

#### 2.3.1 Nominal traffic and safety parameters

```
Unless noted per scenario, runs use a nominal cruise speed of about 15 m/s for delivery-class
trajectories, altitudes between 30 and 50 m AGL within the SJK Airport geofence, and
a maximum mission distance on the order of 12 km (battery-limited sUAS profile). The
MACproxy metric follows a 20 m horizontal / 10 m vertical separation cylinder, consistent
with the ASTM F3442 family of guidelines referenced in the CONOPS. Scenario-specific
layers (reactive DAA, xTM tubes, wind) are defined in the subsections below and in
Table 3.
```
#### 2.3.2 Scenario 1 — Baseline: Blind Flight

```
The purpose of this scenario is to establish a safety baseline by measuring near-collisions
when drones operate without awareness of each other — without DAA and without
centralized UTM (xTM) management.
```
- **Operational Model** : Drones follow random origin/destination paths within the
    SJC geofence, cruising at altitudes of 30–50 m AGL.
- **Safety Metric** : Measured via _MACproxy_ (unique pairs of drones violating the
    separation of 20 m horizontal and 10 m vertical).
- **Key Results** : The experiment generates a "chaos curve" illustrating the exponential
    increase in near-collisions as drone density scales from 5 to 150 aircraft.

```
Operational Context (CONOPS Alignment) : In accordance with Section 7.1 of the
BR-xTM CONOPS, Scenario 1 establishes the "safety floor" for independent operators
in unmanaged airspace. It identifies the critical density threshold where uncoordinated
operations become unsustainable, providing the technical requirement for the introduction
of centralized UTM services.
```

Figure 8: Exponential growth of MACproxy violations as a function of unmanaged drone
density.

As shown in Figure 8, the number of MACproxy violations scales quadratically with
the density of circulating aircraft. This unmanaged environment demonstrates that even
sparse operations quickly cross unacceptable risk boundaries when relying strictly on
visual or rudimentary separation without structured UTM services. The asymptotic rise
establishes an exploratory baseline, suggesting that operation without strategic allocation
or tactical automated DAA is structurally incompatible with the risk targets in urban
zones.

#### 2.3.3 Scenario 2 — DAA Only (Reactive)

This scenario evaluates how an isolated reactive DAA layer affects safety and route
efficiency without strategic management.

- **Technique** : Drones scan for threats within a 150 m radius and execute a tangential
    evasion for 8 seconds.
- **Observations** : Although DAA significantly reduces collisions, it introduces route
    inefficiency. The system "collapses" (inefficiency _>_ 10%) at specific density thresholds.

_Operational Context (CONOPS Alignment)_ : As defined in Section 7.2 of the CONOPS,
this scenario models "Onboard Tactical Resolution." It tests the limit of aircraft autonomy
where separation management is fully delegated to the onboard system. This helps quantify


the "logistical collapse" caused by the cumulative burden of ad-hoc deviations in a dense
network without strategic deconfliction.

Figure 9: Route inefficiency caused by purely tactical reactive DAA maneuvers without
prior deconfliction.

Figure 9 delineates the route inefficiency curve. Relying strictly on a tactical DAA layer
triggers a chain reaction of maneuvers, where a single evasion forces secondary conflicts.
This “daisy-chaining” behavior inherently degrades the navigable airspace, pushing route
inefficiency beyond the 10% acceptable threshold before physical collisions actually occur.
Consequently, purely reactive systems are limited by logistical congestion rather than
absolute safety boundaries.

#### 2.3.4 Scenario 3 — xTM Only (Strategic)

Evaluates capacity when using centralized 4D trajectory reservations as the sole separation
mechanism.

- **Technique** : A centralized strategic deconfliction manager performs prior validation
    of 4D trajectory reservations (using 30 m horizontal / 15 m vertical separation
    buffers). Drones rejected from a full corridor wait in 15-second retry queues before
    reattempting.
- **Observations** : This model eliminates collision risk by design but increases ground
    delay as the airspace reaches its capacity.


_Operational Context (CONOPS Alignment)_ : Section 7.3 of the CONOPS identifies
this as "Strategic xTM Separation." In this model, UAS Service Supplier (USS) providers
synchronize 4D trajectory intents via the Discovery and Synchronization Service (DSS)
to ensure non-overlapping volumes before takeoff. This evaluates the throughput cost of
over-constraint in a purely strategic regime.

Figure 10: Average ground delay escalation due to conservative 30 m horizontal safety
buffers under a purely strategic xTM framework.

The ground delay curve presented in Figure 10 illustrates the drawback of relying
solely on a strategic UTM layer. Because drones cannot react intelligently in the air, the
xTM must assign vast 4D volumetric reserves (30 m horizontally, 15 m vertically) to assure
absolute separation under worst-case kinematic drift. As airspace demand escalates, the
system conservatively rejects takeoff requests, producing an early saturation point where
the median ground delay exceeds the allowable 5-minute logistical window.

#### 2.3.5 Scenario 4A — Optimized xTM + DAA

Demonstrates that a tactical DAA layer allows for narrower xTM corridors, increasing
total throughput.

- **Strategy** : xTM uses reduced separation tubes (22 m H / 12 m V), relying on DAA
    to handle minor tactical deviations.
- **Impact** : Significant increase in sustainable density before reaching the 5-minute
    average takeoff delay threshold.


_Operational Context (CONOPS Alignment)_ : This scenario implements the mature
hybrid architecture advocated in CONOPS Section 7.4. It follows the ICAO Doc 10019
layered safety logic by combining strategic volume allocation (via USS) with tactical
self-separation. This demonstrates that internalizing tactical resilience allows the network
to compress buffers and maximize admissibility.

Figure 11: Delayed saturation and increased operational throughput achieved by coupling
optimized 4D volume allocations with tactical DAA.

Contrasting Figure 11 with the purely strategic approach (Scenario 3) reveals a profound
shift in the throughput curve. By incorporating the active DAA layer as an in-flight safety
backup, the xTM strategic engine can significantly compress the requested 4D tube buffers
from 30/15 m to 22/12 m. This conceptual architecture models a higher sustainable fleet
density within the geofence without breaching the simulated 5-minute average takeoff
delay constraint, providing theoretical support for hybrid management.

**2.3.6 Scenario 4B — xTM + Intelligent DAA + Stochastic Wind (Encounter
Model Validation)**

This scenario serves as a validation framework using _Encounter Models_ , the standard
method for assessing DAA safety levels [15]. The stochastic wind perturbation generates
both _correlated_ encounters (aircraft on similar routes disturbed into conflicting paths)
and _uncorrelated_ encounters (random crossings), enabling a statistically representative
evaluation of the RWC function.


- **Wind Model** : Stochastic perturbation of±1.5 m/s in cruise speed, inducing
    trajectory deviations that produce encounter geometries spanning head-on, crossing,
    and overtaking configurations.
- **Encounter Types** : Correlated encounters arise from fleet operations on adjacent
    corridors perturbed by wind; uncorrelated encounters arise from independent random
    origin-destination pairs.
- **DAA Update** : Intelligent avoidance logic (RWC layer) that determines the ideal
    side of evasion (left/right) based on relative bearing.
- **Indications** : Suggests that elastic reservations with time buffer, combined with
    tactical DAA, help buffer structural safety even under unpredictable flight conditions.
    The encounter-based framework outlines a simulation environment suitable for
    drawing initial comparisons with the safety levels prescribed by ASTM F3442 [1].
_Operational Context (CONOPS Alignment)_ : As per Section 7.5 of the CONOPS,
Scenario 4B assesses "Operational Resilience" under non-deterministic disturbances. It
validates that the dual-layer management structure (intent-sharing + tactical DAA) can
prevent safety degradation even when environmental factors like wind-shear force aircraft
out of their pre-planned 4D tubes.

```
Figure 12: System resilience to kinematic uncertainty: maintaining throughput gains
under stochastic wind perturbations via continuous DAA activation.
```
Figure 12 demonstrates architectural resilience. The introduction of stochastic wind
(±1.5 to 2.0 m/s) forces frequent tactical adjustments. While ground delays intuitively


```
increase compared to the pristine nominal conditions in Scenario 4A, the hybrid system
successfully retains the structural capacity gains without breaching absolute safety invari-
ants. The intelligent DAA layer compensates for the kinetic deviations, providing robust
encounter-model validation. Notably, this persistent tactical activation introduces continu-
ous computational and communicative overhead, reinforcing the mandate for low-latency
onboard sensing parameters defined in Part 1.
```
#### 2.3.6.1 Scenario 4C — Mixed-Fleet xTM + DAA (eVTOL/UAM Proxy)

To approximate the integration of higher-performance UAM/eVTOL flows into the same low-altitude
architecture, an additional Scenario **4C** was executed using the Rust MSLA engine. This case
reuses the hybrid 4B stack — centralized 4D xTM reservations with Python4b-style tactical logic
and stochastic wind — but replaces the homogeneous sUAS fleet with a mixed set of performance
profiles. The traffic mix combines light and heavy rotorcraft with light and heavy fixed-wing
aircraft, representing higher-mass, higher-speed vehicles that act as a proxy for future eVTOL/UAM
corridor operations under the same BR-xTM governance model.

For parity with the other MSLA experiments, the mixed-fleet Scenario 4C was evaluated with
**200 physical aircraft** over a **1-hour** horizon in the SJC geofence, using the same 20 m
horizontal / 10 m vertical MACproxy cylinder and the same GA-tuned DAIDALUS configuration
adopted in Scenario 4B. Table 3a summarizes the key quantitative results for Scenarios 4B and 4C
at this density, distinguishing the baseline (geometric DAA only) arm from the DAIDALUS-enabled
arm.

```
Table 3a: Comparison between homogeneous (4B) and mixed-fleet (4C) hybrid xTM + DAA scenarios
          at N = 200 physical aircraft (1-hour horizon, SJC geofence).

Metric                          Scenario 4B (baseline)   Scenario 4B (+DAIDALUS)   Scenario 4C (baseline)   Scenario 4C (+DAIDALUS)
MACproxy (unique pairs)         71                       1337                      51                        573
DAA alert pairs                 39                       3401                      28                        3808
Completed missions              862 / 986               718 / 986                 882 / 1002                756 / 1002
Route inefficiency (%)          2.85                     47.72                     3.28                      46.41
Total real distance (10^6 m)    6.13                     6.99                      7.03                      8.16
Total ideal distance (10^6 m)   5.96                     4.73                      6.80                      5.57
```

From a safety perspective, the mixed-fleet architecture exhibits **no degradation** relative to the
homogeneous 4B case at the same density. In the baseline arm (hybrid xTM + geometric DAA, without
NASA DAIDALUS), the number of MACproxy events remains low and actually **decreases** from 71
unique violating pairs in Scenario 4B to 51 in Scenario 4C, while the number of completed missions
increases from 862/986 to 882/1002. The modest increase in route inefficiency (from 2.85 % to
3.28 %) is consistent with the longer mean mission distances and vertical stratification associated
with the higher-altitude fixed-wing/eVTOL proxy profiles.

When the DAIDALUS-based tactical arm is enabled, both scenarios exhibit the expected increase in
alert-driven maneuvering and route extension, with route inefficiency in the 46–48 % band. However,
the mixed-fleet configuration **reduces MACproxy** from 1337 to 573 unique violating pairs and
**increases mission completion** from 718/986 to 756/1002 relative to Scenario 4B. This behavior
is consistent with the introduction of altitude bands and differentiated performance envelopes:
faster, higher fixed-wing/eVTOL-like aircraft are naturally separated in the vertical dimension
and spend less time dwelling in the most saturated low-altitude layers, reducing the effective
conflict graph even though the DAIDALUS monitor flags more alert pairs overall.

From an operational-concept standpoint, Scenario 4C supports the BR-xTM premise that an architecture
validated under conservative sUAS assumptions can generalize to mixed UAS–eVTOL operations without
fundamental changes in the safety logic. The strategic xTM tubes and vertical stratification
continue to absorb most conflicts, while the DAIDALUS-aligned tactical layer preserves well clear
margins even when different classes of vehicles share the same urban terminal area. In particular,
the reduction in MACproxy under mixed-fleet conditions indicates that introducing structured
eVTOL/UAM corridors does **not** erode the safety gains established in Scenario 4B; instead, it
slightly improves resilience by distributing traffic across more diverse kinematic envelopes.

For completeness, an additional figure can be defined to visually consolidate these results:

```
Figure 12a: Comparison of MACproxy, route inefficiency and completed-mission ratios between
Scenarios 4B and 4C at N = 200. Bar charts depict (i) MACproxy counts and DAA alert pairs
for baseline and DAIDALUS arms, and (ii) route inefficiency (%) and completed-mission fractions.
The figure highlights that mixed-fleet (eVTOL proxy) operations retain the safety envelope of
Scenario 4B while slightly improving MACproxy in the DAIDALUS-enabled configuration.
```

This additional mixed-fleet experiment therefore closes the MSLA sequence by explicitly exercising
the architecture under a proxy eVTOL/UAM traffic mix. It provides quantitative evidence that the
layered BR-xTM concept, when tuned to ASTM F3442-aligned separation thresholds, can accommodate
heterogeneous low-altitude fleets without compromising the safety margins demonstrated for purely
drone-based operations.

#### 2.3.7 Summary of Experiments

```
Table 3 summarizes the features and primary metrics of the Macro-Scale Strategic Layering
Analysis scenario series.
Table 3: Comparison of Macro-Scale Strategic Simulation Scenarios
```
```
Aspect Scenario 1 Scenario 2 Scenario 3 Scenario 4A Scenario 4B
xTM No No Yes (30/15 m) Yes (22/12 m) Yes (Elastic)
DAA No Reactive No Tactical Intelligent
Wind No No No No Yes (± 1.5 m/s)
Restricted Area No No Yes Yes Yes
Primary Metric MACproxy Inefficiency Avg. Delay Avg. Delay Avg. Delay
Auto-stop None Ineff ≥ 10% Delay ≥ 5 min Delay ≥ 5 min Delay ≥ 5 min
```
**Quantitative Capacity Assessment and Tactical Overhead**
Bridging the metrics derived across the scenarios reveals that unifying narrowed
horizontal strategic buffers directly with autonomous DAA layers systematically shifts the
breakpoint of the structural limitation constraint. Rather than safety being strictly bounded
by static geometric allocation (which penalizes throughput) or purely dynamic reactive
operations (which causes unmanaged routing inefficiency), the _Point D_ architectural
solution balances both.
The capacity constraints analyzed in Figures 10 and 11 confirm that the hybrid architec-
ture delays logistical saturation. Furthermore, the wind variability stress test (Scenario 4B)
underscores a critical operational reality: under high-density perturbations, the tactical
DAA function fires on a continuous basis. This results in an elevated computational
and communicative overhead, ultimately justifying the stringent Size, Weight, and Power
(SWaP) requirements and low-latency hybrid-sensor specifications detailed in Section 1.

#### 2.3.8 Parity with High-Fidelity Tactical Engine

```
The macro-scale MSLA models derived here provide the strategic and geometric reference
behavior for the high-fidelity tactical simulations discussed in the next section. To ensure
```

consistent evaluation, key scenarios are structurally preserved as baseline reference modes
inside the unified High-Fidelity Tactical Logic Validation (HTLV) architecture, enabling
direct analytical comparisons against NASA DAIDALUS (Detect and Avoid Alerting Logic
for Unmanned Systems) maneuvers under identical georeferenced traffic streams.


### 2.4 High-Fidelity Tactical Logic Validation (HTLV)

Following the MSLA conceptual experiments, this section presents the HTLV: a prototype
high-fidelity environment incorporating NASA’s DAIDALUS as a modeled RWC reasoning
engine. The HTLV evaluates kinematic alignment with RTCA DO-365B [2] and ASTM
F3442 [1] separation guidelines through precision kinematic updates at 10 Hz (physics
step), with alert-level evaluation running continuously over a simulated 1-hour mission
window. As a research initiative, it serves to investigate rather than certify complete
operational compliance.
**Methodological Note:** To ensure the precise sub-second physics iteration required
for DAIDALUS validation, this tactical micro-simulator was custom-developed in a high-
performance compiled language. It remained in active research development throughout
Point D and is designed to become a candidate high-performance UTM/xTM research
tool for ITA and ICEA.

#### 2.4.1 HTLV Architecture and Execution Engine

The HTLV operates as a unified simulation runner coupling standard geometric avoidance
schemes with advanced RWC algorithms:

- **Simulator Core:** Built on a high-performance deterministic engine, scenarios are
    generated from structured configuration files. A custom 3-D spatial grid algorithm
    accelerates neighbor search and evaluation of the 20 m horizontal / 10 m vertical
    MACproxy separation threshold.
- **DAIDALUS Bridge:** The NASA DAA logic is compiled as a native module directly
    integrated into the simulation pipeline. The engine continuously queries DAIDALUS
    for relative aircraft pairings, extracting alert levels, time-to-violation (TTV), and
    horizontal safe-heading resolution bands.
- **Monitoring vs. Reactive Steering:** The setup physically decouples the _DAA_
    _Monitoring System_ (which populates active conflict logs) from the _Reactive Avoidance_
    _System_ (which translates DAIDALUS guidance bands into physical control inputs).
    This separation enables distinct validation of standard alerts (Preventive, Corrective,
    Warning) independent of the aircraft’s kinematic evasive response.

#### 2.4.2 Methodological Comparison: Macro-Scale vs. High-Fidelity

Table 4 highlights the complementary strengths of the two modelling approaches used
throughout the experimental campaign.


```
Table 4: Macro-Scale Simulator vs. High-Fidelity Tactical Engine
```
```
Dimension Macro-Scale (MSLA) High-Fidelity Engine (HTLV)
Physics Engine Simple kinematics (dt = 1 s) High-performance deterministic en-
gine (10 Hz)
DAA Engine Custom heuristic (proximity-based) NASA DAIDALUS (DO-365B
aligned)
Alert Information Binary (Threat / No Threat) Multi-level (Preventive / Corrective
/ Warning), TTV, Heading Bands
Avoidance Maneuver Fixed angular (60–90°) heuristic DAIDALUS Bands + Horiz./Vert.
offsets
Scale Up to 2 000 concurrent UAS Up to 1 000 concurrent UAS (1-hour
window)
Simulation Speed Near-realtime (up to 1 600×) Dependent on conflict graph size (1–
6 500×)
```
Figure 13: Visualization of a saturated airspace simulation around SJC Airport with
_N_ = 500 simultaneous drones operating under DAIDALUS guidance. The trajectory
entanglement visible in the dense corridor illustrates the combinatorial interaction growth
that drives the scalability limits detailed in Section 2.4.5.

#### 2.4.3 Complementary Strengths and Integration Path

The **MACproxy Macro-layer** effectively assesses the three-layer conflict management
model defined in the CONOPS — Strategic (xTM), Tactical (DAA), and Collision Avoid-
ance. It utilises real SJC geography and produces metrics directly applicable to capacity
scoping with large drone populations.


```
The HTLV Micro-layer provides the increased fidelity level necessary to investigate
algorithmic alignment with international guidelines such as RTCA DO-365B [2] and ASTM
F3442 [1]. Its localized physics engine resolves finer kinematic details during simulated
RWC avoidance maneuvers.
```
#### 2.4.4 DAIDALUS Core Logic

```
The DAIDALUS algorithm constitutes the mathematical backbone of the HTLV. Within
the DAA layered architecture, DAIDALUS implements the RWC function as defined in
RTCA DO-365B [2]: it transforms surveillance data into maneuver guidance ( Bands )
for the Remote Pilot in Command (RPIC) or autonomous system, with the objective of
maintaining the Well Clear separation volume.
Justification for Evaluation: DAIDALUS was selected for integration because it
serves as the globally recognised aviation-authority reference implementation for DO-365B.
Evaluating it inside the SIMUA parameters answers a critical regulatory question: Can
standardised mathematical compliance models developed for sparse airspace scale safely
into Brazilian high-density urban corridors? Importantly, DAIDALUS operates strictly on
immediate kinematic state vectors (current position and velocity) rather than tracking
pre-planned mission routes. This fundamental characteristic decouples tactical collision
avoidance from strategic 4-D paths, making it the ideal testbed to investigate how onboard
autonomy impacts overarching fleet operations.
```
```
Cooperative vs. Non-Cooperative Operational Modes In a cooperative airspace,
DAIDALUS operates with high-fidelity telemetry data (ADS-B), assessing the Well-Clear
timeline using exact time-to-convergence inequalities based on minimum vertical/horizontal
separation thresholds [16]. The strategic differentiator of the Point D architecture is
its planned behaviour when fed by onboard sensors (Radar and Vision) detecting non-
cooperative aircraft, which provide data characterised by noise and systematic measurement
errors.
```
**Planned Extension: Sensor Uncertainty Mitigation (SUM) and VISA Smooth-
ing** The DAIDALUS framework natively supports Sensor Uncertainty Mitigation (SUM)
( _Sensor Uncertainty Mitigation_ ) [17], which uses error distributions ( _z_ -scores) to dynami-
cally expand the Well Clear volume into a safety ellipsoid encompassing the intruder’s
“worst probable position,” and Virtual Intruder State Aggregation (VISA) ( _Virtual In-
truder State Aggregation_ ), which smooths temporal jitter by averaging consecutive sensor
updates [18].
**Current experimental scope:** All scalability runs presented in Section 2.4.5 operate
under _cooperative perfect-state_ assumptions (exact position and velocity vectors), so neither
SUM expansion nor VISA smoothing was exercised in the results reported here. Activating


SUM with realistic onboard-sensor noise profiles (mmWave Radar, Computer Vision) is a
programmed next step that will widen the effective Well Clear volume and is expected to
increase both alert rates and route inefficiency — quantifying that penalty is a priority for
the next project phase.

**Planned Extension: Human-in-the-Loop (HITL) Alerting Validation** The
DAIDALUS alert taxonomy maps to absolute reaction timelines relevant for RPIC author-
ity [14]: **Preventive** (∼60 s to CPA), **Corrective** (∼30 s), and **Warning** (∼15 s). While
these thresholds are configured in the current HTLV engine, the scalability sweep does not
yet inject RPIC reaction latency or decision-loop delays into the simulation. Validating
that the 5–15 s pilot network latency budget [14] is safely absorbed under dense traffic
conditions remains an explicit future-work objective.

**DAIDALUS Steering Strategies Under Evaluation** Two complementary DAIDALUS-
mediated steering strategies were evaluated in the scalability sweep:

1. **Continuous Safe Band:** At every physics step, the engine selects the nearest
    heading within the current DAIDALUS _safe band_ (i.e. the set of headings that do
    not violate the Well Clear volume for any tracked intruder) and blends that heading
    continuously into the active trajectory. This approach produces the smoothest flight
    path and maximises compliance with the full DAIDALUS resolution logic.
2. **Preferred Horizontal Resolution:** Rather than blending across the full safe band,
    the engine hard-couples to the single optimal avoidance heading recommended by
    the DAIDALUS _preferred resolution_ output at each update. This yields a more
    decisive turn toward the algorithmically chosen escape direction.

Both modes are compared against a **No-DAIDALUS baseline** that uses a simple
proximity-triggered angular maneuver (the same heuristic used in the MSLA), providing
the reference “blind flight” degradation curve.

#### 2.4.5 Scenario 2: DAIDALUS Scalability Evaluation

To push beyond single-encounter validation, a large-scale tactical resolution sweep was
executed within the HTLV unified runner. This benchmark compares the no-DAIDALUS
baseline against the two DAIDALUS steering strategies under fixed geographic and
temporal parameters over a 1-hour simulation window. Fleet densities ranged from _N_ = 50
to _N_ = 1 _,_ 000 simultaneous drones in the geofenced corridor.

**Full Cross-Density Results** Table 5 presents the complete sweep across all density
levels. The metrics are: **CR** — mission completion ratio (completed / scheduled); **MAC**


— total MACproxy events (20 m horizontal / 10 m vertical violations); **Ineff.** — route
inefficiency percentage (excess distance relative to ideal chord); **Wall** — simulator wall-
clock time.
Table 5: DAIDALUS Scalability Sweep — Scenario 2, 1-hour window, 10 Hz physics,
_N_ = 50 to _N_ = 1 _,_ 000.

```
Mode N CR MAC Ineff. (%) Wall (s)
Preferred Horizontal Resolution 50 0.853 0 6.22 4.6
100 0.856 0 8.33 14.5
200 0.851 2 11.85 49.9
500 0.774 36 49.73 623.3
1000 0.306 1 202 90.85 11 447.9
Continuous Safe Band 50 0.853 0 3.68 3.0
100 0.860 5 6.61 12.7
200 0.857 33 14.98 65.7
500 0.724 1 619 66.46 1 574.6
1000 0.334 19 050 138.48 14 721.0
Baseline (No DAIDALUS) 50 0.849 0 4.41 0.5
100 0.856 0 8.16 0.9
200 0.843 0 19.74 2.3
500 0.774 42 70.17 13.2
1000 0.460 3 601 145.56 155.5
```
```
Head-to-Head: DAIDALUS vs. No-DAIDALUS Baseline Table 6 distills the
direct comparison between the best DAIDALUS mode at each density level (Preferred
Horizontal Resolution) and the proximity-only baseline to highlight where standard-aligned
RWC guidance adds value — and where it becomes counterproductive.
Three distinct operational regimes emerge from this comparison:
(i) Low density ( N ≤ 100 ): equivalent safety, comparable efficiency. Both
modes record zero MACproxy events, similar completion rates (≈85%), and nearly identical
route inefficiency. At these densities the encounter rate is low enough that the simple
proximity heuristic suffices; DAIDALUS adds algorithmic rigour and standard-aligned
alerting but does not yet differentiate operationally in the metrics measured.
(ii) Moderate density ( N = 200 – 500 ): DAIDALUS improves route quality.
This is the regime where DAIDALUS delivers its clearest advantage. At N = 200, the
baseline’s proximity heuristic generates 19.7% route inefficiency while DAIDALUS
achieves 11.9% — a≈40% reduction in excess path distance — with comparable safety
```

```
Table 6: DAIDALUS (Preferred Horizontal Resolution) vs. No-DAIDALUS Baseline —
direct comparison at each density level. ∆Ineff. shows the route inefficiency reduction
provided by DAIDALUS (positive = DAIDALUS is more efficient).
```
```
MAC Events Route Ineff. (%) Completion Ratio
N Baseline DAIDALUS Baseline DAIDALUS Baseline DAIDALUS
50 0 0 4.41 6.22 0.849 0.853
100 0 0 8.16 8.33 0.856 0.856
200 0 2 19.74 11.85 0.843 0.851
500 42 36 70.17 49.73 0.774 0.774
1000 3 601 1 202 145.56 90.85 0.460 0.306
```
(2 MACs vs. 0). At _N_ = 500, DAIDALUS reduces MAC events from 42 to 36 _and_
simultaneously cuts route inefficiency from 70% to 50%. The advantage arises because
DAIDALUS computes the _minimum-deviation safe heading_ via the Well Clear inequality,
whereas the proximity heuristic applies a fixed angular offset that often over-corrects. For
battery-constrained sUAS, this 20–30 percentage-point route saving translates directly
into extended operational range and mission feasibility.
**(iii) High density (** _N_ = 1 _,_ 000 **): reactive saturation crossover.** At extreme
density, the comparison inverts. DAIDALUS reduces MAC events (1,202 vs. 3,601 for
the baseline) but at a severe cost: completion ratio drops to 30.6% versus the baseline’s
46.0%, and the Continuous Safe Band variant generates **19,050** MAC events — _5.3_ ×
_worse than no guidance at all_. This paradoxical inversion signals the onset of _reactive
oscillation deadlock_.

**Root Cause: Reactive Oscillation Deadlock at Scale** The wall-clock data reveals
the physical mechanism behind the high-density collapse. Continuous Safe Band requires
14,721 s (≈4 hours) to simulate a 3,600 s scenario at _N_ = 1 _,_ 000 , an amplification factor of
4_._ 1 ×the simulated time, compared to 0_._ 04 ×for the baseline. This growth is consistent
with the _O_ ( _N_^2 ) structure of the DAIDALUS pairwise evaluation graph: at _N_ = 1 _,_ 000 ,
the engine evaluates **102,655 alert pairs** per step versus 74,055 for the baseline.
The continuous re-querying triggers _heading oscillations_ across multiple interacting
pairs: each drone adjusts heading in response to newly generated conflicts caused by the
previous step’s adjustments, creating a feedback loop that prevents mission completion
and paradoxically _increases_ the total number of separation violations. Preferred Horizontal
Resolution exhibits qualitatively similar behaviour (wall-clock: 11,448 s), confirming that
pairwise re-evaluation dominates regardless of how the resolution heading is selected.
**Implication:** DAIDALUS, as a pairwise reactive algorithm designed for sparse co-
operative encounters (DO-365B), was not architecturally intended for dense multi-agent
environments where cascading pair interactions dominate. The scalability sweep empirically


demonstrates the density threshold ( _N_ ≈ 300 – 500 in a 5 km corridor) at which reactive
logic alone becomes insufficient and strategic pre-separation (xTM) becomes operationally
mandatory.

**Performance Trends** The following charts illustrate the degradation curves as the
number of drones ( _N_ ) increases across the geofenced corridor.

Figure 14: Mission completion ratio vs. fleet
size. Both DAIDALUS modes sustain above
80% completion through _N_ = 200, then
degrade sharply. At _N_ = 1 _,_ 000 , completion
drops below 35%, indicating the reactive
saturation limit.

```
Figure 15: MACproxy count (safety viola-
tions) vs. fleet size. Continuous Safe Band
generates 19,050 violations at N = 1 , 000 —
exceeding the 3,601 of the no-DAIDALUS
baseline — confirming the reactive oscilla-
tion deadlock.
```
Figure 16: Route inefficiency (%) vs. fleet
size. Continuous Safe Band reaches 138%
excess distance at _N_ = 1 _,_ 000 , rendering
battery-constrained sUAS missions infeasi-
ble. Even at _N_ = 500, the 50–66% penalty
imposes severe operational constraints.

```
Figure 17: Simulator wall-clock time vs.
fleet size. The O ( N^2 ) computational growth
of the DAIDALUS pairwise evaluation is
clearly visible, reaching over 14,000 s for
Safe Band at N = 1 , 000 — a 94×slowdown
relative to the baseline.
```
#### 2.4.6 Key Finding: The xTM Imperative

The sweep results provide the empirical foundation for a central conclusion: **DAIDALUS
alone is necessary but not sufficient for high-density UTM operations.**


At low-to-moderate densities ( _N_ ≤ 200 ), the DAIDALUS-based RWC layer effectively
resolves conflicts with near-zero safety violations and acceptable route penalties. This
validates DAIDALUS as a viable tactical backbone for initial BVLOS deployments in the
density regimes targeted by SIMUA.
Beyond _N_ ≈ 300 – 500 , however, the pairwise reactive nature of DAIDALUS encounters
a fundamental scalability ceiling: cascading pair interactions generate oscillatory heading
adjustments that degrade both safety and efficiency below the no-guidance baseline. This
is not a flaw in the DAIDALUS algorithm — it performs precisely as designed for sparse
encounter geometries — but rather a confirmation that **high-density corridors require
strategic pre-separation (xTM)** to reduce the effective encounter rate before tactical
DAIDALUS logic engages.
This finding directly reinforces the layered architecture proposed in the CONOPS:

1. **Strategic layer (xTM):** Pre-tactical flow management, route deconfliction, and
    temporal separation to keep the effective _N_ within the DAIDALUS operational
    envelope ( _N_ ≤ 200 – 300 for a 5 km corridor).
2. **Tactical layer (DAIDALUS):** Real-time RWC guidance for residual conflicts that
    escape strategic deconfliction, operating in the density regime where it is proven
    effective.
3. **Collision avoidance layer:** Last-resort emergency maneuvers for encounters that
    breach the RWC boundary.

The MSLA results, which independently demonstrate the effectiveness of xTM in reducing
encounter rates at fleet scale, are therefore _directly complementary_ to the HTLV findings:
together they validate the full strategic-to-tactical pipeline.

#### 2.4.7 Future Integration Directions

The HTLV is designed as a modular research platform. The results above suggest two
concrete integration directions for subsequent project phases.
First, the DAIDALUS resolution logic should be integrated as the tactical avoidance
engine within the MSLA fleet simulator, replacing the current macroscopic heuristic. This
closed-loop integration will allow quantification of how xTM pre-separation + DAIDALUS
tactical guidance perform together across the full density range, and will empirically
determine the minimum xTM separation requirements that keep DAIDALUS within its
effective operating envelope.
Second, once the multi-sensor benchmark as sugested in Section 2.5 can produces
calibrated detection probability profiles per sensor and lighting condition, those empirical
envelopes can be injected into the HTLV pipeline as the source of intruder state estimates —


replacing the current idealised perfect-state assumption and enabling end-to-end evaluation
of the full sense-to-avoid chain under realistic uncertainty budgets.

#### 2.4.8 Summary for DECEA Evaluation

The sequential value chain — from mathematical pre-tactical capacity bounding in SCO-
PAS, through macroscopic 4-D strategic reservations (MSLA), down to high-fidelity,
algorithmically aligned tactical deviation (HTLV) — models a holistic conceptual approach
for managing UAS traffic in Brazilian airspace.
The DAIDALUS scalability sweep provides three operationally relevant conclusions for
DECEA assessment:

1. **DAIDALUS is effective as a tactical RWC layer at operationally relevant**
    **densities.** At _N_ ≤ 200 (the regime corresponding to initial BVLOS deployments),
    both steering modes achieve near-zero safety violations with completion rates above
    85% and route inefficiency below 15%.
2. **A hard scalability ceiling exists for reactive-only guidance.** Beyond _N_ ≈ 300 –
    500 , DAIDALUS-only control collapses due to cascading pairwise oscillations. At
    _N_ = 1 _,_ 000 , the system generates more separation violations than the no-guidance
    baseline, confirming that reactive logic alone cannot sustain high-density operations.
3. **Strategic pre-separation (xTM) is mandatory above the tactical ceiling.**
    The results empirically validate the layered xTM + DAIDALUS architecture proposed
    in the CONOPS: xTM keeps the effective encounter rate within the DAIDALUS
    operational envelope, while DAIDALUS handles residual conflicts with proven effec-
    tiveness.

**Transition: from RWC kinematics to the sense layer.** The HTLV pipeline assumes
that intruder state estimates are available to DAIDALUS at the required rate and with
modelled uncertainty. It does not quantify _which_ onboard sensor provides the earliest
cue, or how _Pd_ falls with range and lighting, those are properties of the perception stack.
Section 2.5 therefore presents proposed methodology with a synchronized benchmark, as
an alternative to develop consolidated data to suport those uncertainty.


### 2.5 Multi-Sensor Simulation Campaign for Method Development

To complement the strategic capacity analysis (MSLA) and the tactical logic validation
(HTLV/DAIDALUS), we conducted a synchronized multi-modal simulation campaign to
empirically investigate the _sense_ layer of the ABDAA architecture. While Sections 2.3
and 2.4 evaluate whether the airspace management and avoidance logic can maintain safe
separation _given_ intruder state estimates, this section asks the preceding question: **which
onboard sensor can actually detect a non-cooperative intruder, at what range,
under what conditions, and how reliably?**
For DECEA evaluators and ATC-oriented readers, the results should be interpreted
as method-development evidence that clarifies practical constraints and sensor comple-
mentarity — not as certification-grade performance claims. The campaign establishes
quantitative foundations for the SUM/VISA uncertainty parameters that feed DAIDALUS,
and identifies which modalities provide the earliest tactical cueing under the SWaP
constraints.
The experiments detailed in this section were primarily executed within high-fidelity
simulations to refine the underlying methodology and deepen the technical understanding
of multi-modal sensing challenges. These efforts were complemented by some real-world
evaluations conducted throughout the project’s duration. This aim to be a symbiotic
development cycle: empirical field data provided critical insights for improving simulation
fidelity, while simulation results directly guided hardware acquisition, sensor selection, and
the planning of subsequent flight experiments.

#### 2.5.1 Objective and Evaluation Questions

```
The campaign addresses three operationally motivated questions directly relevant to the
ABDAA architecture:
```
1. **Earliest warning** : Which sensor detects the intruder first, and at what range does
    that initial detection typically occur? This determines which modality can trigger
    the Preventive Alert timeline (∼60 s to CPA) required by the HITL alerting design.
2. **Detection reliability vs. distance** : How does the probability of acquiring the
    intruder degrade as range increases for each modality? This defines the effective
    detection envelopes that feed DAIDALUS SUM uncertainty expansion.
3. **Environmental robustness** : Do lighting and weather conditions (day, dawn, dusk,
    night, fog, rain) differentially degrade specific sensors? This informs the operational
    need for multi-modal redundancy rather than reliance on a single technology.

```
These questions structure future validation phases, including no-intruder clutter cam-
paigns and mixed-reality flight tests, rather than claiming immediate field readiness.
```

#### 2.5.2 Experimental Setup and Architecture

- **Simulation environment** : Cosys-AirSim [19] high-fidelity rendering and physics
    engine, used exclusively as a controlled technical platform for evaluating sensor
    boundaries. It provides synchronized multi-modal data at identical operational
    frames — ensuring that a detection event on any modality is directly tied to the
    exact physical range recorded in the telemetry at that instant.
- **Encounter scenarios** : 30 distinct encounter geometries generated by the Experi-
    ment 30 campaign, varying approach azimuth, vertical separation, weather (clear,
    fog, rain, dust, snow), and lighting (day, dawn, dusk, night). These geometries force
    the sensor suite to resolve intruders against variable visual backgrounds and varying
    atmospheric conditions.
- **Electro-optical (EO) tracking** : Four forward-facing camera configurations — wide-
    angle low-cost (640 px), medium field-of-view, standard forward, and narrow high-
    definition — process visual streams through neural-network-based object detection.
    The tracking models were trained on thousands of simulated aerial encounters derived
    from segmentation-based ground truth, providing consistent target acquisition across
    optical configurations.
- **Cross-sensor alignment** : Radar returns, LiDAR point clusters, and EO detec-
    tions are strictly aligned against internal simulation telemetry (dist_xy_m). This
    guarantees that every detection is indexed to the true intruder range, enabling fair
    cross-modal comparison within the same encounter frame.
- **Sensor payload evaluated** : The four modalities correspond to the SWaP-constrained
    architecture defined in Table 1 (Section 1.2.8):
       **-** _FMCW Radar_ : return-presence early-warning cueing (analogous to mmWave
          module);
       **-** _High-Density LiDAR_ (OS128 profile): geometric point-cloud acquisition for
          spatial confirmation;
       **-** _Sparse LiDAR_ (VLP16 profile): reduced-density alternative evaluated for SWaP
          comparison;
       **-** _Electro-Optical (EO/Vision)_ : multiple lens configurations for semantic classifi-
          cation and visual tracking.

Figure 18 illustrates representative frames under the principal weather and lighting
regimes used in Experiment 30, complementing the encounter list above.


```
Figure 18: Representative simulation frames under six environment conditions evaluated in
Experiment 30. The campaign spans clear daylight, dusk, rain, night, snow, and dust/haze,
providing a controlled basis for assessing sensor robustness across the operational envelope.
```
#### 2.5.3 Electro-Optical (EO) Tracking and Classification Performance

```
A key operational question for the EO component is whether the onboard visual system
can reliably acquire and classify a small intruder drone across the range of optical hardware
likely available on sUAS platforms. To answer this, we trained and evaluated detection
models under two strategies:
```
1. **Specialized per-lens training** : A dedicated model for each camera type, optimized
    exclusively for that hardware’s resolution and field of view.
2. **Unified multi-camera training** : A single model trained on pooled imagery from
    all four cameras, tested for cross-platform generalization.

Table 7 reports the results of the specialized approach. All models were trained under
identical conditions (100 epochs, early stopping). The reliability metrics (precision, recall,
and detection consistency at standard overlap thresholds) are summarized to characterize
the detection envelope of each optical configuration.
Table 8 reports the cross-platform evaluation: a single unified model — trained once
on pooled data from all cameras — is tested on each camera’s validation set independently.
This answers a practical deployment question: _can one software package serve all optical
hardware, or must each camera carry a dedicated model?_

```
Operational interpretation. The unified model matches or exceeds specialized models
across nearly all optical configurations. This validates a single-software deployment for
diverse camera hardware — reducing maintenance burden and certification scope for
```

```
Table 7: EO detection reliability per optical configuration (specialized training). Higher
values indicate more consistent intruder acquisition.
Optical stream Train Val Precision Recall Det. rate Loc. quality
Pooled multi-camera 680 170 0.952 0.941 96.4% 73.1%
Narrow HD (long-range) 162 41 0.963 0.878 90.9% 66.3%
Medium FOV 215 54 0.939 0.926 95.6% 67.2%
Low-cost wide (640 px) 148 37 0.973 0.992 99.4% 68.9%
Det. rate : fraction of validation encounters where the intruder was correctly detected (mAP50). Loc.
quality : spatial accuracy of the detection box across stricter overlap thresholds (mAP50–95). Higher
localization quality implies tighter spatial estimates, which reduce the SUM uncertainty expansion
required by DAIDALUS.
Table 8: Cross-platform generalization: unified EO model evaluated on each camera’s
validation set. A single software deployment covers all optical hardware without per-lens
recalibration.
Evaluated on Val imgs Precision Recall Det. rate Loc. quality
Pooled multicam 170 0.964 0.953 97.2% 73.4%
Narrow HD only 41 0.973 0.866 91.7% 70.0%
Medium only 54 0.928 0.961 96.7% 70.7%
Low-cost only 37 0.991 1.000 99.5% 74.1%
```
```
operational integration. The narrow HD lens shows a minor recall reduction (86.6% vs.
87.8% for its specialist), attributable to its smaller training set; this nuance becomes
operationally relevant only at extreme long-range encounters where the narrow field of
view severely crops the intruder silhouette.
For the ABDAA fusion pipeline, the key operational takeaway is that EO tracking
achieves > 90% detection rates in the 25–100 m operational band (Table 9), providing
the semantic classification capability that radar and LiDAR cannot offer. In this critical
engagement zone, EO matches or exceeds LiDAR HD, positioning it as a primary classifi-
cation and identification layer within the DAIDALUS SUM logic rather than a last-resort
confirmation sensor.
Figure 19 illustrates qualitative acquisitions on all four camera streams in a single
encounter (Tables 7–8 give the corresponding quantitative scores).
```
#### 2.5.4 Cross-Sensor Detection by Operational Distance Band

This subsection addresses the most operationally consequential question: _at what range
can each sensor modality reliably acquire the intruder?_ The answer directly determines
the available warning time for DAIDALUS alert levels (Preventive at∼60 s, Corrective at
∼30 s, Warning at ∼15 s to CPA — see Section 2.4.5).
Table 9 and Figure 20 present the detection rate stratified by ground-truth distance.
The EO column uses the trained YOLOv8s unified model evaluated on all four camera
streams across the full Experiment 30 dataset (976 unique frames, 30 encounter runs), with


```
Figure 19: EO detection results across four camera configurations during the same
encounter sequence. Green bounding boxes represent automated intruder acquisition. The
visual demonstrates that a single unified detection model successfully acquires the intruder
across all optical hardware.
```
```
an any-camera-detects policy (a frame is counted as detected if at least one optical stream
produces a valid detection). LiDAR and Radar values are from the original synchronized
benchmark.
Global frame-level detection rates:
```
- **Radar (FMCW return-presence)** : 100.0% (640/640 frames)
- **LiDAR High-Density (OS128 profile)** : 63.1% (404/640)
- **EO/Vision (YOLOv8s, unified multi-camera)** : 49.7% (485/976 frames)
- **LiDAR Sparse (VLP16 profile)** : 16.1% (103/640)

**Operational interpretation for DAA timeline.** The 100% radar acquisition reflects
_return-presence detection_ : the sensor registers anomalous mass in the airspace, acting as
a high-availability early-warning trigger. It does not inherently classify the target (e.g.,
drone vs. bird), which is why the ABDAA architecture delegates semantic confirmation
downstream to LiDAR and EO.


Table 9: Detection rate (%) by intruder distance. EO: unified YOLOv8s model, any-
camera-detects policy (976 frames, 30 runs). LiDAR/Radar: synchronized benchmark
(640 frames, 29 runs).

```
Distance (m) EO/Vision LiDAR HD LiDAR Sparse Radar
0–10 55.6 77.6 29.9 100.0
10–25 44.3 77.1 32.1 100.0
25–50 91.1 67.7 16.5 100.0
50–100 100.0 55.4 11.2 100.0
100–150 2.0 58.5 0.0 100.0
150–250 0.0 6.7 0.0 100.0
The EO detection drop at 0–25 m reflects approach geometry: the intruder has passed the observer or
fills/exceeds the frame, reducing model confidence. Peak EO performance occurs in the 25–100 m
operational band most relevant to the Warning and Corrective Alert envelopes.
```
The trained EO model achieves 91–100% detection rates in the 25–100 m operational
band (Table 9), matching or exceeding LiDAR HD in the Corrective and Warning Alert
distance envelopes. The lower EO rates at very close range ( _<_ 25 m) are a geometric
artifact: the intruder has passed the observer plane or overflows the camera frame. At
long range ( _>_ 100 m), the intruder’s angular size drops below the minimum detectable
pixel footprint for most lens configurations, with only the narrow HD camera occasionally
acquiring targets at that distance (96.3% at 50–100 m).
For the DAIDALUS alerting timeline, radar triggers the Preventive Alert envelope
(≥60 s to CPA) at maximum evaluated range. EO now contributes reliable target clas-
sification across the 25–100 m band — covering both the Corrective and Warning Alert
envelopes and supporting RPIC positive identification with high confidence.

#### 2.5.5 Condition-Level Performance (Day/Dawn/Dusk/Night)

```
Environmental robustness is a critical operational concern for BVLOS operations in
Brazilian airspace, where missions may span lighting transitions. Table 10 segments the
synchronized benchmark by lighting condition.
Table 10: Detection rate (%) by lighting condition. EO: unified YOLOv8s, any-camera-
detects (30 runs). LiDAR/Radar: synchronized benchmark (29 runs).
Condition Frames EO LiDAR HD LiDAR Sparse Radar
Day 440 48.6 62.0 15.6 100.0
Dawn 271 39.5 58.2 14.5 100.0
Dusk 183 60.1 75.9 18.5 100.0
Night 82 65.9 65.1 19.0 100.0
```
```
Key observations.
```

```
0 10 1025 2550 50100 100150 150250
Banda de distância (m)
```
```
0
```
```
20
```
```
40
```
```
60
```
```
80
```
```
100
```
```
Taxa de deteção (%)
```
```
Benchmark alinhado 640 frames taxa por modalidade e distância
RGB YOLO (ref. HD)LiDAR OS128
LiDAR VLP-16Radar (presença)
```
```
Figure 20: Detection rate vs. intruder range across all four modalities. EO (YOLOv8s)
achieves 91–100% in the 25–100 m operational band, matching or exceeding LiDAR HD.
Radar provides continuous presence awareness at all ranges, while LiDAR and EO offer
complementary geometric and semantic confirmation.
```
- **Radar and LiDAR are lighting-invariant** : Their detection rates remain stable
    across all conditions, confirming their suitability as the primary and secondary cueing
    layers regardless of time-of-day. This is operationally essential for 24-hour BVLOS
    corridors.
- **EO performs across all lighting conditions** : Unlike the legacy evaluation, the
    trained YOLOv8s model achieves 39.5–65.9% frame-level detection across all lighting
    conditions, with no complete failure at dawn. Counter-intuitively, dusk and night
    conditions show higher EO rates; this likely reflects the higher contrast of the intruder
    against dimmer sky backgrounds, improving neural-network saliency.
- **LiDAR HD shows slight improvement at dusk/night** : Reduced ambient light
    may reduce background clutter in the point cloud processing, though this requires
    further investigation with larger sample sizes.

#### 2.5.6 Earliest Detection and Warning Relevance

For DAA system design, the most operationally decisive metric is _which sensor detects
the intruder first_ in each encounter, and _at what range_ that first detection occurs. This
directly determines whether the system provides sufficient warning time for the DAIDALUS
Preventive → Corrective → Warning alert cascade.

**First-detection winner per encounter.** In the original synchronized benchmark
(29 runs, Radar/LiDAR/legacy-EO on identical frames, tie-shared counting), the first-


detection ranking was: Radar first 65.9%, LiDAR HD 31.4%, EO 2.1%, LiDAR Sparse
0.7%. However, with the trained YOLOv8s model, EO now achieves first detection in _all_
30 encounter runs at a mean range of 79.3 m (median 81.6 m, max 143.5 m). While a fully
re-synchronized multi-sensor comparison is planned for the next campaign, the updated
EO capability would significantly increase EO’s share of first-detection events, particularly
in the 50–100 m band where it now achieves 100% frame-level detection.

**Mean range at first detection:**

- Radar: 116.9 m mean, 117.1 m median ( _n_ =29 runs)
- LiDAR HD: 113.2 m mean, 117.1 m median ( _n_ =19 runs)
- EO/Vision (YOLOv8s): 79.3 m mean, 81.6 m median ( _n_ =30 runs, max 143.5 m)
- LiDAR Sparse: 24.6 m mean ( _n_ =1 run)

**Operational significance for the ABDAA tactical sequence.** These first-detection
ranges map directly onto the alerting timeline architecture defined in Section 2.4.5. At a
typical sUAS closure speed of 15 m/s:

- **Radar at** ∼ **117 m** ⇒ ∼ **7.8 s** to CPA. Under the current simulation envelope, this
    provides the initial unclassified cueing trigger. For the target 60 s Preventive Alert,
    longer-range radar capability or earlier encounter geometries would be required —
    an explicit direction for future development.
- **LiDAR HD at** ∼ **113 m** ⇒ ∼ **7.5 s** to CPA. Provides spatial confirmation and
    vector tracking almost simultaneously with radar first-detection.
- **EO at** ∼ **79 m** ⇒ ∼ **5.3 s** to CPA. Delivers semantic target classification within
    the Warning Alert envelope, supporting RPIC positive identification. The trained
    YOLOv8s model now achieves first detection in all 30 encounters (vs. 2 encounters
    in the legacy pipeline), with maximum first-detection range of 143.5 m.

This temporal layering validates the ABDAA architectural rationale: radar initiates
awareness at the longest ranges, while LiDAR and EO provide complementary spatial
and semantic confirmation at progressively closer distances. Notably, the trained EO
model achieves first detection in all 30 encounters (mean 79.3 m), demonstrating that
the visual channel is no longer a marginal contributor but a reliable mid-range detection
layer. Each modality feeds progressively higher-confidence intruder state estimates into
the DAIDALUS SUM/VISA pipeline, and the multi-sensor engagement pattern is stable
across all encounter geometries evaluated. Figure 21 plots the mean first-detection ranges
against the same DAIDALUS alert-envelope reference lines used in Section 2.4.5.


```
0 20 40 60 80 100 120 140 160
Mean first-detection range (m)
```
```
Radar (FMCW)
```
```
LiDAR HD (OS128)
```
```
EO / Vision
```
```
LiDAR Sparse (VLP16)
```
```
116.9 m
```
```
113.2 m
```
```
72.8 m
```
```
24.6 m
```
```
envelopeWarning Preventiveenvelope
```
```
First Detection Range by Sensor Modality 29 Encounter Runs
```
Figure 21: Mean first-detection range by sensor modality (Radar/LiDAR: 29 runs; EO:
30 runs with trained YOLOv8s), with DAIDALUS alert-envelope reference lines. Radar
provides the earliest cueing at∼117 m, followed closely by LiDAR HD; EO contributes
classification at ∼79 m within the Warning envelope.

#### 2.5.7 Simulation Strengths and Current Limitations

**Validated capabilities.**

- **Synchronized multi-modal acquisition** : All sensors evaluate identical encounter
    frames, enabling fair cross-modal comparison without temporal alignment artifacts.
- **Unified EO processing** : A single detection model generalizes across four distinct
    optical configurations (Tables 7–8), reducing the software certification scope for
    operational deployment.
- **Complementary detection architecture** : Radar provides the broadest coverage at
    all ranges, while the trained EO model now matches or exceeds LiDAR HD in the 25–
    100 m operational band (91–100% vs. 55–68%). The sensors remain complementary:
    radar offers early warning, LiDAR provides geometric point-cloud data for spatial
    confirmation, and EO delivers semantic classification. This complementarity is
    confirmed across 30 encounter scenarios and four lighting conditions.

**Identified limitations and required next steps.**

1. **Radar classification** : The current evaluation uses return-presence detection (maxi-
    mum recall) without target classification. Integrating micro-Doppler or range-profile
    features would enable class discrimination (drone vs. bird), directly reducing the
    nuisance alert rate analyzed in Section 2.6.4.
2. **LiDAR clutter discrimination** : The point-cloud detector uses geometric cluster-
    ing, which may produce false positives in complex urban environments. Supervised
    classification against static clutter is a required hardening step.


3. **EO domain gap** : Visual training data derives from simulation segmentation.
    Transfer to real-world conditions (atmospheric haze, sun glare, diverse backgrounds)
    remains an open integration challenge requiring mixed-reality or field-collected
    datasets.
4. **Encounter geometry scope** : The 30 scenarios focus predominantly on frontal and
    near-frontal approach geometries. Broader angular coverage, lateral intercepts, and
    overtaking scenarios are needed to fully characterize the sensor envelope.
5. **No-intruder baseline** : False-alarm quantification (detections in the absence of an
    intruder) has not yet been conducted. This campaign is identified as a priority next
    step in Section 4.1.2.

These limitations are characteristic of the current research maturity level. They define
the specific hardening activities required before the simulation evidence can support
higher-fidelity validation or field-test planning.

#### 2.5.8 Implications for the ABDAA Architecture

The empirical results from this synchronized campaign provide three specific inputs to the
overall ABDAA design evaluated in this report:

1. **Sensor role assignment** (feeds Section 1.2.8 architecture): Radar serves as the
    continuous early-warning layer with the highest availability ( _Pd_ = 100% return-
    presence). LiDAR HD provides geometric spatial confirmation in tactical distance
    bands (55–78% detection rates from 10 to 100 m). EO delivers semantic classification
    with 91–100% reliability in the 25–100 m operational band, with validated multi-lens
    generalization and a mean first-detection range of 79.3 m.
2. **SUM uncertainty parametrization** (feeds Section 2.4.5): The localization qual-
    ity metrics from EO training (73.1% for the unified model) quantify the spatial
    uncertainty that the SUM module must absorb when expanding the DAIDALUS
    Well Clear volume. Lower localization quality requires larger uncertainty ellipsoids,
    triggering earlier and more conservative avoidance maneuvers.
3. **Environmental robustness for BVLOS operations** (feeds Section 3.2): Radar
    and LiDAR maintain detection capability across all lighting conditions, supporting
    24-hour corridor operations. While EO performance varies by lighting (39.5% at
    dawn to 65.9% at night), it no longer exhibits complete failure under any condition
— confirming that the trained model provides meaningful contribution across the
diurnal cycle. Nonetheless, the variation reinforces the hybrid radar+vision design
selected for the ABDAA baseline.


For DECEA evaluators, the practical value of this campaign is not a definitive sensor
ranking, but rather a transparent, reproducible quantitative basis for understanding _why_
the hybrid architecture combines multiple modalities, _what_ each modality contributes
to the detection timeline, and _where_ the current research boundaries lie. This evidence
supports informed prioritization of future evaluation campaigns with broader scenarios,
operational fidelity, and progressively stricter validation criteria aligned with ASTM F3442
and DO-365B requirements.


## 3 Operational Impact and Regulatory Alignment

This section connects the experimental outputs of the preceding campaign to the regulatory
and operational context that motivates the SIMUA project. The CONOPS and SISCEAB
discussion (Section 3.1) maps the derived technical mitigations directly to national airspace
modernization objectives before the report concludes in Part 4.

### 3.1 Alignment with CONOPS and SISCEAB

#### 3.1.1 Validation of Operational Premises

The results of Point D confirm the strategic framework established in the SIMUA project
CONOPS. The hybrid ABDAA architecture addresses the limitations identified in the
current air traffic management system, which depends on large buffer zones and manual
coordination. By implementing autonomous local perception with a standards-compliant
RWC function (DAIDALUS/DO-365B), the architecture supports the CONOPS vision of
transitioning from static airspace blocks to a flexible, high-capacity environment.
Pre-tactical SCOPAS optimizations (Section 2.1) supply quantified sensing baselines—
cooperative versus non-cooperative, cost-weighted—that ground the surveillance assump-
tions later exercised in tactical and capacity analyses, without conflating infrastructure
planning with onboard or ground-based real-time avoidance.

#### 3.1.2 Link to SISCEAB Strategic Objectives

The technical results directly support the strategic mandates of DECEA and Agência
Nacional de Aviação Civil (ANAC) for airspace modernization:

- **Capacity Expansion** : The MSLA fleet-scaling experiments (Section 2.3) demon-
    strate that the hybrid xTM+DAA architecture sustains significantly higher through-
    put and lower conflict rates than either strategy alone, directly supporting DECEA’s
    objective of transitioning from static airspace blocks to flexible, high-capacity envi-
    ronments informed by the surveillance coverage envelopes optimized by the SCOPAS
    pre-tactical models.
- **Operational Flexibility** : By combining strategic xTM deconfliction with tactical
    RWC self-separation, the architecture allows DECEA to incrementally open airspace
    classes (G→E→D→C) to UAS operations without requiring permanent segregated
    corridors.
- **Sovereign Integration** : The simulation framework, validated with SJC geography
    and SISCEAB airspace class definitions (Section 1.2.2), provides DECEA with a
    nationally developed capability for evaluating DAA performance under Brazilian
    operational conditions.


#### 3.1.3 Compliance with SISCEAB and Federated Management

```
As defined in the project scope, the demonstrated architecture integrates with the Brazilian
Airspace Control System (SISCEAB) while fulfilling the requirements for a decentralized
and federated UTM model. It meets the following national and international milestones:
```
- **Delegated Responsibility** : The CONOPS requires that tactical deconfliction
    be strategically delegated from ATC to UAS operators or the RPIC. The use of
    DAIDALUS ensures the technical feasibility of this transfer of responsibility.
- **Support for DECEA** : _Well Clear_ parameters are synchronized with Brazilian
    guidelines for BVLOS in Classes G and E, supporting the goal of sovereign airspace
    integration.
- **ANAC Principle of Equivalence** : The hybrid approach satisfies safety equivalence
    for operations in populated areas (RBAC-E 91) without the need for permanent
    segregated areas.

#### 3.1.4 Convergence of UTM and UAM (eVTOL) Operations

The BR-xTM CONOPS explicitly targets the convergence of UTM (sUAS) and UAM
(eVTOL) operations into a unified airspace management framework. It is important to
clarify that the empirical campaigns of Point D are strictly bounded to sUAS kinematics
and payloads (due to extreme SWaP constraints). However, this serves as a highly
conservative baseline. Because the ABDAA node utilizes standard DO-365B (DAIDALUS)
logic—an algorithm inherently designed to scale to larger airframes—the architectural
success at the micro-UAS tier validates the underlying data-sharing and RWC feasibility.
Furthermore, the developed simulation infrastructure (linking the xTM spatial hashing to
the HTLV engine) represents an ongoing work that can be easily adapted to eVTOL study
cases simply by tuning the alerting time horizons and kinematic envelopes.

#### 3.1.5 Integration with Digital Flight Rules (DFR)

```
As outlined in the CONOPS, transitioning from segregated operations to dense, shared en-
vironments requires the adoption of Digital Flight Rules (DFR). The ABDAA architecture
serves as a foundational enabler for DFR by digitizing visual separation responsibilities.
The sensor fusion outputs and DAIDALUS guidance bands transform qualitative visual
flight rules (VFR) into quantifiable, machine-readable digital intent, thereby enabling
interoperability between eVTOLs, sUAS, and automated xTM services.
```

#### 3.1.6 ASTM Interoperability and Ecosystem Architecture

While Point D focuses on the tactical DAA requirements (ASTM F3442-25), the demon-
strated architecture fundamentally relies on the surrounding digital ecosystem defined in
the CONOPS. Operational viability requires integration with the federated data-sharing
framework for USS interoperability (ASTM F3548-21) and the mandated identity and
tracking backbone (ASTM F3411-22a for Remote ID). In the Brazilian context, the xTM
nodes simulated in our macroscopic experiments directly map to the ECO-UTM and
ECO-UAM coordination structures established by DECEA (DCA 351-6 and PCA 351-7),
providing the necessary bridge between regulatory authority and decentralized USS /
Provider of Services for UAM (PSU) service provision.

#### 3.1.7 Mitigation of Identified Risks

Table 11 maps the collision risks identified in the CONOPS safety analysis — including
_Geographical and Jurisdictional_ risks — and the mitigations provided by the ABDAA
architecture. Each mitigation is directly linked to a specific ABDAA feature, demonstrating
traceability from risk to technical solution.


```
Table 11: Risk Mapping and Mitigation by the ABDAA Architecture and UTM Services
```
```
Identified Risk Scenario Mitigation (Feature /
Service)
```
```
CONOPS
Category
```
```
Res.
```
```
Collision with non-
cooperative UAS
```
```
Urban BVLOS mmWave Radar Fusion +
planned SUM/VISA (RWC)
```
```
Operational Low
```
```
ADS-B channel fail-
ure
```
```
High density Autonomous local perception
( backup sensor)
```
```
Technical Low
```
```
Low-light / fog de-
tection
```
```
Night / Ad-
verse Weather
```
```
mmWave Radar
(weather-immune) + IR
Fusion
```
```
Geographical Medium
```
```
Adverse Microcli-
mate and Wind
Shear
```
```
Urban / Low-
Altitude
```
```
Strategic pre-flight forecasting
(WRF/UCM)
```
```
Environmental Low
```
Low-altitude
_ground clutter_

```
Near urban
structures
```
```
Adaptive FMCW filtering +
CFAR
```
```
Geographical Medium
```
```
Edge processor sat-
uration
```
```
High traffic
density
```
```
Distance prioritization
( Near-Field gate )
```
```
Technical Low
```
```
RPIC response la-
tency
```
```
All BVLOS HITL-aware alerting
thresholds ( 5 – 15 s margin)
```
```
Human Fac-
tors
```
```
Low
```
```
Jurisdictional
airspace transition
```
```
Cross-class
boundary
```
```
OSED-defined parameter
switching (G/E/D/C)
```
```
Jurisdictional Low
```

## 4 Conclusions and Strategic Vision

### 4.1 Conclusions and Deliverables Summary

#### 4.1.1 Research Nature and Overall Assessment

**Point D closes the current SIMUA project phase as an ongoing research
initiative.** All studies, experiments, and prototypes documented in this report are active
research contributions; they are not intended as immediately deployable, field-certified
operational solutions for DECEA or any other authority. The central value of the work lies
in the **technical understanding and capability consolidation** developed across the
project’s five research threads. This body of knowledge provides the structured evidence
base to support future investment decisions, identify viable development alternatives, and
guide progression toward higher Technology Readiness Levels (TRL) in subsequent project
phases.
With this framing established, the methodology presented consolidates the technical
transition necessary for the delivery of Point D of the ITA/ICEA project. The work is
structured as a progressive evaluation framework composed of five individual research
initiatives, which collectively inform the hybrid ABDAA architecture direction:

- **Deliverable 1: Pre-Tactical Infrastructure Optimization (SCOPAS)** : Es-
    tablishes the mathematical bounds for surveillance coverage and optimized sensor
    infrastructure layouts prior to tactical engagement (Section 2.1).
- **Deliverable 2: Macro-Scale Strategic Layering (MSLA)** : Explores fleet-scale
    capacity and efficiency trade-offs between xTM reservation tubes and interactive
    airspace demand, demonstrating through progressive density sweeps ( _N_ = 5 to 2 _,_ 000 )
    that the hybrid xTM+DAA architecture sustains the highest throughput with the
    lowest conflict rates (Section 2.3).
- **Deliverable 3: High-Fidelity Tactical Logic (HTLV)** : Evaluates the physical
    kinematics of DAIDALUS (acting as the RWC engine) against RTCA DO-365B
    separation parameters in a standard-aligned environment, empirically demonstrating
    a density-dependent scalability ceiling ( _N_ ≈ 300 – 500 ) beyond which reactive-only
    guidance becomes insufficient and strategic pre-separation (xTM) becomes mandatory
(Sections 2.4 and 2.4.5).
- **Deliverable 4: Multi-Sensor Empirical Benchmark** : Provides an exploratory
    frame-level sensing campaign comparing Radar, LiDAR, and EO/Vision under
    identical encounter geometries to inform early-stage fusion strategies (Section 2.5).
- **Deliverable 5: Strategic Microclimate Forecasting** : Integrates mesoscale mete-
    orological modeling (WRF) as a foundational UTM layer for dynamic environmental


```
risk mitigation and active volume management (Section 2.2).
```
These five research threads connect sequentially to address the full conflict management
spectrum, from preflight capacity modeling in SCOPAS through macroscopic MSLA flow
analysis, down to onboard tactical perception and HTLV resolution, and outward to the
environmental operational layer in the microclimate prototype.

#### 4.1.2 Research Maturity and Identified Limitations

1. **Current Maturity (TRL)** : The frameworks and algorithms explored in Point D
    remain **lower-TRL research initiatives**. While the simulations provide valuable
    directional evidence and conceptual alignment with SISCEAB objectives, they require
    deeper consolidation, field-testing, and rigorous engineering maturation prior to any
    practical operational deployment or regulatory certification.
2. **Platform Kinematics (sUAS vs. eVTOL)** : The empirical campaigns and
    hardware evaluations are intentionally restricted to sUAS parameters due to strict
    SWaP limitations. Extrapolating these results to AAM passenger-carrying eVTOLs
    requires dedicated study cases to adjust descent kinematics and evaluate larger
    sensor suites, though the underlying simulation structure smoothly supports this
    adaptation.
3. **Simulation Abstractions** : Current macro simulations rely on idealized behavior or
    specific stochastics that do not yet fully capture chaotic real-world edge cases (e.g.,
    compounding sensor failures, complex dynamic occlusions, and human cognitive
    overload).
4. **Computational Scalability** : The DAIDALUS pairwise evaluation exhibited _O_ ( _N_^2 )
    wall-clock scaling, leading to reactive oscillation deadlock at fleet densities above
    _N_ ≈ 300 – 500. At _N_ = 1 _,_ 000 , continuous safe-band guidance required over 14,000 s
    to simulate a 3,600 s scenario and paradoxically increased separation violations above
    the no-guidance baseline. This empirically confirms that high-density corridors
    require strategic xTM pre-separation to reduce the effective encounter rate before
    tactical DAIDALUS logic engages.
5. **Lighting Sensitivity** : Despite the trained EO detection model performs across
    all lighting conditions (39.5% at dawn to 65.9% at night), with no complete failure
    under any condition, those results where valid only for the simulated scenarios. The
    performance variability across the diurnal cycle require the hybrid radar+vision
    design, where radar provides lighting-invariant continuous cueing and EO contributes
    semantic classification.


6. **Ground Clutter** : mmWave Radar is affected by multipath near urban structures
    at low altitudes, requiring advanced adaptive filtering and robust multi-modal fusion
    logic that remains to be formalized.

#### 4.1.3 Contribution to the SIMUA Project and Future Vision

The results of Point D directly contribute to the SIMUA project’s international mission
by providing:

- A replicable technical base for AAM integration scenarios in Brazilian cities (São
    Paulo, Campinas, São José dos Campos) and Swedish cities (Stockholm, Gothenburg),
    with an OSED mapped to SISCEAB airspace classes (G, E, D, C).
- A three-part demonstration framework — MSLA (strategic capacity analysis), HTLV
    (high-fidelity tactical validation), and the multi-sensor simulation benchmark (Sec-
       tion 2.5) — extendable to commercial delivery, surveillance, and emergency response,
       with standards compliance verified against RTCA DO-365B and ASTM F3442 [2, 1].
- Foundations for the development of national standards for certifying ABDAA systems,
    with quantitative safety metrics (Risk Ratio, nuisance alert rate, throughput) aligned
    with ASTM F3442, EUROCAE ED-269, and RTCA SC-228 benchmarks.

**Proposed Roadmap Initiatives** To advance the ABDAA architecture toward higher
Technology Readiness Levels (TRL), the following strategic steps are identified for future
phases of the SIMUA project:

- **Multi-Modal Bayesian Fusion** : Moving beyond simple "OR" logic to a framework
    that dynamically weighs Radar and Vision based on weather sensors (e.g., relying
    100% on Radar in total fog).
- **Nocturnal and Adverse-Condition Robustness** : Although the trained EO
    model shows no complete failure at night in simulations, dawn conditions remain
    the weakest operating point (39.5% detection) with all requiring more real data
    evaluations. Integrating Long-Wave Infrared (LWIR) or near-IR channels would
    further stabilise detection consistency across the diurnal cycle and adverse weather.
- **Urban Canopy/Microclimate Integration (WRF-UCM)** : Refining the 3 km
    meteorological forecasting grid down to sub-kilometric resolutions, coupling atmo-
    spheric models with urban roughness mapping to classify hyper-local thermal and
    wind-shear risks.
- **Closed-Loop Integration** : Feeding high-fidelity HTLV maneuvers back into the
    MSLA fleet simulator to conduct a "true" capacity analysis using standard-aligned
    logic.


- **Hardware-in-the-Loop (HITL)** : Transitioning from synthetic simulation data to
    edge-processor testing to measure real-world latency and computational bottlenecks
    under mission-representative workloads.
- **UAM/eVTOL Adaptation Studies** : Adapting the current simulation infrastruc-
    ture to include the specific aerodynamic profiles, higher-fidelity sensors, and vertiport
    operational envelopes of passenger-carrying eVTOLs.


## References

```
[1] ASTM International. F3442/F3442M-20: Standard Specification for Detect and Avoid
System Performance Requirements. Standard. Performance requirements for sUAS
DAA systems. ASTM Committee F38 on Unmanned Aircraft Systems, 2020.
[2] RTCA Inc. DO-365B: Minimum Operational Performance Standards (MOPS) for
Detect and Avoid (DAA) Systems. Standard. Revision B. Defines DAA equipment
requirements for UAS operating in the NAS. RTCA Special Committee 228, 2020.
[3] Ouster Inc. OS0 Ultra-Wide View High-Resolution Imaging Lidar – Datasheet Rev. 05
v2.5. 2023.url:https://data.ouster.io/downloads/datasheets/datasheet-
rev05-v2p5-os0.pdf.
[4] Stereolabs. Ouster OS0 – Product Page. 2024.url:https://www.stereolabs.com/
store/products/ouster-os0.
[5] SLAMTEC. Lidar vs. Millimeter-Wave Radar: What’s the Difference? 2024.url:
https://www.slamtec.com/en/news/detailen/lidar-vs-millimeter-wave-
radar-what-s-the-difference.
[6] Texas Instruments. IWR6843, IWR6443 Single-Chip 60 to 64 GHz mmWave Sensor
Datasheet (Rev. F). 2022.url:https://www.ti.com/lit/ds/symlink/iwr6843.
pdf.
[7] Lei Li et al. “Recent Advances in mmWave-Radar-Based Sensing, Its Applications,
and Machine Learning Techniques: A Review”. In: Sensors (2023).url:https:
//pmc.ncbi.nlm.nih.gov/articles/PMC10650102/.
[8] Promwad. How to Choose the Best Edge AI Platform: Jetson, Kria, Coral and Others.
2025.url:https://promwad.com/news/choose-edge-ai-platform-jetson-
kria-coral-2025.
[9] Gia-Hung Tran et al. “Benchmarking YOLOv8 Variants for Object Detection Effi-
ciency on Jetson Orin NX for Edge Computing Applications”. In: Computers 15.2
(2026), p. 74.url: https://www.mdpi.com/2073-431X/15/2/74.
```
[10] André Luiz Santos et al. “A Comparative Evaluation of YOLOv9, YOLOv10, and
YOLOv11 on NVIDIA Jetson Orin for Real-Time Service Robotics”. In: _Proceedings
of BRAHUR/BRASERO 2025_. 2025.url:https://static.even3.com/anais/
brahurbrasero2025_paper_3.9ea63eaa84804c93ac7b.pdf.

[11] DSIAC. _What is an Acoustic Drone Detection System?_ 2024.url:https://dsiac.
dtic.mil/primers/what-is-an-acoustic-drone-detection-system/.

[12] Pedro J. Sánchez-Cuevas et al. “Analysis of Distance and Environmental Impact on
UAV Acoustic Detection”. In: _Preprints.org_ (2024).url:https://www.preprints.
org/manuscript/202401.0209.


[13] David P. Thipphavong et al. _Sensitivity Analysis of Detect and Avoid Well Clear
Parameter Variations on UAS DAA Sensor Requirements_. Tech. rep. NASA/TM-
2019-000985. NASA Ames Research Center, 2019.url:https://ntrs.nasa.gov/
api/citations/20190000985/downloads/20190000985.pdf.

[14] Arik-Quang V. Dao et al. _Air Traffic Controller Acceptability of Unmanned Aircraft
System Detect-and-Avoid Thresholds_. Tech. rep. NASA Ames Research Center, 2016.
url: https://ntrs.nasa.gov/citations/20160014320.

[15] Mykel J. Kochenderfer et al. _Airspace Encounter Models for Estimating Collision
Risk_. Tech. rep. ATC-358. Defines correlated and uncorrelated encounter model
frameworks for DAA safety assessment. MIT Lincoln Laboratory, 2010.

[16] NASA WellClear Project. _WellClear: Well-Clear Boundary Models for Integration of
UAS in the NAS_. 2020.url: [http://nasa.github.io/WellClear/.](http://nasa.github.io/WellClear/.)

[17] Michael Abramson, Anthony J. Narkawicz, and César A. Muñoz. “Applying Sensor
Uncertainty Mitigation Schemes to Detect-and-Avoid Systems”. In: _AIAA/IEEE
Digital Avionics Systems Conference (DASC)_. 2020.url:https://ntrs.nasa.gov/
citations/20205002286.

[18] Michael Abramson et al. _Evaluation of Sensor Uncertainty Mitigation Methods for
Detect-and-Avoid Systems_. Tech. rep. NASA/TM-20210022513. NASA Langley Re-
search Center, 2021.url:https://ntrs.nasa.gov/api/citations/20210022513/
downloads/20210022513_Abramson_SumTuningTM_manuscript_final.pdf.

[19] Wouter Jansen et al. “COSYS-AIRSIM: a real-time simulation framework expanded
for complex industrial applications”. In: _arXiv preprint arXiv:2303.13381_ (2023).


