# ExecutiveSummary

■ **Purpose:** Define the BR-xTM Operational Concept (CONOPs) for integrated low-

```
altitude operations in Brazil, converging UTM (drones) and UAM (eVTOL) under
one coordinated framework.
```
■ **Strategic objective:** Provide a safe, scalable, and governable transition path from

current fragmented operations to a unified Advanced Air Mobility (AAM) ecosys-

tem.

■ **Scope covered:** Government/authority functions, industry service suppliers, and

```
operational users (operators and pilots), including their interfaces, responsibili-
ties, and coordination logic.
```
■ **Safety model adopted:** Layered logic aligned with ICAO Doc 10019:

**-** Strategic conflict management (before flight),
**-** Separation management (during execution),
**-** Collision avoidance/DAA as last-resort protection.

■ **Standards baseline and traceability:** System elements are mapped to reference

standards, with primary operational impact from:

**-** ASTM F3548-21 (service-supplier interoperability and intent coordination),
**-** ASTM F3411-22a (Remote ID and tracking),
**-** ASTM F3442-25 (DAA performance requirements).

■ **Operational assessment method:** Scenario-based analysis from unmanaged base-

line to hybrid coordinated operations, including stress conditions.

i


ii

■ **Scenario set evaluated in the CONOPs:**

**-** Scenario 1: Operational Chaos Baseline (Blind Flight),
**-** Scenario 2: Onboard Tactical Resolution (Standalone DAA),
**-** Scenario 3: Strategic xTM Separation (Strict 4D Tubes),
**-** Scenario 4A: Optimized Hybrid Architecture (xTM + DAA),
**-** Scenario 4B: Hybrid under Stochastic Conditions (Real-World Chaos).

■ **Decision-relevant conclusion:** The document establishes a traceable operational

```
baseline for policy alignment, architecture governance, and staged implementa-
tion decisions for Brazilian low-altitude traffic management.
```
■ **Note:** Detailed simulation results for each scenario are documented in a separate

results-focused document.


# Abstract

This work is motivated by the layered safety logic of ICAO Doc 10019 and by the need

for a CONOPS that organizes, in a traceable manner, the convergence between UTM and

UAM within the Brazilian context. Based on this framework, the document proposes

BR-xTM as an integrated operational architecture for low-altitude traffic management,

with a focus on governance, interoperability, and scalability.

The CONOPS defines scope, boundaries, actors (government, service providers, and

users), operational interfaces, system capabilities, and architectural behavior, including

decomposition into system elements and the applicability of ASTM standards to crit-

ical components. In particular, it highlights the structuring impact of ASTM F3548-

(interoperability and coordination among providers), ASTM F3411-22a (Remote ID and

traceability), and ASTM F3442-25 (DAA performance), in alignment with FAA and DE-

CEA references.

For operational evaluation, the document establishes a set of progressive scenar-

ios, ranging from unmanaged conditions to hybrid strategic+tactical architectures un-

der stochastic disturbances, enabling the analysis of safety, capacity, delays, robustness,

and recovery. As a contribution, the CONOPS provides a methodological and norma-

tive baseline to guide implementation decisions, support simulation-based validation,

and structure future research on topics such as multi-service supplier coordination via

DSS, dynamic constraint management, resilience under non-cooperative traffic, fairness

in route allocation, and progressive integration toward the AAM ecosystem.

iii


iv

**Resumo**

Este trabalho é motivado pela lógica de segurança em camadas do ICAO Doc 10019 e

pela necessidade de um CONOPs que organize, de forma rastreável, a convergência en-

tre UTM e UAM no contexto brasileiro. Partindo desse referencial, o documento propõe

o BR-xTM como uma arquitetura operacional integrada para gestão de tráfego de baixa

altitude, com foco em governança, interoperabilidade e escalabilidade.

O CONOPs define escopo, fronteiras, atores (governo, provedores de serviço e usuários),

interfaces operacionais, capacidades do sistema e comportamento arquitetural, incluindo

a decomposição por elementos de sistema e a aplicabilidade de normas ASTM aos com-

ponentes críticos. Em particular, destaca-se o impacto estruturante da ASTM F3548-

(interoperabilidade e coordenação entre provedores), da ASTM F3411-22a (Remote ID

e rastreabilidade) e da ASTM F3442-25 (desempenho de DAA), em alinhamento com

referências FAA e DECEA.

Para avaliação operacional, o documento estabelece um conjunto de cenários pro-

gressivos, desde condições não gerenciadas até arquiteturas híbridas estratégicas+táticas

sob perturbações estocásticas, permitindo analisar segurança, capacidade, atrasos, ro-

bustez e recuperação. Como contribuição, o CONOPs oferece uma linha de base metodológ-

ica e normativa para orientar decisões de implementação, apoiar validação por sim-

ulação e estruturar pesquisas futuras em temas como coordenação multi-SS via DSS,

gestão dinâmica de restrições, resiliência sob tráfego não cooperativo, equidade de alo-

cação de rotas e integração progressiva rumo ao ecossistema AAM.


## Contents




- 1 Scope
   - 1.1 System Identification
   - 1.2 Purpose and Scope
   - 1.3 Document Overview
- 2 Referenced Documents
   - 2.1 Top-Level References (References/)
   - 2.2 AAM (References/AAM/)
   - 2.3 ASTM (References/Docs ASTM/)
   - 2.4 DECEA (References/Docs DECEA/)
   - 2.5 FAA (References/Docs FAA/)
   - 2.6 CORUS (References/CORUS/)
   - 2.7 SIMUA (References/SIMUA/)
- 3 Background Information
   - 3.1 Needed Capability and Historical Context
   - 3.2 Higher-Level Organizational Infrastructure
   - 3.3 Project Background and Rationale
   - 3.4 Stakeholders and Roles
   - 3.5 Related Projects and Systems
- 4 Existing Systems and Operations
   - 4.1 Operational Overview and Environment
   - 4.2 Personnel and Organizations
   - 4.3 System Overview
      - 4.3.1 Current Air Traffic Management (ATM) Infrastructure and Services vi Contents
         - System Traffic Management (UTM) Baseline 4.3.2 Current Unmanned Aircraft Systems (UAS)/Unmanned Aircraft
      - 4.3.3 FAA UTM and UAM Reference Architectures
         - Solutions) 4.3.4 CORUS U-space Deployment Architecture (Final Architecture and
   - 4.4 Support Environment
   - 4.5 Ongoing Studies and Operational Evaluations
         - Space Administration (NASA) UTM Maturation Studies 4.5.1 Federal Aviation Administration (FAA)/National Aeronautics and
      - 4.5.2 BR-UTM Initiative and Field Tests
   - 4.6 Digital Flight Rules (DFR) as a Common Interface for eVTOL and UAS
- 5 Proposed System Operational Overview
   - 5.1 Missions
   - 5.2 Operational Policies and Constraints
   - 5.3 Operational Environment
   - 5.4 Personnel
      - 5.4.1 5.4.1 Organizational Structure
      - 5.4.2 Personnel Profile
   - 5.5 Justification for and Nature of Changes
      - 5.5.1 Justification for Change
      - 5.5.2 Summary of Needed Changes
      - 5.5.3 Changes Considered but Not Included
- 6 6 System Overview
   - 6.1 6.1 System Scope
   - 6.2 6.2 System Goals and Objectives
   - 6.3 6.3 Users and Operators
   - 6.4 6.4 System Interfaces and Boundaries
   - 6.5 6.6 System Capabilities
   - 6.6 6.7 System Architecture
- 7 7 Operational Processes
   - 7.1 Scenario 1: Operational Chaos Baseline (Blind Flight)
      - 7.1.1 Scenario Objective
      - 7.1.2 Operational Events
      - 7.1.3 Users
   - 7.1.4 Key Actions Contents vii
   - 7.1.5 Post Conditions
   - 7.1.6 Policies and Business Rules
   - 7.1.7 Summary
- 7.2 Scenario 2: Onboard Tactical Resolution (Standalone DAA)
   - 7.2.1 Scenario Objective
   - 7.2.2 Operational Events
   - 7.2.3 Users
   - 7.2.4 Key Actions
   - 7.2.5 Post Conditions
   - 7.2.6 Policies and Business Rules
   - 7.2.7 Summary
- 7.3 Scenario 3: Strategic xTM Separation (Strict 4D Tubes)
   - 7.3.1 Scenario Objective
   - 7.3.2 Operational Events
   - 7.3.3 Users
   - 7.3.4 Key Actions
   - 7.3.5 Post Conditions
   - 7.3.6 Policies and Business Rules
   - 7.3.7 Summary
- 7.4 Scenario 4A: Optimized Hybrid Architecture (xTM + DAA)
   - 7.4.1 Scenario Objective
   - 7.4.2 Operational Events
   - 7.4.3 Users
   - 7.4.4 Key Actions
   - 7.4.5 Post Conditions
   - 7.4.6 Policies and Business Rules
   - 7.4.7 Summary
   - Chaos) 7.5 Scenario 4B: Hybrid Architecture under Stochastic Conditions (Real-World
   - 7.5.1 Scenario Objective
   - 7.5.2 Operational Events
   - 7.5.3 Users
   - 7.5.4 Key Actions
   - 7.5.5 Post Conditions
   - 7.5.6 Policies and Business Rules
   - 7.5.7 Summary
- References viii Contents
- Appendix A Acronym, Abbreviations, and Glossary
   - A.1 ASTM Definitions Traceability Matrix
   - A.2 DECEA Definitions Traceability Matrix


# ListofFigures

1.1 Nominal operation at the sky of Florianópolis - SC................ 1

4.1 Components of the Air Traffic Management (ATM) System (adapted from

Departamento de Controle do Espaço Aéreo (DECEA) DCA 351-7, Figure 1)

DECEA (2025c)..................................... 15

4.2 BR-UTM architecture (adapted from DECEA DCA 351-6, Figure 1) DECEA

(2022)........................................... 18

4.3 UAM architecture (adapted from DECEA PCA 351-7, Figure 10) DECEA

(2024a).......................................... 20

4.4 Notional FAA UTM architecture (adapted from FAA UTM CONOPS v2.0,

Figure 3) Federal Aviation Administration (2020)................. 22

4.5 Notional FAA UAM architecture (adapted from FAA UAM CONOPS v2.0,

Figure 8) Federal Aviation Administration (2023a)................. 23

4.6 CORUS deployment overview (Figure 28, adapted from CORUS Final Archi-

tecture and Solutions) CORUS Consortium (2020a)................ 25

4.7 UTM high-level architecture (adapted from FAA UTM Field Test (UFT) Final

Report, Figure 1) Federal Aviation Administration (2023b)............ 27

5.1 Government–Industry–Users relationship in the BR-xTM Level 1 organiza-

tional view........................................ 35

6.1 BR-xTM user-role view focused on users and operators.............. 43

6.2 BR-xTM interfaces view (functional links among user, provider, and author-

ity domains)....................................... 44

6.3 Three-layer safety logic for RPAS operations (strategic conflict management,

separation provision, and collision avoidance), adapted from ICAO Doc 10019. 52

ix


x List of Figures

6.4 BR-xTM Level 2 architecture (integrated UTM+UAM operational structure).. 53

6.5 System-elements tree with requirement traceability: decomposition by gov-

ernment, industry/service-provider, and user/operator sides with ASTM

applicability mapping................................. 55

7.1 Scenario 1 illustration: unmanaged chaos baseline (blind-flight condition)... 60

7.2 Scenario 2 illustration: standalone DAA with reactive maneuver inefficiency. 62

7.3 Scenario 3 illustration: strict strategic xTM with 4D tubes and ground-delay

effects.......................................... 65

7.4 Scenario 4A illustration: optimized hybrid architecture (xTM + DAA)..... 69

7.5 Scenario 4B illustration: resilience under stochastic disturbances and wind

deviations........................................ 72


# ListofTables

2.1 All Requirement.................................... 7

6.1 System interface links and observations (reviewed against FAA/DECEA CONOPS

references)........................................ 44

6.2 Link-type flow dictionary: expected data flows and reference definitions.... 47

xi



## 1 Scope

Unmanned aviation has been rapidly evolving and, as consequence, the drones capabil-

ities keep on an ongoing improvement (Figure 1.1). This market shows a diverse scope

of applications such as inspections, infrastructure monitoring, mapping, filming and

photography, precision agriculture, search and rescue, disaster relief and public safety.

Figure 1.1: Nominal operation at the sky of Florianópolis - SC.


Chapter1. Scope 1.1. SystemIdentification

The Operational Concept Description (herein referred to as OCD) describes, out-

lines, establishes the strategic and operational framework required to facilitate the safe,

efficient, and scalable integration of Unmanned Aircraft System Traffic Management

(UTM) and UAM within the SISCEAB.

This document encompasses the technical requirements, jurisdictional boundaries,

and collaborative responsibilities between stakeholders, specifically addressing:

```
■ Geographic and Jurisdictional Limits: The application of these operations within
sovereign Brazilian airspace, focusing on high-density urban centers (e.g., São
Paulo and Rio de Janeiro) and transition zones between uncontrolled (Class G)
```
and controlled airspace (Classes C, D, and E).

```
■ Regulatory Alignment: Compliance with the mandates of the Department of Airspace
Control (DECEA) and the ANAC, ensuring that UTM/UAM protocols harmonize
with existing ICA 100-40 regulations and RBAC standards.
```
■ Operational Services: The definition of essential services, including automated

```
flight authorization, dynamic airspace reconfiguration, real-time situational aware-
ness (e-Identification), and conflict detection and resolution (CD&R) for both au-
tonomous and piloted VTOL aircraft.
```
■ Infrastructure Integration: The interface between Vertiports and the existing ANSP

infrastructure, ensuring seamless data exchange through the SWIM architecture.

■ Safety and Security: The mitigation of risks associated with high-frequency low-

```
altitude operations, including the protection of "critical infrastructure" and the
management of contingencies in complex meteorological conditions typical of trop-
ical latitudes.
```
**1.1 | SystemIdentification**

The system addressed in this document is designated as **BR-xTM**. BR-xTM is a Brazil-

ian advanced air mobility concept aligned with AAM, integrating both UAM and UTM

operational domains under a coordinated framework for planning, authorization, mon-

itoring, and traffic management.

**System Identifier:** BR-xTM-CONOPS-v0.


Chapter1. Scope 1.2. PurposeandScope

**1.2 | PurposeandScope**

The document aims to create directives and procedures to ensure safety, security, ef-

ficiency and equity of the aerial space. A key objective is to present a vision for the

integration of eVTOLs, as well as sUAS, through the UAM and UTM concepts, into

the Brazilian airspace structure, maintaining safety, fluidity, and efficiency standards

through the progressive evolution of the use of new technologies.

This hereby document describes the current state of operations, establishes the rea-

sons for change, and defines operations for the future in terms of functions/features

and supporting operations. This document will be used to present the vision, goals and

direction for the project and support the detailed systems engineering development pro-

cess.

**1.3 | DocumentOverview**

This subsection summarizes the purpose and contents of this Operational Concept Doc-

ument (OCD), including its intended audience. The primary audience comprises decision-

makers, regulators, air navigation service stakeholders, system developers, operators,

and researchers involved in advanced air mobility in Brazil. The document presents the

comparative CONOPS baseline between FAA and DECEA definitions, establishes the

operational context for BR-xTM, and organizes the subsequent sections that describe

existing operations, proposed operational concepts, system overview, operational pro-

cesses, and analysis of impacts and tradeoffs.

The document roadmap is organized as follows:

```
■ Chapter 1 (Scope): Defines the problem space, system identification (BR-xTM),
purpose, scope boundaries, and intended audience.
```
```
■ Chapter 2 (Referenced Documents): Lists the standards, regulations, and source
material used as the technical and regulatory baseline.
```
```
■ Chapter 3 (Background Information): Presents contextual and historical informa-
tion needed to understand the comparative FAA/DECEA framing.
```
```
■ Chapter 4 (Existing Systems and Operations): Describes the current operational
baseline, including relevant limitations and gaps.
```

Chapter1. Scope 1.3. DocumentOverview

■ Chapter 5 (Proposed System Operational Overview): Introduces the proposed op-

```
erational concept, mission profile, constraints, personnel, and support assump-
tions.
```
```
■ Chapter 6 (System Overview): Summarizes BR-xTM scope, goals, users, inter-
faces, operating modes, capabilities, and high-level architecture.
```
```
■ Chapter 7 (Operational Processes): Details the core operational workflows, includ-
ing normal, degraded, and contingency operations.
```
■ Chapter 8 (Other Operational Needs): Consolidates mission needs, personnel needs,

and quality factors that influence requirements.

■ Chapter 9 (Analysis of the Proposed System): Compares advantages, limitations,

impacts, and major tradeoffs of the proposed concept.

■ Appendix A (Acronyms, Abbreviations, and Glossary): Defines terminology used

throughout the document.

■ Appendix B (Detailed System Operational Scenarios): Provides representative sce-

narios that illustrate end-to-end system use.


## 2 Referenced Documents

This chapter lists the reference material used in this work, organized by source folder

for filtering and traceability.

**2.1 | Top-LevelReferences(** References/ **)**

```
■ ANSI/AIAA-043B-2018 Guide for the Preparation of Operational Concept Docu-
ments American National Standards Institute and American Institute of Aeronau-
```
tics and Astronautics (2018).

■ ICAO Doc 10019 (2015) International Civil Aviation Organization (2015).

■ Rules of the Air – Annex 2 International Civil Aviation Organization (2009).

■ ICAO Doc 8168, Volume 1 International Civil Aviation Organization (2007).

**2.2 | AAM(** References/AAM/ **)**

■ AAM Comprehensive Plan 2025 United States Government (2025a).

■ AAM National Strategy United States Government (2025b).

■ NASA-CR-20230012505 National Aeronautics and Space Administration (2023).

**2.3 | ASTM(** References/Docs ASTM/ **)**

```
■ ASTM F3341/F3341M-24: Standard Terminology for Unmanned Aircraft Systems
ASTM International (2024a).
```

Chapter2. ReferencedDocuments 2.4. DECEA(References/Docs DECEA/)

■ ASTM F3411-22a: Standard Specification for Remote ID and Tracking ASTM In-

ternational (2022a).

■ ASTM F3423/F3423M-22: Standard Specification for Vertiport Design ASTM In-

ternational (2022b).

```
■ ASTM F3442-25: Standard Specification for Detect and Avoid System Performance
Requirements ASTM International (2025).
```
```
■ ASTM F3548-21: Standard Specification for UAS Traffic Management (UTM) UAS
Service Supplier (USS) Interoperability ASTM International (2021).
```
```
■ ASTM F3623-23: Standard Specification for Surveillance Supplementary Data Ser-
vice Providers ASTM International (2023).
```
```
■ ASTM F3673-24: Standard Specification for Performance for Weather Information
Reports, Data Interfaces, and Weather Information Providers (WIPs) ASTM Inter-
```
national (2024b).

**2.4 | DECEA(** References/Docs DECEA/ **)**

```
■ ICA 100-40 – Aeronaves não Tripuladas e o Acesso ao Espaço Aéreo Brasileiro
DECEA (2023).
```
■ DCA 351-6 – Concepção Operacional UTM Nacional DECEA (2022).

```
■ DCA 351-7 – Diretriz da Aeronáutica para o Controle do Espaço Aéreo Brasileiro
DECEA (2025c).
```
```
■ PCA 351-6 – Concepção Operacional do Espaço Aéreo de Rotas Livres DECEA
(2025d).
```
■ PCA 351-7 – Concepção Operacional UAM Nacional DECEA (2024a).

■ Novo Tutorial SARPAS DECEA 2024 DECEA (2024b).

**2.5 | FAA(** References/Docs FAA/ **)**

```
■ UTM Field Test (UFT) Version 1.0 Final Report Federal Aviation Administration
(2023b).
```

Chapter2. ReferencedDocuments 2.6. CORUS(References/CORUS/)

■ FAA UAM CONOPS Version 2 Federal Aviation Administration (2023a).

■ FAA UTM CONOPS Version 2 Federal Aviation Administration (2020).

**2.6 | CORUS(** References/CORUS/ **)**

■ Final Architecture and Solutions CORUS Consortium (2020a).

■ Final Operations and UTM Requirements CORUS Consortium (2020b).

```
■ CORUS Volume 1 – Concept of Operations Enhanced Overview CORUS Consor-
tium (2019a).
```
■ CORUS Volume 2 – U-space Concept of Operations CORUS Consortium (2019b).

**2.7 | SIMUA(** References/SIMUA/ **)**

■ Convênio nº003 ITA 2022 SIMUA Project (2022a).

■ DocuSign Agreement – SIMUA Final Statement of Work SIMUA Project (2022b).

■ Termo Aditivo ao Plano de Trabalho ITA x ICEA SIMUA Project (2024).

The following documents (Table 2.1) are listed to ensure full traceability between the

proposed system architecture and international aviation standards. Note that only the

documents cited earlier were actually accessed to develop this document.

Table 2.1: All Requirement

**ASTM ID Document Title**

```
F3548-21 Standard Specification for UAS Traffic Management (UTM) UAS Ser-
vice Supplier (USS) Interoperability ??
```
```
F3442-25 Standard Specification for Detect and Avoid System Performance Re-
quirements ??
```
```
F3411-22a Standard Specification for Remote ID and Tracking ??
F3547-24 Standard Specification for Fuel Cell Power Systems for Use in Small
Unmanned Aircraft Systems (sUAS)
```
```
F3322-24a Standard Specification for Small Unmanned Aircraft System (sUAS)
Parachutes
```

Chapter2. ReferencedDocuments 2.7. SIMUA(References/SIMUA/)

Table 2.1 continued

**ASTM ID Document Title**

F3005-22 Standard Specification for Batteries for Use in Small Unmanned Air-

```
craft Systems (sUAS)
F3609-25 Standard Specification for PNT for Unmanned Aircraft Systems (UAS)
F3002-22 Standard Specification for Design of the Command and Control System
```
```
for Small Unmanned Aircraft Systems (sUAS)
F3673-24 Standard Specification for Performance for Weather Information Re-
```
```
ports, Data Interfaces, andWIPs
F3623-23 Standard Specification for Surveillance Supplementary Data Service
```
```
Providers
F2849-10 Standard Practice for Handling of Unmanned Aircraft Systems at Di-
```
```
vert Airfields
F3600-22 Standard Guide for Unmanned Aircraft System (UAS) Maintenance
Technician Qualification
```
```
F3266-23 Standard Guide for Training for Remote Pilot in Command of Un-
manned Aircraft Systems (UAS) Endorsement
```
```
F3196-18 Standard Practice for Seeking Approval for Beyond Visual Line of Sight
(BVLOS) Small System (sUAS) Operations
```
```
F3379-20 Standard Guide for Training for Public Safety Remote Pilot of Un-
manned Aircraft Systems (UAS) Endorsement
F3423M-22 Standard Specification for Vertiport Design
```
```
F3366-19 Standard Specification for GMM for a Small Unmanned Aircraft Sys-
tem (sUAS)
```
```
F3657-23 Standard Specification for Verification of Lightweight Unmanned Air-
craft Systems (UAS)
```
```
F2910-22 Standard Specification for Design and Construction of a Small Un-
manned Aircraft System (sUAS)
F3298-24 Standard Specification for Design and Construction of Lightweight Un-
```
```
manned Aircraft Systems (UAS)
F2908-23 Standard Specification for UFM for an Unmanned Aircraft System
```
(UAS)


## 3 Background Information

This chapter establishes the operational background for the Brazilian xTM concept and

identifies the context, constraints, and institutional conditions that drive the proposed

concept of operations.

**3.1 | NeededCapabilityandHistoricalContext**

Demand for low-altitude operations is increasing due to growth in UAS services and

expected introduction of high-frequency eVTOL operations. Existing operational meth-

ods based primarily on airspace segregation, static constraints, and case-by-case coor-

dination remain adequate for low traffic density; however, they are not sufficient for

sustained, high-density, mixed-operator environments DECEA (2023, 2024a); Federal

Aviation Administration (2020).

The required capability is a scalable traffic management construct that supports

strategic intent sharing, cooperative deconfliction, conformance monitoring, and dy-

namic management of airspace constraints. International CONOPS references describe

this transition as a move from isolated authorizations to interoperable digital service

networks with defined authority/service-provider boundaries CORUS Consortium (2019a,b);

Federal Aviation Administration (2020, 2023a).

U.S. national AAM strategy documents reinforce this same need from a policy and

implementation perspective. At high level, they frame AAM as a whole-of-government

modernization effort requiring synchronized evolution of airspace operations, infras-

tructure, certification pathways, public acceptance, and data-sharing mechanisms. In

CONOPS terms, this implies that traffic management capability cannot be treated as

a standalone technical component; it must be integrated with governance, phased de-


Chapter3. BackgroundInformation 3.2. Higher-LevelOrganizationalInfrastructure

ployment milestones, and cross-agency execution mechanisms from the outset United

States Government (2025a,b).

Those strategy documents also emphasize near-term operational pragmatism: de-

ploy incrementally, start from viable use cases, and expand capacity as interoperability

and safety assurance mature. This is directly consistent with an xTM concept based

on progressive service enablement, performance-based oversight, and structured inte-

gration between legacy ATM functions and new low-altitude service ecosystems. The

strategic implication for Brazil is that scale should be pursued through sequenced oper-

ational maturity rather than through abrupt structural substitution of existing airspace

services National Aeronautics and Space Administration (2023); United States Govern-

ment (2025a,b).

ICAO high-level references provide the harmonization framework for this transi-

tion: integration must preserve safety performance, procedural coherence, and compat-

ibility with established rules of the air and operational procedures International Civil

Aviation Organization (2007, 2009, 2015).

The current legislations that regulate the airspace segregate areas to ensure safety

through isolation; however, this model is inherently unscalable for the projected volume

of UAS and eVTOL operations. Traditional air traffic management relies on maintain-

ing large buffer zones and manual coordination between pilots and controllers, which

cannot accommodate the high density of aircraft expected to operate simultaneously in

restricted urban corridors. As the number of concurrent flights increases in localized

areas, the reliance on static airspace blocks creates significant capacity constraints and

prevents the flexible movement required for urban air mobility. This density of oper-

ations exceeds the threshold of current manual monitoring capabilities, leading to an

inevitable saturation of the existing system.

**3.2 | Higher-LevelOrganizationalInfrastructure**

The Brazilian institutional baseline is defined by SISCEAB governance, with DECEA re-

sponsible for strategic direction and operational control of the national airspace system

DECEA (2025c). For unmanned aviation, ICA 100-40 already establishes authorization

processes, operator obligations, and access criteria for the Brazilian airspace structure

DECEA (2023).

Accordingly, the xTM concept is framed as an extension layer to legacy ATM/ATS

functions, not as a parallel replacement. UTM/UAM services must remain interoper-

able with existing surveillance, flow management, aeronautical information, and ATC


Chapter3. BackgroundInformation 3.3. ProjectBackgroundandRationale

responsibilities, while preserving state authority over airspace decisions DECEA (2022,

2024a); Federal Aviation Administration (2023a).

**3.3 | ProjectBackgroundandRationale**

The project addresses a capability gap between current regulatory-operational mech-

anisms and projected operational demand in low-altitude, high-tempo environments.

The problem is multi-domain: technology readiness, operational procedures, institu-

tional governance, and cross-stakeholder coordination.

The project baseline consolidates DECEA doctrine, FAA federated-service patterns,

CORUS/U-space operational decomposition, and ICAO-level harmonization guidance

to derive a Brazil-adapted implementation path. The intended outcome is a concept

that increases capacity and service diversity while maintaining safety performance and

regulatory accountability CORUS Consortium (2020b); DECEA (2022); Federal Aviation

Administration (2020); International Civil Aviation Organization (2015).

**3.4 | StakeholdersandRoles**

The xTM concept includes the following primary stakeholder groups:

■ **Regulators and State Authorities:** DECEA, ANAC, and public safety agencies de-

```
fine policy, oversight, and enforcement boundaries, and retain decision authority
for airspace governance DECEA (2023, 2025c).
```
■ **Service Providers:** USS/PSU/SDSP-type entities provide operational planning

```
support, information exchange, monitoring, and coordination services under ap-
proved governance and interoperability requirements CORUS Consortium (2019b);
DECEA (2024a); Federal Aviation Administration (2020, 2023a).
```
■ **Operators:** UAS and UAM operators are accountable for mission planning, com-

```
pliance with authorization conditions, and safe execution of operations DECEA
(2023, 2024a).
```
■ **Conventional Airspace Users:** Manned aircraft operators participate directly or

```
indirectly depending on airspace class, service availability, and operational profile
CORUS Consortium (2019a); Federal Aviation Administration (2020).
```

Chapter3. BackgroundInformation 3.5. RelatedProjectsandSystems

■ **Public and Infrastructure Stakeholders:** Municipal entities, aerodrome/vertiport

```
operators, logistics actors, and communities are affected by access, safety, environ-
mental, and equity outcomes.
```
**3.5 | RelatedProjectsandSystems**

The concept development uses the following reference baselines:

```
■ DECEA baseline: National UTM/UAM conceptual documents and ATM strate-
gic directives define doctrinal and institutional constraints for Brazilian imple-
```
mentation DECEA (2022, 2024a, 2025c).

```
■ FAA baseline: UTM/UAM CONOPS define a mature federated model with ex-
plicit allocation of roles between authority functions and industry-provided ser-
```
vices Federal Aviation Administration (2020, 2023a).

■ **CORUS/U-space baseline:** European references provide service-layer decompo-

```
sition and interoperability logic applicable to scenario definition and requirement
engineering CORUS Consortium (2019a,b, 2020a,b).
```
```
■ ICAO high-level baseline: International references provide harmonization guid-
ance for integration, procedures, and safety consistency across heterogeneous op-
```
erations International Civil Aviation Organization (2007, 2009, 2015).

These baselines collectively support a phased transition from low-density, segre-

gated operations toward scalable, interoperable, and safety-assured xTM operations in

Brazil.


## 4 Existing Systems and Operations

This chapter describes the current operational baseline used to provide airspace ser-

vices in Brazil, including the existing Air Traffic Management (ATM) structure, the cur-

rent integration model for Unmanned Aircraft Systems (UAS), and ongoing Unmanned

Aircraft System Traffic Management (UTM)/Urban Air Mobility (UAM)-related studies

that inform the proposed concept.

**4.1 | OperationalOverviewandEnvironment**

The current Brazilian environment is centered on the Air Traffic Management (ATM)

system operated under Sistema de Controle do Espaço Aéreo Brasileiro (SISCEAB) gover-

nance, with integrated civil-military coordination and nationwide Air Traffic Services

(ATS)/Air Traffic Control (ATC) service provision DECEA (2025c). Operational service

delivery is organized to support gate-to-gate air navigation in en-route, terminal, and

aerodrome contexts, with planning and execution continuously adjusted by airspace

organization, flow management, synchronization, and conflict management functions

DECEA (2025c).

In practical terms, current operations include a heterogeneous mix of users and mis-

sion types: high-altitude scheduled commercial traffic, military missions, executive avi-

ation, rotary-wing operations (including offshore and urban helicopter profiles), low-

altitude specialized flights (e.g., agricultural and survey operations), and increasing

Unmanned Aircraft Systems (UAS) activity DECEA (2023, 2025c). This mix already cre-

ates localized complexity in terminal areas and low-altitude corridors, especially where

traffic density, weather variability, and infrastructure constraints overlap.

For Unmanned Aircraft Systems (UAS), Brazil currently applies an access-control

model in which operations are authorized according to airspace context, risk, and mis-


Chapter4. ExistingSystemsandOperations 4.2. PersonnelandOrganizations

sion profile, with significant reliance on predefined constraints and operational accom-

modation measures DECEA (2023). This model is effective for current demand levels,

but faces scalability challenges as operation volume, simultaneity, and mission diversity

increase.

**4.2 | PersonnelandOrganizations**

The existing system relies on a multi-actor structure:

```
■ Departamento de Controle do Espaço Aéreo (DECEA): central authority for strate-
gic direction and operational control of the national airspace system, including Air
```
```
Traffic Services (ATS)/Air Traffic Control (ATC) service policy and oversight DE-
CEA (2025c).
```
```
■ Centro de Gerenciamento da Navegação Aérea (CGNA) and Air Traffic Services
(ATS) Units: tactical and pre-tactical coordination of flow/capacity and opera-
```
tional execution across sectors, terminals, and aerodromes DECEA (2025c).

```
■ Agência Nacional de Aviação Civil (ANAC): civil aviation regulatory roles re-
lated to certification, licensing, and operator oversight in coordination with airspace-
```
access rules DECEA (2023).

```
■ Operators (manned and unmanned): mission planning and execution responsi-
bility under applicable authorization and safety conditions DECEA (2022, 2023).
```
The personnel baseline remains dependent on human decision-making for tactical

safety assurance, particularly in complex mixed-traffic contexts. Current modernization

initiatives therefore focus on decision-support, digital data exchange, and progressive

automation without removing regulatory accountability from state authorities DECEA

(2025c); Federal Aviation Administration (2020).

**4.3 | SystemOverview**

4.3.1 | Current Air Traffic Management (ATM) Infrastructure and

Services

The current infrastructure includes communication, navigation, surveillance, meteoro-

logical, and aeronautical information services integrated with flow and conflict-management


Chapter4. ExistingSystemsandOperations 4.3. SystemOverview

functions. Service delivery supports both structured route operations and progres-

sive flexibility initiatives, with emphasis on safety, orderly flow, and efficiency DECEA

(2025c).

The scheme in Figure 4.1 can be interpreted in four complementary ways to clarify

how the existing system operates in practice DECEA (2025c).

Figure 4.1: Components of the Air Traffic Management (ATM) System (adapted from

Departamento de Controle do Espaço Aéreo (DECEA) DCA 351-7, Figure 1) DECEA

(2025c).

Parts (Distinctions): what each component is and why it exists - The diagram de-

composes Air Traffic Management (ATM) into functional parts so that each operational

problem has a dedicated management function:

■ **Airspace Organization and Management (AOM)** exists to structure and allocate

airspace in a flexible and equitable way.

■ **Demand and Capacity Balancing (DCB)** exists to balance demand and capacity

before overload degrades safety and predictability.

■ **Aerodrome Operations (AO)** exists to integrate runway, surface, and aerodrome

constraints with en-route/terminal flow.

■ **Traffic Synchronization (TS)** exists to sequence and synchronize traffic in time

and space (gate-to-gate continuity).

```
■ Conflict Management (CM) exists to detect, prevent, and resolve conflicts among
aircraft and operational hazards.
```

Chapter4. ExistingSystemsandOperations 4.3. SystemOverview

■ **Airspace Users Operations (AUO)** exists to represent user-side operational needs,

capabilities, and intent.

```
■ ATM Service Delivery Management (ATM SDM) exists to orchestrate service
delivery and agreement execution across phases of flight.
```
```
Art. 90. Esses componentes são: a Organização e Gerenciamento do Espaço
Aéreo (AOM), Balanceamento entre Demanda e Capacidade (DCB), Operações de
Aeródromo (AO), Sincronização de Tráfego (TS), Gerenciamento de Conflitos (CM),
```
```
Operações dos Usuários do Espaço Aéreo (AUO) e Gerenciamento da Entrega de
Serviços ATM (ATM SDM).
```
Whole (Systems): why the complete system is more than the parts - The figure ex-

plicitly frames Air Traffic Management (ATM) as a holistic entity. The whole value is

produced by integrated behavior: the system only achieves safe, orderly, and efficient

flow when all components operate concurrently and exchange consistent information.

In other words, local optimization of one component is insufficient if global flow, safety,

and predictability are not jointly optimized DECEA (2025c).

Relationships: internal and external interactions - Internal relationships are the con-

tinuous couplings among Airspace Organization and Management (AOM), Demand

and Capacity Balancing (DCB), Aerodrome Operations (AO), Traffic Synchronization

(TS), Conflict Management (CM), Airspace Users Operations (AUO), and ATM Service

Delivery Management (ATM SDM) through the information-management layer shown

in the scheme. Decisions in one component (e.g., capacity limits) propagate to sequenc-

ing, conflict handling, and user operations. External relationships connect the ATM core

to the wider operational environment: aircraft operators, aerodromes, military and civil

authorities, weather/information services, and emerging Unmanned Aircraft System

Traffic Management (UTM)/Urban Air Mobility (UAM) service layers. These interfaces

are what allow the system to absorb operational variability without losing regulatory

control or safety performance DECEA (2022, 2024a, 2025c).

4 Perspectives: three operational viewpoints

```
■ User perspective (we): the scheme defines the service logic we rely on to plan,
execute, and adapt operations with predictable constraints and shared situational
awareness.
```
```
■ Operator perspective (Air Traffic Control (ATC) / pilots / airport): the scheme is a
coordination framework for balancing throughput and safety in real time, ensur-
```

Chapter4. ExistingSystemsandOperations 4.3. SystemOverview

ing that sector, cockpit, and aerodrome decisions remain temporally and spatially

coherent.

```
■ Regulatory perspective: the scheme is an assurance architecture. It supports
accountability, standardization, and oversight by showing where decisions are
```
```
made, how responsibilities are distributed, and how performance/safety can be
monitored across the full operation lifecycle.
```
Operationally, this baseline is designed for mixed traffic classes and a broad mission

spectrum, including:

```
■ high-altitude and medium-altitude commercial operations under Instrument Flight
Rules (IFR);
```
■ military and state missions with specific operational constraints;

■ low-altitude operations, including rotary-wing and specialized services;

■ rural and regional profiles with variable infrastructure density; and

■ emerging digital-intensive operations requiring higher tempo coordination.

4.3.2 | CurrentUnmannedAircraftSystems(UAS)/UnmannedAir-

craftSystemTrafficManagement(UTM)Baseline

Current Unmanned Aircraft Systems (UAS) integration remains transitional. Regula-

tory and operational mechanisms exist, but routine large-scale, federated low-altitude

traffic management is still in maturation. DECEA conceptual references define the di-

rection toward cooperative, data-driven operation management and interoperability be-

tween Air Traffic Management (ATM), Unmanned Aircraft System Traffic Management

(UTM), and Urban Air Mobility (UAM) service layers DECEA (2022, 2024a).

4.3.2.1 | DECEAArchitectures

At the national level, DECEA establishes two foundational concept documents for this

transition path: first, the UTM operational concept in DCA 351-6 (focused on unmanned

traffic management integration into the Brazilian context), and later the UAM opera-

tional concept in PCA 351-7 (focused on urban air mobility integration as an additional

operational layer coordinated with ATM) DECEA (2022, 2024a).


Chapter4. ExistingSystemsandOperations 4.3. SystemOverview

The architecture proposed in DCA 351-6 (Figure 4.2 BR-UTM around a regulated

ecosystem where state data sources and ATM-related services interface with UTM ser-

vice providers and operators through structured information exchange DECEA (2022).

In broad terms, the model combines regulatory oversight, shared situational data, service-

provider interoperability, and operator-level execution.

Figure 4.2: BR-UTM architecture (adapted from DECEA DCA 351-6, Figure 1) DECEA

(2022).

Main elements represented in the DECEA UTM architecture include:

■ **DECEA/ATM-side data and systems:** ATM and institutional information sources

that feed UTM awareness and constraints.

■ **UTM ecosystem core:** national-level integration functions that consolidate data,

priorities, and regulatory conditions.

```
■ UAS Service Suppliers (USS) and supplemental providers: service layers for
planning, restriction handling, monitoring, notifications, and coordination.
```
```
■ Operators and vehicles: execution layer for UAS missions under shared con-
straints and service-provided information.
```

Chapter4. ExistingSystemsandOperations 4.3. SystemOverview

■ **External/public interfaces:** authorities and other actors interacting with the ecosys-

tem for safety, oversight, and operational coordination.

PCA 351-7 extends the architectural logic (Figure 4.3) to the UAM environment by

introducing urban operational layers (national, operational, and local/vertiport con-

texts), while preserving coupling with ATM/UTM ecosystems and ATS institutional

functions DECEA (2024a).

Main elements represented in the DECEA UAM architecture include:

```
■ UAM operational domain: UAM operators, vehicles, and provider entities acting
within defined urban airspace layers.
```
■ **Vertiport/local area structures:** local infrastructure nodes and associated opera-

tional constraints.

■ **Ecosystem bridges (ECO-UAM/ECO-UTM):** coordination interfaces linking UAM

services with UTM and broader ATM governance.

```
■ ATS/system components: PSNA, SDSP, ATM systems, and CGNA-related func-
tions supporting integration, supervision, and service continuity.
```
Conceptually, both DECEA architectures are closely aligned with the FAA proposi-

tion described in the FAA CONOPS references: they maintain authority-centric gover-

nance while enabling distributed, data-driven service provision by specialized providers

and interoperable operational actors DECEA (2022, 2024a); Federal Aviation Adminis-

tration (2020, 2023a).

4.3.3 | FAAUTMandUAMReferenceArchitectures

The FAA Concept of Operations documents provide useful reference architectures be-

cause they separate regulatory authority from distributed service provision, while pre-

serving shared situational awareness and coordinated decision-making among actors

Federal Aviation Administration (2020, 2023a).

In the FAA UTM architecture (Figure 4.4), the FAA remains the sovereign authority

for airspace and operating rules, while UTM ecosystem services are largely provided

through interoperable industry participants (for example, UAS Service Suppliers), with

standardized data exchange, discovery, and coordination functions Federal Aviation

Administration (2020).

Core principles emphasized in the UTM CONOPS include:


Chapter4. ExistingSystemsandOperations 4.3. SystemOverview

]

Figure 4.3: UAM architecture (adapted from DECEA PCA 351-7, Figure 10) DECEA

(2024a).


Chapter4. ExistingSystemsandOperations 4.3. SystemOverview

■ **Federated service provision:** multiple service suppliers can operate concurrently

under common interoperability rules.

```
■ Strategic deconfliction first: operation intent is shared in advance to reduce tacti-
cal conflicts.
```
```
■ Data-centric coordination: participants rely on structured digital information ex-
change instead of voice-centric coordination.
```
■ **Authority preservation:** regulatory and public-safety interfaces remain explicit

and enforceable.

```
■ Scalable participation: architecture supports growth in operation density, mis-
sion diversity, and service providers.
```
Main architectural parts include:

■ FAA data and regulatory interfaces;

■ UAS Service Suppliers (USS) and inter-USS coordination;

■ Supplemental Data Service Providers (SDSP);

■ operators and UAS vehicles with operation-intent publication; and

■ discovery, authentication/authorization, and external/public-safety interfaces.

In the FAA UAM architecture (Figure 4.5), cooperative management is organized

around UAM-specific operational needs in dense urban and peri-urban environments,

while still preserving FAA regulatory authority and interface consistency with broader

NAS operations Federal Aviation Administration (2023a).

Core principles emphasized in the UAM CONOPS include:

```
■ Cooperative management environment: service providers and operators coordi-
nate through shared data products and standardized interfaces.
```
■ **Modular service design:** services are decoupled to allow phased capability growth

and technology evolution.

```
■ Infrastructure integration: vertiports, corridor constraints, weather, and urban
contingencies are treated as first-class operational elements.
```
```
■ Public-safety integration: public and public-safety access to relevant information
is explicitly modeled.
```

Chapter4. ExistingSystemsandOperations 4.3. SystemOverview

Figure 4.4: Notional FAA UTM architecture (adapted from FAA UTM CONOPS v2.0,

Figure 3) Federal Aviation Administration (2020).

```
■ Inter-provider interoperability: multiple providers can synchronize intent, con-
straints, and notifications.
```
Main architectural parts include:

■ FAA data exchange and security gateway functions;

■ Providers of Services for UAM (PSU);

■ Supplemental Data Service Providers (SDSP);

■ UAM operators, vehicles, and vertiport elements; and

■ provider-to-provider coordination plus public/public-safety interfaces.

The federated UTM model establishes a scalable, low-altitude operational frame-

work that balances regulatory authority with commercial agility. By leveraging a de-

centralized ecosystem of private-sector services, the system accelerates the deployment


Chapter4. ExistingSystemsandOperations 4.3. SystemOverview

Figure 4.5: Notional FAA UAM architecture (adapted from FAA UAM CONOPS v2.0,

Figure 8) Federal Aviation Administration (2023a).

of aerial capabilities through market-driven innovation while significantly reducing the

government’s infrastructural and human resource expenditures. This construct ensures

a stable environment for high-volume operations by utilizing shared situational aware-

ness and standardized protocols to mitigate risk and maintain systemic integrity. Ulti-

mately, this flexible architecture allows the aviation authority to retain absolute airspace

sovereignty while delegating the tactical management of authorized UAS flights to in-

dustry stakeholders.

4.3.4 | CORUSU-spaceDeploymentArchitecture(FinalArchitec-

tureandSolutions)

The CORUS Final Architecture and Solutions report proposes a deployment view in

which U-space/Drone Traffic Management (DTM) services can be implemented through

either monolithic or federated arrangements, depending on the criticality and coupling

of each service CORUS Consortium (2020a). The key architectural principle is that cen-

tralization versus federation should not be decided once for the whole ecosystem, but

service-by-service according to safety, security, privacy, performance, and governance

constraints CORUS Consortium (2020a).


Chapter4. ExistingSystemsandOperations 4.3. SystemOverview

In this architecture, interoperability is treated as the core enabler: heterogeneous

systems exchange operational, registration, and constraint information through clearly

defined interfaces, allowing multiple providers and authorities to coordinate operations

consistently in shared airspace CORUS Consortium (2020a).

Main elements represented in Corus Architecture (4.6) include:

■ **ATM System:** the interface with conventional air traffic management and manned-

aircraft operations.

■ **USSP/Country DTM Core:** principal and local DTM functions that orchestrate

U-space services in a given jurisdiction.

```
■ Registration Systems: identity and registration services linked to states/countries
and service providers.
```
```
■ Operator DTM Systems: operator-side systems that consume DTM services and
manage mission execution.
```
■ **Drone Operation Systems:** operational platforms that connect operator intent

with flight execution and monitoring.

■ **Supporting Systems:** external enablers such as CNS infrastructure, weather/sensor

services, and digital terrain models.

```
■ Cross-border/Jurisdiction Interfaces: interconnections among neighboring coun-
try/state systems for coordinated operations.
```
From a transition perspective, CORUS therefore frames U-space architecture as a

modular ecosystem with layered responsibilities, where some capabilities may remain

centralized for assurance reasons while others can be federated to improve scalability

and market openness CORUS Consortium (2020a).

International references (Federal Aviation Administration (FAA) and Concept of

Operations for European UTM Systems (CORUS)/U-space) indicate that scalable Un-

manned Aircraft System Traffic Management (UTM)/Urban Air Mobility (UAM) oper-

ation depends on structured intent-sharing, interoperable service providers, and clear

authority boundaries. These patterns are being used as comparative inputs for Brazil-

ian adaptation CORUS Consortium (2019a,b); Federal Aviation Administration (2020,

2023a).


Chapter4. ExistingSystemsandOperations 4.4. SupportEnvironment

Figure 4.6: CORUS deployment overview (Figure 28, adapted from CORUS Final Ar-

chitecture and Solutions) CORUS Consortium (2020a).

**4.4 | SupportEnvironment**

The current support environment combines legacy Air Traffic Management (ATM) as-

sets with ongoing digitalization initiatives. Key enabling dimensions include:

■ data integration across airspace, operations, and constraints;

■ secure information exchange among authorities, providers, and operators;

■ procedural harmonization for mixed manned/unmanned environments; and

■ progressive validation through operational evaluations and field tests.


Chapter4. ExistingSystemsandOperations 4.5. OngoingStudiesandOperationalEvaluations

Within this digitalization path, the DECEA ATM guideline aligns with the System

Wide Information Management (SWIM) initiative by promoting a service-oriented in-

formation environment in which operational data is standardized, discoverable, and

shareable across the ATM community, instead of being exchanged only through frag-

mented point-to-point channels DECEA (2025c). In practice, this SWIM-oriented di-

rection supports better interoperability among ATM, UTM, and UAM service layers by

improving data consistency, timeliness, and coordination quality for both strategic plan-

ning and operational execution DECEA (2022, 2024a, 2025c).

This support baseline is sufficient for present operations but requires incremental

enhancement in interoperability, real-time coordination, and contingency handling to

support high-density future demand DECEA (2022); Federal Aviation Administration

(2020).

**4.5 | OngoingStudiesandOperationalEvaluations**

4.5.1 | FederalAviationAdministration(FAA)/NationalAeronautics

andSpaceAdministration(NASA)UTMMaturationStudies

In the U.S. context, Federal Aviation Administration (FAA)-National Aeronautics and

Space Administration (NASA)-industry Unmanned Aircraft System Traffic Manage-

ment (UTM) maturation efforts have been used to validate federated coordination, strate-

gic deconfliction, security mechanisms for data exchange, and higher-complexity oper-

ational scenarios. These studies are relevant as reference material because they provide

evidence on progressive deployment, standards maturation, and operational perfor-

mance limits in realistic environments Federal Aviation Administration (2020); National

Aeronautics and Space Administration (2023).

The FAA UTM Field Test (UFT) Version 1.0 was executed as a structured test-and-

evaluation campaign to assess practical maturity of UTM infrastructure, services, and

interoperability in realistic operating environments Federal Aviation Administration

(2023b). The effort was organized with FAA test-site partners and industry participants,

using staged activities (onboarding, checkouts, shakedowns, and showcase operations)

to progressively increase operational complexity and evaluate service behavior under

representative mission conditions Federal Aviation Administration (2023b).

At architecture level, the tested ecosystem followed a federated model in which FAA

interfaces and industry service providers exchange operational data through standard-

ized service interactions. Figure 4.7 (from the UFT report) summarizes this UTM high-


Chapter4. ExistingSystemsandOperations 4.5. OngoingStudiesandOperationalEvaluations

level architecture Federal Aviation Administration (2023b).

Figure 4.7: UTM high-level architecture (adapted from FAA UTM Field Test (UFT) Final

Report, Figure 1) Federal Aviation Administration (2023b).

Broadly, the architecture tested during UFT included the following main elements:

```
■ FAA Flight Information Management System (FIMS): data-exchange interface
between FAA systems and UTM participants.
```
```
■ USS network and DSS-based interoperability: cooperative information sharing
among UAS Service Suppliers (USS), including discovery/synchronization ser-
```
vices.

```
■ Supplemental Data Service Providers (SDSP): external data sources (e.g., weather/
surveillance/ performance-related inputs) supporting operational decisions.
```
```
■ Operators and public/ public-safety interfaces: operational execution and autho-
rized data access for situational awareness, oversight, and response.
```
Regarding scenarios, the UFT campaign created and executed multiple scenario fam-

ilies to validate progressive capabilities. Shakedown scenarios included: (i) UTM op-

erations in environments of varying complexity, (ii) public-safety UTM operations in

varying complexity, (iii) public-safety queries due to concern of UAS operations, and


Chapter4. ExistingSystemsandOperations 4.5. OngoingStudiesandOperationalEvaluations

(iv) future concept elements for post-incident investigation involving UAS Federal Avi-

ation Administration (2023b). Showcase scenarios then emphasized strategic decon-

fliction, dynamic replanning, priority operations, conformance monitoring, and data-

correlation/historical-query functions in increasingly dense operations Federal Avia-

tion Administration (2023b).

Operationally, the campaign reported 76 operations in Shakedown 1, 65 operations

in Shakedown 2, and final-showcase execution totaling 197 operations at NYUASTS

and 147 at MAAP, providing empirical evidence for infrastructure and service-maturity

assessment under diverse operational tempos Federal Aviation Administration (2023b).

4.5.2 | BR-UTMInitiativeandFieldTests

Within the Brazilian operational baseline, SARPAS (Sistema para Solicitação de Acesso

ao Espaço Aéreo Brasileiro por Aeronaves não Tripuladas) remains the main digital

channel used by operators to request and manage UAS access authorizations, provid-

ing structured submission of operation data, documentation, and mission constraints to

support airspace assessment and authorization decisions DECEA (2023); Governo Fed-

eral do Brasil (2026). Although detailed technical architecture publications are limited,

DECEA CONOPS references and official service material show SARPAS NG as a key

operational interface in the broader UTM ecosystem and regulatory workflow DECEA

(2022, 2024b).

From an operational perspective, SARPAS supports a lifecycle centered on: request

submission, rule/constraint checking, authority analysis, and issuance (or denial) of

access conditions, with traceability for the requesting operator and oversight authorities

DECEA (2023, 2024b); Governo Federal do Brasil (2026).

At Brazilian level, Brazilian Unmanned Aircraft System Traffic Management (BR-

UTM) operational evaluations are being used as ongoing studies to validate progres-

sively more complex service behaviors, including discovery/synchronization, strategic

deconfliction, operational intent lifecycle management, and dynamic contingency re-

sponse.

Field-test documentation indicates an evolution path from baseline interoperability

checks (initial tests) toward end-to-end multi-provider operations, priority handling,

in-flight contingency procedures, and response-time assessment under dynamic con-

straints DECEA (2025a,b).

These ongoing evaluations are particularly relevant to this Operational Concept

Document (OCD) because they provide empirical inputs for defining realistic transition


Chapter4. ExistingSystemsandOperations4.6. DigitalFlightRules(DFR)asaCommonInterfaceforeVTOLandUAS

steps, required provider capabilities, and institutional readiness conditions for broader

cross-domain Traffic Management (xTM) deployment in Brazil.

**4.6 | DigitalFlightRules(DFR)asaCommonInterface**

**foreVTOLandUAS**

An additional reference that strengthens this transition discussion is the NASA Tech-

nical Memorandum NASA/TM-20220013225, which introduces Digital Flight and the

associated Digital Flight Rules (DFR) concept as a cooperative operating mode intended

to complement Visual Flight Rules (VFR) and Instrument Flight Rules (IFR) in shared

airspace National Aeronautics and Space Administration (2022). In this view, DFR is

not limited to a single vehicle class; it is framed as a common operational paradigm for

multiple new entrants, including drone operations and urban air-taxi/eVTOL services.

The core idea is that qualified operators can use connected digital information, in-

tent sharing, and automation-assisted self-separation practices to maintain flight-path

safety, instead of relying exclusively on visual see-and-avoid or continuous tactical sep-

aration services from Air Traffic Control (ATC) National Aeronautics and Space Admin-

istration (2022). This characteristic is particularly relevant for high-tempo low-altitude

operations, where both UAS and eVTOL missions require dynamic replanning, scalable

coordination, and interoperability across different service providers.

From an architecture and governance perspective, DFR contributes a useful integra-

tion hypothesis for this chapter’s baseline analysis:

```
■ single digital-operational logic across vehicle classes: a harmonized ruleset can
reduce fragmentation between UTM-oriented drone services and UAM/eVTOL
services;
```
■ **common data and intent interfaces:** interoperability requirements converge around

structured intent publication, constraint sharing, and conformance monitoring;

■ **progressive integration with incumbent ATM:** DFR is positioned as complemen-

```
tary to existing VFR/IFR operations, supporting phased deployment instead of
abrupt replacement; and
```
```
■ regulatory focus and scalability: a shared framework can simplify certification/oversight
pathways and support higher traffic densities with predictable safety assurance.
```
Therefore, for Brazilian xTM evolution, DFR can be interpreted as a strategic ref-

erence model for converging UAS and eVTOL operations toward a common interface


Chapter4. ExistingSystemsandOperations4.6. DigitalFlightRules(DFR)asaCommonInterfaceforeVTOLandUAS

layer, aligned with ongoing ATM/UTM/UAM digitalization and interoperability goals

discussed throughout this chapter DECEA (2022, 2024a); Federal Aviation Administra-

tion (2020, 2023a); National Aeronautics and Space Administration (2022).


## 5 Proposed System Operational Overview

**5.1 | Missions**

The mission is to enable safe, scalable, and coordinated low-altitude air operations in

Brazil through a joint UTM + UAM operational architecture, as a practical transition

path toward a broader AAM (Advanced Air Mobility) ecosystem.

The intended operational outcome is not the creation of separate traffic management

paradigms for uncrewed and urban air mobility users, but a converged architecture

in which both domains share compatible monitoring, authorization, and deconfliction

mechanisms. The core premise is that UTM and UAM operational behaviors are suf-

ficiently similar in low-altitude, high-density contexts that maintaining distinct archi-

tectures would create avoidable complexity, reduced interoperability, and inconsistent

safety outcomes.

Priority mission threads are defined as follows:

```
■ Primary mission: Provide low-altitude flight safety and traffic control through
continuous monitoring of operations, pre-flight and dynamic authorization mech-
```
anisms, and coordinated response to non-conformance or emergent hazards.

```
■ Secondary mission: Establish a unified architecture model that allows UTM and
UAM actors to operate under harmonized rules, shared situational awareness, and
common service interfaces.
```
■ **Enabling mission:** Support Brazil’s progressive evolution toward AAM by defin-

```
ing foundations that can accommodate future vehicle classes, service providers,
and regulatory maturation without architectural fragmentation.
```

Chapter5. ProposedSystemOperationalOverview 5.2. OperationalPoliciesandConstraints

At this stage, this section does not define implementation dates or deployment phases;

instead, it defines the operational intent and mission logic that justify a converged

UTM+UAM architecture.

The following goals translate the mission intent into operational priorities aligned

with the SIMUA project direction.

**Goal 1: Establish a Unified Low-Altitude Traffic Management Baseline in Brazil**

**Goal 2: Improve Safety and Flow in High-Density Urban Air Corridors**

**Goal 3: Enable the Progressive Transition to AAM rather than a fragmented UTM-**

**UAM**

**5.2 | OperationalPoliciesandConstraints**

This section defines the policy baseline and current operational constraints for a joint

UTM+UAM architecture in Brazil, considering the present DECEA regulatory ecosys-

tem and the transition toward AAM-oriented operations.

For operations in Brazilian airspace, the following DECEA documents and services

are directly relevant to this mission context:

```
■ ICA 100-40 – Aeronaves não Tripuladas e o Acesso ao Espaço Aéreo Brasileiro
DECEA (2023).
```
■ DCA 351-6 – Concepção Operacional UTM Nacional DECEA (2022).

```
■ DCA 351-7 – Diretriz da Aeronáutica para o Controle do Espaço Aéreo Brasileiro
DECEA (2025c).
```
■ PCA 351-6 – Concepção Operacional do Espaço Aéreo de Rotas Livres DECEA

(2025d).

■ PCA 351-7 – Concepção Operacional UAM Nacional DECEA (2024a).

■ Novo Tutorial SARPAS DECEA 2024 DECEA (2024b).

Although this CONOPs focuses on DECEA references, operational applicability also

depends on alignment with ANAC requirements (airworthiness and operation) and

ANATEL requirements (spectrum and equipment), since mission execution is interde-

pendent across these authorities.

The joint architecture is constrained by technical, social, and institutional factors that

currently limit performance, scale, and predictability:


Chapter5. ProposedSystemOperationalOverview 5.2. OperationalPoliciesandConstraints

■ **Meteorological limitations:** low ceilings, convective weather, precipitation, wind

```
shear, and localized urban microclimates reduce operational windows and in-
crease contingency rates for both drones and eVTOL missions.
```
```
■ Airspace complexity and mixed-traffic coordination: coexistence with manned
aviation, public-safety flights, and temporary segregated areas increases planning
and tactical deconfliction burden.
```
```
■ Authorization latency and procedural overhead: depending on mission profile
and location, operations may require additional coordination, NOTAM handling,
```
and lead times incompatible with some on-demand use cases.

■ **Public acceptance and social license to operate:** noise perception, privacy con-

```
cerns, visual pollution, and risk perception can reduce community acceptance in
dense urban areas.
```
■ **Digital interoperability maturity:** despite advances (e.g., ECO-UTM), heteroge-

```
neous service providers, uneven API maturity, and data-governance gaps still con-
strain seamless interconnection.
```
Key technology constraints shared by RPAS and eVTOL ecosystems include:

■ **Navigation, surveillance, and CNS resilience:** robust positioning, communica-

```
tion continuity, and remote identification performance in dense urban and interference-
prone environments.
```
■ **Detect-and-avoid and conformance monitoring:** consistent tactical separation as-

surance across heterogeneous vehicle capabilities and mixed levels of autonomy.

■ **Vehicle endurance and energy constraints:** battery performance, payload-range

tradeoffs, and turnaround-time limitations that affect network reliability.

```
■ Automation assurance and cybersecurity: need for verifiable autonomy behavior,
secure command-and-control links, and resilient digital infrastructures.
```
```
■ Scalable vertiport/ground infrastructure integration: synchronization between
airspace management, ground operations, charging/energy systems, and emer-
```
gency response procedures.

This operational concept assumes progressive maturation of DECEA UTM regula-

tion, continued development of BR-UTM ecosystem mechanisms, and institutional co-

ordination among DECEA, ANAC, ANATEL, operators, and municipalities. Until these


Chapter5. ProposedSystemOperationalOverview 5.3. OperationalEnvironment

dependencies mature, joint UTM+UAM operations remain feasible but constrained in

scale, density, and service regularity.

**5.3 | OperationalEnvironment**

The joint UTM+UAM concept operates in dense low-altitude and terminal environ-

ments where safety depends on synchronized performance of the aircraft segment, re-

mote pilot station, command-and-control (C2) links, and services. In line with ICAO

Doc 10019, the operational environment must therefore be defined as an integrated air-

ground-digital ecosystem rather than as airspace alone International Civil Aviation Or-

ganization (2015).

Over the system life cycle, this environment is expected to evolve toward higher

automation, stronger digital interconnection, and greater traffic density. As foreseen

in ICAO RPAS guidance, these changes increase operational capability but also raise

assurance requirements for interoperability, human-system coordination, cybersecurity

resilience, and performance monitoring under abnormal conditions International Civil

Aviation Organization (2015).

To align this baseline with international RPAS safety guidance, ICAO Doc 10019

identifies five major hazard elements that remote-flight operations must continuously

manage through procedures, surveillance, and conformance monitoring International

Civil Aviation Organization (2015):

■ **Conflicting traffic:** risk of loss of separation with other aircraft in shared or adja-

cent airspace.

```
■ Terrain and fixed obstacles: collision risk with natural relief, buildings, towers,
and other structures.
```
■ **Hazardous meteorological conditions:** safety degradation under adverse weather

and rapidly changing local conditions.

```
■ Incompatible airspace activity: exposure to operations or restrictions that are not
coordinated with the remote-flight mission profile.
```
■ **Manoeuvring-area obstructions and vehicles:** surface movement hazards during

taxi, take-off, landing, and ground repositioning phases.


Chapter5. ProposedSystemOperationalOverview 5.4. Personnel

**5.4 | Personnel**

This OCD section defines “who” will operate the system.

5.4.1 | 5.4.1OrganizationalStructure

The organizational structure for joint UTM+UAM operations can be represented by

three interacting domains: **government** , **industry** , and **users**. In both FAA and DECEA

architectural models, these domains exist with similar mission intent (safe, scalable op-

erations), but with different allocation of operational control and service orchestration

authority DECEA (2022, 2024a); Federal Aviation Administration (2020, 2023a).

Figure 5.1: Government–Industry–Users relationship in the BR-xTM Level 1 organiza-

tional view.

**Government side (FAA / DECEA role):** defines policy, safety rules, airspace con-

straints, compliance criteria, and oversight mechanisms. In the FAA model, gover-

nance tends to emphasize performance-based rules and market-enabled service pro-

vision with federal oversight interfaces. In the DECEA model, governance is more

centrally integrated with national airspace management structures and state-led opera-

tional coordination.

**Industry side (service and technology role):** provides UTM/UAM enabling ser-

vices, digital platforms, integration middleware, aircraft/avionics capabilities, and op-

erational support functions. Under FAA-oriented architecture, industry service sup-

pliers have broader responsibility for tactical digital service delivery under regulatory

constraints. Under DECEA-oriented architecture, industry innovation is incorporated


Chapter5. ProposedSystemOperationalOverview 5.4. Personnel

through interfaces that remain strongly coupled to central CNS/ATM governance and

authorization workflows.

**Users side (operators and mission consumers):** includes drone operators, eVTOL

operators, logistics/public-safety mission users, and other authorized airspace partic-

ipants that consume the service ecosystem. In both models, users are accountable for

conformance, qualification, and operational safety performance; however, the interac-

tion pattern differs: FAA models prioritize distributed service mediation, while DECEA

models emphasize coordinated access via nationally harmonized channels.

**Relationship between domains:** government establishes the rule-space and assur-

ance envelope; industry implements interoperable operational services inside that enve-

lope; users execute missions through those services and return operational data/compliance

evidence. The relationship is therefore bidirectional and continuous: policy constrains

service design, service design shapes user behavior, and user/system performance feeds

back into regulatory and architectural evolution.

5.4.2 | PersonnelProfile

Personnel for the joint UTM+UAM architecture is organized by the same three-domain

structure presented in Section 5.4.1 (gvn/ind/users). The following subsections sum-

marize representative personnel profiles, responsibilities, and ownership/maintenance

patterns.

GovernmentPersonnel(gvn)

On the government side, representative personnel includes airspace policy managers,

regulatory specialists, safety and risk analysts, ATC/UTM supervisory teams, govern-

ment centralized-hub operators (national UTM/UAM coordination cell), and cyberse-

curity/audit personnel. Their primary responsibilities are to define constraint priorities

and operating rules, approve strategic constraints and emergency priorities, supervise

compliance, maintain national situational-awareness functions, and coordinate contin-

gency response with public-safety authorities. These structures are typically owned by

State institutions (civil/military aviation authorities and delegated agencies) and main-

tained by government technical teams, with contracted support when required.

IndustryPersonnel(ind)

On the industry side, representative personnel includes USSP/U-space service-provider

operators, SDSP (Supplemental Data Service Provider) teams, network and C2 engi-


Chapter5. ProposedSystemOperationalOverview5.5. JustificationforandNatureofChanges

neers, software/API integration teams, fleet-operations-center staff, and maintenance/reliability

engineers. Their main responsibilities are to provide digital traffic services and data

products, sustain flight-intent exchange and conformance support, integrate operator

systems with government interfaces, and maintain service-level performance and cyber-

security posture. These organizations are typically owned by private or mixed-capital

companies (service providers, OEMs, telecom/data firms, and vertiport operators) and

maintained by company operations and engineering teams, sometimes complemented

by managed-service partners.

User-SidePersonnel(users)

On the user side, representative personnel includes RPAS and eVTOL remote pilots/operators,

dispatchers, mission planners, public-safety crews, emergency coordinators, vertiport

owners/managers, and community-facing operations staff. Their responsibilities are

to execute missions within approved constraints, maintain operational conformance,

report incidents and anomalies, coordinate with service providers and authorities dur-

ing abnormal events, and manage passenger/cargo/public interfaces in local ground

operations. These structures are usually owned by operating organizations (air oper-

ators, logistics companies, municipalities, emergency services, and vertiport owners)

and maintained through internal training, certification, and recurrent competency pro-

grams.

Across both FAA- and DECEA-influenced architectures, staffing depth tends to in-

crease with traffic density, automation level, and criticality of missions. Personnel evo-

lution therefore requires recurrent qualification in digital interoperability, cybersecurity,

safety management, and multi-agency coordination.

**5.5 | JustificationforandNatureofChanges**

This section consolidates why a converged UTM+UAM operational architecture is needed

and what must change from the current fragmented baseline. The rationale is consistent

with DECEA transition documents for BR-UTM/UAM, with FAA CONOPS lessons on

scalable digital coordination, with CORUS/U-space deployment principles for interop-

erability and service modularity, and with the U.S. AAM strategic-planning baseline

that explicitly anticipates increased use of low-altitude airspace and the need for inter-

operable, scalable integration mechanisms CORUS Consortium (2019b, 2020a); DECEA

(2022, 2024a); Federal Aviation Administration (2020, 2023a); United States Government

(2025a,b).


Chapter5. ProposedSystemOperationalOverview5.5. JustificationforandNatureofChanges

5.5.1 | JustificationforChange

Change is required because projected low-altitude operations (RPAS growth plus eV-

TOL introduction) increase traffic density, mission diversity, and time-critical demand

beyond what isolated authorization and monitoring workflows can safely absorb at

scale. In operational terms, the current baseline is functional for low-to-moderate com-

plexity, but it becomes progressively limited under high-density, mixed-traffic scenar-

ios requiring near-real-time intent sharing, dynamic constraint propagation, and coor-

dinated contingency handling DECEA (2022, 2024a); Federal Aviation Administration

(2020).

This demand-growth direction is reinforced by the U.S. AAM National Strategy and

AAM Comprehensive Plan (2025), which frame AAM as a progressively expanding op-

erational layer requiring coordinated governance, digital interoperability, infrastructure

readiness, and phased scaling across public and private actors United States Govern-

ment (2025a,b). Although developed for the U.S. context, these strategic references are

relevant here because they strengthen the case that fragmented UTM/UAM constructs

become increasingly inefficient as low-altitude traffic density and service diversity grow.

The main deficiencies to be addressed are: heterogeneous interfaces among actors;

variable latency in coordination and authorization chains; uneven interoperability ma-

turity between ATM/UTM/UAM services; and limited standardization of digital oper-

ational evidence for safety assurance and post-event analysis. FAA and CORUS CONOPS

references, together with the strategic direction in the AAM National Strategy and Com-

prehensive Plan, indicate that these limitations are recurrent in early-stage ecosystems

and are mitigated through structured service roles, explicit data-exchange interfaces,

and clearly partitioned authority boundaries CORUS Consortium (2019a, 2020a); Fed-

eral Aviation Administration (2023a); United States Government (2025a,b).

This CONOPs therefore justifies a new integrated architecture baseline rather than in-

cremental local fixes only. The intent is not to replace existing state authority functions,

but to reorganize interactions among government, industry, and users so that scaling

can occur without degrading safety, accountability, or regulatory coherence.

5.5.2 | SummaryofNeededChanges

The required changes are grouped below by implementation priority. (Note: they are

not described by this document, but were raised during the group discussions, litera-

ture reviews, workshops, conferences, operational areas visits, and on meetings of the

SIMUA project.)


Chapter5. ProposedSystemOperationalOverview5.5. JustificationforandNatureofChanges

**Essential changes (E):**

■ **E1 – Common operational data model and interface governance:** establish manda-

```
tory, interoperable exchange of flight intent, constraints, conformance status, and
contingency events across government-industry-user interfaces.
```
```
■ E2 – Dynamic constraint and priority management: implement coordinated mech-
anisms to publish, update, and enforce airspace constraints and mission-priority
```
rules (including public-safety and emergency precedence).

■ **E3 – Integrated monitoring and conformance assurance:** move from isolated su-

```
pervision to a shared monitoring picture with traceable responsibility allocation
and incident evidence retention.
```
```
■ E4 – Defined authority boundaries and escalation workflows: formalize who
decides, who executes, and how escalation occurs under degraded, abnormal, or
```
emergency conditions.

**Desirable changes (D):**

```
■ D1 – Federated service ecosystem with assurance controls: allow multi-provider
innovation (USSP/SDSP-like roles) while preserving central safety and regulatory
oversight.
```
```
■ D2 – Progressive automation of coordination tasks: increase automation in strate-
gic deconfliction, flow balancing, and decision support while maintaining human
```
accountability.

■ **D3 – Cross-domain performance metrics:** define common KPIs (safety events, co-

```
ordination latency, conformance rates, service availability) to support continuous
improvement.
```
**Optional/Longer-term changes (O):**

■ **O1 – Advanced predictive services:** adoption of higher-order predictive risk and

capacity-management services for dense metropolitan corridors.

■ **O2 – Expanded automation for routine approvals:** limited-scope automated ap-

provals for well-characterized operations under validated constraints.

This prioritization follows the common pattern observed across DECEA, FAA, and

CORUS references: establish interoperability and governance first, then scale service

federation and automation in controlled increments CORUS Consortium (2020a); DE-

CEA (2022); Federal Aviation Administration (2020).


Chapter5. ProposedSystemOperationalOverview5.5. JustificationforandNatureofChanges

5.5.3 | ChangesConsideredbutNotIncluded

The following alternatives were considered but are not included in the current baseline:

```
■ Full centralization of all operational services: excluded because it may reduce
ecosystem scalability and innovation speed, and can create single-point bottle-
```
necks for non-critical service functions.

■ **Fully uncoordinated market-only federation:** excluded because safety assurance,

```
priority management, and state accountability require a stronger common gover-
nance envelope than purely bilateral integrations provide.
```
```
■ Immediate high-autonomy decision replacement of human supervisors: excluded
due to current assurance, certification, and trust limits for abnormal and mixed-
```
traffic edge cases.

```
■ Parallel permanent architectures for UTM and UAM: excluded because long-
term duplication of interfaces, rules, and monitoring chains increases complexity
```
and creates avoidable interoperability and safety risks.

Accordingly, this CONOPs adopts a phased converged model: centralized gover-

nance and safety assurance combined with controlled federation of industry services,

consistent with comparative DECEA/FAA/CORUS architectural lessons CORUS Con-

sortium (2019b); DECEA (2024a); Federal Aviation Administration (2023a).


## 6 6 System Overview

This chapter provides a high-level system overview aligned with the Operational Con-

cept Document (OCD) intent, focusing on scope, boundaries, operators, interfaces, ca-

pabilities, and architecture only to the level needed to support understanding of the

operational concept. It does not provide a detailed design description.

At this stage, the architecture is presented in SysML only at the joint Unmanned Air-

craft System Traffic Management (UTM) + Urban Air Mobility (UAM) CONOPS level,

emphasizing integration logic and operational relationships rather than implementation

detail.

The operators, interfaces, capabilities, and architectural elements described in this

chapter establish the common baseline that will be used throughout the operational

scenarios.

**6.1 | 6.1SystemScope**

The scope is limited to the Government/ authority, industry service-provider, and op-

erational user domains that directly participate in BR-xTM operation (joint UTM/UAM

context). Accordingly, this chapter addresses the institutional and operational interac-

tions among public authorities, certified or authorized service providers, and mission

operators/end users that are required for planning, authorization, execution, monitor-

ing, and contingency handling.

This scope does not extend to broader upstream or downstream supply-chain ele-

ments (e.g., manufacturing, component logistics, financing, insurance, or other indirect

support markets), except when a minimal reference is necessary to explain an opera-

tional interface. We recognize that additional stakeholder roles are involved in real-


Chapter6. 6SystemOverview 6.2. 6.2SystemGoalsandObjectives

world operations; however, they are intentionally out of scope in this document to pre-

serve clarity and analytical simplicity for the scenario-based operational assessment.

**6.2 | 6.2SystemGoalsandObjectives**

Based on the mission definition in Chapter 5 and the prioritized change set (E/D/O),

the system goals are decomposed into operational objectives that guided architecture

decisions and scenario description.

At system level, BR-xTM shall provide a converged UTM+UAM operational base-

line that preserves safety, enables coordinated industry service provision, and supports

user operations with predictable rules and performance.

The mission-level decomposition is summarized as follows:

■ **Safety and orderly flow objective (from Primary Mission):** assure separation/deconfliction

```
support, conformance monitoring, and timely contingency escalation for mixed
low-altitude operations.
```
■ **Convergence objective (from Secondary Mission):** use harmonized data models,

```
interfaces, and operational rules so drones and eVTOL users interact through a
common service framework.
```
```
■ Transition objective (from Enabling Mission): allow phased growth in traffic
density, automation, and provider federation without architectural fragmentation
or loss of accountability.
```
**6.3 | 6.3UsersandOperators**

This section focuses on the BR-xTM user side (operators and direct operational users).

Government and industry service-provider domains are treated as enabling actors that

exist to allow users to plan and conduct operations safely, but they are not the primary

focus of this subsection.

Figure 6.1 summarizes the user-role view adopted for BR-xTM operations.

**Operators** The operator is the primary operational user responsible for overall mis-

sion management, compliance, intent submission, and safe execution decisions.

```
“The Operator is the person or entity responsible for the overall management of their
operation.” Federal Aviation Administration (2020)
```

Chapter6. 6SystemOverview 6.4. 6.4SystemInterfacesandBoundaries

Figure 6.1: BR-xTM user-role view focused on users and operators.

```
“Explorador ou Operador que solicite a operação da Aeronave Não Tripulada.” DECEA
(2023)
```
**Remote Pilot in Command (RPIC) / Pilot in Command (PIC).** The pilot user role is

responsible for safe flight conduct at execution level, either remotely (UAS) or onboard

(UAM), consistent with the operation type.

```
“The remote pilot in command (RPIC) is the person responsible for the safe conduct of
each UAS flight.” Federal Aviation Administration (2020)
```
```
“The PIC is the person aboard the UAM aircraft who is ultimately responsible for the
operation and safety during flight.” Federal Aviation Administration (2023a)
```
**Public-interest/public-safety user.** This user class includes authorized entities that

access operational information for safety, security, and public-interest purposes, without

acting as the flight-execution operator.

```
“Public interest stakeholders are entities declared by governing processes (e.g., COPs)
to be able to access UAM operational information and notifications.” Federal Aviation
Administration (2023a)
```
**6.4 | 6.4SystemInterfacesandBoundaries**

This section cross-correlates the architecture with Figure 6.2 (interface view) to identify

which interface links are used by each user/operator class defined in Section 6.3.


Chapter6. 6SystemOverview 6.4. 6.4SystemInterfacesandBoundaries

Figure 6.2: BR-xTM interfaces view (functional links among user, provider, and author-

ity domains).

From the FAA CONOPS perspective, the user-facing links are primarily digital infor-

mation exchange links for intent submission, operational status exchange, advisories/constraints

reception, and oversight-access traces.

```
Table 6.1: System interface links and observations (reviewed
against FAA/DECEA CONOPS references).
```
```
System Ele-
ment A
```
```
System Ele-
ment B
```
**Link Type Observation**

```
SDSP SDSP Inter_SDSP Bidirectional link for discovery/query services
and possible supplemental-data sharing among
providers in federated environments.
```

Chapter6. 6SystemOverview 6.4. 6.4SystemInterfacesandBoundaries

Table 6.1: System interface links and observations (continued).

```
System Ele-
ment A
```
```
System Ele-
ment B
```
**Link Type Observation**

```
SDSP Vertiport SDSP_Link Optional bidirectional link for direct
supplemental-data request/response (e.g.,
local weather/obstacle/context data) when
exposed by the vertiport ecosystem.
SDSP UAM Vehi-
cles
```
```
SDSP_Link Optional bidirectional link for supplemental-
data responses. In FAA UAM CONOPS, this is
often mediated by PSU/SDSP services, though
direct consumption can exist depending on ar-
chitecture.
SDSP UAM Opera-
tor
```
```
SDSP_Link Optional bidirectional link for request/response
of supplemental data. Operators may receive it
directly or via service suppliers (PSU/USS-style
mediation).
SDSP UAS SDSP_Link Optional bidirectional link for supplemental-
data responses to UAS operations, direct or me-
diated by the service supplier depending on im-
plementation.
SDSP UAS Opera-
tors
```
```
SDSP_Link Optional bidirectional link for request/response
of supplemental data, including contextualiza-
tion via service suppliers before use in opera-
tions.
SDSP SS Supplier SDSP_Link Bidirectional link for request/response of sup-
plemental data that service suppliers can relay,
contextualize, and integrate into user-facing op-
erational services.
UAM Vehicle UAM Vehicle V2V_Link Bidirectional inter-vehicle coordina-
tion/awareness link (e.g., position/status
broadcast such as Remote ID/ADS-B-
compatible paradigms or equivalent coop-
erative awareness means).
UAM Vehicle SS Supplier SS_V Link Bidirectional link for positioning and flight-
status exchanges. In UAM terminology this
aligns with PSU-facing service interactions.
UAM Opera-
tor
```
```
UAM Vehicle Vehicle Op-
eration_Link
```
```
Bidirectional operator-aircraft control/feedback
link (human/automated/hybrid), includ-
ing HMI/data-link/audio feedback loops as
applicable.
```

Chapter6. 6SystemOverview 6.4. 6.4SystemInterfacesandBoundaries

Table 6.1: System interface links and observations (continued).

```
System Ele-
ment A
```
```
System Ele-
ment B
```
**Link Type Observation**

```
UAS Opera-
tor
```
```
UAS Vehicle Op-
eration_Link
```
```
Bidirectional operator-aircraft control/feedback
link (human/automated/hybrid), includ-
ing HMI/data-link/audio feedback loops as
applicable.
UAM Opera-
tor
```
```
UAM Opera-
tor
```
```
O2O_Link Operator-to-operator coordination link
(formal/informal), potentially via ser-
vice systems and/or direct channels
(voice/text/radio/visual procedures).
UAM Opera-
tor
```
```
SS Supplier SS_OP_Link Bidirectional flight-coordination link: opera-
tional intents, notifications, constraints, airspace
updates, and supplemental data exchanges.
UAM Opera-
tor
```
```
UAS Visual_Link Human/operator-level see/detect interaction
capability where operationally relevant in
mixed environments.
UAM Opera-
tor
```
```
UAS Opera-
tor
```
```
O2O_Link Cross-domain operator-to-operator coordina-
tion link for deconfliction and operational
awareness in mixed UAM/UAS operations.
UAM Vehicle UAS V2V_Link Bidirectional inter-vehicle aware-
ness/coordination link in mixed traffic, in-
cluding cooperative position/status exchange
and detect-and-avoid support cues.
UAS SS Supplier SS_V Link Bidirectional link for vehicle positioning/flight-
status exchange with service supplier support
functions.
UAS Opera-
tor
```
```
UAM Vehicle Visual_Link Human/operator-level visual or procedu-
ral awareness link with UAM vehicles
during mixed operations when line-of-
sight/observation is relevant.
UAS Opera-
tor
```
```
UAS Opera-
tor
```
```
O2O_Link Operator-to-operator coordination link via
systems and/or direct communications
(text/voice/radio/visual procedures).
UAS UAS V2V_Link Bidirectional inter-UAS aware-
ness/coordination link (position/status
broadcast and cooperative safety support,
technology-dependent).
```

Chapter6. 6SystemOverview 6.4. 6.4SystemInterfacesandBoundaries

Table 6.1: System interface links and observations (continued).

```
System Ele-
ment A
```
```
System Ele-
ment B
```
**Link Type Observation**

```
UAS Opera-
tor
```
```
SS Supplier SS_OP_Link Bidirectional flight-coordination link for intent
exchange, notifications, constraints, airspace
modifications, and supplemental data support.
Public or
Public Safety
```
```
SS Supplier SS_Public
_Link
```
```
Authorized bidirectional query/access link for
flight information, notifications, constraints,
and safety/security-relevant operational data.
SS Supplier SS Supplier Inter_SS_C2 Bidirectional service-to-service coordina-
tion/discovery link supporting intent ex-
change, notifications, constraints propagation,
and cooperative airspace use.
CVTMS SS Supplier RVMS
_SS_Link
```
```
Bidirectional link between centralized govern-
ment hub and service suppliers for constraints,
requests, responses, operational status, and no-
tifications.
CVTMS Other Man-
agement
Systems
```
```
FlightMng Bidirectional link with ATM/other manage-
ment systems for exchange of UTM+UAM
(AAM-layer) operational information.
```
**Link-type flow dictionary (derived from the interface decomposition).**

```
Table 6.2: Link-type flow dictionary: expected data flows and ref-
erence definitions.
```
```
Link Type What can flow (with FAA/DECEA/ASTM anchor definitions)
Inter_SDSP
■ Discovery/query metadata and service-availability indications
between supplemental-data providers.
```
```
■ Supplemental data products (e.g.,
weather/surveillance/obstacle context) for downstream op-
erational use.
```
```
■ FAA anchor: SDSP-type services provide supporting operational
data to operators/USSs/PSUs in federated models Federal Avi-
ation Administration (2020, 2023a).
```
```
■ ASTM anchor: supplementary data service and weather-
provider roles/interfaces are standardized in SDSP/WIP-
oriented specifications ASTM International (2023, 2024b).
```

Chapter6. 6SystemOverview 6.4. 6.4SystemInterfacesandBoundaries

Table 6.2: Link-type flow dictionary (continued).

```
Link Type What can flow (with FAA/DECEA/ASTM anchor definitions)
SDSP_Link
■ Request/response exchanges for weather, terrain, obstacle, per-
formance, and contextual safety data.
```
```
■ Optional direct user-consumption path or mediated path
through service suppliers (USS/PSU).
```
```
■ FAA anchor: UTM/UAM CONOPS identify SDSP support
as data consumed by operators and suppliers for plan-
ning/execution Federal Aviation Administration (2020, 2023a).
```
```
■ DECEA anchor: BR-UTM/UAM concepts require integrated
data-sharing services to support operational decisions and con-
straints management DECEA (2022, 2024a).
V2V_Link
■ Position/status awareness broadcasts and cooperative traffic-
awareness cues.
```
```
■ Detect-and-avoid support cues and proximity/conflict-related
state awareness.
```
```
■ FAA anchor: cooperative low-altitude operations depend on
shared situational awareness and intent/state exchange Federal
Aviation Administration (2020, 2023a).
```
```
■ ASTM anchor: Remote ID/tracking and related interoperability
mechanisms support broadcast/awareness layers ASTM Inter-
national (2021, 2022a).
SS_V Link
■ Vehicle telemetry/state, position updates, and mission-status
events to supplier systems.
```
```
■ Supplier-originated advisories/constraints and service re-
sponses back to vehicle-facing systems.
```
```
■ FAA anchor: USS/PSU services support confor-
mance/coordination by ingesting operational state and issuing
service outputs Federal Aviation Administration (2020, 2023a).
```

Chapter6. 6SystemOverview 6.4. 6.4SystemInterfacesandBoundaries

Table 6.2: Link-type flow dictionary (continued).

```
Link Type What can flow (with FAA/DECEA/ASTM anchor definitions)
Vehicle Opera-
tion_Link ■ Operator/remote-pilot command/control actions to the aircraft
system.
```
```
■ Aircraft-system feedback to operator (flight status, health, alerts,
mission progress).
```
```
■ FAA anchor: Operator/RPIC/PIC roles require continuous
control-feedback loops for safe conduct Federal Aviation Admin-
istration (2020, 2023a).
```
```
■ DECEA anchor: operator/solicitante responsibility in access and
operation lifecycle implies command/feedback accountability
DECEA (2023).
O2O_Link
■ Operator-to-operator coordination messages (deconfliction, local
procedures, contingency coordination).
```
```
■ Informal or formal communication exchanges
(text/voice/radio/procedural channels).
```
```
■ FAA anchor: shared situational awareness and cooperative oper-
ations require coordination among participants Federal Aviation
Administration (2020, 2023a).
SS_OP_Link
■ Operational intent submission/update/cancellation and strate-
gic deconfliction responses.
```
```
■ Constraints, notifications, advisories, conformance states, and
off-nominal coordination data.
```
```
■ FAA anchor: USS/PSU define the operator-facing service bridge
for intent sharing and coordinated operations Federal Aviation
Administration (2020, 2023a).
```
```
■ ASTM anchor: USS interoperability and coordinated in-
tent/conformance services are central to the ASTM UTM base-
line ASTM International (2021).
```

Chapter6. 6SystemOverview 6.4. 6.4SystemInterfacesandBoundaries

Table 6.2: Link-type flow dictionary (continued).

```
Link Type What can flow (with FAA/DECEA/ASTM anchor definitions)
Visual_Link
■ Human-observed traffic/context cues used for tactical awareness
in mixed environments.
```
```
■ Supplemental see/detect awareness where procedures require
human visual contribution.
```
```
■ FAA anchor: pilot/operator safe-conduct responsibilities in-
clude continuous awareness of aircraft, obstacles, and environ-
ment Federal Aviation Administration (2020, 2023a).
SS_Public_Link
■ Authorized public/public-safety queries and responses for oper-
ational information/notifications.
```
```
■ Safety/security-relevant access to selected operational data un-
der governance controls.
```
```
■ FAA anchor: public-interest/public-safety stakeholders may ac-
cess operational information via authorized mechanisms Federal
Aviation Administration (2020, 2023a).
```
```
■ DECEA anchor: access/authorization and institutional coordi-
nation roles frame controlled information use DECEA (2023).
Inter_SS_C2
■ Supplier-to-supplier discovery, coordination, and
intent/conflict-related synchronization exchanges.
```
```
■ Constraints and notifications propagation supporting coopera-
tive use of shared airspace.
```
```
■ FAA anchor: federated USS/PSU network behavior relies on
inter-provider data sharing and coordination Federal Aviation
Administration (2020, 2023a).
```
```
■ ASTM anchor: USS interoperability requirements establish com-
mon exchange behavior across suppliers ASTM International
(2021).
```

Chapter6. 6SystemOverview 6.5. 6.6SystemCapabilities

Table 6.2: Link-type flow dictionary (continued).

```
Link Type What can flow (with FAA/DECEA/ASTM anchor definitions)
RVMS_SS_Link
■ Centralized hub-to-supplier exchanges for constraints, requests,
responses, and operational notifications.
```
```
■ Oversight/support channel for consolidated operational aware-
ness at authority side.
```
```
■ FAA/DECEA anchor: authority-facing data interfaces (e.g.,
FIMS-like in FAA and centralized governance in DECEA) sup-
port regulatory/operational oversight DECEA (2022, 2025c);
Federal Aviation Administration (2020).
FlightMng
■ Exchange with ATM/other management systems: constraints,
coordination messages, status updates, and integration-layer op-
erational data.
```
```
■ Supports cross-domain synchronization between conventional
ATM functions and UTM/UAM service layers.
```
```
■ FAA/DECEA anchor: UTM/UAM integration with legacy
ATM/ATS information environments is a core CONOPS require-
ment DECEA (2024a, 2025c); Federal Aviation Administration
(2020, 2023a).
```
**6.5 | 6.6SystemCapabilities**

The primary capability of BR-xTM is to provide safe use of low-altitude airspace for

mixed UTM/UAM operations. In practical terms, this means the system shall con-

tinuously support conflict prevention first, conflict separation second, and collision-

avoidance as a last-resort safety net, consistent with the safety layering described in

ICAO Doc 10019 International Civil Aviation Organization (2015).


Chapter6. 6SystemOverview 6.5. 6.6SystemCapabilities

Figure 6.3: Three-layer safety logic for RPAS operations (strategic conflict management,

separation provision, and collision avoidance), adapted from ICAO Doc 10019.

Accordingly, BR-xTM shall be capable of:

```
■ Strategic conflict management (planning layer): organizing airspace use, balanc-
ing demand/capacity, and synchronizing intended operations before flight to re-
```
```
duce exposure to hazards DECEA (2022); Federal Aviation Administration (2020);
International Civil Aviation Organization (2015).
```
```
■ Separation provision (operational layer): maintaining safe separation minima (or
equivalent well-clear conditions) during execution through conformance moni-
toring, dynamic constraints, and coordinated service/authority actions DECEA
```
```
(2024a); Federal Aviation Administration (2023a); International Civil Aviation Or-
ganization (2015).
```
```
■ Collision avoidance / DAA (last-resort layer): activating detect-and-avoid re-
sponses when the separation layer is degraded or compromised, so conflicting
```
```
traffic or hazards can still be avoided in time ASTM International (2025); Interna-
tional Civil Aviation Organization (2015).
```

Chapter6. 6SystemOverview 6.6. 6.7SystemArchitecture

To make these three layers effective in BR-xTM, the system also requires cross-cutting

capabilities in interoperable data exchange, shared situational awareness, event trace-

ability, and contingency escalation workflows across operators, service suppliers, and

authorities ASTM International (2021); DECEA (2025c); Federal Aviation Administra-

tion (2020).

**6.6 | 6.7SystemArchitecture**

Figure 6.4 presents the BR-xTM Level 2 architectural view used in this OCD to connect

users, service suppliers, and authority-facing management functions under a single op-

erational logic.

Figure 6.4: BR-xTM Level 2 architecture (integrated UTM+UAM operational structure).

From an operational-behavior perspective, the architecture promotes the capabil-

ities of Section 6.6 by enforcing a closed-loop cycle across all actors: mission intent

publication, strategic deconfliction, execution authorization, conformance monitoring,


Chapter6. 6SystemOverview 6.6. 6.7SystemArchitecture

off-nominal handling, and traceable closure/archiving. In this loop, users are the mis-

sion drivers, service suppliers provide coordination and information mediation, and

authority-side hubs provide constraints, oversight, and system-level safety governance.

The system-elements tree illustration (Figure 6.5) should be interpreted as a decom-

position of the CONOPs into the three operational elements: **industry/service-provider**

**side** , **government/authority side** , and **user/operator side**. For each element in that de-

composition, the tree indicates applicability of ASTM references listed in Chapter 2, so

traceability is explicit between standard requirements and the role each element per-

forms in operation.

Within this mapping, three ASTM documents have major structural impact on this

CONOPs baseline:

■ **ASTM F3548-21:** interoperability and coordination behavior among Service Sup-

```
pliers (including intent/conflict-data exchange logic), which is foundational for
strategic deconfliction in federated operations ASTM International (2021).
```
```
■ ASTM F3411-22a: Remote ID and tracking foundations that support shared iden-
tification/position awareness across system elements and improve cross-actor sit-
```
uational understanding ASTM International (2022a).

■ **ASTM F3442-25:** DAA performance requirements that define last-resort tactical

```
safety behavior when strategic and separation layers are stressed or degraded
ASTM International (2025).
```
**Initial behavior by ICAO Doc 10019 safety layers.**

```
■ Layer 1 – Strategic conflict management (before flight): UAM Operator and UAS
Operator publish mission intent and planning constraints through SS_OP_Link
```
```
to SS Supplier ; SS Supplier exchanges coordination data through Inter_SS_C2 ;
CVTMS publishes restrictions/priorities through RVMS_SS_Link ; supplemental
```
```
context can be requested via SDSP_Link. This pre-flight information flow is the
initial strategic baseline for scenario setup.
```
```
■ Layer 2 – Separation/tactical management (during execution): UAM Vehicle
and UAS provide state/position updates to SS Supplier via SS_V Link ; UAM
```
```
Operator and UAS Operator receive conformance/constraint updates through
SS_OP_Link ; Inter_SS_C2 and RVMS_SS_Link propagate dynamic changes among
```
```
suppliers and authority-side hub; tactical awareness is reinforced by V2V_Link
and, when applicable, Visual_Link.
```

Chapter6. 6SystemOverview 6.6. 6.7SystemArchitecture

Figure 6.5: System-elements tree with requirement traceability: decomposition by gov-

ernment, industry/service-provider, and user/operator sides with ASTM applicability

mapping.


Chapter6. 6SystemOverview 6.6. 6.7SystemArchitecture

■ **Layer 3 – Collision avoidance / DAA (last resort):** when the separation layer is

```
degraded, immediate hazard-mitigation information is driven at vehicle/operator
level through V2V_Link , Visual_Link , and Vehicle Operation_Link ; off-nominal
```
```
status and recovery coordination are propagated back to SS Supplier via SS_V
Link / SS_OP_Link , then synchronized across Inter_SS_C2 and RVMS_SS_Link
```
for traceable ecosystem response.

In summary, the BR-xTM Level 2 architecture is intended to operationalize safety as

a layered behavior rather than a single function: prevent conflicts early, manage separa-

tion continuously, and preserve a last-resort avoidance mechanism when residual risk

emerges.


## 7 7 Operational Processes

This chapter presents the operational scenarios used to evaluate safety, capacity, and

resilience in low-altitude traffic management (initially through simulation). The sce-

narios are structured to compare conditions, isolated strategic and tactical approaches,

and hybrid architectures under deterministic and stochastic disturbances. Operational

Scenarios:

```
■ Scenario 1: Operational Chaos Baseline (Blind Flight) – This scenario establishes
the safety baseline by simulating drones flying without centralized management
```
```
(xTM) or detect-and-avoid (DAA) technology, operating on direct routes with no
prior coordination. The objective is to empirically identify the density threshold
```
```
at which collision risk (Mid-Air Collision Proxy) becomes unsustainable, serving
as a technical justification for the implementation of UTM infrastructure.
```
```
■ Scenario 2: Onboard Tactical Resolution (Standalone DAA) – Focused on air-
craft autonomy, this scenario relies solely on the DAA system to manage conflicts
```
```
in real time, without flight plan approval from xTM. The analysis aims to demon-
strate the limitations of relying exclusively on onboard sensors, assessing the “lo-
```
```
gistical collapse” caused by route inefficiencies and the continuous increase of ad
hoc deviations required to maintain safe separation.
```
```
■ Scenario 3: Strategic xTM Separation (Strict 4D Tubes) – In this model, man-
agement is purely strategic and centralized, with xTM blocking flight plans on
```
```
the ground and issuing slots in rigid, non-overlapping “4D tubes,” but without
in-flight DAA support. The focus is to quantify the impact on ground delay prop-
```
```
agation, demonstrating that although mathematically safe, network-based resolu-
tion overly constrains airspace capacity by breaking efficiency thresholds (ATFM).
```

Chapter7. 7OperationalProcesses

■ **Scenario 4A: Optimized Hybrid Architecture (xTM + DAA)** – This configura-

```
tion validates the model advocated by FAA/DECEA by combining macro-level
volume allocation via xTM with tactical micro-conflict resolution via DAA. By en-
```
```
abling narrower reserved 4D tubes, the system optimizes flow and flight admis-
sibility, demonstrating that strategic intent management delegated to cooperative
```
onboard systems maximizes network performance without compromising safety.

■ **Scenario 4B: Hybrid Architecture under Stochastic Conditions (Real-World Chaos)**

- Expanding the hybrid model, this scenario introduces non-deterministic vari-

```
ables such as wind and physical disturbances to test the resilience of the UTM
architecture under real operational conditions. The objective is to consolidate
```
```
the robustness of the design, demonstrating that the dual-layer service structure
(FIMS/USS and DAA) can mitigate performance degradation and dynamic de-
```
lays, preventing incidents even under environmental stress.

Before detailing each scenario, this section compares the experiment design with

the operational logic proposed in DECEA and FAA CONOPs for both UTM and UAM.

The purpose is to show which CONOPs capabilities are intentionally absent, partially

present, or fully integrated in each scenario, and why this progression is relevant for

safety and capacity assessment.

Comparative framing:

From a CONOPs perspective, the scenarios evaluate the transition from non-cooperative

operations to a coordinated hybrid ecosystem:

■ **FAA UTM/UAM perspective:** progression from minimal coordination toward

```
federated service-based operations, with strategic intent sharing, conformance
monitoring, and tactical conflict mitigation.
```
```
■ DECEA UTM/UAM perspective: progression from isolated operation toward in-
tegrated low-altitude governance with authorization workflows, dynamic con-
straints, and coordinated service-provider participation.
```
Capability mapping across scenarios:


Chapter7. 7OperationalProcesses 7.1. Scenario1:OperationalChaosBaseline(BlindFlight)

```
Scenario FAA UTM/UAM use-
case alignment
```
```
DECEA UTM/UAM
use-case alignment
```
**Interpretation in this study**

```
1 – Blind
Flight
```
```
Pre-CONOPs base-
line (no service-layer
orchestration)
```
```
Pre-CONOPs base-
line (no coordinated
access/control layer)
```
```
Stresses unmanaged den-
sity and defines the empir-
ical safety floor.
2 – Stan-
dalone DAA
```
```
Tactical-only layer
without strategic
intent services
```
```
Tactical-only be-
havior without
centralized pre-
authorization logic
```
```
Tests whether autonomy
alone can sustain scalabil-
ity.
```
```
3 – Strict 4D
Tubes
```
```
Strategic decon-
fliction with rigid
pre-tactical allocation
```
```
Strategic control
emphasis with strict
ground-based slot-
ting
```
```
Tests safe-but-constrained
throughput and delay
propagation.
```
```
4A – Hybrid
xTM+DAA
```
```
Full strategic+tactical
complementarity
expected in mature
CONOPs
```
```
Integrated authoriza-
tion/coordination
plus onboard conflict
handling
```
```
Target architecture for bal-
ancing safety and capacity.
```
```
4B – Hybrid
+ Stochastic
Disturbance
```
```
Mature CONOPs
behavior under real-
world uncertainty
and variability
```
```
Operational resilience
under dynamic con-
straints and distur-
bances
```
```
Validates robustness of
the hybrid concept under
stress.
```
Considering both FAA and DECEA CONOPs references, the scenarios are also mapped

against core operational functions:

```
■ Strategic intent management (pre-flight): absent in Scenarios 1–2, dominant in
Scenario 3, and balanced with tactical autonomy in Scenarios 4A–4B.
```
■ **Tactical separation management (in-flight):** absent in Scenario 1, isolated in Sce-

nario 2, intentionally suppressed in Scenario 3, and integrated in Scenarios 4A–4B.

```
■ Conformance and dynamic adaptation: minimal in Scenarios 1–2, rigid in Sce-
nario 3, adaptive and cooperative in Scenarios 4A–4B.
```
■ **Network performance objective (safety vs. capacity):** Scenario 1 prioritizes diag-

```
nosis of risk, Scenario 2 diagnoses tactical overload, Scenario 3 diagnoses strategic
over-constraint, and Scenarios 4A–4B evaluate balanced performance.
```
**7.1 | Scenario1:OperationalChaosBaseline(BlindFlight)**


Chapter7. 7OperationalProcesses 7.1. Scenario1:OperationalChaosBaseline(BlindFlight)

7.1.1 | ScenarioObjective

Establish an empirical baseline of collision exposure in unmanaged low-altitude oper-

ations, where aircraft fly direct trajectories without strategic deconfliction, centralized

service orchestration, or onboard detect-and-avoid support. The primary objective is

to identify the traffic-density threshold at which the Mid-Air Collision Proxy becomes

operationally unacceptable. See Figure 7.1.

Figure 7.1: Scenario 1 illustration: unmanaged chaos baseline (blind-flight condition).

7.1.2 | OperationalEvents

1. Mission demand is generated for a defined airspace and time window.
2. Flights are launched with direct origin-destination routing and no pre-flight con-
    flict filtering.
3. Aircraft progress simultaneously in shared volumes with no coordinated spacing
    logic.
4. Potential conflicts emerge as density increases and crossing points accumulate.
5. Proximity and conflict indicators are measured continuously during execution.
6. Scenario run is closed and safety/performance data are consolidated for threshold
    analysis.


Chapter7. 7OperationalProcesses 7.1. Scenario1:OperationalChaosBaseline(BlindFlight)

7.1.3 | Users

```
■ Remote pilots/operators: execute flights as submitted, without external tactical or
strategic support.
```
7.1.4 | KeyActions

■ Define initial density sets, airspace geometry, and mission generation rules.

■ Run unmanaged traffic batches under blind-flight assumptions.

```
■ Record conflict-proxy occurrences, loss-of-separation events, and congestion pat-
terns.
```
■ Compare observed behavior across increasing demand levels.

```
■ Determine the operational breaking point where unmanaged traffic is no longer
acceptable.
```
7.1.5 | PostConditions

At scenario completion, the study produces a validated baseline dataset containing

collision-proxy rates, traffic-density versus risk curves, and reference evidence of unmanaged-

airspace saturation. These outputs become the benchmark against which all subsequent

managed scenarios (DAA-only, xTM-only, and hybrid) are compared.

7.1.6 | PoliciesandBusinessRules

```
■ No xTM/FIMS/USS strategic approval, slot allocation, or intent negotiation is ap-
plied.
```
■ No onboard DAA maneuvering logic is enabled for conflict resolution.

■ Direct routing remains fixed after departure except for termination conditions de-

fined by the simulated collisions.

```
■ Safety acceptability is assessed through predefined Mid-Air Collision Proxy thresh-
olds established by the experiment protocol.
```

Chapter7. 7OperationalProcesses7.2. Scenario2:OnboardTacticalResolution(StandaloneDAA)

7.1.7 | Summary

Scenario 1 intentionally represents an operationally chaotic baseline to expose the in-

trinsic safety limits of uncoordinated low-altitude traffic. Its function in the chapter

is foundational: it quantifies why purely unmanaged operations are not scalable and

establishes the technical rationale for introducing strategic (xTM) and tactical (DAA)

service layers. This scenario is a worst-case safety reference and must not be used as a

real operational configuration.

**7.2 | Scenario2:OnboardTacticalResolution(Standalone**

**DAA)**

7.2.1 | ScenarioObjective

Assess the operational limits of a tactical-only safety architecture in which aircraft rely

exclusively on onboard DAA logic for in-flight conflict management, without strategic

xTM pre-coordination. The objective is to quantify how far autonomy can sustain safe

separation before route inefficiency and deviation accumulation degrade network per-

formance. See Figure 7.2.

Figure 7.2: Scenario 2 illustration: standalone DAA with reactive maneuver inefficiency.


Chapter7. 7OperationalProcesses7.2. Scenario2:OnboardTacticalResolution(StandaloneDAA)

7.2.2 | OperationalEvents

1. Mission demand is generated in the same airspace and temporal envelope used
    for baseline comparability.
2. Flights are launched without strategic slot allocation or pre-flight conflict filtering
    by xTM services.
3. Onboard sensing detects nearby traffic and predicts short-horizon conflicts.
4. DAA logic commands local maneuvers to preserve minimum separation.
5. Repeated tactical resolutions create route drift, travel-time growth, and local traffic

distortion. (This is a future research opportunity regarding KPI to AAM.)

6. Scenario run is closed with consolidation of safety, delay, and maneuver-burden

indicators.

7.2.3 | Users

```
■ Remote pilots/operators: supervise missions where tactical conflict mitigation is
delegated to onboard DAA.
```
```
■ Vehicle autonomy systems: configure sensing, detection thresholds, and maneuver-
response logic.
```
7.2.4 | KeyActions

■ Configure onboard detection envelopes and DAA trigger logic.

■ Execute traffic batches with no strategic xTM intervention.

■ Track conflict detections, maneuver frequency, and cumulative path deviations.

■ Measure effects on mission duration, throughput, and spatial congestion.

```
■ Identify the point where tactical-only management becomes operationally unsus-
tainable.
```

Chapter7. 7OperationalProcesses7.2. Scenario2:OnboardTacticalResolution(StandaloneDAA)

7.2.5 | PostConditions

At scenario completion, the study produces a tactical-performance dataset including

maneuver load, deviation growth, residual conflict exposure, and delay propagation

under DAA-only operations. These results define the practical ceiling of standalone

onboard conflict resolution and provide evidence for coupling tactical autonomy with

strategic orchestration.

7.2.6 | PoliciesandBusinessRules

```
■ No strategic xTM/FIMS/USS plan approval or slot negotiation is applied before
departure.
```
■ Tactical separation is handled only by onboard DAA sensing, prediction, and

avoidance logic.

```
■ Conflict resolution must respect aircraft performance and maneuverability con-
straints.
```
```
■ All runs preserve common initial demand assumptions to ensure comparability
with Scenario 1 and subsequent managed scenarios.
```
■ Performance acceptance is evaluated through predefined thresholds for separa-

tion preservation, maneuver burden, and operational delay.

7.2.7 | Summary

Scenario 2 demonstrates that tactical autonomy improves immediate conflict handling

compared with blind-flight conditions, but does not by itself guarantee scalable net-

work performance. The accumulation of local maneuvers and route inefficiencies high-

lights the need for strategic coordination layers in dense operations. In addition, this

scenario requires dedicated study of sensor and actuator capabilities and limitations

against applicable ASTM frameworks describing Remote ID and DAA interoperabil-

ity/performance expectations, in alignment with the referenced ASTM, FAA, and DE-

CEA guidance ASTM International (2021, 2022a, 2025); DECEA (2022, 2024a); Federal

Aviation Administration (2020, 2023a).


Chapter7. 7OperationalProcesses 7.3. Scenario3:StrategicxTMSeparation(Strict4DTubes)

**7.3 | Scenario 3: Strategic xTM Separation (Strict 4D**

**Tubes)**

7.3.1 | ScenarioObjective

Evaluate a purely strategic separation model in which conflict prevention is achieved

exclusively through pre-flight 4D deconfliction and slot allocation, without tactical in-

flight DAA support. The objective is to quantify how a mathematically safe but rigid

strategic regime affects throughput, delay propagation, and mission admissibility under

increasing demand. See Figure 7.3.

Figure 7.3: Scenario 3 illustration: strict strategic xTM with 4D tubes and ground-delay

effects.

7.3.2 | OperationalEvents

1. Operators submit intended trajectories and time windows as strategic flight in-
    tents.
2. Service Suppliers (SS) publish and query intent information through the DSS to

obtain a shared view of planned use of 4D volumes.

3. Strategic deconfliction logic detects overlaps and applies constraints (time shifts,
    denials, or alternative slots) to avoid 4D conflicts before departure.


Chapter7. 7OperationalProcesses 7.3. Scenario3:StrategicxTMSeparation(Strict4DTubes)

4. Multiple SS synchronize approved intents and constraints through DSS updates

to maintain cross-provider consistency.

5. Flights are authorized only when strict non-overlap criteria are satisfied in the
    reserved 4D tubes.
6. During execution, no onboard tactical conflict-resolution maneuvers are assumed;
    conformance is expected to follow the approved strategic plan.
7. Scenario run is closed with consolidation of acceptance rates, delay chains, and

residual strategic-conflict indicators.

7.3.3 | Users

```
■ Operators/flight requesters: submit mission intents and receive approval, delay,
or denial decisions.
```
■ **Service Suppliers (SS):** perform strategic conflict checks, manage local client in-

tents, and synchronize information via DSS.

```
■ Regulatory/supervisory authority: defines strategic separation rules and moni-
tors policy compliance across the network.
```
7.3.4 | KeyActions

1. **Intent packaging:** each operator encodes the mission as a 4D intent (planned vol-
    ume, altitude band, time of occupancy, and basic operational constraints).
2. **Initial submission to local SS:** the intent is submitted through the operator-to-
    supplier interface (SS_OP_Link), where format/completeness checks are applied.
3. **DSS publication:** the local SS publishes intent metadata to DSS so other SS can

discover overlapping candidates and common constraint context.

4. **Cross-SS discovery and query:** peer SS query DSS for potential 4D conflicts in the
    same spatiotemporal window and retrieve relevant intent identifiers.
5. **Strategic conflict evaluation:** each SS runs pre-flight deconfliction logic against
    local and external intents to detect 4D tube intersections.
6. **Constraint synchronization:** SS exchange/update constraints via DSS (for exam-

```
ple: slot shifts, denied windows, or priority reservations) until a consistent net-
work state is reached.
```

Chapter7. 7OperationalProcesses 7.3. Scenario3:StrategicxTMSeparation(Strict4DTubes)

7. **Decision and slot assignment:** the local SS returns authorization, delay, reroute

window, or rejection to each operator based on strict non-overlap policy.

8. **Pre-departure freeze:** once approved, the 4D tube reservation is frozen for execu-
    tion and shared status is updated across SS through DSS.
9. **Execution under strategic-only rules:** flights depart only inside approved win-

```
dows; no tactical DAA conflict-resolution maneuvers are considered in this sce-
nario.
```
10. **Outcome logging and KPI extraction:** the run records acceptance ratio, ground-

```
delay accumulation, queue propagation, and under-utilized capacity caused by
rigid strategic constraints.
```
7.3.5 | PostConditions

At scenario completion, the study provides a strategic-performance dataset including

accepted-versus-rejected intents, slot-induced delay distributions, propagation of ground

holding, and network utilization under strict 4D non-overlap rules. The results charac-

terize the operational ceiling of strategic-only management and define where tactical

support becomes necessary to recover efficiency.

7.3.6 | PoliciesandBusinessRules

■ Strategic separation is enforced through pre-flight intent management and strict

4D tube allocation.

```
■ DSS is used as the shared coordination mechanism for multiple SS to exchange/synchronize
intents, constraints, and conflict-status updates.
```
```
■ Authorization is granted only to operations whose planned 4D occupancy is conflict-
free under the applicable policy set.
```
```
■ Tactical in-flight DAA conflict resolution is intentionally out of scope for this sce-
nario.
```
```
■ Constraint-priority rules favor conflict prevention and policy compliance, even
when this increases delay or reduces throughput.
```

Chapter7. 7OperationalProcesses7.4. Scenario4A:OptimizedHybridArchitecture(xTM+DAA)

7.3.7 | Summary

Scenario 3 represents the strategic-only endpoint of UTM orchestration: safety is pri-

marily achieved through strict pre-flight 4D separation and network-wide consistency

of intent data across Service Suppliers coordinated via DSS. The step sequence above

follows the architecture/interface behavior shown in Figure 6.4 and Figure 6.2. This

approach aligns with ASTM UTM interoperability principles for intent sharing and dis-

tributed coordination, but it also exposes the cost of over-constraint in dense operations,

especially delay propagation and reduced admissibility when tactical flexibility is ab-

sent ASTM International (2021); DECEA (2022, 2024a); Federal Aviation Administration

(2020, 2023a).

**7.4 | Scenario4A:OptimizedHybridArchitecture(xTM**

**+DAA)**

7.4.1 | ScenarioObjective

Establish and evaluate the integrated safety architecture based on ICAO Doc 10019 lay-

ered logic, combining strategic xTM separation and tactical onboard DAA to maximize

safety without collapsing operational efficiency. The objective is to demonstrate that

preventive strategic management, continuous conformance awareness, and tactical con-

flict resolution operate as complementary layers when all available resources are acti-

vated. See Figure 7.4.


Chapter7. 7OperationalProcesses7.4. Scenario4A:OptimizedHybridArchitecture(xTM+DAA)

Figure 7.4: Scenario 4A illustration: optimized hybrid architecture (xTM + DAA).

7.4.2 | OperationalEvents

1. Operators prepare missions as 4D intents and submit them to their local SS for

strategic processing.

2. SS publish/query intents and constraints through DSS to synchronize network-

wide strategic context across multiple suppliers.

3. Strategic deconfliction allocates 4D reservations, but with narrower tubes enabled
    by confidence in tactical mitigation capacity.
4. Before departure, authorization outcomes (approved/delayed/rerouted) are re-
    turned to operators and synchronized across SS.
5. During flight, onboard DAA continuously evaluates local traffic encounters and
    issues tactical maneuvers when residual conflicts emerge.
6. Position capture and conformance state are shared through SS services, enabling
    cross-operator and cross-SS situational consistency.
7. Strategic and tactical layers are continuously reconciled (intent updates, advi-
    sories, and constraint refinements) to avoid divergence between plan and execu-

tion.

8. Scenario run is closed with integrated safety-capacity-performance assessment.


Chapter7. 7OperationalProcesses7.4. Scenario4A:OptimizedHybridArchitecture(xTM+DAA)

7.4.3 | Users

```
■ Operators/remote pilots: submit missions, monitor execution, and supervise automation-
assisted operations.
```
```
■ Service Suppliers (SS): perform strategic deconfliction, DSS coordination, intent/conformance
exchange, and shared traffic-state mediation.
```
```
■ Vehicle autonomy/avionics systems: provide onboard sensing, conflict predic-
tion, and DAA maneuver execution.
```
```
■ Regulatory/supervisory authority: defines policy constraints, oversees compli-
ance, and validates layered safety behavior.
```
7.4.4 | KeyActions

1. **Mission intent packaging (strategic layer):** operators encode missions as 4D in-
    tents with route, altitude, timing, and operational constraints.
2. **Submission and validation:** intents are submitted to local SS via SS_OP_Link and
    pass format/compliance checks.
3. **DSS publication/discovery:** SS publish intent metadata and query peer SS through
    DSS to detect potential inter-SS conflicts.
4. **Strategic conflict processing:** SS apply pre-flight deconfliction to remove 4D over-
    laps and negotiate synchronized constraints.
5. **Constraint synchronization across SS:** slot adjustments, denials, and priority rules
    are propagated through DSS until consistent network state is reached.
6. **Authorization decision:** each mission receives approval, delayed slot, constrained
    reroute window, or rejection.
7. **Pre-departure reservation freeze:** approved 4D allocations are frozen and shared
    across SS before launch.
8. **Onboard tactical readiness:** DAA detection envelopes, thresholds, and maneuver
    policies are activated per mission profile.
9. **In-flight conformance and position capture:** aircraft state/position updates are
    captured and shared through SS services for common situational awareness.


Chapter7. 7OperationalProcesses7.4. Scenario4A:OptimizedHybridArchitecture(xTM+DAA)

10. **Tactical conflict handling:** when residual conflicts occur, onboard DAA com-

mands local avoidance maneuvers while preserving strategic safety intent.

11. **Plan-execution reconciliation:** intent updates and advisories are exchanged be-

tween operators and SS so strategic and tactical layers remain aligned.

12. **Integrated KPI logging:** the run records conflict exposure, maneuver burden, ac-

ceptance ratio, delay propagation, and capacity utilization.

7.4.5 | PostConditions

At scenario completion, the study provides an integrated-performance dataset showing

how layered safety mechanisms affect risk reduction, mission admissibility, and opera-

tional efficiency. Outputs include strategic acceptance rates, tactical maneuver demand,

conformance quality, delay behavior, and net throughput under hybrid management.

7.4.6 | PoliciesandBusinessRules

```
■ Strategic pre-flight separation via xTM/SS and DSS coordination remains manda-
tory.
```
```
■ Tactical onboard DAA remains active as a complementary safety layer for resid-
ual/confined encounters.
```
```
■ Shared position capture and conformance information exchange through SS is re-
quired to maintain synchronized operational awareness.
```
```
■ Intent/constraint updates must be propagated across participating SS to preserve
interoperability and policy consistency.
```
```
■ Safety policy prioritizes layered risk mitigation (prevent, monitor, resolve) while
minimizing unnecessary strategic over-constraint.
```
7.4.7 | Summary

Scenario 4A operationalizes the ICAO Doc 10019 layered safety concept by combining

all relevant resources: strategic intent management, DSS-based multi-SS coordination,

shared position/conformance information through SS, and onboard DAA tactical res-

olution. By merging the strategic sequence from Scenario 3 with the tactical sequence

from Scenario 2, this scenario defines the intended mature architecture for high-density


Chapter7. 7OperationalProcesses7.5. Scenario4B:HybridArchitectureunderStochasticConditions(Real-WorldChaos)

operations where both safety and network performance must be sustained concurrently

ASTM International (2021, 2022a, 2025); DECEA (2022, 2024a); Federal Aviation Admin-

istration (2020, 2023a); International Civil Aviation Organization (2015). In this scenario

scope, we did not evaluate NFZ(no fly zones) creation policies or fairness criteria for

route allocation among operators.

**7.5 | Scenario4B:HybridArchitectureunderStochas-**

**ticConditions(Real-WorldChaos)**

7.5.1 | ScenarioObjective

Evaluate resilience of the hybrid architecture by starting from the balanced operating

condition achieved in Scenario 4A (high utilization, stable flow, and no collision events)

and then injecting chaotic elements over time. The objective is to measure how well

the combined strategic+tactical safety layers absorb disturbances when NFZs and non-

cooperative traffic dynamically disrupt a previously stable system. See Figure 7.5.

Figure 7.5: Scenario 4B illustration: resilience under stochastic disturbances and wind

deviations.


Chapter7. 7OperationalProcesses7.5. Scenario4B:HybridArchitectureunderStochasticConditions(Real-WorldChaos)

7.5.2 | OperationalEvents

1. The scenario begins from a validated balanced baseline equivalent to Scenario 4A
    steady-state performance.
2. All cooperative actors operate under normal hybrid rules (xTM strategic coordi-

nation + onboard DAA tactical protection).

3. New disturbances are progressively introduced, including stochastic wind and

timing perturbations.

4. Dynamic NFZs are created during execution, reducing available airspace and forc-
    ing strategic replanning.
5. Non-cooperative vehicles enter the operational volume without full intent-sharing
    behavior.
6. SS and operators update constraints/intents while DAA handles local residual

conflicts in real time.

7. Position capture, conformance status, and conflict-related data continue to be shared
    through SS for cross-network awareness.
8. The run ends after disturbance escalation phases, with resilience and degradation
    metrics consolidated.

7.5.3 | Users

```
■ Operators/remote pilots: execute missions from a balanced initial state and re-
spond to dynamic restrictions.
```
■ **Service Suppliers (SS):** manage strategic replanning, DSS coordination, and dis-

semination of dynamic constraints.

```
■ Vehicle autonomy/avionics systems: perform onboard tactical conflict mitigation
under rising uncertainty.
```
```
■ Regulatory/supervisory authority: injects/validates temporary restrictions (in-
cluding NFZ conditions) and monitors compliance.
```

Chapter7. 7OperationalProcesses7.5. Scenario4B:HybridArchitectureunderStochasticConditions(Real-WorldChaos)

7.5.4 | KeyActions

1. **Balanced initialization:** load the end-state configuration of Scenario 4A as the

reference operating point.

2. **Nominal verification window:** confirm full-capacity cooperative operation with

no collision events before perturbation starts.

3. **Disturbance schedule activation:** apply phased stochastic disturbances (wind,
    timing noise, and state uncertainty).
4. **Dynamic NFZ injection:** activate temporary no-fly constraints that invalidate por-
    tions of previously usable 4D volumes.
5. **Strategic reallocation cycle:** SS use DSS to synchronize updated constraints and
    recompute admissible slots/routes.
6. **Non-cooperative traffic insertion:** inject vehicles with limited/no intent sharing
    to stress detectability and coordination assumptions.
7. **Shared surveillance and position capture:** maintain SS-mediated distribution of

traffic/conformance updates to preserve common operational picture.

8. **Tactical containment actions:** onboard DAA performs local avoidance against

emergent encounters, including uncertainty-driven proximate conflicts.

9. **Hybrid reconciliation loop:** propagate intent changes, advisories, and revised

constraints so strategic and tactical layers stay synchronized.

10. **Recovery assessment:** evaluate whether the system converges to a new stable
    regime or accumulates unstable delay/congestion.
11. **Resilience KPI extraction:** log safety proxies, conflict rates, delay growth, reroute
    burden, throughput loss, and recovery time.

7.5.5 | PostConditions

At scenario completion, the study delivers a resilience dataset comparing pre-chaos

baseline versus disturbed-operation outcomes. Outputs capture performance degrada-

tion magnitude, safety preservation effectiveness, ability to re-stabilize operations, and

the limits of hybrid coordination under compounded uncertainty.


Chapter7. 7OperationalProcesses7.5. Scenario4B:HybridArchitectureunderStochasticConditions(Real-WorldChaos)

7.5.6 | PoliciesandBusinessRules

```
■ The scenario must start from the balanced, collision-free hybrid configuration es-
tablished in Scenario 4A.
```
```
■ Disturbances are introduced incrementally to isolate degradation mechanisms and
avoid ambiguous causality.
```
```
■ Dynamic NFZ constraints are treated as mandatory strategic restrictions once ac-
tivated.
```
```
■ Non-cooperative traffic is modeled as reduced/absent intent-sharing behavior, re-
quiring stronger tactical reliance.
```
■ SS-based sharing of position/conformance information remains active to support

cross-operator/cross-SS situational awareness.

■ Safety preservation has priority over throughput when disturbance escalation forces

trade-offs.

7.5.7 | Summary

Scenario 4B is the controlled transition from order to chaos: it starts from a balanced

Scenario 4A condition and then introduces dynamic NFZs, non-cooperative vehicles,

and stochastic disturbances into that stable system. The purpose is to test whether the

hybrid architecture can preserve safety and recover acceptable performance when coop-

erative assumptions are progressively violated ASTM International (2021, 2022a, 2025);

DECEA (2022, 2024a); Federal Aviation Administration (2020, 2023a); International Civil

Aviation Organization (2015).

**ClosingNote**

The simulation results for each operational scenario defined in this chapter are docu-

mented in a separate results-focused document.



# References

American National Standards Institute and American Institute of Aeronautics and As-

tronautics. ANSI/AIAA-043B-2018 Guide for the Preparation of Operational Con-

```
cept Documents. PDF, 2018. URL https://webstore.ansi.org/standards/aiaa/
ansiaiaa043b2018.
```
ASTM International. ASTM F3548-21 Standard Specification for UAS Traffic Manage-

```
ment (UTM) UAS Service Supplier (USS) Interoperability. PDF, 2021. URL https:
//store.astm.org/f3548-21.html.
```
ASTM International. ASTM F3411-22a Standard Specification for Remote ID and Track-

ing. PDF, 2022a. URL https://store.astm.org/f3411-22a.html.

ASTM International. ASTM F3423/F3423M-22 Standard Specification for Vertiport De-

sign. PDF, 2022b. URL https://store.astm.org/f3423_f3423m-22.html.

ASTM International. ASTM F3623-23 Standard Specification for Surveillance Sup-

```
plementary Data Service Providers. PDF, 2023. URL https://store.astm.org/
f3623-23.html.
```
ASTM International. ASTM F3341/F3341M-24 Standard Terminology for Unmanned

```
Aircraft Systems. PDF, 2024a. URL https://store.astm.org/f3341_f3341m-24.
html.
```
ASTM International. ASTM F3673-24 Standard Specification for Performance for

```
Weather Information Reports, Data Interfaces, and Weather Information Providers
(WIPs). PDF, 2024b. URL https://store.astm.org/f3673-24.html.
```

References References

ASTM International. ASTM F3442-25 Standard Specification for Detect and Avoid

```
System Performance Requirements. PDF, 2025. URL https://store.astm.org/
Standards/F3442.htm.
```
CORUS Consortium. CORUS Volume 1 - Concept of Operations Enhanced Overview.

PDF, 2019a. URL https://cordis.europa.eu/project/id/763551.

CORUS Consortium. CORUS Volume 2 - U-space Concept of Operations. PDF, 2019b.

```
URL https://www.sesarju.eu/sites/default/files/documents/events/U-space%
20ConOps%2020190930.pdf.
```
CORUS Consortium. Final Architecture and Solutions. PDF, 2020a. URL https://

cordis.europa.eu/project/id/763551/results.

CORUS Consortium. Final Operations and UTM Requirements. PDF, 2020b. URL

https://cordis.europa.eu/project/id/763551/results.

DECEA. DCA 351-6 - Concepção Operacional UTM Nacional. PDF, 2022. URL https:

//publicacoes.decea.mil.br/publicacao/dca-351-6.

DECEA. ICA 100-40 - Aeronaves não Tripuladas e o Acesso ao Espaço Aéreo Brasileiro.

PDF, 2023. URL https://publicacoes.decea.mil.br/publicacao/ica-100-40.

DECEA. PCA 351-7 Concepcão Operacional UAM Nacional. PDF, 2024a. URL https:

//publicacoes.decea.mil.br/publicacao/PCA-351-7.

DECEA. Novo Tutorial SARPAS DECEA 2024. Web tutorial / PDF,

2024b. URL https://www.decea.mil.br/static/uploads/2024/07/

Novo-Tutorial-SARPAS-DECEA-2024.pdf.

DECEA. Briefing BR-UTM Field Test 2. Wiki / Technical Documentation, 2025a. URL

```
https://servicos2.decea.mil.br/br-utm/wiki/books/documentacao-tecnica/
page/briefing-br-utm-field-test-2.
```
DECEA. Ensaio Operacional 3 – Dezembro 2025. Wiki / Technical Docu-

```
mentation, 2025b. URL https://servicos2.decea.mil.br/br-utm/wiki/books/
documentacao-tecnica/chapter/ensaio-operacional-3-dezembro-2025.
```
DECEA. DCA 351-7 - Diretriz da Aeronáutica para o Controle do Espaço Aéreo

```
Brasileiro. PDF, 2025c. URL https://publicacoes.decea.mil.br/publicacao/
dca-351-7.
```

References References

DECEA. PCA 351-6 - Concepção Operacional do Espaço Aéreo de Rotas Livres. PDF,

2025d. URL https://publicacoes.decea.mil.br/publicacao/PCA-351-6.

Federal Aviation Administration. FAA UTM CONOPS Version 2. PDF,

2020. URL https://www.faa.gov/researchdevelopment/trafficmanagement/

utm-concept-operations-version-20-utm-conops-v20.

Federal Aviation Administration. FAA UAM CONOPS Version 2. PDF, 2023a. URL

https://www.faa.gov/air-taxis/uam_blueprint.

Federal Aviation Administration. UTM Field Test (UFT) Version 1.0 Final Report. PDF,

```
November 2023b. Local copy in project repository: References/Docs FAA/FAA -
UTM Field Test (UFT).pdf.
```
Governo Federal do Brasil. Solicitar acesso ao espaço aéreo brasileiro por aeronaves não

tripuladas. Portal de Serviços, 2026.

International Civil Aviation Organization. ICAO Doc 8168, Volume 1. PDF, 2007. ICAO

Doc 8168, Volume I.

International Civil Aviation Organization. Rules of the Air – Annex 2. PDF, 2009. Official

Gov.br service page.

International Civil Aviation Organization. ICAO Doc 10019

```
(2015). PDF, 2015. URL https://store.icao.int/en/
manual-on-remotely-piloted-aircraft-systems-rpas-doc-10019.
```
National Aeronautics and Space Administration. Digital Flight Rules: Applying Au-

```
tomation to Low-Altitude Flight. Technical Memorandum, 2022. URL https://ntrs.
nasa.gov/citations/20220013225. NASA/TM-20220013225.
```
National Aeronautics and Space Administration. NASA-CR-20230012505. PDF, 2023.

URL https://ntrs.nasa.gov/citations/20230012505.

SIMUA Project. Convênio nº003 ITA 2022. PDF, 2022a. Internal source (SIMUA); no

public URL available.

SIMUA Project. DocuSign Agreement – SIMUA Final Statement of Work. PDF, 2022b.

Internal source (SIMUA); no public URL available.

SIMUA Project. Termo Aditivo ao Plano de Trabalho ITA x ICEA. PDF, 2024. Internal

source (SIMUA); no public URL available.


References References

United States Government. AAM Comprehensive Plan 2025. PDF, 2025a. URL https:

//www.transportation.gov/aam-plan.

United States Government. AAM National Strategy. PDF, 2025b. URL https://www.

transportation.gov/aam-strategy.


# A

# Acronym,Abbreviations,andGlossary

[Provide project-specific acronym list, abbreviations, and glossary definitions.]

## A.1 | ASTMDefinitionsTraceabilityMatrix

This section consolidates definitions extracted from all ASTM documents in References/Docs

ASTM/. Repeated terms are intentionally preserved with their respective source citation

for full traceability.

```
Term Definition Source
3D volume a volume of airspace defined in terms of latitude, longitude, and altitude. ASTM International (2021)
4D volume a 3D volume plus a start and end time for the volume. ASTM International (2021)
Accepted one of the operational intent states. See 4.4 for more details. ASTM International (2021)
Activated one of the operational intent states. See 4.4 for more details. ASTM International (2021)
AES advanced encryption standard ASTM International (2022a)
AFIT Air Force Institute of Technology ASTM International (2021)
Air Gap An unobstructed clear area dimensionally dependent on site-specific con-
ditions that is located under a rooftop vertiport and between it and the
architectural structure immediately below it, which is designed to allow
the air circulating around and over a building to flow under the vertiport
rather than over the vertiport to reduce turbulence at the landing and
takeoff site(s).
```
```
ASTM International (2022b)
```
```
Air Taxi Used to describe a VTOL aircraft movement conducted above the surface
but typically below 100 ft [30.5 m] AGL, which allows for more rapid
aircraft movement from one point to another.
```
```
ASTM International (2022b)
```
```
AIRAC aeronautical information regulation and control ASTM International (2021)
ANSP air navigation service provider ASTM International (2021)
AOI area of interest ASTM International (2021)
API application programming interface ASTM International (2022a)
API application programming interface ASTM International (2021)
application
programming
interface (API)
```
```
inputs and outputs for operations intended for use by two or more soft-
ware modules.
```
```
ASTM International (2024b)
```

AppendixA. Acronym,Abbreviations,andGlossary A.1. ASTMDefinitionsTraceabilityMatrix

```
Term Definition Source
Approach Sur-
face (VFR)
```
```
The approach surface begins at each edge of the vertiport FA TO with
the same width as the FA TO and extends outward and upward for
a horizontal distance of 4000 ft [1219.2 m] where its width is then
500 ft [152.4 m]. The slope of the approach surface is 8:1. Although
VTOL approach/departure paths may curve, the length of the ap-
proach/departure surface remains fixed. The approach surface slope
may be reevaluated on a case-by-case basis at such time performance data
for individual aircraft has been certified and published that would indi-
cate a steeper, higher performance profile may be safely accomplished
and accommodated for.
```
```
ASTM International (2022b)
```
```
ARC aviation rulemaking committee ASTM International (2022a)
associated
elements
```
```
those elements that are not airborne or directly affixed to the unmanned
aircraft (UA) and are necessary to interact with the UA for safe initiation,
conduct, or termination of flight, for all normal, abnormal, or emergency
operations.
```
```
ASTM International (2024a)
```
```
authentication the process or action of verifying that the source of a Remote ID message
is the originator of the message. 3.3.2 broadcast, v—to transmit data to no
specific destination or recipient; data can be received by anyone within
broadcast range.
```
```
ASTM International (2022a)
```
```
authorized con-
straint provider
```
```
an organization or individual that has been granted the authority to cre-
ate and manage constraints in a region by a competent authority.
```
```
ASTM International (2021)
```
```
beyond visual
line of sight
(BVLOS)
```
```
operation when the UA cannot be seen by the individuals responsible for
see-and-avoid with unaided (other than corrective lenses or sunglasses,
or both) vision, but where the location of the UA is known through tech-
nological means without exceeding the performance capabilities of the
command and control (C2) link (see Terminology
```
```
ASTM International (2025)
```
```
broadcast UAS a UAS that is equipped for and is actively broadcasting Remote ID data
during an operation; being a broadcast UAS is not mutually exclusive
with being a networked UAS.
```
```
ASTM International (2022a)
```
```
C2 command and control ASTM International (2022a)
C2 command and control ASTM International (2021)
CAA Civil Aviation Authority ASTM International (2022a)
CAA civil aviation authority ASTM International (2021)
CMSA conformance monitoring for situational awareness ASTM International (2021)
collision avoid-
ance
```
```
avoidance maneuver with the objective of preventing the predicted pen-
etration of the nearmid-air collision volume (NMAC).
```
```
ASTM International (2025)
```
```
conflict a situation where two operational intents intersect both in space and time.
For operational intents to intersect both in space and time, at least one 4D
volume from each operational intent must intersect. For two 4D volumes
to intersect, the spatial dimensions of the 4D volumes must share at least
one point and the start/end time range for the two 4D volumes must
overlap.
```
```
ASTM International (2021)
```
```
conformance a situation where a UA is flying according to its Activated operational
intent. A UA flying inside of its Activated operational intent is in con-
formance. A UA flying outside of its Activated operational intent is non-
conforming or contingent.
```
```
ASTM International (2021)
```
```
constrained-
space operation
```
```
an unmanned aircraft systems operation in which UA ’s flight environ-
ment is limited by walls, ceiling, net, or other physical limitation of the
volume; also referred to as an “indoor operation.” This definition is not
to be used to denote virtual constraints, such as geofences or geocages.
```
```
ASTM International (2024a)
```

AppendixA. Acronym,Abbreviations,andGlossary A.1. ASTMDefinitionsTraceabilityMatrix

```
Term Definition Source
constraint one or more 4D volumes that inform USSs, UAS personnel, operator’s au-
tomation systems, or other stakeholders, or combinations thereof, about
specific geographically and time-limited airspace information. A con-
straint may restrict access to airspace for some or all operations, or it may
be informational.
```
```
ASTM International (2021)
```
```
constraint inter-
section
```
```
a situation where an operational intent and a constraint overlap in both
space and time. This is similar to operational intent conflicts, but conflicts
is deliberately not used because a constraint may not restrict access to
airspace.
```
```
ASTM International (2021)
```
```
Constraint
Management
```
```
a USS service and role that supports the creation, modification, and dele-
tion of constraints, as well as the dissemination of constraint information
to other USSs.
```
```
ASTM International (2021)
```
```
Constraint Pro-
cessing
```
```
a USS service and role that enables the USS to ingest constraint informa-
tion and relay it to the UAS personnel, operator’s automation systems, or
other stakeholders, or combinations thereof, for applicable operations.
```
```
ASTM International (2021)
```
```
Contingent one of the operational intent states. See 4.4 for more details. ASTM International (2021)
controlled
airspace
```
```
an airspace of defined dimensions within which air traffic control service
is provided in accordance with the airspace classification.
```
```
ASTM International (2025)
```
```
Controlling Di-
mension (CD)
```
```
The greatest distance between the two outermost opposite points on an
aircraft as measured along either the horizontal or longitudinal axis (that
is, wingtip to wingtip, rotor tip to rotor tip, rotor tip to wingtip, fuselage
to rotor tip, fuselage to fuselage, etc.), measured on a level horizontal
plane that includes all adjustable components extended to their maxi-
mum outboard deflection. This equates to the smallest circle enclosing
the VTOL aircraft projection on a horizontal plane in all possible opera-
tional configurations with rotor(s) turning.
```
```
ASTM International (2022b)
```
```
CONUS contiguous United States ASTM International (2022a)
cooperative in-
truder
```
```
those intruders using a Mode C/S transponder or ADS-B, or both, that
operate with like equipment used on other aircraft or ground-based ser-
vices to establish the intruder’s position.
```
```
ASTM International (2025)
```
```
coordinated op-
erational intent
```
```
an operational intent that has been coordinated with other relevant USSs
to prevent disallowed conflicts. Operational intents are required to be
coordinated prior to transitioning to the Accepted state
```
```
ASTM International (2021)
```
```
DAA detect and avoid ASTM International (2021)
DAA cycle maximum time from the detection of the intruder’s presence to the initi-
ation of an avoidance maneuver.
```
```
ASTM International (2025)
```
```
DAA system in-
tegrator
```
```
person/organization/entity who integrates the parts of a DAA system,
and then shows that the risk ratios required by this standard are met.
3.3.10 detect function, DF , n— function within the DAA system tasked
with maintaining temporal and spatial awareness of intruders.
```
```
ASTM International (2025)
```
```
DAR DSS airspace representation ASTM International (2022a)
DAR DSS airspace representation ASTM International (2021)
derived
weather data
```
```
data from non-weather measurement systems translated into a weather
data element, for example, generating wind reports derived from flight
control systems and telemetry.
```
```
ASTM International (2024b)
```
```
Design Aircraft A single or composite, that is, multiple, aircraft that reflects the maximum
weight, maximum contact load/minimum contact area, controlling di-
mension, undercarriage dimensions, and pilot’s eye height of all aircraft
expected to operate at the vertiport.
```
```
ASTM International (2022b)
```

AppendixA. Acronym,Abbreviations,andGlossary A.1. ASTMDefinitionsTraceabilityMatrix

```
Term Definition Source
detect and
avoid (DAA)
```
```
subsystem within the UAS providing the situational awareness, alerting,
and avoidance necessary to maintain safe operation of the ownship in the
presence of intruders.
```
```
ASTM International (2025)
```
```
discovery the process of determining the set of USSs with which data exchange is
required for some UTM function; discovery is accomplished by means of
the discovery and synchronization service (DSS).
```
```
ASTM International (2022a)
```
```
discovery the process of determining the set of USSs with which data exchange is
required for some UTM function; discovery is accomplished by means of
the discovery and synchronization service (DSS).
```
```
ASTM International (2021)
```
```
Discovery and
Synchroniza-
tion Service
(DSS)
```
```
a service defined in this specification that enables USSs to discover other
USSs with which data exchange is required and to ensure that USSs use
current and consistent entity data.
```
```
ASTM International (2021)
```
```
DSS discovery and synchronization service ASTM International (2022a)
DSS discovery and synchronization service ASTM International (2021)
DSS entity a generic concept that refers to information that can be discovered using
the discovery and synchronization service (DSS).
```
```
ASTM International (2022a)
```
```
DSS instance for availability purposes, multiple synchronized copies of the DSS sup-
porting a DSS region. Each copy is referred to as a DSS instance. USSs
can interact with any DSS instance within a pool and switch over to any
other instance in the event of a failure.
```
```
ASTM International (2021)
```
```
DSS pool a synchronized set of DSS instances where operations may be performed
on any instance with the same result, and information may be queried
from any instance with the same result. A DSS region will often have a
production DSS pool along with one or more test or staging DSS pools.
```
```
ASTM International (2022a)
```
```
DSS pool a synchronized set of DSS instances where operations may be performed
on any instance with the same result, and information may be queried
from any instance with the same result. A DSS region will often have a
production DSS pool along with one or more test or staging DSS pools.
```
```
ASTM International (2021)
```
```
DSS region the geographic area supported by a DSS pool. ASTM International (2022a)
DSS region the geographic area supported by a DSS pool. ASTM International (2021)
dynamic data data that changes over the duration of the flight; for example, longitude
and latitude.
```
```
ASTM International (2022a)
```
```
Dynamic Load For design purposes, assume the dynamic load at 150 percent of the max-
imum takeoff weight of the design aircraft applied through the main
undercarriage on a wheel-equipped aircraft or aft contact areas of skid-
equipped aircraft.
```
```
ASTM International (2022b)
```
```
EIRP effective isotropic radiated power ASTM International (2022a)
Electric Vehicle
Power Transfer
System
```
```
A means of replenishing an aircraft’s electrical energy reserves. This in-
cludes portable and stationary charging systems that are designed to be
connected to an aircraft as well as battery swapping programs. NFPA 70
```
```
ASTM International (2022b)
```
```
Elevated Verti-
port
```
```
A vertiport located on a raised structure on land. (A ground-level verti-
port where the TLOF is located on an earthen mound is not considered
an elevated vertiport).
```
```
ASTM International (2022b)
```
```
EMI electromagnetic interference ASTM International (2022a)
EMI electromagnetic interference ASTM International (2021)
encounter event associated with the presence of an intruder. ASTM International (2025)
encounter rate number of encounters per unit of time. ASTM International (2025)
Ended one of the operational intent states. See 4.4 for more details. ASTM International (2021)
```

AppendixA. Acronym,Abbreviations,andGlossary A.1. ASTMDefinitionsTraceabilityMatrix

```
Term Definition Source
Energy Storage
System (ESS)
```
```
Complete energy storage device consisting of one or more energy stor-
age cells arranged into one or more packs, with ancillary subsystems
for physical support and enclosure, thermal management, and electronic
control. Typical energy storage cells include, but are not limited to, bat-
teries or capacitors.
```
```
ASTM International (2022b)
```
```
entity a generic term referring to types of data that need to be shared between
USSs. This specification defines operational intent and constraint entities.
```
```
ASTM International (2021)
```
```
entity reference limited information about an entity (including the approximate location
and contact details for the managing USS) that is stored in the DSS and
supports the discovery process.
```
```
ASTM International (2021)
```
```
F AA Federal Aviation Administration ASTM International (2022a)
fail-safe denotes a situation where the failure of a system software or hardware
component or interface does not result in an unsafe condition. Note that
in a fail-safe situation, a loss of service may occur. (For example, opera-
tional intents cannot be activated if the associated USS is down.)
```
```
ASTM International (2021)
```
```
false alert an incorrect alert caused by a nonaircraft track or by a failure of the alert-
ing system, including the sensor.
```
```
ASTM International (2025)
```
```
FATO Final Approach and Takeoff area; a defined area over which the aircraft
completes the final phase of the approach to a hover or a landing, and
from which the aircraft initiates takeoff that has an unobstructed perime-
ter area that allows for safe maneuvering of the design aircraft in all
modes of operation. The FA TO elevation is the lowest elevation of the
edge of the TLOF. The FA TO may or may not need to be load bearing de-
pendent upon the type of operations that are intended to be conducted.
```
```
ASTM International (2022b)
```
```
FMEA failure modes and effects analysis ASTM International (2021)
FTE flight technical error ASTM International (2021)
GCS ground control station ASTM International (2022a)
Ground Control
Station (GCS)
```
```
the part of a UAS that remotely controls the UA. It may or may not have
a remote pilot directly manipulating the controls. 3.3.10 identify—the
result of the process to establish the identity of a specific UAS that is
traceable to the owner and remote pilot.
```
```
ASTM International (2022a)
```
```
Ground Effect When hovering near the ground, a phenomenon known as ground effect
takes place. This effect usually occurs at a consistent distance above the
surface that is proportional to the main rotor diameter for helicopters, or
total disk area for multirotor vehicles. As the induced airflow through the
rotor disc is reduced by the surface friction, the lift vector increases. This
allows a lower rotor blade angle, or reduced RPM, for the same amount
of lift, which reduces induced drag.
```
```
ASTM International (2022b)
```
```
Ground Taxi The surface movement of a wheeled VTOL under its own power with
wheels touching the ground.
```
```
ASTM International (2022b)
```
```
Ground Towing The movement of an aircraft while in contact with the ground with the
assistance of a ground handling device where the aircraft is not produc-
ing thrust or lift.
```
```
ASTM International (2022b)
```
```
Hover Taxi Used to describe the movement of a wheeled or skid-equipped VTOL
aircraft above the surface, typically used to move short distances from
one point to another. Generally, this task takes place at a wheel/skid
height of 1 ft to 5 ft [0.3 m to 1.5 m] and at a ground speed of less than 20
knots [37 km ⁄h]. For facility design purposes, assume a skid-equipped
eVTOL aircraft to hover-taxi.
```
```
ASTM International (2022b)
```

AppendixA. Acronym,Abbreviations,andGlossary A.1. ASTMDefinitionsTraceabilityMatrix

```
Term Definition Source
Imaginary Sur-
faces
```
```
Surfaces used for the purposes of preventing existing or proposed man-
made objects, objects of natural growth, or terrain from extending up-
ward into navigable airspace. These surfaces include the Approach Sur-
face, Primary Surface, and Transitional Surface.
```
```
ASTM International (2022b)
```
```
intent-based
network partic-
ipant
```
```
a UAS for which the operator has reported an intended area (a volume of ASTM International (2022a)
```
```
intruder a crewed aircraft external to ownship within or projected to be in the
ownship’s vicinity in the near future.
```
```
ASTM International (2025)
```
```
ISMS information security management system ASTM International (2021)
K-index the K-index and, by extension, the Planetary K-index are used to char-
acterize the magnitude of geomagnetic storms (that is, the disturbances
in the Earth’s magnetic field); the planetary 3-hour-range index Kp is the
mean standardized K-index from 13 geomagnetic observatories between
44° and 60° northern or southern geomagnetic latitude.
```
```
ASTM International (2024b)
```
```
LAANC low altitude authorization and notification capability ASTM International (2021)
loss of well
clear (LoWC)
```
```
two aircraft coming within the well clear boundary ( 3.3.34) of each other
while in flight. 3.3.16 loss of well clear risk ratio (LR) measurement,
n—LR is the quotient of the probability of a loss of well clear (LoWC)
given an encounter with a DAA system, and the probability of loss of
well clear given an encounter without a DAA system. The lower the LR,
the better the DAA system is at preventing a loss of well clear. The LR is
a measurement to ensure that a portion of the mitigation happens before
loss of well clear as opposed to after. See Fig. 1 for example depictions
and formulae. See also Ref (1).8
```
```
ASTM International (2025)
```
```
lowest bound
priority status
```
```
a priority status value that is lower than the lowest priority bound de-
fined by the regulator for the strategic conflict detection prioritization
schema. For example, if the regulator assigns “0” as the lowest prior-
ity value for an operation that is subjected to strategic conflict detection
prioritization, then a negative integer would be an acceptable value to
assign as the lowest bound priority status.
```
```
ASTM International (2021)
```
```
MAC midair collision ASTM International (2021)
maintain well
clear
```
```
the act of maneuvering an aircraft with the objective of preventing the
predicted erosion of the well clear margin of safety.
```
```
ASTM International (2025)
```
```
managing USS the USS responsible for an operational intent from creation (that is, suc-
cessfully transitioned to the Accepted state) or a constraint, including ac-
tivities such as making it discoverable through the DSS, providing associ-
ated details when requested by other relevant USSs, and making modifi-
cations. In the context of Conformance Monitoring for Situational Aware-
ness, the managing USS monitors position reports and operator reports
of nonconformance by means of approved methods.
```
```
ASTM International (2021)
```
```
mid-air colli-
sion (MAC)
```
```
two aircraft colliding with each other while in flight. 3.3.19 mid-air colli-
sion proxy, MAC
```
```
ASTM International (2025)
```
```
Monitoring a USS service that monitors an operator’s aggregate conformance with
operational intents over time to ensure the target level of safety for strate-
gic coordination is being met. Operators could also implement their own
Aggregate Operational Intent Conformance Monitoring capability.
```
```
ASTM International (2021)
```
```
MSB most significant bit ASTM International (2022a)
Net-RID network Remote ID ASTM International (2022a)
```

AppendixA. Acronym,Abbreviations,andGlossary A.1. ASTMDefinitionsTraceabilityMatrix

```
Term Definition Source
network Re-
mote ID (Net-
RID) display
provider
```
```
a logical entity that aggregates network Remote ID data from potentially
multiple Net-RID service providers and provides the data to a display
application (that is, an app or website); in practice, it is expected that
many USSs may be both Net-RID display providers and Net-RID service
providers, but standalone Net-RID display providers are possible. 3.3.14
network publishing, v—the act of transmitting data to an internet service
or federation of services; clients, whether air traffic control (A TC), public
safety officials, or possibly the general public can access the data to ob-
tain ID and tracking information for UAS for which such data has been
published.
```
```
ASTM International (2022a)
```
```
network Re-
mote ID (Net-
RID) service
provider
```
```
a logical entity denoting a UTM system or comparable UAS flight man-
agement system that participates in network Remote ID and provides
data for and about UAS it manages.
```
```
ASTM International (2022a)
```
```
networked UAS a UAS that during operations is in electronic communication with a Net-
RID service provider (for example, by means of internet Wi-Fi, 14 cellular,
or satellite, or other communications medium such as short burst data
satellite communications).
```
```
ASTM International (2022a)
```
```
non-
cooperative
intruder
```
```
any aircraft not meeting the definition of cooperative in 3.3.6. ASTM International (2025)
```
```
non-
coordinated
operational
intent
```
```
an operational intent that has not been coordinated with other relevant
USSs and may contain disallowed conflicts. This situation occurs for op-
erational intents with off-nominal 4D volumes.
```
```
ASTM International (2021)
```
```
non-equipped
UAS
```
```
in the context of Remote ID, a UAS that is neither a networked nor broad-
cast UAS (for example, a radio controlled model aircraft) and cannot di-
rectly report its location or identity.
```
```
ASTM International (2022a)
```
```
Nonconforming one of the operational intent states. See 4.4 for more details. 3.2.29
off-nominal, adj—in the context of this specification, refers to situations
where an operational intent is in the Noncoforming or Contingent states.
```
```
ASTM International (2021)
```
```
NSE navigation system error ASTM International (2021)
nuisance alert alert generated by a system that is functioning as designed, but which is
inappropriate or unnecessary for the particular condition.
```
```
ASTM International (2025)
```
```
off-nominal 4D
volumes
```
```
4D volumes that characterize where and when a UA is expected to travel
while it is off-nominal. Off-nominal 4D volumes may reflect a specific
route of flight when known, or a broader area when a specific route of
flight is not known.
```
```
ASTM International (2021)
```
```
OIV operational intent volume ASTM International (2021)
opaque version
number (OVN)
```
```
unique value associated with a version of an entity, updated when the
entity 4 is modified. OVNs are used to ensure that USSs have the current
version of entities.
```
```
ASTM International (2021)
```
```
OpenAPI open-source format and initiative for designing and creating machine-
readable interface files that are used in producing, describing, consum-
ing, and visualizing RESTful APIs and web services.
```
```
ASTM International (2024b)
```

AppendixA. Acronym,Abbreviations,andGlossary A.1. ASTMDefinitionsTraceabilityMatrix

```
Term Definition Source
operational in-
tent
```
```
a volume-based representation of the intent for a UAS operation; com-
prises one or more overlapping or contiguous 4D volumes, where the
start time for each volume is the earliest entry time, and the stop time for
each volume is the latest exit time. V olumes are constructed based on the
performance of the UAS and represent the airspace to which a UA must
conform to a sufficient degree to achieve a target level of safety for strate-
gic deconfliction. An operational intent’s volumes normally indicate the
intent for the operation in the Accepted and Activated states. How-
ever, an operational intent is supplemented with off-nominal 4D volumes
when in the Nonconforming or Contingent states. Strictly speaking, off-
nominal 4D volumes do not represent intent, but the underlying structure
of operational intents (4D volumes) and the mechanisms for discovery
and notification of relevant USSs and operations makes the operational
intent a convenient vehicle for conveying the necessary information in
off-nominal situations.
```
```
ASTM International (2021)
```
```
operational vol-
ume
```
```
volume of airspace in which the UA operation intends, or is authorized,
to take place.
```
```
ASTM International (2025)
```
```
operator the individual or organization who uses, causes to use, or authorizes to
use an aircraft for the purpose of air navigation, including the piloting of
an aircraft, with or without the right of legal control (as owner, lessee, or
otherwise).
```
```
ASTM International (2022a)
```
```
operator the person or organization that applies for CAA approval to operate a
UAS or who seeks operational approval for types of flight operations pro-
hibited by a CAA for that UAS.
```
```
ASTM International (2021)
```
```
operator loca-
tion
```
```
the geographic location of the remote pilot in command of a UAS. ASTM International (2022a)
```
```
operator’ s au-
tomation
```
```
optional automation used by an operator to handle aspects of UAS oper-
ations during the preflight, in-flight, or postflight timeframe that other-
wise would be performed by UAS personnel. The scope of functionality
is operator-dependent. Operator’s automation may interact with a USS
instead of UAS personnel.
```
```
ASTM International (2021)
```
```
OVN opaque version number ASTM International (2021)
ownship UA controlled by the pilot flying and for which the pilot in command
(PIC) is responsible.
```
```
ASTM International (2025)
```
```
Parking Posi-
tion
```
```
A designated location at a V ertiport designed for transient aircraft to be
positioned by means of ground or air taxi taxiways for the purpose of
loading and unloading of cargo or passengers, charging, fueling, or short
duration maintenance. Landing and takeoff operations are not permitted
from designated parking positions. A TLOF may be used as a parking
position with the understanding that it may reduce or halt landing and
takeoff operations until the aircraft has cleared the location.
```
```
ASTM International (2022b)
```
```
PBN performance-based navigation ASTM International (2021)
PHY physical layer ASTM International (2022a)
PII personally identifiable information ASTM International (2022a)
PII personally identifiable information ASTM International (2021)
pilot flying individual or system that manipulates the flight controls of an aircraft
during flight; may or may not be the pilot in command.
```
```
ASTM International (2025)
```
```
position data information provided by a UAS that describes the location of an un-
manned aircraft, including its latitude, longitude, altitude, and the time
the unmanned aircraft was at the location.
```
```
ASTM International (2021)
```

AppendixA. Acronym,Abbreviations,andGlossary A.1. ASTMDefinitionsTraceabilityMatrix

```
Term Definition Source
position extrap-
olation
```
```
a capability of a Net-RID service provider to predict the location of a
UAS based on a modeled 4-D trajectory derived from an intended UAS
operation plan.
```
```
ASTM International (2022a)
```
```
present weather any weather or obstructions (obscurations) to vision occurring at an
observation location and includes precipitation, obscurations, well-
developed dust/sand whirls, squalls, tornadic activity, sandstorms, dust
storms, smoke, and volcanic ash occurring at the time the present
weather was observed and time stamped.
```
```
ASTM International (2024b)
```
```
Primary Surface An imaginary surface positioned along a horizontal plane at the estab-
lished elevation of a vertiport that coincides in size and shape with the
designated takeoff and landing area FA TO.
```
```
ASTM International (2022b)
```
```
proxy proximity threshold used in calculating risk ratios and is defined as two
aircraft coming within a horizontal and vertical distance such that the
probability of collision is 10 percent, considering the expected maximum
dimensions of those two aircraft; this specification defines MAC proxy as
two aircraft coming within 100 ft (30.5 m) vertically and 500 ft (152 m)
horizontally of each other while in flight, although CAAs may determine
or accept other definitions as they deem appropriate.
```
```
ASTM International (2025)
```
```
proxy risk ra-
tio (RR) mea-
surement
```
```
RR is the quotient of the probability of a MAC proxy given an encounter
with the DAA system and the probability of a MAC proxy given an en-
counter without the DAA system. The lower the RR, the better the DAA
system is at preventing MAC proxy.
```
```
ASTM International (2025)
```
```
regain well
clear
```
```
the act of maneuvering an aircraft with the objective of restoring the
well clear margin of safety that has been degraded by preceding circum-
stances.
```
```
ASTM International (2025)
```
```
registration the process by which an owner/ operator (including contact information
and other PII) and aircraft (for example, make, model) are associated with
an assigned, unique identifier. 3.3.21 shall, must versus should versus
may— use of the word “shall” implies that a procedure or statement is
mandatory and must be followed to comply with this practice, “should”
implies recommended, and “may” implies optional at the discretion of
the supplier, manufacturer, or operator.
```
```
ASTM International (2022a)
```
```
relevant opera-
tional intent
```
```
an operational intent that overlaps or is in close proximity to another
operational intent. Close proximity versus strict overlapping is included
because the DSS defined in this specification does not determine intersec-
tion using the precise 3D extents of operational intents (or constraints),
but instead using a coarser representation. The coarser representation
results in actual intersections always being detected, but also in the oc-
casional identification of operational intents that are merely close to each
other. (This concept also applies to constraints.) The distance that qual-
ifies as in close proximity is not fixed, but depends on the configuration
of the DSS airspace representation. See Annex A2 for further detail.
```
```
ASTM International (2021)
```
```
relevant USSs (a) USSs that manage operational intents or constraints, or both, that, due
to their proximity, must be evaluated by the Strategic Conflict Detection
or the Constraint Processing service, or both, of a USS attempting to cre-
ate or modify an operational intent; (b) USSs that manage operational
intents that, due to their proximity, are potentially affected by a Non-
conforming or Contingent operational intent or a new or modified con-
straint; or, (c) a USS that has established a subscription for operational
intents or constraints, or both, in an area where it may not yet manage
operational intents.
```
```
ASTM International (2021)
```

AppendixA. Acronym,Abbreviations,andGlossary A.1. ASTMDefinitionsTraceabilityMatrix

```
Term Definition Source
Remote ID remote identification ASTM International (2022a)
remote pilot
in command
(RPIC)
```
```
person who is directly responsible for and is the final authority as to the
operation of the UAS; has been designated as remote pilot in command
before or during the flight of a UAS; and holds the appropriate CAA
certificate for the conduct of the flight.
```
```
ASTM International (2025)
```
```
risk ratio mea-
surement
```
```
used to measure the performance of a DAA system(s); the probability of
an outcome with the DAA system(s), divided by the probability of an out-
come without the DAA system(s); see Fig. 1 for depictions and formulae.
The lower the risk ratio, the better the DAA system is at mitigations.
```
```
ASTM International (2025)
```
```
root mean
square error
```
```
the square root of the mean of the squares of a set of values. 3.2.8 shall,
should, may, and will, v— shall indicates a mandatory requirement,
should indicates a recommended requirement, may indicates an optional
requirement, and will indicates futurity and it is not a requirement.
```
```
ASTM International (2024b)
```
```
Rotor Load Rotor downwash loads are approximately equal to the weight of the air-
craft distributed uniformly over the disk area of the rotors.
```
```
ASTM International (2022b)
```
```
Safety Area A defined unobstructed area surrounding the FA TO of a vertiport de-
signed to allow for any accidental divergence of an aircraft from the FA
TO perimeter.
```
```
ASTM International (2022b)
```
```
Safety Net A physical and structurally supported safety device surrounding any
landing/takeoff surface, parking areas, taxiway, walkway, access point,
passenger area, and crew area that is elevated greater than 30 in. that is
designed to provide fall protection in accordance with OSHA standard
Title
```
```
ASTM International (2022b)
```
```
SDO standards development organization ASTM International (2021)
shielded oper-
ating volume
```
```
operating volume where the competent authority accepts that UA are
well clear and DAA may not be required. Crewed aircraft normally
will not fly in this volume because of regulatory limitations, or because
crewed aircraft yield to a characteristic of the environment in the interest
of safety.
```
```
ASTM International (2025)
```
```
smaller near
mid-air colli-
sion (sNMAC)
```
```
two UAs coming sufficiently close to each other horizontally and laterally
such that the probability of a mid-air collision is 10 % or less (see RTCA
DO-396 and Ref ( 2)).
```
```
ASTM International (2025)
```
```
SMS safety management system 3.3.28 ASTM International (2021)
space weather phenomena that lie wholly or in part outside the Earth’s atmosphere. ASTM International (2024b)
static data data that remains the same or does not change often over the duration of
a flight (for example, Unique ID); this is in contrast to dynamic data that
may change more frequently (such as longitude and latitude).
```
```
ASTM International (2022a)
```
```
Static Load For design purposes, the design static load is equal to the aircraft’s maxi-
mum takeoff weight applied through the total contact area of the wheels
or skids.
```
```
ASTM International (2022b)
```
```
Strategic Con-
flict Detection
```
```
a USS service that determines if an operational intent conflicts with other
operational intents. The process of detecting conflicts by comparing op-
erational intents. In contrast, tactical conflict detection generally relies on
nonstrategic information such as current location, heading, and speed.
```
```
ASTM International (2021)
```
```
Strategic Con-
flict Resolution
```
```
the process of resolving conflicts through the modification of operational
intents. Although there is no absolute time threshold, strategic conflict
resolution requires sufficient time before the conflict to generate, coordi-
nate, and implement the modification to the operational intent.
```
```
ASTM International (2021)
```
```
Strategic Coor-
dination
```
```
a USS role comprising the Strategic Conflict Detection and Aggregate Op-
erational Intent Conformance Monitoring services.
```
```
ASTM International (2021)
```

AppendixA. Acronym,Abbreviations,andGlossary A.1. ASTMDefinitionsTraceabilityMatrix

```
Term Definition Source
strategic decon-
fliction
```
```
the arrangement, negotiation, coordination, and prioritization of in-
tended operational volumes, routes, or trajectories to minimize the like-
lihood of airborne conflicts between operations. (adapted from ICAO
UTM Framework)
```
```
ASTM International (2024a)
```
```
subscription a DSS mechanism that allows a USS to be notified and provided the de-
tails of any new, modified, or deleted entities in a specified area of interest
defined by a 4D volume.
```
```
ASTM International (2021)
```
```
Taxiway (TW) Defined unobstructed clear path established for the taxiing (air, ground,
or both) of aircraft from one part of a vertiport to another.
```
```
ASTM International (2022b)
```
```
TBO trajectory-based operations ASTM International (2021)
tethered aircraft a configuration where the unmanned aircraft remains securely attached
(tethered) via a physical link to an anchor (a surface vehicle, the ground,
or other object on the ground) at all times while it is flying and is unable
to cause the anchor to move. DISCUSSION—This is different from the
recreational practice of “control line model aircraft,” where the aircraft is
flown in a circular pattern in close proximity to the remote pilot, who is
acting as the anchor.
```
```
ASTM International (2024a)
```
```
TLOF Touchdown and Liftoff Area; a loadbearing surface area normally cen-
tered in its own FA TO, on which the aircraft may touchdown or liftoff.
```
```
ASTM International (2022b)
```
```
TLS transport layer security ASTM International (2022a)
TLS target level of safety ASTM International (2021)
track specific collection of data that a particular DAA system accumulates and
is used in determining whether an intruder aircraft is a collision risk or
loss of well clear risk, or both.
```
```
ASTM International (2025)
```
```
Transitional
Surfaces
```
```
These surfaces extend outward and upward from the lateral boundaries
of the primary surface and from the approach surfaces at a slope of 2:1
for a distance of 250 ft [76.3 m] measured horizontally from the centerline
of the primary and approach surfaces.
```
```
ASTM International (2022b)
```
```
TSE total system error ASTM International (2021)
TTL time to live ASTM International (2021)
UA unmanned aircraft ASTM International (2022a)
UA unmanned aircraft ASTM International (2021)
UAS unmanned aircraft system ASTM International (2022a)
UAS unmanned aircraft system ASTM International (2021)
UAS operation
plan
```
```
a UAS operation plan is developed prior to the operation and should in-
dicate the volume of airspace within which the operation is expected to
occur, the times and locations of the key events associated with the oper-
ation, including launch, recovery, and any other information deemed im-
portant (for example, segmentation of the operation trajectory by time).
UTM ConOps v1.0
```
```
ASTM International (2022a)
```
```
UAS personnel refers to any personnel associated with a UAS operation, including the
operator, the remote pilot in charge, and other personnel who may per-
form preflight, in-flight, or postflight activities. This generic reference
to personnel is frequently used in order to avoid incorrect assumptions
about the activities carried out by any particular role in an operator’s
organization.
```
```
ASTM International (2021)
```
```
UAS registra-
tion ID
```
```
an identification number or combination of letters and numbers assigned
by a CAA or authorized representative to a UAS; this is sometimes re-
ferred to as a registration number (which may or may not contain letters).
```
```
ASTM International (2022a)
```

AppendixA. Acronym,Abbreviations,andGlossary A.1. ASTMDefinitionsTraceabilityMatrix

```
Term Definition Source
UAS service
supplier (USS)
```
```
USSs provide UTM services to support the UAS community, to connect
operators and other entities to enable information flow across the USS
network, and to promote shared situational awareness among UTM par-
ticipants. UTM ConOps v1.0
```
```
ASTM International (2022a)
```
```
UAS Service
Supplier (USS)
```
```
for purposes of this specification, a USS is an entity that provides one or
more of the UTM services defined in this specification.
```
```
ASTM International (2021)
```
```
UAS Traffıc
Management
(UTM)
```
```
a federated set of services operated under regulatory oversight that sup-
port safe and compliant UAS operations.
```
```
ASTM International (2021)
```
```
UAS Zone (alt.
UAS Geograph-
ical Zone)
```
```
the terms used in EUROCAE ED-269, Minimum Operational Perfor-
mance Standard for UAS Geo-Fencing, for what are defined as con-
straints in this specification. (From ED-269, a UAS zone is an airspace of
defined dimensions, above the land areas or territorial waters of a state,
within which a particular restriction or condition for UAS flights applies.
)
```
```
ASTM International (2021)
```
```
UASSP unmanned aircraft system service provider ASTM International (2021)
uncontrolled
airspace
```
```
an airspace that is not controlled (see 3.3.5). ASTM International (2025)
```
```
unique ID a data element that can be traced to a unique UAS and its operator. ASTM International (2022a)
unmanned air-
craft (UA)
```
```
an aircraft operated without the possibility of direct human intervention
from within or on the aircraft. 14 CFR 107.3
```
```
ASTM International (2024a)
```
```
Unmanned
Aircraft System
(UAS)
```
```
composed of unmanned aircraft (UA) and all required on-board subsys-
tems, 5 payload, control station, other required off-board subsystems,
any required launch and recovery equipment, all required crew mem-
bers, and communication links.
```
```
ASTM International (2021)
```
```
User notifica-
tion
```
```
information provided by a USS to UAS personnel or to an operator’s au-
tomation system, or both. Because UAS-related concepts of operations
can vary widely from operator to operator, this specification does not
mandate a particular form for a user notification; possible implementa-
tions include messages or graphical indications through a user interface;
text messages; email; and system to system messages.
```
```
ASTM International (2021)
```
```
USS UAS service supplier ASTM International (2022a)
USS UAS service supplier ASTM International (2021)
USS network the set of USSs operating collaboratively in a region. ASTM International (2021)
USS role a grouping of one or more USS Services. USS roles may be used by a
competent authority to establish the granularity of authorizations that
can be granted to a USS. Roles are also used within this specification to
indicate services that should be provided together.
```
```
ASTM International (2021)
```
```
USS service a UTM-related function performed by a USS. ASTM International (2021)
USSP U-Space service provider ASTM International (2021)
UTM UAS traffic management ASTM International (2022a)
UTM UAS traffic management ASTM International (2021)
UTMSP UTM service provider ASTM International (2021)
UUID universally unique identifier based on RFC4122 (128 bit) ASTM International (2022a)
Vertical Lift Air-
craft
```
```
Heavier-than-air aircraft capable of vertical takeoff and vertical landing. ASTM International (2022b)
```
```
Vertiport Eleva-
tion
```
```
The highest point of a vertiport’s FA TO measured in feet or meters above
mean sea level or equivalent elevation component as approved by the
authority having jurisdiction.
```
```
ASTM International (2022b)
```
```
VIP very important person ASTM International (2022a)
```

AppendixA. Acronym,Abbreviations,andGlossary A.2. DECEADefinitionsTraceabilityMatrix

```
Term Definition Source
visual range distance that unaided (except for normal prescription eyewear) human
vision can effectively monitor and provide deconfliction during a UAS
operation. F2395
```
```
ASTM International (2024a)
```
```
weather state of the atmosphere at a given time and place. 5 ASTM International (2024b)
weather alert proactive notification disseminated by a WIP for specific airworthiness
or operationally impactful weather provided for specific thresholds re-
quested by the user for weather that is occurring or may occur.
```
```
ASTM International (2024b)
```
```
weather analy-
sis
```
```
enhanced depiction or interpretation of observed weather data, or both,
conducted objectively by machine analysis and subjectively by humans.
```
```
ASTM International (2024b)
```
```
weather analy-
sis data
```
```
weather data elements, such as precipitation, wind, temperature, and so
forth, that meet the applicable performance tiers in this specification.
```
```
ASTM International (2024b)
```
```
weather area
data
```
```
weather data on a horizontal or vertical plane in a specified space and
time with three or more points connected to depict a weather data ele-
ment area; examples include cloud ceiling height, two-dimensional (2-D)
depictions of weather radar reflectivity, and 2-D weather analysis of a
weather element at a specific time.
```
```
ASTM International (2024b)
```
```
weather data
sets
```
```
collection of data that may be obtained from in situ sensors, remote sen-
sors, or be derived from other data sources.
```
```
ASTM International (2024b)
```
```
weather data
tier
```
```
category of weather information reports and analyses based on the per-
formance of the sensor and the quality of the data produced by the sen-
sor and modeled after instrument landing system (ILS) categories with
Weather Data Tier 3 being the most precise followed by Weather Data
Tier 2 and then Weather Data Tier 1. 3.2.17 weather information provider
, WIP , n— provider of one or more essential or enhanced weather-related
services.
```
```
ASTM International (2024b)
```
```
weather line
data
```
```
weather data on a horizontal or vertical line connected by two or more
measurements of a weather data element during a specified time; exam-
ples include a line of thunderstorms, thunderstorm gust front, and atmo-
spheric profile measurement.
```
```
ASTM International (2024b)
```
```
weather point
data
```
```
weather data element at a specific point and time; examples include tem-
perature, dewpoint, wind speed and direction, and so forth.
```
```
ASTM International (2024b)
```
```
weather vol-
ume analysis
```
```
weather data element represented by horizontal, vertical, and perpen-
dicular planes (x, y, z) with eight or more points to depict a volumetric
weather region at a specific time.
```
```
ASTM International (2024b)
```
```
well clear state where there is a low residual mid-air collision risk informed by op-
erational suitability.
```
```
ASTM International (2025)
```
```
well clear (WC)
boundary
```
```
extent of the volume defined to calculate the operating performance of a
DAA system. For encounters between a UA and a crewed aircraft, it is
assumed that the probability of a MAC proxy given a LoWC is 10 % or
less. The WC boundary is sized based on that assumption.
```
```
ASTM International (2025)
```
```
YAML Y AML ain’t markup language ASTM International (2021)
```
**A.2 | DECEADefinitionsTraceabilityMatrix**

This section consolidates definitions extracted from DECEA documents in References/Docs

DECEA/. Repeated terms are intentionally preserved with their respective origin for

traceability.


AppendixA. Acronym,Abbreviations,andGlossary A.2. DECEADefinitionsTraceabilityMatrix

```
Term Definition Source
Acomodação Termo genérico utilizado para definir uma atividade no espaço aéreo que
não pode ser integrada ao sistema ATM devido à possibilidade de causar
impacto à segurança e regularidade das operações aéreas. A acomodação
pode ser feita delimitando um volume do espaço aéreo para a atividade
por meio de re serva ou restrição do espaço aéreo ou ainda por meio do
estabelecimento de condicionantes operacionais.
```
### DECEA (2023)

```
Acordo Opera-
cional
```
```
Documento que visa estabelecer procedimentos operacionais padroniza-
dos a serem seguidos pelas Partes Signatárias durante a execução de suas
atividades.
```
### DECEA (2023)

```
Administrador
SARPAS
```
```
Pessoa física, proprietária ou não de aeronave não tripulada, responsável
por gerenciar as ações referentes à pessoa jurídica no SARPAS.
```
### DECEA (2023)

```
ADS-B Vigilância Dependente Automática por Radiodifusão (Automatic Depen-
dent Surveillance — Broadcast) é o meio pelo qual a aeronave, veículos de
aeródromo e outros objetos podem automaticamente transmitir ou rece-
ber dados tais como identificação, posição e dados adicionais, conforme
o caso, em modo radiodifusão via enlace de dados; e
```
```
DECEA (2025d)
```
```
Aeródromo Área delimitada em terra ou na água destinada, no todo ou em parte,
para pouso, decolagem e movimentação em superfície de aeronaves; in-
clui quaisquer edificações, instalações e equipamentos de apoio e de con-
trole das operações aéreas, se existirem. Quando destinado exclusiva-
mente a helicópteros, recebe denominação de heliponto.
```
### DECEA (2023)

```
Aero-
levantamento
```
```
Conjunto de Operações aéreas e/ou espaciais de medição, computação
e registro de dados do terreno com o emprego de sensores e/ou equipa-
mentos adequados, bem como a interpretação dos dados levantados ou
sua tradução sob qualquer forma.
```
### DECEA (2023)

```
Aeromodelo Aeronave não tripulada, utilizada para fins exclusivamente recreativos. DECEA (2023)
Aeronave Qualquer aparelho que possa sustentar-se na atmosfera a partir de
reações do ar que não sejam as reações do ar contra a superfície da terra.
```
### DECEA (2023)

```
Aeronave de
Acompan-
hamento
```
```
Aeronave tripulada capaz de acompanhar voos experimentais de UA,
com a finalidade de transmitir informações à equipe de UAS. NOTA: É a
única aeronave tripulada que poderá ser autorizada a compartilhar um
espaço aéreo reservado para uma UA.
```
### DECEA (2023)

```
Aeronave Não
Tripulada
```
```
Qualquer aparelho que possa sustentar-se na atmosfera, a partir de
reações do ar que não sejam as reações do ar contra a superfície da terra,
e que se pretenda operar sem piloto a bordo.
```
### DECEA (2023)

```
Aeronave
Não Tripulada
Autônoma
```
```
Aeronave não tripulada que não permite a intervenção do piloto no
gerenciamento do voo.
```
### DECEA (2023)

```
Aeronave Re-
motamente
Pilotada
```
```
Subconjunto de Aeronaves Não Tripuladas, pilotadas a partir de uma
estação de pilotagem remota, com finalidade diversa de recreação, que
seja capaz de interagir com o Controle de Tráfego Aéreo em tempo real.
```
### DECEA (2023)

```
Altitude Distância vertical entre um nível, pont o ou objeto considerado como
ponto e o nível médio do mar.
```
### DECEA (2023)


AppendixA. Acronym,Abbreviations,andGlossary A.2. DECEADefinitionsTraceabilityMatrix

```
Term Definition Source
Altitude Limite
de Voo
```
```
Altitude de voo resultante da soma entre a altitude do solo no ponto de
decolagem declarado na solicitação de acesso ao espaço aéreo e a Al-
tura de Voo Solicitada. NOTA: Para fins de análise de gerenciamento
de tráfego aéreo, a Altitude Limite de Voo é considerada como lim-
ite vertical superior do volume de espaço aéreo solicitado pelo Explo-
rador/Operador e não poderá ser extrapolada independentemente de
variações de relevos, obstáculos e de eventuais decolagens de outros lo-
cais que não o declarado na solicitação de voo, pois sua inobservância
pode constituir perigo à navegação aérea.
```
### DECEA (2023)

```
Altura Distância Vertical de um nível, ponto ou objeto considerado como ponto
e uma determinada referência.
```
### DECEA (2023)

```
Altura de Voo
Solicitada
```
```
Altura relativa ao nível do solo no ponto de decolagem informada pelo
Explorador/Operador na solicitação de acesso ao espaço aéreo. NOTA:
Durante a operação, a aeronave não tripulada poderá manter no máximo
tal altura sobre o terreno ou obstáculos que está sendo sobrevoado, desde
que não ultrapasse a Altitude Limite de Voo.
```
### DECEA (2023)

```
Análise de Im-
pacto Sobre a
Segurança Op-
eracional
```
```
Documento elaborado pelo operador de aeródromo com vistas à consol-
idação do processo de gerenciamento de risco da segurança operacional.
```
### DECEA (2023)

```
Área Perigosa Espaço aéreo de dimensões definidas, sobre o território ou mar territo-
rial brasileiro, dentro do qual podem existir, em momentos específicos,
atividades perigosas para o voo de aeronaves.
```
### DECEA (2023)

```
Área Proibida Espaço aéreo de dimensões definidas, sobre o território ou mar territorial
brasileiro, dentro do qual o voo de aeronaves é proibido.
```
### DECEA (2023)

```
Área Restrita Espaço aéreo de dimensões definidas, sobre o território ou mar territo-
rial brasileiro, dentro do qual o voo de aeronaves é restringido conforme
certas condições definidas.
```
### DECEA (2023)

```
Autorização Autorização emitida para que uma Aeronave Não Tripulada acesse o
Espaço Aéreo Brasileiro, com o propósito de garantir a manutenção da
segurança da navegação aérea, conforme previsto no artigo 8º da Con-
venção de Chicago.
```
### DECEA (2023)

```
Aviso aos
Aeronaveg-
antes
```
```
Aviso distribuído por meio de telecomunicações que contém informação
relativa a estabelecimento, condição ou modificação de qualquer insta-
lação aeronáutica, s erviço, procedimento ou perigo, cujo conhecimento
oportuno seja indispensável para o pessoal encarregado das operações
de voo.
```
### DECEA (2023)

```
Carga Útil (Pay-
load)
```
```
Todos os elementos da aeronave não necessários para o voo e pilotagem,
mas que são carregados com o propósito de cumprir objetivos específicos.
```
### DECEA (2023)

```
Comunicação
entre Veículo e
Infraestrutura –
V2I
```
```
Refere-se à capacidade de sistemas embarcados em aeronaves estabele-
cerem comunicação de dados com outros sistemas instalados em in-
fraestrutura localizada no solo
```
```
DECEA (2024a)
```
```
Comunicação
entre Veículos –
V2V
```
```
Refere-se à capacidade de sistemas embarcados em aeronaves distintas
estabelecerem comunicação de dados entre si
```
```
DECEA (2024a)
```

AppendixA. Acronym,Abbreviations,andGlossary A.2. DECEADefinitionsTraceabilityMatrix

```
Term Definition Source
Comunidade
ATM
```
```
a) conjunto de organizações, agências ou entidades que podem partici-
par, colaborar e cooperar no planejamento, desenvolvimento, regulação,
operação e manutenção do Sistema ATM; e b) fazem parte da comu-
nidade ATM: operadores de aeronaves civis e militares, administradores
aeroportuários, indústria aeronáutica, usuários do espaço aéreo, prove-
dores de serviços ATM, indústria de suporte ATM, OACI e demais au-
toridades reguladoras
```
```
DECEA (2024a)
```
```
Comunidade
ATM
```
```
Conjunto de organizações, agências ou entidades que podem participar,
colaborar e cooperar no planejamento, desenvolvimento, uso, regulação,
operação e manutenção do Sistema ATM
```
```
DECEA (2025c)
```
```
AOM (Airspace
Organization
and Manage-
ment)
```
```
Componente funcional do Sistema ATM responsável por estruturar e alo-
car o espaço aéreo de forma flexível e equitativa no contexto operacional.
```
```
DECEA (2025c)
```
```
DCB (Demand
and Capacity
Balancing)
```
```
Componente funcional do Sistema ATM responsável por balancear de-
manda e capacidade para evitar sobrecarga e preservar segurança e pre-
visibilidade operacional.
```
```
DECEA (2025c)
```
```
AO (Aero-
drome Opera-
tions)
```
```
Componente funcional do Sistema ATM responsável por integrar re-
strições de pista, superfície e aeródromo ao fluxo terminal e em rota.
```
```
DECEA (2025c)
```
```
TS (Traffic Syn-
chronization)
```
```
Componente funcional do Sistema ATM responsável por sequenciar e
sincronizar o tráfego no tempo e no espaço, assegurando continuidade
gate-to-gate.
```
```
DECEA (2025c)
```
```
CM (Conflict
Management)
```
```
Componente funcional do Sistema ATM responsável por detectar, pre-
venir e resolver conflitos entre aeronaves e demais perigos operacionais.
```
```
DECEA (2025c)
```
```
AUO (Airspace
Users Opera-
tions)
```
```
Componente funcional do Sistema ATM responsável por representar ne-
cessidades operacionais, capacidades e intenções dos usuários do espaço
aéreo.
```
```
DECEA (2025c)
```
### ATM SDM

```
(ATM Ser-
vice Delivery
Management)
```
```
Componente funcional do Sistema ATM responsável por orquestrar a en-
trega de serviços e a execução de acordos ao longo das fases do voo.
```
```
DECEA (2025c)
```
```
Detectar e Evi-
tar
```
```
Capacidade de ver, perceber ou detectar tráfegos conflitantes ou outros
perigos e tomar as medidas adequadas para evitá-los.
```
### DECEA (2023)

```
Ecossistema
UAM – ECO-
UAM
```
```
É uma interface de troca de dados entre os sistemas do DECEA e de out-
ros sistemas e entidades, como os PSU, SDSP, outras instituições governa-
mentais, órgãos de segurança pública etc., permitindo gerenciar dados de
restrição de espaço aéreo e ponto de acesso a informações de operações
ativas no ambiente UAM e, além disso, fornece meio para que as partes
interessadas aprovadas consultem e recebam dados sobre as operações
no ambiente UAM
```
```
DECEA (2024a)
```
```
Elementos Con-
stitutivos Bási-
cos (BBB)
```
```
Estrutura que descreve a base de um Sistema de Navegação Aérea ro-
busto, definindo os serviços básicos que devem ser prestados à aviação
civil internacional, atendendo às normas da OACI. Estes serviços bási-
cos, também conhecidos como habilitadores, são relacionados às áreas de
aeródromos, gerenciamento de tráfego aéreo, busca e salvamento, mete-
orologia e gerenciamento da informação. Os BBB também identificam os
usuários finais desses serviços, assim como a infraestrutu ra de comuni-
cações, navegação e vigilância necessária para a provisão dos mesmos
```
```
DECEA (2025c)
```

AppendixA. Acronym,Abbreviations,andGlossary A.2. DECEADefinitionsTraceabilityMatrix

```
Term Definition Source
Enlace C2 Enlace entre a Aeronave Não Tripulada e a Estação de Pilotagem Remota
com o propósito de gerenciar o voo. Este enlace, além de possibilitar a pi-
lotagem da aeronave, poderá incluir a telemetria necessária para prover
a situação do voo ao Piloto Remoto. NOTA: O enlace de pilotagem difere
dos enlaces relacionados à carga útil (como sensores).
```
### DECEA (2023)

```
Equipe UAS Todos os membros de uma Equipe com atribuições essenciais à operação
de um Sistema de Aeronaves Não Tripuladas.
```
### DECEA (2023)

```
Espaço Aéreo
ATS
```
```
Espaço aéreo de dimensões definidas, designado alfabeticamente, dentro
dos quais podem operar tipos específicos de voos e para os quais são
estabelecidos os serviços de tráfego aéreo e as regras de operação. NOTA:
Os espaços aéreos ATS são classificados de A até G.
```
### DECEA (2023)

```
Espaço Aéreo
Condicionado
```
```
Expressão genérica que se aplica, segundo o caso, a uma área proibida,
restrita ou perigosa.
```
### DECEA (2023)

```
Espaço Aéreo
Controlado
```
```
Espaço aéreo de dimensões definidas, dentro do qual se presta o serviço
de controle de tráfego aéreo, de conformidade com a classificação do es-
paço aéreo. NOTA: Espaço aéreo controlado é um termo genérico que
engloba as Classes A, B, C, D e E dos espaços aéreos ATS.
```
### DECEA (2023)

```
Espaço Aéreo
de Rotas Livres
```
- FRA

```
É o espaço aéreo específico no qual os usuários podem planejar livre-
mente uma rota entre um ponto de entrada e um ponto de saída
definidos, com a possibilidade de voar por meio de pontos inter-
mediários (publicados ou não publicados), sem referência à rede de rotas
ATS, sujeito à disponibilidade do espaço aéreo
```
```
DECEA (2024a)
```
```
Espaço Aéreo
Segregado
```
```
Espaço aéreo de dimensões especificadas, alocado para uso exclusivo de
um usuário (ou usuários) específico(s).
```
### DECEA (2023)

```
Estação de
Pilotagem
Remota
```
```
Componente do sistema de Aeronaves Não Tripuladas que contém o
equipamento utilizado para pilotar a aeronave.
```
### DECEA (2023)

```
Evoluções
por Blocos do
Sistema de
Aviação (ASBU)
```
```
Metodologia desenvolvida pela OACI, que orienta a evolução do Sistema
ATM e viabiliza um planejamento global e flexível, permitindo que os
Estados desenvolvam capacidades de Navegação Aérea de acordo com
suas necessidades operacionais específicas. É composta de um conjunto
de melhorias operacionais e seus benefícios conexos em termos de efi-
ciência, organizados por áreas -chave do Sistema de Navegação Aérea e
programados de acordo com a data de previsão de disponibilidade
```
```
DECEA (2025c)
```
```
Explorador Pessoa física ou jurídica, proprietária ou não, que utiliza a aeronave de
forma legítima, direta ou indireta, com ou sem fins lucrativos. NOTA
1: No contexto de Aeronaves Não Tripuladas, a exploração da aeron-
ave inclui todo o Sistema de Aeronaves Não Tripuladas. NOTA 2: Em
algumas regulamentações, o “Explorador” também poderá ser definido
pelo termo “Operador”, assim como a “exploração”, pelo termo “oper-
ação”. NOTA 3: Em situações de contratação de empresas terceirizadas,
o EXPLORADOR se torna corresponsável pela operação e pelos resul-
tados que dela advenham. Art. 268, § 1º, Lei 7.565: “prevalece a resp
onsabilidade do EXPLORADOR quando a aeronave é pilotada por seus
prepostos, ainda que exorbitem de suas atribuições.”
```
### DECEA (2023)

```
Falha de Enlace
C2
```
```
Falha de enlace entre a Aeronave Não Tripulada e a Estação de Pilotagem
Remota (RPS) que impossibilite, mesmo que momentaneamente, a sua
pilotagem. NOTA: A Falha de Enlace de Pilotagem é também conhecida
como Falha de “Enlace C2”.
```
### DECEA (2023)


AppendixA. Acronym,Abbreviations,andGlossary A.2. DECEADefinitionsTraceabilityMatrix

```
Term Definition Source
Fixo de
Medição (Me-
tering Fix)
```
```
Ponto de referência para o qual é fornecida a informação de ajuste no
tempo de passagem sobre um fixo por determinada aeronave ao ATCO
do ACC, através da tela do software AMAN, de forma a auxiliá-lo no
planejamento da sequência de chegada
```
```
DECEA (2024a)
```
```
FRA Espaço Aéreo de Rotas Livres (Free Routes Airspace) é o espaço aéreo es-
pecífico, sujeito ao controle de tráfego aéreo, no qual os usuários podem
planejar livremente uma rota entre um ponto de entrada e um ponto de
saída definidos, com a possibilidade de voar por meio de pontos inter-
mediários, publicados ou não, sem referência à rede de rotas dos Serviços
de Tráfego Aéreo — ATS.
```
```
DECEA (2025d)
```
```
Geofence É um limite de espaço aéreo virtual que proíbe (keep-out) ou restringe
(keep-in) o acesso a um volume específico de espaço aéreo (RIBEIRO,
2023), conforme as características abaixo: a) pode ser estática, se perma-
nente, ou dinâmica, se ativada em função das condições operacionais; b)
uma geofence estática pode ser usada para definir corredores de voo e
evitar obstáculos, enquanto uma geofence dinâmica pode ser alocada de-
vido a condições operacionais específicas, emergências ou eventos me-
teorológicos; e c) no contexto deste documento, uma geofence funciona
como uma barreira, isto é, um perímetro virtual para uma determinada
área geográfica no mundo real, e esse perímetro é definido em termos
de uma combinação de coordenadas geográficas, raios e arcos conforme
necessário
```
```
DECEA (2024a)
```
```
Gerenciamento
de Tráfego
Aéreo (ATM)
```
```
Expressão genérica que representa a administração dinâmica e integrada
do tráfego aéreo e do espaço aéreo, incluindo os serviços de tráfego aéreo
e o do espaço aéreo e do fluxo de tráfego aéreo, de forma segura, econô
mica, eficiente, contínua, colaborativa e ambientalmente sustentável, me-
diante o emprego de instalações e serviços e envolvendo funções a bordo
das aeronaves e em terra
```
```
DECEA (2025c)
```
```
Gerenciamento
de Tráfego de
Aeronave Não
Tripulada –
UTM
```
```
Aspecto específico do gerenciamento de tráfego aéreo que gerencia as
operações UAS de forma segura, econômica e eficiente, por meio da
disponibilidade de instalações e de um conjunto de serviços contínuos
em colaboração com todos os envolvidos, incluindo funções aéreas e ter-
restres
```
```
DECEA (2024a)
```
```
Heliponto Área h omologada e demarcada oficialmente para o pouso e a decolagem
de aeronaves de asas rotativas (helicópteros).
```
### DECEA (2023)

```
Observador de
Aeronave Não
Tripulada
```
```
Integrante da equipe UAS designado pelo Explorador/Operador que,
por meio da observação visual de uma Aeronave, auxilia o Piloto Remoto
na condução segura do voo. NOTA: A observação visual, aos moldes do
estabelecido para operação VLOS, deverá ser estabelecida sem o auxílio
de outros equipamentos ou lentes, excetuando -se as corretivas.
```
### DECEA (2023)

```
Operação
Aeroagrícola
```
```
Operação com a finalidade de proteger ou fomentar o desenvolvimento
da agricultura em qualquer de seus aspectos, mediante a aplicação em
voo de fertilizantes, sementes, inseticidas, herbicidas e outros defensivos,
povoamento de águas e combate a incêndios em campos e florestas, com-
bate a insetos, a vetores de doenças ou outros empregos correlatos.
```
### DECEA (2023)

```
Operação Além
da Linha de
Visada Rádio
```
```
Refere-se a qualquer outra situação em que o enlace de pilotagem não seja
direto (ponto a ponto) entre a Estação de Pilotagem Remota e a Aeron-
ave Não Tripulada. Nesse contexto, o enlace eletrônico é estabelecido de
forma indireta, por meio de outros equipamentos (como antenas repeti-
doras de sinal, outras UA ou satélites)
```
### DECEA (2023)


AppendixA. Acronym,Abbreviations,andGlossary A.2. DECEADefinitionsTraceabilityMatrix

```
Term Definition Source
Operação Além
da Linha de
Visada Visual
```
```
Operação em que o Piloto Remoto não consiga manter a Aeronave Não
Tripulada dentro do seu alcance visual.
```
### DECEA (2023)

```
Operação
Atípica
```
```
Operação que apresenta características que impossibilitam o cumpri-
mento de critérios estabelecidos nesta Instrução.
```
### DECEA (2023)

```
Operação Au-
tomatizada
```
```
Operação em que a aeronave não tripulada cumpre automaticamente o
planejamento de voo programado e durante a qual, em condições nor-
mais d e funcionamento dos componentes UAS, é possível ao Piloto Re-
moto intervir na condução da operação em todas as suas fases. NOTA:
Em condições normais, o Piloto Remoto deve estar apto para interferir no
voo da aeronave não tripulada, cuja pilotagem está sob sua responsabili-
dade e supervisão.
```
### DECEA (2023)

```
Operação
Baseada em
Trajetória –
TBO
```
```
a) conceito para viabilizar o gerenciamento de trajetória 4D (4DT), que
leva em consideração adicional o tempo, baseado em desempenho glob-
almente consistente, compartilhando e gerenciando informações de tra-
jetória; e b) o TBO aprimorará o planejamento e a execução de voos efi-
cientes, reduzindo possíveis conflitos e resolvendo antecipadamente os
futuros desequilíbrios de demanda/capacidade da rede e do sistema
```
```
DECEA (2024a)
```
```
Operação
de Aero-
levantamento
```
```
Operação com a finalidade de realizar medição, computação e registro
de dados do terreno com o emprego de sensores e/ou equipamentos ad-
equados.
```
### DECEA (2023)

```
Operação em
Área Confinada
```
```
Operação realizada na fachada interna de prédios e construções, mesmo
que parcialmente, incluindo ginási os, estádios e arenas a céu aberto até
o limite vertical da sua estrutura lateral.
```
### DECEA (2023)

```
Operação em
Linha de Visada
Rádio
```
```
Refere-se a situação em que o enlace de pilotagem é caracterizado pela
ligação direta (ponto a ponto) entre a Estação de Pilotagem Remota e a
aeronave.
```
### DECEA (2023)

```
Operação em
Linha de Visada
Visual
```
```
Operação na qual o piloto ou Observador de UA mantém o contato vi-
sual direto com a aeronave não tripulada (sem auxílio de lentes ou out-
ros equipamentos, exceto as lentes corretivas), de modo a conduzir o voo
com as responsabilidades de manter o afastamento de outras aeronaves,
bem como evitar colisões com obstáculos.
```
### DECEA (2023)

```
Operação em
Linha de Visada
Visual Esten-
dida
```
```
Refere-se à situação na qual o Piloto Remoto, sem auxílio de lentes ou
outros equipamentos, não é capaz de manter o contato visual direto com
a Aeronave Não Tripulada, necessitando, dessa forma, do auxílio de Ob-
servadores de UA para conduzir o voo com a s responsabilidades de
manter a segurança da navegação, bem como evitar colisões com ob-
stáculos, seguindo as mesmas regras de uma operação VLOS.
```
### DECEA (2023)

```
Operação no
Entorno de
Estrutura
```
```
Operação realizada em torno de qualquer estrutura ou obstáculo, quer
seja artificial ou natural, limitada verticalmente a 5 m (cinco metros)
acima da altura da estrutura ou do obstáculo e afastada horizontalmente
até 30 m (trinta metros) deste.
```
### DECEA (2023)

```
Operação
Padrão
```
```
Operação realizada conforme condicionantes previstas nesta Instrução
diversa de Aeroagrícola, Aerolevantamento, Atípica e No Entorno de Es-
trutura.
```
### DECEA (2023)

```
Operações
Gate-to-Gate
```
```
Conjunto de procedimentos contínuos que buscam o pleno atendimento
do planejamento dos usuários, envolvendo as operações das aeronaves
desde o momento em que se inicia o deslocamento, ainda na superfície,
passando por todas as fases de voo até a chegada no destino, incluindo o
estacionamento
```
```
DECEA (2025c)
```

AppendixA. Acronym,Abbreviations,andGlossary A.2. DECEADefinitionsTraceabilityMatrix

```
Term Definition Source
Operador de
Aeródromo
```
```
É toda pessoa natural ou jurídica a quem a ANAC tenha outorgado o
direito de administrar ou prestar serviços em aeródromo público ou pri-
vado, próprio ou não, com ou sem fins lucrativos.
```
### DECEA (2023)

```
Órgão de Cont-
role de Tráfego
Aéreo
```
```
Expressão genérica que se aplica, segundo o caso, a um Centro de Con-
trole de Área (ACC), a um Órgão de Controle de Operações Aéreas Mil-
itares (OCOAM), a um Controle de Aproximação (APP) ou a uma Torre
de Controle de Aeródromo (TWR).
```
### DECEA (2023)

```
Órgão dos
Serviços de
Tráfego Aéreo
```
```
Expressão genérica que se aplica, segundo o caso, a um órgão de controle
de tráfego aéreo ou a um órgão de informação de voo. NOTA: Por con-
veniência, a expressão “órgão dos serviços de tráfego” é abreviada para
“órgão ATS” nesta publicação.
```
### DECEA (2023)

```
Órgãos Region-
ais
```
```
São órgãos que desenvolvem atividades na Circulação Aérea Geral
(CAG) e na Circulação Operacional Militar (COM), responsáveis por co-
ordenar ações de gerenciamento e controle do espaço aéreo e de naveg-
ação aérea nas suas áreas de jurisdição. NOTA: São Órgãos Regionais do
DECEA os CINDACTA I, II, III e IV e o CRCEA-SE.
```
### DECEA (2023)

```
Pequena Aeron-
ave Não Tripu-
lada
```
```
Subconjunto de Aeronaves Não Tripuladas com peso máximo de deco-
lagem (PMD) menor ou igual a 25 Kg.
```
### DECEA (2023)

```
Peso Máximo
de Decolagem
```
```
É o máximo peso que uma aeronave não tripulada (incluído seu com-
bustível, cargas e equipamentos transportados) pode ter para ser capaz
de decolar e realizar um voo com segurança. NOTA: O PMD independe
de a aeronave estar equipada ou não com seus acessórios. Por exem-
plo, se uma aeronave é capaz de decolar e realizar um voo seguro, es-
tando equipada com um protetor de hélices e o uso desse acessório deixa
a aeronave com um peso de 255 g, o PMD da aeronave é de, no mínimo,
255 g, independentemente de estar voando com ou sem o acessório do
exemplo.
```
### DECEA (2023)

```
Pessoa Anuente Pessoa cuja presença não é indispensável para que ocorra uma operação
de aeronave não tripulada bem -sucedida, mas que por von tade própria
e por sua conta e risco concorde que uma aeronave não tripulada opere
perto de sua própria pessoa ou de seus tutelados legais, sem observar os
critérios das áreas distantes de terceiros.
```
### DECEA (2023)

```
Pessoa En-
volvida
```
```
Pessoa cuja presença é indispensável para que ocorra uma operação bem
```
- sucedida da aeronave não tripulada.

### DECEA (2023)

```
Piloto Remoto
em Comando
```
```
É o piloto que conduz o voo com as responsabilidades essenciais pela op-
eração, podendo ou não ser o responsável pelo manuseio dos controles
de pilotagem da aeronave. Quando responsável, exclusivamente, pelo
manuseio dos controles de pilotagem, será denominado PILOTO RE-
MOTO. NOTA: A transferência de responsabilidade entre Piloto Remoto
ou Piloto Remoto em Comando, quando aplicável, deverá ser efetuada
de acordo com os procedimentos estabelecidos pelo operador UAS.
```
### DECEA (2023)

```
Plano de Termi-
nação de Voo
```
```
Conjunto de procedimentos, sistemas e funções preestabelecidos e plane-
jados para finalizar um voo de forma controlada, em caso de emergência,
com a finalidade de minimizar a possibilidade de ferir ou causar dano a
pessoas, propriedades ou outras aeronaves no solo e no ar.
```
### DECEA (2023)

```
Produto Ais Informação aeronáutica disponibilizada na forma de um conjunto de da-
dos digitais ou em uma apresentação padrão em papel ou em format o
digital, conforme ICA 53-8 “Serviços de Informação Aeronáutica”.
```
### DECEA (2023)


AppendixA. Acronym,Abbreviations,andGlossary A.2. DECEADefinitionsTraceabilityMatrix

```
Term Definition Source
Proteção Am-
biental na
Aviação
```
```
Objetivo estratégico da OACI que contempla três temáticas principais:
mudanças climáticas e emissões da aviação, ruído de aeronaves e quali-
dade do ar local.
```
```
DECEA (2025c)
```
```
Registro de
Análise Pre-
liminar de
Segurança
Operacional
```
```
Documento que registra e formaliza a realização de uma Análise Prelim-
inar de Segurança Operacional (APSO), aplicado a mudanças no ANS,
quando ficar evidente que o objeto da avaliação, afetando ou não o
ANS, não tem potencial para acarretar risco à segurança operacional, não
cabendo, portanto, a adoção de medidas mitigadoras.
```
### DECEA (2023)

```
Rota Especial
de Aeronave
em Voo Visual –
REA
```
```
Rota ATS estabelecida com o propósito de permitir, exclusivamente, voos
VFR de aeronaves sob condições específicas
```
```
DECEA (2024a)
```
```
Rota Especial
de Helicópteros
```
- REH

```
a) rota estabelecida com o propósito de permitir, exclusivamente, voos
VFR (visuais) de helicópteros sob condições específicas; b) visa evitar in-
terferência com o tráfego de voos IFR (por instrumentos) dos aeródromos
de uma determinada área, por meio do estabelecimento de altitudes máx-
imas e percursos com referências visuais bem definidas; e c) a REH tam-
bém tem o objetivo de propiciar o máximo de áreas livres no solo onde o
helicóptero possa efetuar um pouso de emergência, com o mínimo risco
possível para pessoas e propriedades, e adequar o uso de helicópteros às
suas características peculiares
```
```
DECEA (2024a)
```
```
Seção SARPAS Seção, localizada no CGNA, caracterizada por um conjunto de encargos
com a finalidade de gerenciar atividades administrativas referentes ao
cadastramento de Pilotos Remotos e Aeronaves Não Tripuladas, além de
gerenciar a posição Tático SARPAS.
```
### DECEA (2023)

```
Serviço de
Informação
de Voo de
Aeródromo
```
```
Serviço prestado com a finalidade de proporcionar avisos e informações
úteis para a realização segura e eficiente dos voos na jurisdição d e um
determinado aeródromo, homologado ou registrado, que não dispõe de
Órgão ATS. NOTA: O AFIS é, normalmente, prestado por uma estação
aeronáutica, também nomeada “órgão AFIS”, localizada no aeródromo
ou remotamente e identificada como “RÁDIO”.
```
### DECEA (2023)

```
Serviços de
Navegação
Aérea
```
```
Este termo inclui o ATM, a infraestrutura de comunicações, nave-
gação e vigilância (CNS), os serviços meteorológicos para a naveg-
ação aérea (MET), a Busca e Salvamento (SAR) e os Serviços de In-
formação Aeronáutica/Gestão da Informação Aeronáutica (AIS/AIM).
Esses serviços são prestados ao tráfego aéreo durante todas as fases de
operação (aeródromo, aproximação e em rota)
```
```
DECEA (2025c)
```
```
Serviços de
Tráfego Aéreo
```
```
Expressão genérica que se aplica, segundo o caso, aos serviços de in-
formação de voo, alerta, assessoramento de tráfego aéreo e controle de
tráfego aéreo (controle de área, controle de aproximação ou controle de
aeródromo)
```
```
DECEA (2025c)
```
```
Sistema ATM Sistema que proporciona o Gerenciamento de Tráfego Aéreo mediante a
integração colaborativa de pessoas, informação, tecnologia, instalações
e serviços, apoiados por comunicações, navegação e vigilância baseadas
em terra, a bordo e/ou no espaço (satélites)
```
```
DECEA (2024a)
```
```
Sistema ATM Sistema que proporciona o Gerenciamento de Tráfego Aéreo mediante a
integração colaborativa de pessoas, informações, tecnologia, instalações
e serviços, apoiado por meios de comunicações, navegação e vigilância
baseados em terra, a bordo das aeronaves e/ou no espaço (satélites)
```
```
DECEA (2025c)
```

AppendixA. Acronym,Abbreviations,andGlossary A.2. DECEADefinitionsTraceabilityMatrix

```
Term Definition Source
Sistema de
Aeronave Não
Tripulada
```
```
Sistema composto pela Aeronave e seus elementos associados, podendo
ser remotamente pilotada ou totalmente autônoma.
```
### DECEA (2023)

```
Sistema de
Aeronave Re-
motamente
Pilotada
```
```
Subconjunto do Sistema de Aeronave Não Tripulada, que seja capaz de
interagir com o Controle de Tráfego Aéreo em tempo real, composto pela
aeronave remotamente pilotada (RPA), sua(s) estação(ões) de pilotagem
remota, o enlace de pilotagem e qualquer outro componente associado à
sua operação.
```
### DECEA (2023)

```
Sistema de Con-
trole do Espaço
Aéreo Brasileiro
```
```
Sistema que tem por finalidade prover os meios necessários para o geren-
ciamento e o controle do espaço aéreo e o serviço de navegação aérea, de
modo seguro e eficiente, conforme estabelecido nas normas nacionais e
nos acor dos e tratados internacionais de que o Brasil seja parte. As ativi-
dades desenvolvidas no âmbito do SISCEAB são aquelas realizadas em
prol do gerenciamento e do controle do espaço aéreo, de forma integrada,
civil e militar, com vistas à vigilância, segurança e defesa do espaço aéreo
sob a jurisdição do Estado Brasileiro. NOTA: O DECEA é o Órgão Central
do SISCEAB.
```
### DECEA (2023)

```
Sistema de
Gerenciamento
da Segurança
Operacional
```
```
Sistema que apresenta objetivos, políticas, responsabilidades e estruturas
organizacionais necessárias ao funcionamento do Gerenciamento da Se-
gurança Operacional, de acordo com metas de desempenho, contendo os
procedimentos para o Gerenciamento do Risco.
```
### DECEA (2023)

```
Sistema de
Navegação
Aérea
```
```
Sistema que apoia o desenvolvimento seguro e ordenado da aviação civil
internacional, mediante a integração cooperativa de seres humanos, in-
formações, tecnologias, instalações e serviços, envolvidos na provisão e
no uso dos rec ursos de navegação aérea. Compreende as operações de
aeródromo, o ATM, os serviços meteorológicos, a informação aeronáu-
tica, a busca e salvamento, apoiados por capacidades de comunicações,
navegação e vigilância a bordo, em terra ou baseados no espaço, bem
como as operações em rota e aeroportuárias, incluindo os tempos de es-
cala
```
```
DECEA (2025c)
```
```
Sistema para
Solicitação
de Acesso ao
Espaço Aéreo
Brasileiro
```
```
POR AERONAVES NÃO TRIPULADAS Sistema desenvolvido para so-
licitação de acesso ao espaço aéreo brasileiro pelos usuários desse seg-
mento aeronáutico.
```
### DECEA (2023)

```
Sistema UAM
```
- Mobilidade
Aérea Urbana
(Urban Air
Mobility)

```
Sistema concebido como um subconjunto do Sistema ATM, com o ob-
jetivo de proporcionar o Gerenciamento de Tráfego Aéreo, dentro e en-
tre ambientes urbanos e rurais, mediante a integração colaborativa de
pessoas, informações, tecnologia, instalações e serviços, apoiados por co-
municações, navegação e vigilância baseadas em terra, a bordo e/ou no
espaço (satélites)
```
```
DECEA (2024a)
```
```
Sistema UTM –
Gerenciamento
de Tráfego
de Aeronaves
não Tripuladas
(Unmanned
Aircraft Sys-
tem Traffic
Management)
```
```
Sistema concebido como um subconjunto do Sistema ATM, com o obje-
tivo de proporcionar o Gerenciamento de Tráfego Aéreo aos Sistemas de
Aeronaves não Tripuladas – UAS mediante a integração colaborativa de
pessoas, informações, tecnologia, instalações e serviços, apoiados por co-
municações, navegação e vigilância baseadas em terra, a bordo e/ou no
espaço (satélites)
```
```
DECEA (2024a)
```

AppendixA. Acronym,Abbreviations,andGlossary A.2. DECEADefinitionsTraceabilityMatrix

```
Term Definition Source
Solicitante Explorador ou Operador que solicite a operação da Aeronave Não Trip-
ulada.
```
### DECEA (2023)

```
Tático SARPAS Posição Operacional, localizada no CGNA, caracterizada por um con-
junto de encargos atribuídos ao Gerente Nacional de Fluxo (GNAF), com
a finalidade de receber as informações relatadas pelos usuários externos,
referentes à perda de Enlace C2, e difundir alertas de perigo aos Órgãos
ATS locais, com vistas a subsidiar as equipes para que sejam adotadas as
medidas necessárias em prol da manutenção da segurança operacional.
```
### DECEA (2023)

```
Termo de Coor-
denação
```
```
Termo que contém informações operacionais para a operação de UA,
med iante coordenação entre o Explorador/Operador da aeronave e o
Órgão ATS local ou, na ausência deste, o Operador de Aeródromo, com
a finalidade de assessorar o Órgão Regional durante a análise da solici-
tação de acesso ao espaço aéreo brasileiro no SARPAS.
```
### DECEA (2023)

```
Vertiporto a) área delimitada em terra, na água ou em uma estrutura destinada para
uso, no todo ou em parte, para pouso, decolagem e movimentação em
superfície de aeronaves VTOL (ex.: helicópteros e eVTOL); e b) embora
haja muitas outras definições mais detalhadas sobre os tipos de locais de
operação de aeronaves eVTOL, no contexto deste documento, o termo
Vertiporto será aplicado em todos os casos
```
```
DECEA (2024a)
```
```
Vigilância
Dependente
Automática –
Radiodifusão –
ADS-B
```
```
Meio pelo qual a aeronave, veículos de aeródromo e outros objetos po-
dem automaticamente transmitir e/ou receber dados, tais como identi-
ficação, posição e dados adicionais, conforme o caso, em modo radiodi-
fusão via enlace de dados.
```
```
DECEA (2024a)
```
```
Zona de Aprox-
imação ou de
Decolagem
```
```
Área no setor de pouso e decolagem do aeródromo. Fo rmada por uma
linha perpendicular ao eixo longitudinal da pista, posicionada nas ex-
tremidades das cabeceiras com 150 m de comprimento para cada lado,
tendo em cada uma de suas extremidades uma reta com abertura de vinte
graus cujo centro está posicionado no encontro das duas retas e possui ar-
cos com distância variável em relação à cabeceira e em função da altura
do voo.
```
### DECEA (2023)

```
Zona de En-
torno de Aeró-
dromo
```
```
Área no entorno do aeródromo, excluindo-se as áreas pertencentes à
ZAD. Tem como origem o eixo da pista e possui limite variável, em
função da altura do voo.
```
### DECEA (2023)

```
Zona de En-
torno de He-
liponto
```
```
Área no entorno do heliponto. Tem como origem o Ponto de Referência
de Aeródromo (ARP) e possui valor de raio variável, em função da altura
do voo.
```
### DECEA (2023)

```
Zona de Re-
strição de Voo
```
```
Área específica na qual o acesso de Aeronave Não Tripulada (UA) requer
autorização mediante análise ATM do Órgão Regional, considerando as
restrições previstas em função das alturas e distâncias de aeródromos e
helipontos ou das áreas de segurança. NOTA: A Zona de Aproximação
ou de Decolagem (ZAD), a Zona de Entorno de Aeródromo (ZEA), a
Zona de Entorno de Heliponto (ZEH) e as Áreas de Segurança são con-
sideradas Zona de Restrição de Voo (FRZ).
```
### DECEA (2023)

```
Zona Proibida
ao Voo
```
```
Área específica na qual o voo normalmente não é permitido. A origem
da NFZ é Técnica, geralmente criada pelo fabricante do equipamento.
```
### DECEA (2023)

```
Traceability note: DCA 351-6 (DECEA (2022)) text extraction is not machine-readable in this repository copy due embedded
font encoding; definitions from this document require manual transcription for full inclusion.
```

