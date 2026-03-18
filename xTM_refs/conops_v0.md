1. #  **Scope** 

*This OCD section documents the scope of the OCD.*

	Unmanned aviation has been rapidly evolving and, as consequence, the drones capabilities keep on an ongoing improvement. This market shows a diverse scope of applications such as inspections, infrastructure monitoring, mapping, filming and photography, precision agriculture, search and rescue, disaster relief and public safety. 

The Operational Concept Description (herein referred to as OCD) describes, outlines, establishes the strategic and operational framework required to facilitate the safe, efficient, and scalable integration of Unmanned Aircraft System Traffic Management (UTM) and Urban Air Mobility (UAM) within the Brazilian Airspace Control System (SISCEAB).

This document encompasses the technical requirements, jurisdictional boundaries, and collaborative responsibilities between stakeholders, specifically addressing:

* Geographic and Jurisdictional Limits: The application of these operations within sovereign Brazilian airspace, focusing on high-density urban centers (e.g., São Paulo and Rio de Janeiro) and transition zones between uncontrolled (Class G) and controlled airspace (Classes C, D, and E).  
* Regulatory Alignment: Compliance with the mandates of the Department of Airspace Control (DECEA) and the National Civil Aviation Agency (ANAC), ensuring that UTM/UAM protocols harmonize with existing ICA (Instruction of the Air Force Command) 100-40 regulations and RBAC (Brazilian Civil Aviation Regulation) standards.  
* Operational Services: The definition of essential services, including automated flight authorization, dynamic airspace reconfiguration, real-time situational awareness (e-Identification), and conflict detection and resolution (CD\&R) for both autonomous and piloted vertical take-off and landing (VTOL) aircraft.  
* Infrastructure Integration: The interface between Vertiports and the existing National Air Navigation Service Provider (ANSP) infrastructure, ensuring seamless data exchange through the System Wide Information Management (SWIM) architecture.  
* Safety and Security: The mitigation of risks associated with high-frequency low-altitude operations, including the protection of "critical infrastructure" and the management of contingencies in complex meteorological conditions typical of tropical latitudes.

## **1.1**    **Identification**

*This OCD subsection should contain the approved identification number, title, and abbreviation, if applicable, of the system to which the OCD applies.*

## **1.2**    **System Purpose** 

*This OCD subsection should briefly state the purpose of the system to which the OCD applies.* 

The document aims to create directives and procedures to ensure safety, security, efficiency and equity of the aerial space. A key objective is to present a vision for the integration of eVTOLs, as well as sUAS, through the UAM and UTM concepts, into the Brazilian airspace structure, maintaining safety, fluidity, and efficiency standards through the progressive evolution of the use of new technologies.

This hereby document describes the current state of operations, establishes the reasons for change, and defines operations for the future in terms of functions/features and supporting operations. This document will be used to present the vision, goals and direction for the project and support the detailed systems engineering development process.

### **1.2.1**    **Document Overview** 

*This OCD subsection should summarize the purpose (including intended audience) and contents of the OCD.* 

*ICA 100-40* 

*MCA 56-1,2,3 AND 4*

 

 

# 

# **2**     **Referenced Documents** 

| \# | Document (Title, source, version, date, location) |
| :---- | :---- |
| 1 | DCA 351-6 National UTM Concept of Operations (*Concepção Operacional UTM Nacional*). Available at: https://publicacoes.decea.mil.br/publicacao/dca-351-6 |
| 2 | DCA 351-7 Air Force Guideline for Brazilian Airspace Control (*Diretriz da Aeronáutica para o Controle do Espaço Aéreo Brasileiro*). Available at: https://publicacoes.decea.mil.br/publicacao/DCA-351-7 |
| 3 | PCA 351-6 Operational Design of Free Route Airspace \- FRA (Concepção Operacional do Espaço Aéreo de Rotas Livres \- FRA). Available at: https://publicacoes.decea.mil.br/publicacao/PCA-351-6 |
| 4 | PCA 351-7 National UAM Operational Concept (*Concepção Operacional UAM Nacional*). Available at: https://publicacoes.decea.mil.br/publicacao/PCA-351-7 |
| 5 | Unmanned Aircraft System (UAS) Traffic Management (UTM) v2.0. Available at: https://www.faa.gov/sites/faa.gov/files/2022-08/UTM\_ConOps\_v2.pdf |
| 6 | Urban Air Mobility (UAM) Concept of Operations v2.0. Available at: https://www.faa.gov/sites/faa.gov/files/Urban%20Air%20Mobility%20%28UAM%29%20Concept%20of%20Operations%202.0\_0.pdf |
| 7 | F3548−21 Standard Specification for UAS Traffic Management (UTM) UAS Service Supplier (USS) Interoperability, ASTM International, West Conshohocken, PA: ASTM International. Available at:  |
| 8 | F3411−22a Standard Specification for Remote ID and Tracking, ASTM International, West Conshohocken, PA: ASTM International. Available at:  |
| 9 | F3442−25 Standard Specification for Detect and Avoid System Performance Requirements, ASTM International, West Conshohocken, PA: ASTM International. Available at:  |
| 10 | F3379− 20 Standard Specification for Training for Public Safety Remote Pilot of Unmanned Aircraft Systems (UAS) Endorsement, ASTM International, West Conshohocken, PA: ASTM International. Available at:  |
| 11 | F3657−23 Standard Specification for Verification of Lightweight Unmanned Aircraft Systems (UAS), ASTM International, West Conshohocken, PA: ASTM International. Available at:   |
|  | ASTM International (2014) ASTM F3002-14a: Standard Specification for Design of the Command and Control System for Small Unmanned Aircraft Systems (sUAS). West Conshohocken, PA: ASTM International. Available at: https://doi.org/10.1520/F3002-14A |
|  | ASTM International (2020) ASTM F3060-20: Standard Terminology for Aircraft. West Conshohocken, PA: ASTM International. Available at: https://doi.org/10.1520/F3060. |
|  | ASTM International (2022) Protocol/utm.yaml at v1.0.0. Available at: https://github.com/astm-utm/Protocol/blob/v1.0.0/utm.yaml |
|  | ASTM International (2019) ASTM F3298-19: Standard Specification for Design, Construction, and Verification of Lightweight Unmanned Aircraft Systems (UAS). West Conshohocken, PA: ASTM International. Available at: https://doi.org/10.1520/F3298 |
|  | Mizell, S. and Foster, M. W. (2018) RESTful JSON. Available at: https://restfuljson.org |
|  | Joint Authorities for Rulemaking on Unmanned Systems (JARUS) (2024) JARUS guidelines on Specific Operations Risk Assessment (SORA): V2.5 Package. Available at: http://jarus-rpas.org/publications/ |
|  | International Organization for Standardization and International Electrotechnical Commission (2022) ISO/IEC 27001:2022: Information security, cybersecurity and privacy protection — Information security management systems — Requirements. 3rd edn. Geneva: ISO. Available at: https://www.iso.org/standard/27001 |
|  | International Organization for Standardization (2015) ISO 9001:2015: Quality management systems — Requirements. Geneva: ISO. Available at: https://www.iso.org/standard/62085.html |
|  | ISO/IEC (2019) ISO/IEC 27701:2019: Security techniques — Extension to ISO/IEC 27001 and ISO/IEC 27002 for privacy information management — Requirements and guidelines. Geneva: International Organization for Standardization. Available at: https://www.iso.org/standard/71670.html |
|  | IEEE (2021) IEEE 802.11ax-2021 \- IEEE Standard for Information Technology--Telecommunications and Information Exchange between Systems Local and Metropolitan Area Networks--Specific Requirements Part 11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications. New York, NY: IEEE. doi: 10.1109/IEEESTD.2021.9442429. |
|  |  |

 

# 

# **3**     **Background Information** 

*This OCD section contains background information that is useful in understanding the needed capability, the existing system, the proposed system, and/or the project to provide the proposed system. Where information is only relevant to the existing or proposed system, that information should be provided in the appropriate sections rather than this section. Typical information that may be included in this section includes the following:* 

·       *details and history of the needed capability;* 

·       *a description of the higher level organizational infrastructure;* 

·       *details and history of the project;* 

·       *a review of stakeholders for the system and project; and* 

·       *discussion of related projects and systems.* 

*The section helps to define the “why” of the system.* 

Beyond basic connectivity, aviation drives economic development by providing the essential throughput for international trade and specialized services. The industry’s transition toward sustainable technologies and automated safety systems ensures that this economic contribution remains compatible with modern environmental and reliability standards. This development, combined with technological changes in the automation, telecommunications, information technology, and navigation sectors, including onboard equipment and satellite capabilities, is driving remarkable progress in the safety and efficiency of Air Traffic Management (ATM) and encouraging the use of airspace by new and diverse participants.

There is a projection that road traffic in large cities will become even more congested, making it difficult to transport people and cargo efficiently. Therefore there's going to be an increase in demand for air space services, such as deliveries, infrastructure inspections, agriculture and general locomotion. 

One of the proposed solutions to aid traffic congestion is the implementation of eVTOL, generating innovative services of cargo and passenger transportation. The perspective of low environmental impact and more efficient travel have attracted the attention of multiple aviation companies and investors, each with their own expectations. Still, in order to implement the UAM (Urban Air Mobility) concept, it is necessary to restructure the airspace in which this concept will be applied, as well as to make progressive technological and regulatory advances in the provision of services to users, in order to allow for an increase in the number of flights while maintaining a level of safety compatible with aviation activity.

On the other hand, an already ongoing solution is the application of small unmanned aerial vehicles, referred to as UAS, is being used to manage deliveries, infrastructure inspections and agricultural needs, supporting business and creating economic opportunities. Currently, commercial and recreational UAS operators can fly within visual line of sight (VLOS) under current regulations ICA 100-40 and MCA 56-1, 2, 3, and 4; other UAS operations today require individualized case-by-case evaluation.

The current legislations that regulate the airspace segregate areas to ensure safety through isolation; however, this model is inherently unscalable for the projected volume of UAS and eVTOL operations. Traditional air traffic management relies on maintaining large buffer zones and manual coordination between pilots and controllers, which cannot accommodate the high density of aircraft expected to operate simultaneously in restricted urban corridors. As the number of concurrent flights increases in localized areas, the reliance on static airspace blocks creates significant capacity constraints and prevents the flexible movement required for urban air mobility. This density of operations exceeds the threshold of current manual monitoring capabilities, leading to an inevitable saturation of the existing system.

The integration of these aircraft into a highly regulated environment with almost eight decades of history must be carried out through a careful assessment of the possible impacts on other airspace users. This includes establishing a regulatory framework, developing operational rules to ensure accountability of the actors involved, and promoting efficient and equitable access to airspace for all operators, both manned and unmanned.

The federated UTM model establishes a scalable, low-altitude operational framework that balances regulatory authority with commercial agility. By leveraging a decentralized ecosystem of private-sector services, the system accelerates the deployment of aerial capabilities through market-driven innovation while significantly reducing the government’s infrastructural and human resource expenditures. This construct ensures a stable environment for high-volume operations by utilizing shared situational awareness and standardized protocols to mitigate risk and maintain systemic integrity. Ultimately, this flexible architecture allows the aviation authority to retain absolute airspace sovereignty while delegating the tactical management of authorized UAS flights to industry stakeholders.

The implementation of a structured UAM system represents a critical shift toward a modernized aeronautical infrastructure capable of generating significant economic, social, and environmental value, particularly as operations scale to meet high-density demands. While current low-altitude structures, such as the REA and REH, were originally designed to manage VFR traffic through segregation, they are increasingly insufficient for the growing demand for IFR and high-frequency digital operations. Consequently, transitioning to an integrated UAM framework is essential to overcome the limitations of these legacy routes, allowing the airspace to evolve from a series of isolated corridors into a scalable, high-capacity environment that supports advanced navigation and sustainable development.

## **3.x Abbreviations**

A1F \- Alert function

A2F \- Avoid function

AAM \- Advanced Air Mobility

ADS-B \- Automatic Dependent Surveillance

AES \- Advanced Encryption Standard

AFCS \- Automated Flight Control System

AFM \- Airplane Flight Manual

AFR \- Automated Flight Rules

AGL \- above ground level 

AHJ \- authority having jurisdiction

AO \- Aerodrome Operations

AOM \- Airspace Organization Management

API \- Application Programming Interface

AR \-

ARC \-

ASOS \-

ATC \-

ATFM \- Air Traffic Flow Management

ATM \- Air Traffic Management

ATM SDM \- ATM Service Delivery Management

ATS \- Air Traffic Services

AUO \- Airspace User Operations

AuthType \-

AWOS \-

C2 \- Command and Control

CA \- UAM Corridor

CGNA \- Air Navigation Management Center

CM \- Conflict Management

COPs \- Cooperative Operating Practices 

ECO-UAM \- UAM Ecosystem

eVTOL \- electric Aircraft capable of Vertical Takeoff and Landing

DAA \- Detect and Avoid

DCB \- Demand-Capacity Balancing

D-TWR \- Digital Aerodrome Control Towers

EAC \- Conditioned Airspace

FF-ICE \- Flight and Flow Information for a Collaborative Environment

FIMS \- Flight Information Management System

FRA \- Free Routes Airspace

GATMOC \- Global Air Traffic Management Operational Concept

GANP \- Global Air Navigation Plan

GNSS \- Global Navigation Satellite Systems

HIRF- high-intensity radiated field

IFR \- Instrument Flight Rules

LoWC \- Loss of Well Clear

LR \- Loss of Well Clear Risk Ration

MACproxy \- Mid-air Collision Proxy

xSU \- Unmanned Aircraft System Service Supplier

P2P \- Peer to Peer communication

PSNAs \- Air Navigation Service Providers

PVR \- Priority Volume Reservation

R-AFIS \- Remote Aerodrome Flight Information Services

REA \- Special Visual Flight Route

REH \- Special Helicopter Route

RID \- Remote Identification

RFI \- Request for Information

RPA \- Remote Piloted Aircraft

RPAS \- Remotely Piloted Aircraft System

RPS \- Remote Piloting Station

RT Information \- Real-Time Information

SDSP \- Supplementary Data Service Provider

SISCEAB \- Brazilian Airspace Control System

TS \- Traffic Synchronization

TBO \- Trajectory Based Operation 

UAM \- Urban Air Mobility

UASx/UA \- Unmanned Aircraft System 

UTM \- Unmanned Traffic Management

V2V \- Vehicle to vehicle communication

VFR \- Visual Flight Rules

## **3.x Definitions**

AAM \- Air mobility encompassing both UAM, UTM and ATM.

ADS-B \- A means by which aircraft, aerodrome vehicles, and other objects can automatically transmit and/or receive data, such as identification, position, and additional data, as applicable, in broadcast mode via a data link.

Aircraft \- Any device that can sustain itself in the atmosphere by means of reactions of the air other than reactions of the air against the surface of the earth.

ATM Community \- All organizations, agencies, or entities that can participate, collaborate in the planning, development, regulation, operation, and maintenance of the ATM system. Includes aircraft operators, airport administrators, the aeronautical industry, airspace users, ATM service providers and ICAO.

ATM System \- System that provides Air Traffic Management through the collaborative integration of people, information, technology, facilities, and services, supported by ground-based, airborne, and/or space-based (satellite) communications, navigation, and surveillance.

Automated Flight Rules (AFRs) – Refers to rules, applied within UAM Corridors, which reflect the evolution of the current regulatory regime (e.g., VFR/IFR) and take into account advancing technologies and procedures (e.g., Vehicle-to-Vehicle \[V2V\] and data exchanges). Under defined conditions, the systems/automation may be allocated the role of the “predetermined separator”.

C2 \- Data link between the unmanned aircraft and the remote piloting station for flight control.

Cooperative Area – An airspace volume (e.g., UAM Corridor) within which cooperatively managed operations can occur. ATC ensures separation of non-participating aircraft from the cooperative operations and/or CA.

Cooperative Operating Practices (COPs) – Industry-defined, FAA-approved practices that address how operators cooperatively manage their operations within the CA (i.e., UAM Corridor), including conflict management, equity of airspace usage, and Demand-Capacity Balancing (DCB).

Cooperative Operation – A term used to describe an operation making use of cooperative services (e.g., separation, flow management) and is sharing/exchanging Operational Intent and other information in compliance with applicable regulations and COPs within a CA.

Detect and Avoid \- The ability to see or detect conflicting traffic or other hazards and take appropriate action to comply with applicable flight rules.

ECO-UAM \- Data exchange interface between DECEA systems and other systems and entities, such as PSU, SDSP, other government institutions, public security agencies, etc., enabling the management of airspace restricted data and access points to information on active operations in the UAM environment and, in addition, providing a means for approved stakeholders to consult and receive data on operations in the UAM environment.

Federated Service Network – A group of service providers sharing information within a federated network to support operating in a common, agreed manner consistent with the approved COPs.

Fully Integrated Information Environment – Information environment and key attributes necessary to effectively deliver services and facilitate information exchange between stakeholders.

FRA \- The designated airspace in which users can freely plan a route between a defined entry point and exit point, with the possibility of flying through intermediate points (published or unpublished), without reference to the ATS route network, subject to airspace availability.

Geofence \- Virtual airspace boundary that prohibits (keep-out) or restricts (keep-in) access to a specific volume of airspace (RIBEIRO, 2023), according to the characteristics below:

a) it can be static, if permanent, or dynamic, if activated depending on operational conditions;

b) a static geofence can be used to define flight corridors and avoid obstacles, while a dynamic geofence can be allocated due to specific operational conditions, emergencies, or weather events; and

c) in the context of this document, a geofence functions as a barrier, that is, a virtual perimeter for a given geographic area in the real world, and this perimeter is defined in terms of a combination of geographic coordinates, radii, and arcs as necessary.

Metering Fix \- Reference point for which information on the adjustment of the transit time over a fixed point by a given aircraft is provided to the ACC ATCO via the AMAN software screen, in order to assist him in planning the arrival sequence.

Priority Volume Reservation (PVR) \- an airspace reservation procedure resulting in the establishment of a priority volume, temporarily and in response to activities, on the ground or in the air, within the UTM environment. PVRs are established to support the safety of manned and unmanned operations and are related, among other things, to activities such as emergency response, security and public disaster, and military operations.

REA \- ATS route established for the sole purpose of allowing VRF flights by aircraft under specific conditions.

REH \-  Route established for the sole purpose of allowing VFR (visual) helicopter flights under specific conditions. Aims to avoid interference with IFR (instrument) flight traffic from aerodromes in a given area by establishing maximum altitudes and routes with well-defined visual references and to provide maximum free areas on the ground where the helicopter can make an emergency landing, with the least possible risk to people and property, and to adapt the use of helicopters to their unique characteristics.

RID \- Ability of an UA on board to provide identification and location information that can be received by other parties. 

Remote Pilot in Command \- Person responsible for safe conduct of UAS operations, may be the same person as the operator. The RPIC adheres to operational rules and regulations of the airspace in which the UAS operates, avoiding other aircrafts, terrain and obstacles, as well as, evaluating and respecting the airspace limitations and flight restrictions, avoiding climate conditions and unsafe environments and monitoring the flight performance and UAS location. There may be more than one RPIC, provided that they are properly identified and a sole person operates the UAS at any given time.

RPS \- Component of an unmanned aircraft system that contains the equipment necessary for piloting.

Service Environment(s) – Refers collectively to the distinct regulatory, procedural, and supporting automation mechanisms through which services (e.g., conflict management, flow management) are provided. In the future, the NAS is envisioned to include the current (i.e., traditional) ATS environment as well as incorporate a complementary, cooperative xTM services environment.

TBO \- concept to enable 4D trajectory management (4DT), which takes additional time into account, based on globally consistent performance, sharing and managing trajectory information; and improves the planning and execution of efficient flights, reducing potential conflicts and resolving future network and system demand/capacity imbalances in advance.

Unmanned Aircraft \- Any aircraft that can sustain itself in the atmosphere by means other than reactions of the air against the earth's surface and that is intended to operate without a pilot on board.

UAM Aircraft – An aircraft that chooses to participate in UAM operations.

UAM Corridor – A specific type of CA, as an airspace volume within which cooperatively managed operations can occur. ATC ensures separation of non-participating aircraft from the cooperative operations and/or CA. It consists of an airspace volume defining a three- dimensional route, possibly divided into multiple segments, with associated performance requirements.

UAM Operation – A specific type of cooperative operation that occurs within a UAM Corridor and is conducted in compliance with UAM specific rules, procedures, performance requirements, and COPs.

UAM Operator – The person or entity responsible for the overall management and execution of one or more UAM operations. The operator plans operations, shares flight information (e.g., planning, live flight), and ensures infrastructure, equipment, and services are in place to support safe execution of flight. 

UAM System – System designed as a subset of the ATM System, with the objective of providing Air Traffic Management within and between urban and rural environments through the collaborative integration of people, information, technology, facilities, and services, supported by ground-based, on-board, and/or space-based (satellite) communications, navigation, and surveillance.

UTM System – System designed as a subset of the ATM System, with the objective of providing Air Traffic Management to UAS through the collaborative integration of people, information, technology, facilities, and services, supported by ground-based, airborne, and/or space-based (satellite) communications, navigation, and surveillance. Manages UAS operations safely, economically, and efficiently through the availability of facilities and a set of continuous services in collaboration with all stakeholders, including air and ground functions.

V2V \- Ability of different aircraft embedded systems capability to establish data communication among themselves.

V2I \- Ability of embedded systems to establish data communication with other systems installed in ground-based infrastructure.

Vertiports – An area of land or structure used or intended to be used for electric, hydrogen, and hybrid VTOL landings and takeoffs. A vertiport can include associated buildings and facilities.

Vertistop – A vertistop is a term generally used to describe a minimally developed vertiport for boarding and discharging passengers and cargo (i.e., no fueling, defueling, maintenance, repairs, or storage of aircraft, etc.).

## 

## **3.x Architectures**

### **3.x.1 FAA \- UTM Architecture**

The high-level UTM architecture establishes a decentralized information exchange framework where UAS Operators share operational intent and real-time telemetry with a UAS Service Supplier (USS). The USS facilitates flight efficiency and conflict management. Supplemental data, such as weather, terrain, and surveillance, is provided by Supplemental Data Service Providers (SDSPs) to the USS, which then relays relevant flight information to the operators.  To ensure systemic integrity, operational data is exchanged directly between multiple UAS Service Suppliers via inter-USS communication protocols, while the FIMS ensures that all service providers have access to a unified, authoritative source of airspace data.

![][image1]

Within the UTM ecosystem, the FAA maintains its regulatory and operational authority for airspace and traffic operations; however, the operations are not managed by ATC. Rather, they are organized, coordinated, and managed by a federated set of actors in a distributed network of highly automated systems via application programming interfaces (APIs). Figure 3 depicts a notional UTM architecture that visually identifies, at a high level, the various actors and components, their contextual relationships, as well as high-level functions and information flows. The gray dashed line in Figure 3 represents the demarcation between the FAA and industry responsibilities for the infrastructure, services, and entities that interact as part of UTM. As shown, UTM comprises a sophisticated relationship between the FAA, the Operator, and the various entities providing services and/or demonstrating a demand for services within the UTM ecosystem. The illustration highlights a model, which heavily leverages utilization of third-party entities to support the FAA and the Operator in their respective roles and responsibilities.

### **3.x.2 DECEA \- UTM Architecture**

	The UAS Service Supplier (USS) facilitates the management of flight operations by receiving route planning data from operators and real-time information from the aircraft, enabling the tactical resolution of conflicts and adherence to airspace restrictions. Within the Brazilian framework, this operational data is integrated into a central platform designated as the UTM-Ecosystem.

This centralized hub serves as the authoritative database for the consolidation of SISCEAB data, USS information, and regulatory mandates. It aggregates essential registration, performance, and geographic data—sourced from entities such as ANAC, DECEA, and IBGE—to ensure a unified source of truth. By synchronizing information across USS, UAM, and traditional ATM systems, the UTM-Ecosystem guarantees that high-density operations maintain full regulatory compliance and safety standards within the cooperative traffic airspace.

![][image2]

Within the UTM ecosystem, DECEA retains its regulatory and operational authority for traffic management and airspace surveillance. However, operations are not managed by ATC; instead, they are organized, coordinated, and managed by a set of actors in a distributed network of automated systems through application programming interfaces (APIs). Figure 1 (above) describes an imaginary UTM architecture that visually identifies, at a high level, the various actors and components, their contextual relationships, as well as high-level functions and information flows. As shown, UTM comprises a relationship between DECEA, the Operator, and the various entities that provide services or demonstrate a demand for services within the UTM ecosystem.

### **3.x.3 FAA \- UAM/AAM Architecture**

Within the UAM cooperative management environment, the FAA would maintain regulatory and operational authority for airspace and traffic operations. UAM operations may be organized, coordinated, and managed by a federated set of actors through a distributed network that leverages interoperable information systems. Figure 8 depicts a notional architecture of the UAM actors and contextual relationships and information flows. This architecture is based on patterns established within the UTM architecture described in the UTM ConOps and is consistent with the architecture described in the ETM ConOps.

The federated service network, comprised of individual PSUs operating as a collective, lies at the center of the UAM notional architecture and exchanges data with UAM operators, USSs, SDSPs, the FAA, and public interest stakeholders. PSUs receive supplemental data supporting UAM operation management from the SDSPs and provide relevant UAM operational data to the public. PSUs communicate and coordinate via the federated service network. This allows other UAM stakeholders (e.g., UAM operators, ATC, law enforcement) connected to a PSU to access data shared across the federated service network.

PSUs and USSs may exchange operational information about UAM and UTM operations in airspace under 400 feet where there is a potential need for cooperative separation (e.g., vertiports). Notionally, a USS can expand their service offerings to become a PSU and vice versa. Combined service providers may support operations in both the UAM and UTM environments. The architecture depicts the connectivity of the federated service network to USSs for information exchange while retaining a UAM-centric architectural view.

Vertiports exchange information with the federated service network to facilitate the communication of situational awareness and resourcing information to UAM operators. The PSUs make the aggregate vertiport information available for the operator to be aware of capacity and situational constraints present at the time of respective departure and arrival time. PSUs could potentially provide additional services with this information (e.g., suggested alternate vertiports, suggested alternate departure/arrival times). 

The vertical dashed line in Figure 8 represents the demarcation between the FAA and industry responsibilities for the infrastructure, services, and entities that interact as part of UAM. The FAA-Industry Data Exchange Protocol provides an interface for the FAA to request UAM operational data on demand and send FAA information to the federated service network for distribution to UAM operators, PICs, UAM aircraft, and public interest stakeholders through the Service Security Gateway.

![][image3]

### **3.x.4 DECEA \- UAM/AAM Architecture**

The systemic architecture planned for the implementation of the UAM, as shown in Figure 10 below, represents a significant advance in urban airspace management, integrating contemporary and emerging technologies and innovative air traffic control concepts.

This integration requires precise synergy with the new traffic management system in the UTM environment and the existing ATM system. The new UAM ecosystem is designed to operate in parallel with the ATM system, offering an additional layer of management specific to the urban environment, where airspace is more congested and dynamic.

Although the urban environment is mentioned in correlation with the term UAM, this architectural solution will be applicable to any environment where eVTOL operation may occur, whether urban, suburban, rural, or regional. The architecture provides for interoperability between systems, allowing critical data on air traffic, weather conditions, and flight plans, for example, to be shared more efficiently.

![][image4]

At the operational level, UAM Operators manage UAM Vehicles, which utilize Vehicle-to-Vehicle (V2V) communication for local coordination. These operations are overseen by a PSU (UAM Service Provider), which facilitates Peer-to-Peer (P2P) coordination between different providers across national and operational areas.  The PSU directly manages the flow of traffic to and from Vertiports (VP-1, VP-2), which are organized into localized areas to handle takeoff and landing logistics. 

The architecture relies on several critical external components for data and regulation such as the PSNA, that provides air traffic services and oversight and the CGNA, which provides macro-level flow management and strategic coordination. Supplementary data is provided by SDSP,  analogous to utm architecture.

## **3.x Stakeholders**

Hereon will briefly describe the stakeholders affecting the system, as to present the entities and their relations with the system and each other. 

| Stakeholder | Stakeholder category |
| :---- | :---- |
| Private investors \- Interested in making air taxis profitable on-demand mobility. | Investors |
| Airports \- Can act both as an investor and service provider in case they support air taxi operations. | Investors |
| Developers \- May be interested in the business case for the leisure and entertainment industry. | Investors |
| The city administration \- Also can act as an investor to support special air taxi services, such as medical, police, fire, etc. by analogue with helicopters. | Investors |
| Municipality \- Regulate, limit, or approve possible concepts of UAM integration. May issue a UAM regulation department. | Decision-makers and regulatory bodies  |
| Planning department \- Specify the use of the territory, functional zoning, and restricted areas. | Decision-makers and regulatory bodies  |
| Permit issuing departments \- Approve or deny the proposed concepts from health and safety regulation, risk of fire, environment, etc. | Decision-makers and regulatory bodies  |
| “Green” government \- Has an interest in forcing “green” technologies and the development of electrical air transport. | Decision-makers and regulatory bodies  |
| Infrastructure operators \- Service providers for a physical and IT infrastructure aimed to provide a smooth passenger transition. | Service providers  |
| Airport operators \- Airports that seek to implement air taxis as a complementary transport or shuttle service. | Service providers |
| Airlines \- Air taxi airlines that define the routes for operation and provide air taxi service. | Service providers |
| ATC \- Interested in selling their service for ATC. May need a separate UAM traffic control department. | Service providers |
| Business travellers \- One of the core customers expected at the first phase of UAM development. | Customers |
| Tourists \- The next group of potential customers seeking leisure and entertainment in air transport. | Customers |
| Individual users and others \- The core focus group for an ideal UAM development model. In the best case, a huge part of the cities' population. | Customers |
| Aircraft manufacturers \- Working on air taxi prototypes to meet the market potential. | Suppliers  |
| Power supplier \- Interested in providing energy to power and charge electric vehicles and IT systems. Also, provide charging stations or batteries. | Suppliers  |
| Public \- Group of non-user that can limit air taxi service by raising concerns. | Non-users |
| Property owners \- Maybe not be involved in the aviation business, but can allow or limit the use of the property for landing. | Non-users |
| Special services \- Non-user that can restrict the operation, such as the military sector, hospital, school, etc. | Non-users |

3.1.1 DECEA \-  Is the regulatory authority for all Air Traffic Services, which includes monitoring flight information, alerting, air traffic advisory and air traffic control activities. Adheres to ICAO’s recommended standards and methods, subjected to restrictions or modifications relating to economic, regional or societal differences. Furthermore, it provides services related to air traffic management, air traffic control, air traffic flow management, aeronautical cartography, aeronautical telecommunications, air surveillance, aeronautical information, air navigation aids, flight inspections, search and rescue. In the UTM Context, DECEA provides a regulatory and operational framework, having access to data to guarantee regulatory compliance.

3.1.2 ANAC \- Responsible for civil aviation licensing, authorizations and concessions for airlines, air taxi companies, or specialized services (schools, workshop, civil aviation professionals, and aerodrome and airport operators), and for issuing licenses and technical qualifications for civil aviation professionals. ANAC was created to regulate and supervise civil aviation activities and aeronautical and airport infrastructure in Brazil, its actions fall within the scope of certification, oversight, standardization, and institutional representation activities.

3.1.3 Operators \- Person or entity responsible for operation management of UAS, complying with regulatory responsibilities, planning flights and operations, sharing operational intent information, and safely conducting operations using all available information.

3.1.4 Public Safety and General Public \- Public Safety entities, when authorized, are granted access to UTM operations data to ensure airspace and public safety, airport safety, critical infrastructure and general public privacy. The aforementioned data can be accessed through specialized platforms or directly transferred by USS. The general public can access any data that is publicly available.

## **3.x UTM Operational Principles**

### **3.x.1 Operators Responsibilities**

UAS operators operating outside the jurisdiction of traditional Air Traffic Control (ATC) separation services are mandated to participate in the UTM ecosystem. This engagement is regulated by a performance-based approach, where the scope and complexity of the required services are contingent upon the mission's operational profile, geographical location, and specific Communication, Navigation, and Surveillance (CNS) requirements. UTM system supports the management and safe conduct of operations in the following ways:

1) Issuance of operating authorization in accordance with the operational requirements of the intended airspace;  
2) Issuance of flight permission categories, with differences between controlled and uncontrolled airspace;  
3) Operational planning that supports the sharing of flight intentions;  
4) Airspace restrictions and dissemination of advisory information; and  
5) Conflict resolution capabilities.

### **3.x.1.1 BVLOS UAS Operators**

BVLOS operations are characterized by the absence of direct visual observation, necessitating a technological reliance on telemetry tracking, GNSS, and DAA capabilities.  In most cases, these technologies are able to satisfy CNS performance requirements, however,  are not able to handle the range of UAS operations occurring simultaneously, information exchanges with other operators and FAA and establishing flight priorities.  Consequently, the operational viability of BVLOS missions is contingent upon the integration of centralized UTM services. These services provide essential functions such as RID, strategic de-confliction through intent sharing, dynamic airspace authorization, and real-time situational awareness updates, including tactical alerts and contingency rerouting.

### **3.x.1.2 VLOS UAS Operators**

In contrast to BVLOS modalities, VLOS operations leverage the PIC capability to maintain safe separation through direct visual observation of the surrounding airspace. Consequently, the safety case for VLOS missions is not inherently predicated upon automated data exchanges with other UTM participants for tactical de-confliction.

Nonetheless, VLOS operators remain subject to stringent regulatory frameworks and must ensure compliance with fundamental mandates. These include systemic registration, the broadcasting of RID data, and the procurement Airspace Authorization when navigating within controlled airspace volumes. While participation in intent-sharing services may be voluntary for VLOS actors, it is often encouraged to further enhance the shared situational awareness of the integrated low-altitude environment.

VLOS UAS Operators may voluntarily use services not required of them, such as those applicable to BVLOS Operators. Use of such additional services enhances the situational awareness of the VLOS Operator, as well as that of other Operators and stakeholders within the system.

### **3.x.1.3 Manned Aircraft Operators**

While participation in the UTM framework remains discretionary for manned aircraft operators, their involvement is strategically encouraged to maximize the safety dividends derived from collaborative situational awareness. By bridging the gap between legacy ATM and emergent UTM services, manned operators contribute to a more comprehensive Common Operational Picture (COP), which is essential for mitigating the risk of mid-air incursions in shared low-altitude airspace.

The degree of integration for manned aircraft is categorized by the level of data interoperability:

* Passive Participation: This tier involves the unilateral consumption of data from the USS Network. In this mode, manned pilots utilize the reported flight intents of UAS operators to enhance their own situational awareness and trajectory planning, yet they do not broadcast their own operational intent to the UTM ecosystem.  
* Active Participation: This level establishes a bi-directional information exchange where manned operators broadcast their flight intent to UAS Remote Pilots-in-Command (RPICs) via the USS Network. Furthermore, active participants may voluntarily adopt secondary surveillance technologies—such as ADS-B or Remote ID (RID)—to increase their digital visibility, thereby fostering a transparent and cooperative environment for all airspace users.

### **3.x.2 Performance Authorization**

The operational integrity of the UTM ecosystem is underpinned by a performance-based framework, formalized through the issuance of Performance Authorizations. Given the inherent heterogeneity of UAS and their diverse mission profiles, CNS capabilities vary significantly across the fleet. Consequently, these authorizations move away from rigid, technology-specific mandates; instead, CNS performance requirements are derived from operator-specific safety cases or agilely determined by the service providers to support the specific operational needs of the airspace.

The USS acts as the primary entity responsible for managing this CNS variance, ensuring that safety and equity are upheld within the shared airspace. The USS must dynamically account for the disparate performance levels of participating aircraft to effectively deliver services such as strategic de-confliction and intent monitoring. By acting as a mediator of performance data, the USS ensures that the variance in vehicle capabilities does not compromise the collective safety architecture, allowing for a scalable and flexible integration of diverse aerial platforms.

To obtain a Performance Authorization, an Operator submits a Performance Authorization request to the regulatory entities for evaluation.  The Operator’s proposal demonstrates compliance of the overall system (inclusive of air/ground assets, USS/SDSP services, personnel, training, and procedures) and associated capabilities to applicable performance standards \- not to individual, equipment-specific requirements, such as the ability of the system to maintain the aircraft within a specified Operation Volume during flight.

The standards of the Performance Authorization can vary depending on the complexity of the proposed operation. For lower risk operations (e.g., VLOS, rural, low traffic density, and/or sparse population/property on the ground), Operators could self-declare compliance to standards \- and USSs could assist with formulating these declarations \- to ease direct FAA oversight. 

### **3.x.3 Strategic Management of Operations**

strategically managed through interactive planning and orchestration of intent information as well as relevant environmental considerations that enable strategic de-confliction for multiple UAS operations. Operation intent sharing, strategic de-confliction, airspace constraint evaluation, weather reporting and forecasting capabilities, and other key supporting features of UTM reduce the need for tactical separation management and reduce the likelihood of in-flight intent changes due to weather or airspace restrictions.

Intent data predominantly consists of the spatial and temporal elements of an operation. At a minimum, operation intent includes Operation Volume segments that make up the intended flight path. Operation Volumes are 4D blocks of airspace that have specified entry and exit times for the Operator’s UA. These volumes may be stacked in sequence such that one volume’s exit time coincides with the entry time of an adjacent volume along the flight path; the result is that each Operation Volume in the sequence comprises a segment of the overall flight profile.

Navigational performance requirements may be more stringent in certain airspace during periods when traffic density/operational tempo is high. USSs assist in managing and minimizing overlap of Operation Volume segments when necessary, with the goal of maintaining separation through strategic de-confliction.

intent data

- informs other operators of nearby operations to promote safety and shared awareness  
- enables de-confliction of operation volumes  
- supports conformance monitoring and tracking

intent information is made available to utm participants and other airspace users via the uss network to promote uss network to promote situational awareness and support cooperative interaction.

Real-time NAS airspace constraint data is available to the USS Network via FIMS to separate aircraft from flight restrictions, SAA/Special Use Airspace (SUA) activity, or other airspace management decisions that affect UTM operations.

USSs work with FAA, state, municipalities, and other entities as required to define airspace reservations (i.e. UVRs) in support of first responder activities. These are incorporated into the USS Network, and affected Operators are alerted to these areas during intent sharing processes.

USSs continue to monitor for, and notify Operators of, changes or conflicts leading up to and including flight that could affect the safety of the operation.

Strategic management services alone may be sufficient to ensure the safety of low risk, low complexity UAS operations. the low density of operations at these low altitudes, those who become aware of this operation via a USS, plan around that operation \- or when objectives result in a potential overlap, spatial or temporal adjustments are made to ensure strategic separation.

### **3.x.4 Separation Provision/Conflict Management**

The corresponding requirements for separation provision \- in terms of data exchange, tracking and conformance monitoring, equipage, and Operator responsibilities \- are commensurate with the risks to people and property. Aircraft/capability requirements are addressed in the Performance Authorization obtained by the Operator prior to the operation.

UAS Operators share separation responsibility with other UAS Operators (BVLOS and VLOS) and other airborne traffic. UAS Operators desiring to operate in areas with high density or heterogeneous traffic may be required to equip with DAA technologies to meet these responsibilities. Low altitude manned aircraft operating in both uncontrolled and controlled airspace have access to, and are encouraged to utilize UTM Operation Planning services to de-conflict their aerial work; low-altitude manned aircraft pilots share some responsibility with BVLOS UAS Operators for maintaining separation from each other (though they do not share responsibility for separation from VLOS UAS Operators). Because UAs can be difficult to identify when small in size, certain UAS may be required to comply with conspicuity requirements designed to increase visibility.

The Operator maintains a connection with the USS to support data exchange pertaining to aircraft tracking and monitoring, terrain and obstacle clearance data, weather, and/or notifications and advisories regarding airspace constraints, traffic, or other hazards that could affect the flight. In the case of a notification or advisory, the RPIC responsible for the overall safety of the flight acts accordingly.

USSs can further assist with in-flight separation responsibilities by providing services that assist Operators with staying within the bounds of their volume (e.g., aircraft tracking and conformance monitoring services), disseminating information that facilitates avoidance of flight hazards (e.g., weather/wind information, terrain and obstacle data, UREPs), and coordinating with affected airspace users to facilitate effective airspace management responses in the event of a contingency.

Though low altitude operating manned aircraft and VLOS unmanned aircraft are not required to share intent, they are encouraged to, at minimum, utilize UTM services that enable them to identify UAS operations that may affect their route of flight to increase the likelihood they identify UAS.

UTM BVLOS Operators must be capable of tracking their vehicle and remaining within the bounds of their shared intent volumes. USSs can assist Operators in meeting this requirement through vehicle tracking and conformance monitoring services whereby UAS transmit near-real time tracking data to the USS, so the USS can provide services that enable Operators to monitor the UA’s position and conformance to applicable system-based Operation Volume boundaries during BVLOS portions of flight. USSs may also use conformance monitoring to track Operator conformance to the geographical boundaries specified in the Performance Authorization.

If impacted by a UVR, Operators/RPICs exercise discretion when deciding to take action, understanding they are responsible for the overall safety of the flight. The Operator/RPIC can (1) proceed with the operation if confident it is safe to continue (e.g., has onboard detection and/or V2V capabilities), (2) avoid or exit the airspace, or (3) land.

Contingency Management

(1) experiencing a critical on-board equipment failure or degradation (e.g., lost link, engine failure), (2) not tracking, or vehicle position is unknown for some period of time, or (3) not conforming to flight intent and/or conformance is not expected to be restored, USS-assisted response protocols are in place to support the Operator/RPIC in mitigating potential for damage or injury.

Vehicle capabilities also support notification to impacted airspace users during contingencies. If a UA is equipped with V2V communication capability (e.g., V2V broadcast capability), it broadcasts relevant information (e.g., position) to nearby vehicles with cooperative equipment, allowing for affected stakeholders (e.g., nearby Operators in four dimensional proximity to the compromised UA) to gain awareness of the situation and respond accordingly.

## **3.x UAM Operational Principles**

Any aircraft operating within a designated UAM Corridor must strictly adhere to the performance and participation requirements defined for the UAM environment. Within these corridors, the responsibility for deconfliction is strategically delegated by ATC to UAM Operators or the PIC, ensuring tactical agility in high-density areas. To maintain systemic safety and predictability, the UAM community is responsible for the collaborative development of Community Operating Protocols (COPs), which serve as the standardized operational benchmarks for all participants within the ecosystem.

As the UAM environment covers a relatively small area compared to the ATM system, these new operations can strategically serve as proof of concept, or anticipation, for the application of other concepts such as TBO, FF-ICE, and 4DT.

The segregation or exclusive use of corridors or areas reserved for eVTOLs can be less efficient in relation to other traffic in more congested areas. A possible solution encountered to prevent this is to integrate airspace flights, sharing the use of airspace volumes with other fixed-wing aircrafts, helicopters, and unmanned aircraft, provided that the performance and capacity requirements defined for each type of airspace are met. To enable the integration of eVTOL aircraft into the airspace without segregation, digital technologies and information should be used to assist in providing separation between aircraft.

UAM Service Providers are responsible for sharing information during aircraft operations with air operators. The central system of shared information and communication can be managed by regulatory agencies or another institution designated by it. 

Moreover, the Providers can offer services of flight intent management, operation information sharing, traffic deconfliction, vertiport slot management, demand-capacity balancing, flow control, compliance monitoring, coordination of access to airports, vertiports, meteorological services, cartographic services, aeronautical information.

Operators, supported by digital information, may adopt cooperative separation practices to ensure flight path safety, replacing visual procedures based exclusively on natural vision or the provision of separation services by ATC.

In the UAM environment, no standardized minimum or maximum altitude will be established to be applied identically throughout Brazilian airspace. Instead, there will be flexibility considering the following parameters:

I \- the minimum altitude will be established considering the volume above the UTM airspace (if any);

II \- the maximum altitude will also be established flexibly according to the trajectories belonging to the existing traditional IFR air traffic (SID, STAR, IAC, AWY, etc.); and

III \- in horizontal terms, limits (Geofence) will be established defining the areas of application of the UAM concept and, depending on the case, other airspace structures (REA, REH, EAC, etc.) may constitute lateral limits.

# **4**     **Existing Systems and Operations** 

*This OCD section describes the system(s) currently being used for the operations described in the OCD, and the nature of the operations being conducted. This section is only relevant where the capability has previously been provided by an existing system (or systems), and where discussion of that system is useful in understanding the capability. Note that the existing operations may be manual or include manual process components. The information provided, including the level of detail, should be constrained to what is useful in understanding the future operations.* 

*The structure of Section A.5 should be used as an indication of the structure and content for this OCD section. Appropriate information may include for example:* 

·       *operational overview, including the operational environment;* 

·       *personnel;* 

·       *system overview; and* 

·       *support environment.* 

## **4.x**    **ATM System**

### **4.x.1    Organizational Structure** 

### 

![][image5]

(Explicar elementos da DCA-351-7)

The organization of Brazilian airspace, based mainly on a structure of fixed routes, will evolve progressively, depending on the volume and complexity of traffic, towards a mixed solution, with the implementation of direct, flexible, or free routes through Free Route Operations (FRTO). 

Innovative techniques should be sought to leverage the organization and capacity of airspace, even if they are for isolated applications in certain regions or terminals, such as Point Merge or Climb Vectoring Area (AVS) approaches.

### **4.x.1.1**    **AOM \- Airspace Organization Management**

Airspace Management is the process by which the various options available in the airspace will be selected and applied, aiming at the needs of the ATM Community. The Airspace Management will be dynamic and flexible, leaving the management of UAM and UTM environments may be delegated to operators, under the supervision of DECEA.

Restrictions on the use of any volume of airspace will be considered temporary. Restrictions on user operations will be imposed only when necessary for operational safety or efficiency, or when there is a specific national interest.

the use of airspace shall always be based on the principles of equity among all users; and

airspace shall be organized and managed in such a way as to accommodate all current and future uses, including unmanned aerial vehicles and space vehicles in transit, among others.

The optimal, balanced, and equitable use of airspace between civil and military users, including unmanned aircraft operators, shall be facilitated by strategic coordination and dynamic interaction between them and the Air Navigation Management Center (CGNA), allowing for the establishment of optimal flight paths, increasing efficiency, and reducing operating costs.

Tools and processes shall be implemented to determine the forecast air traffic demand in order to provide information for the strategic planning of Airspace Organization and, as a consequence, for the definition of air navigation infrastructure and human resource needs.

The establishment of Controlled Airspace (EAC) should be avoided, especially those of a permanent nature or of fixed dimensions, even if activated on a temporary basis, given that the reservation of airspace should be proportional to the specific type of operation intended by the user.

The CGNA shall be responsible for coordinating the use of the already structured airspace in a dynamic manner, making allocations based on the specific needs presented by its various users. This flexible use of airspace will require the implementation of air operations coordination procedures.

### **4.x.1.2**    **DCB \- Demand Capacity Balancing** 

The balance between demand and capacity will enable a strategic assessment of traffic flows and existing capacities to allow users to determine when, where, and how to operate, mitigating conflicting needs for airspace and airport capacity. This collaborative process will enable efficient management of air traffic flow.

Under normal operating conditions, the Brazilian ATM System shall have sufficient capacity to meet normal or seasonal air traffic demand at its optimal flight profiles, contributing to the fulfillment of scheduled landing and takeoff times. Thus, the ATM-related air navigation infrastructure (CNS, MET, AIS, and Automation) and associated human resources shall be made available, qualitatively and quantitatively, for the proper operation of the System.

In the event of unexpected events that lead to a degradation of capacity (e.g., meteorological phenomena, inoperability of air navigation or airport facilities, and unexpected demands), appropriate Flow and Capacity Management measures will be applied, planned for each affected aircraft, with due measurement of the impact. Such measures will allow a balance between demand and capacity, avoiding overload and providing the necessary conditions for the use of maximum available capacity.

The centralized processing of information related to Flight Plans should evolve, allowing for the necessary adjustments to be made in terms of routes and schedules, through the establishment of effective communication between aircraft operators, ATS agencies, and the CGNA, as well as the evolution towards the FF-ICE concept.

FF-ICE era flight plans and the sharing of related information will be built on the seven components of the ATM System and paved by the principles established in GATMOC. Given its scalable nature, FF-ICE will be the mechanism on which global aviation will depend for gate-to-gate planning, paving the way and being one of the main enablers for operationalizing TBOs.

The improvement of Flow and Capacity Management will provide the following conditions for safe, orderly, and expeditious air traffic:

I \- maintenance of demand within installed capacity;

II \- reduction of operating costs caused by capacity constraints in air traffic control and airport infrastructure; and

III \- improvement of the capacity of the ATM System, based on obtaining indicators for the improvement of airport infrastructure and Air Traffic Control (ATC).

Airspace capacity is directly related to airport capacity; therefore, in order for airspace to exploit its capacity to the fullest, it is important to increase runway capacity.

For the correct application of Flow Management measures and adaptation of ATM System capacity, recommended capacities shall be established for each control sector and airport, based on the implementation of optimization measures, such as:

I \- implementation of air traffic procedures that make maximum use of the available airport infrastructure, including parallel approaches under Visual Meteorological Conditions (VMC), successive or dependent parallel takeoffs, Reduced Runway Separation Minimums (RRSM), High Intensity Runway Operations (HIRO), and the implementation of tools for Arrival and Departure Management (AMAN and DMAN);

II \- reduction of runway occupancy time through the implementation of rapid exits and procedures applicable to pilots; and

III \- implementation of taxiways to reduce ground transit time, construction of new runways, etc.

The implementation of DCB measures will be based on the Collaborative Decision Making (CDM) process, applied at the strategic, pre-tactical, and tactical levels.

### **4.x.1.3**    **AO \- Aerodrome Operations**

Flow and Capacity Management depends on the efficiency of airport management, particularly in the movement area, given that any increase in air traffic demand must be absorbed by airports.

As an integral part of the ATM System, national airport operators must provide the necessary infrastructure to meet the expected operations, maximizing aerodrome capacity in all weather conditions and improving safety levels.

Aerodrome operators shall consider, in an integrated manner, the departure, en route, and arrival phases, together with ground operations, when determining their role within the ATM System. The main challenge to be faced by airport operators will be to provide sufficient capacity, while the challenge for the ATM System will be to ensure that all available capacity is used safely and efficiently. With regard to the optimized operation of aerodromes, the following principles shall be observed in the planning of the national ATM System:

I \- runway occupancy time shall be reduced without compromising safety, taking into account the different operational capacities of users;

II \- regardless of weather conditions, it shall be ensured that maneuvers on the surface of aerodromes are carried out safely, maintaining capacity unchanged; and

III \- all activities carried out in the movement area of aerodromes shall have direct effects on ATM.

Airport infrastructure planning shall consider the use of simulation tools to ensure operational efficiency. Joint simulations for airports and airspace shall be applied whenever economically feasible, as this is the most effective way to obtain a complete picture of operations. To this end, there shall be the necessary cooperation between the members of the ATM Community involved.

The improvement of operational performance and the expansion of accessibility to aerodromes throughout the country, including the promotion of services in locations currently lacking ATS, will be made possible by the adoption of digital tools, including the remote provision of Air Traffic Services, specifically with Digital Aerodrome Control Towers (D-TWR) and Remote Aerodrome Flight Information Services (R-AFIS).

Such solutions will not only allow operational coverage to be extended to low- and medium-traffic aerodromes, but will also bring benefits in terms of safety and operational efficiency. In addition, benefits are also expected in terms of the optimized use of air navigation service infrastructure and the efficient management of human and financial resources.

In this sense, the use of D-TWR will allow for more efficient and flexible use of resources, substantially improving the efficiency and cost-effectiveness of service provision. As a result, PSNAs will have modular and scalable systems at their disposal that will enable easier updating, improved interoperability, and the ability to adapt to unexpected traffic developments, such as slowdowns in demand or rapid returns to growth.

The ability to provide ATS remotely is relevant in all operating environments: aerodromes, terminal control areas, and en route. In airport environments, the D-TWR concept supports multiple usage scenarios, allowing ATS to be provided from a Remote Tower Center, with the dynamic allocation of a series of physical aerodromes to remote modules. In addition, it is feasible to integrate approach services to these airports through a remote virtual center, increasing flexibility and operational efficiency.

Future possibilities for the use of remote solutions for the provision of ATS at aerodromes include:

I \- “Simple” Mode of Operation: remote provision of ATS for a single aerodrome from a single D-TWR or R-AFIS module;

II \- “Multiple” Mode of Operation: remote provision of ATS to two or more aerodromes simultaneously from a single D-TWR or R-AFIS module; and

III \- Remote Center: a concept that covers the remote provision of ATS in “Simple” or “Multiple” mode from a facility that concentrates two or more D-TWR or R-AFIS modules, allowing for the sharing of infrastructure in an economical and integrated manner.

### **4.x.1.4**    **TS \- Traffic Synchronization**

TS uses integrated and automated assistance means, both on the ground and on board, for the management of surface movements, departure, route, and arrival, aiming to ensure an optimal traffic flow, gate-to-gate. This component is directly related to DCB and CM and constitutes a flexible mechanism for capacity management, allowing for a reduction in traffic density and adjustment of infrastructure in response to variations in demand. Its objective is to eliminate congestion points and, in summary, optimize traffic sequencing to make the most of runway capacity.

The principles of Traffic Synchronization that will be considered in the Brazilian ATM System include:

I \- the ability to modify sequences, tactically and collaboratively, to optimize aerodrome operations, considering gate management and/or airspace user operations, as well as their different operational capacities;

II \- the evolution to four-dimensional (4D) control, in which the flight receives a time profile to be followed to optimize flow;

III \- the delegation to the pilot in command of maintaining spacing between aircraft, aiming to increase traffic flow and, at the same time, reduce the workload on the ground; and

IV \- the spacing and dynamic sequencing of aircraft on arrival and departure, knowing the restrictions determined by wake turbulence and relevant flight parameters.

In the departure phase, TS will involve integrating departing aircraft into the en route traffic environment. The improvement of departure flows will be achieved through tools that support more efficient surface operations and provide better real-time assessment of departure and en route traffic activity.

In the en route phase, TS will involve the sequencing, integration, and spacing of traffic flows to reduce dependence on tactical conflict management. Improved flow sequencing will be achieved through techniques and tools that provide the most efficient prediction of demand and capacity at crossing points, the best real-time assessment of traffic activity in departure/arrival airspace, greater use of onboard equipment capable of maintaining spacing, and expanded use of dynamic routes based on advanced navigation capabilities.

Arrival operations will also benefit from these tools. However, the main task at this stage will be to plan and obtain the optimal spacing and sequencing of the arrival flow. The runway designation, which provides the basis for this activity, will be made as early as possible. The user's preferred runway indication will be available in the ATM environment information tool. To facilitate optimal runway assignment, decision support solutions will be used for departures and arrivals, as well as integrated surface movement management tools.

In the final part of the arrival phase, decision support tools will use time to optimize flight sequencing, maximizing airspace and airport capacity. Other tools will facilitate final approach interception maneuvers in accordance with the planned traffic sequence.

Still with the aim of optimizing traffic sequencing, making the most of runway capacity, studies by the ICAO, supported by work by the European Aviation Safety Agency (EASA) and the Federal Aviation Administration (FAA) of the United States of America, regarding the alternative application at busy aerodromes of a new turbulence wake categorization covering seven groups (from A to G), allowing for a reduction in the separation between aircraft during approach and departure phases.

At all stages, the service provider may delegate to the pilot the responsibility for maintaining spacing or for reaching a point or points in space at specific times, with a view to maintaining the necessary sequence and desired traffic flow.

In the case of unmanned aircraft, the delegation of separation will depend on technological solutions that allow the remote pilot to comply with the Rules of the Air.

### **4.x.1.5**    **CM- Conflict Management**

This component arises to provide an extension of the concept of ATC separation. From this perspective, separation will be performed and considered not only between aircraft, but also between potential risks, such as terrain, weather formations, EAC, ATFM restrictions, etc.

The need for airspace users to achieve maximum efficiency for their flights is a high priority, whether in terms of time to arrival or more economical operation. Tactical changes in flight path to ensure separation between the aircraft and hazards or to wait for access to an available ATM resource will have a significant impact on flight efficiency. Thus, the desired goal of the ATM System is the establishment of negotiated 4D trajectories that do not require tactical intervention. However, it is recognized that certain inaccuracies in the available information and unforeseen or uncontrollable changes will still require tactical modifications to flight profiles. Thus, the ATM System must contain an element of tactical intervention that will be employed as an alternative solution to some ATM issues.

Conflict is any situation involving aircraft and hazards in which the applicable minimum separation may be compromised. The purpose of CM is to limit the risk of collision between an aircraft and a hazard to an acceptable level.

CM can be applied at any point along an aircraft's future trajectory, from initial flight planning or itinerary preparation to real-time flight execution. Thus, the component is applied in layers, comprising: strategic conflict management, separation provision, and collision prevention.

Strategic conflict management is the first layer and is achieved through the components of Airspace Organization and Management, Demand and Capacity Balancing, and Traffic Synchronization. Strategic conflict management measures reduce the need for the second layer, separation provision, to an appropriate level. In strategic conflict management, a conflict occurs whenever there is competing demand for the same resources from the departure gate to the arrival gate.

Separation provision is the tactical process of keeping aircraft away from hazards, ensuring at least the appropriate minimum separation. This layer will only be used when strategic management cannot be used efficiently.

Collision avoidance is the third layer of conflict management and should be activated when separation mode has been compromised. Collision avoidance (anti-collision) is not part of the separation provision layer. Collision avoidance systems are not used to determine the calculated level of operational safety required for separation provision. The collision prevention functions and the applicable separation mode, although independent, must be compatible.

### **4.x.1.6**    **AUO \- Airspace User Operations**

This component refers to the ATM aspects of flight operations and serves to indicate the importance of the participation of all users in the integration of ATM components, as the information provided by them will be an essential element for the development and operationalization of AOM, DCB, AO, and TS.

The AUO component was established to indicate that all airspace users should be considered in the ATM System, including unmanned aircraft operations. Within the national airspace, these must comply with the rules established or to be established for this purpose.

Unmanned Aircraft comprise a broad spectrum, ranging from freely flying weather balloons to complex aircraft programmed to be fully autonomous or remotely piloted by trained professionals. The latter type of unmanned aircraft is part of a subcategory known as Remotely Piloted Aircraft (RPA) and operates as part of the Remotely Piloted Aircraft System (RPAS).

According to Annex 2 of the ICAO “Rules of the Air,” RPAS consists of a remotely piloted aircraft, its associated remote piloting station(s), command and control links, and any other components, as specified in the type design.

RPAs are considered a subset of Unmanned Aircraft (UA) and must be capable of complying with applicable normal and emergency procedures, as well as airspace requirements defined by the State. RPAs will be subject to integration into the ATM environment, as established in the GANP.

The use of UAs has social, economic, and environmental impacts and, in this context, States have faced major challenges in safely and efficiently integrating this new technology into a highly regulated environment with more than seven decades of history.

Due to the absence of technological solutions that guarantee the remote pilot's faithful compliance with the Rules of the Air, it is expected that unmanned aircraft operations will be carried out through the accommodation of this technology.

With technological advances and the establishment of a robust regulatory framework, RPAS is expected to be fully integrated in the medium term, allowing for the scalable and safe exploitation of this segment, considered by ICAO as the new era of aviation.

The Brazilian ATM System will adapt to the various types of operations carried out by airspace users, including those using UAS, the most likely being:

I \- air transport;

II \- military operations;

III \- executive aircraft operations;

IV \- specialized air services (aerial surveying, aerial agriculture, among others);

V \- recreational flights; and

VI \- space operations in transition.

In order to accommodate the various capabilities of UAS, the ATM environment may require changes to its infrastructure, procedures, and regulations. The challenge is to integrate Unmanned Aircraft with diverse capabilities into the current airspace structure without compromising the safety of other users, people, and property on the ground.

Operations will be differentiated according to their planning, from those scheduled well in advance to those scheduled shortly before execution.

The main conceptual changes include:

I \- interoperability between ATM, UAM, and UTM environments;

II \- the need to accommodate mixed capabilities and global implementation will be considered to increase safety and efficiency;

III \- relevant ATM data will be merged to increase the overall situational, tactical, and strategic awareness of airspace users, as well as for conflict management;

IV \- relevant operational information from airspace users will be available;

V \- the availability of individual aircraft performance, flight conditions, and ATM resources will enable the planning of dynamically optimized 4D trajectories; and

VI \- the collaborative decision-making process will ensure that aircraft and user system designs that impact ATM are considered in a timely manner.

### **4.x.1.7**    **ATM SDM \- ATM Service Delivery Management**

This component has been created to enable the evolution of the process of requesting and providing Air Traffic Services. ATM SDM will operate within a gate-to-gate vision, covering all phases of flight with the participation of all providers, without any noticeable boundaries between them. The component suggests that the request for services will correspond to the provision of a service based on the components previously presented. To make this possible, solutions will be made available that enable interaction between the user and the ATM provider, allowing for the establishment of an “agreement” between them, through collaborative decisions, enabling the flight to be as close to ideal as possible.

It is important to note that, after the agreement between the user and the ATM service provider has been established, it will still be necessary to formalize the air traffic authorization, which must be complete and include all phases of the gate-to-gate flight.

ATM SDM will be responsible for ensuring that flights use the runway according to the schedule set out in the takeoff slot (where applicable) and for integrating these movements with all other departing and arriving flights, ensuring safety and optimizing the use of aerodrome movement areas. The SDM ATM will ensure that service providers have real-time access to data on departure and arrival forecasts, runway use, airport congestion, parking locations, and environmental considerations, with a view to reducing inefficiencies in aircraft and vehicle movement.

In the en route phase, ATM SDM will be involved in correlating ATM capacities with respective demands.

During the flight, from the start of scheduling or planning, through its actual operation, and until arrival at the parking location, ATM SDM will consider the objectives for each flight in the course of gate-to-gate operations. The degree to which these objectives are evident during a flight and the necessary interaction is a function of both traffic volume and flight duration.

O que existe hoje é essa DCA que regula o trafego aéreo “normal”.

## **4.x**    **UTM Tests**

### **4.x.1    FAA** 

Main Objectives (Principais Objetivos)

The UFT project was established to continue the collaboration between the FAA, NASA, and industry to mature UTM concepts and standards. Its primary goals were:

Advance Standards: Develop and field test capabilities proposed by current industry standards, specifically focusing on strategic coordination in complex environments.

Enhance Functionality: Test improvements to UTM services, such as data correlation between broadcast Remote ID and FAA-held registration data.

Secure Information Exchange: Develop and evaluate updated security management, including message signing and Identity Access Management (IAM), for data exchanges between the FAA, industry, and authorized entities.

Explore Future Concepts: Evaluate new elements like authorized historical data queries, which allow the FAA to access USS-held operational data on demand.

Inform Policy: Provide observations and data to support the development of future policies and best practices for routine, scalable UTM operations.

Studied Scenarios 

The testing was executed at two primary FAA UAS test sites, each evaluating different use cases:

New York UAS Test Site (NYUASTS):

Strategic Deconfliction: Demonstrated submission of operational intent, constraint management, and conflict detection.

Dynamic Replanning: Focused on deconfliction without priority and in-route rerouting based on updated situational data.

Operational Complexity: Tested high-density operations in a Class D airspace environment at Griffiss International Airport.

Mid-Atlantic Aviation Partnership (MAAP):

Mixed Operations in Complex Environments: Evaluated how standards support a variety of UAS platforms operating simultaneously.

Public Safety Operations: Tested the use of higher-priority operations (e.g., emergency response) and how they impact lower-priority traffic.

Public Safety Queries: Focused on data correlation and historical queries initiated by law enforcement/security personnel due to concerns about UAS activities.

3\. Results Obtained (Resultados Obtidos)

The UFT project validated that current industry standards are effective but identified areas for further maturation:

Increased Situational Awareness: The sharing of operational intent between USSs allowed most operations to be accepted on the first attempt, improving an operator's ability to plan and replan flights safely.

Validated Strategic Deconfliction: The ASTM standard was confirmed as a viable framework for managing conflicts among multiple USSs and operators in a federated system.

Effective Data Correlation: The prototype for correlating Remote ID data with registration databases was successful, showing a significant decrease in error rates (from 56% to 4%) as the implementations matured during the test phases.

Security Success: UFT partners successfully implemented message signing and OAuth 2.0 authorization, ensuring that over 99.9% of messages validated correctly by the end of the project.

Automation Utility: The use of an automated test harness (InterUSS) proved effective for verifying USS functionality and streamlining the checkout process for new participants.

Performance Gaps: Testing identified that further work is needed in "availability arbitration" and "aggregated intent conformance monitoring" to meet high-density operational needs.

**4.x.2  BR-UTM**

### **4.x.2.1** BR-UTM First Operational Evaluation

### The first field test was conducted in April 2024, in the city of São Carlos, São Paulo, where the basic functionalities of coordination between drone traffic service providers were validated. 

### The BR-UTM Field Test 1 successfully validated the foundational capabilities of the Discovery and Synchronization Service (DSS), based on the InterUSS platform. Participants demonstrated the ability to perform basic strategic deconfliction of Operational Intent References (OIRs) and deconfliction from static Constraints.

### **4.x.2.2** BR-UTM Second Operational Evaluation

### This Second Field Test will expand upon that foundation, introducing critical new capabilities to validate the complete, end-to-end operational lifecycle. The vision is to simulate a real-world operational environment where multiple UAS Service Suppliers (USS) coordinate flights, and operators conduct live drone operations based on these coordinated intents.

### Participants can choose to act in one or both of the following roles:

### USS Provider: An entity running a software implementation that provides UAS services.

### Responsibilities:

* ### Implement the full API contract.

* ### Integrate with the authentication service.

* ### Connect to the central DSS to discover other operations and publish their own.

* ### Manage the full lifecycle of OIRs on behalf of their operator clients.

* ### Coordinate directly with other USSs for strategic deconfliction.

* ### Provide an endpoint for other USSs to subscribe to updates for OIRs they manage.

### Drone Operator: An entity that plans and executes drone flights.

### Responsibilities:

- ### Partner with a registered USS Provider for flight planning.

- ### Conduct pre-flight checks.

- ### Execute the flight mission precisely according to the activated OIR (trajectory, altitude, and time).

- ### Equip the drone with the necessary hardware for Remote ID broadcast.

- ### Maintain communication with the USS during flight and be prepared to act on in-flight instructions, including immediate termination of the operation.

### **Test Scenarios**

### The field test will be structured around a series of progressively complex scenarios.

### **Scenario 1: Nominal Coordination and Flight Activation**

### **Objective:** Validate the basic workflow, authentication, and OIR activation.

### **Execution:**

* ### Two or more USS providers will each create a distinct, non-conflicting OIR in the DSS.

* ### Just prior to the scheduled flight time, each USS will update their OIR state to Accepted and then Activated. They must notify any subscribers of this change.

* ### The corresponding Drone Operator will execute the flight.

* ### During the flight, the drone will broadcast Remote ID data.

* ### Upon completion, the USS will update the OIR state to Ended.

### **Scenario 2: Strategic Deconfliction with a Constraint**

### **Objective:** Validate conflict detection and resolution against a static geographical constraint.

### **Execution:**

* ### The DSS will be pre-populated with a Constraint (e.g., a no-fly zone).

* ### A USS will attempt to create an OIR that partially overlaps with the constraint. 

* ### The USS must identify the conflict by querying the DSS.

* ### The USS must then modify the OIR's geometry to remove the conflict before it can be successfully created and activated.

* ### The Operator will fly the deconflicted mission.

### **Scenario 3: Inter-USS Deconfliction & Negotiation**

### **Objective:** Validate peer-to-peer coordination to resolve a conflict between two OIRs.

### **Execution:**

* ### USS-A creates and submits a valid OIR to the DSS.

* ### USS-B attempts to create an OIR whose 4D volume overlaps with USS-A's OIR.

* ### USS-B's initial attempt to create the OIR in the DSS should fail due to the conflict.

* ### USS-B must query the DSS, identify the conflicting OIR from USS-A, and initiate a strategic negotiation (as defined by the ASTM standard, though this may be a manual coordination step for the test).

* ### One or both USSs will adjust their OIRs to resolve the conflict.

* ### Once resolved, both OIRs can be created and subsequently activated for flight.

### **Scenario 4: Priority Operation (Pre-Flight)**

### **Objective:** Validate the system's response to a high-priority flight identified during the planning phase.

### **Execution:**

* ### Multiple "standard" priority OIRs are planned or active in the DSS.

* ### A designated USS (the "Emergency Services USS") will introduce a new OIR with priority set higher than the others (e.g., for a simulated medical delivery or security overwatch). This OIR will overlap with existing standard operations.

* ### Other USSs must detect this high-priority OIR and are required to modify or cancel their own conflicting operations to clear the area.

* ### The high-priority flight is then activated and flown.

### **Scenario 5: In-Flight Contingency \- Dynamic Constraint**

### **Objective:** Validate a USS's ability to monitor for new conflicts during an active flight and instruct the operator to take immediate, appropriate action.

### **Execution:**

* ### USS-A has an OIR in the Activated state, and its Operator is conducting the flight.

* ### An "Emergency Services USS" creates a new, high-priority Constraint or OIR that dynamically appears and conflicts with USS-A's active flight volume.

* ### USS-A must detect this new, superseding conflict in near real-time by monitoring the DSS or receiving a notification from a subscription.

* ### Upon detecting the unmitigable conflict, USS-A must immediately relay a command to its Drone Operator to cease the operation.

* ### The Operator must comply with the instruction and safely terminate the flight (e.g., land immediately or execute a pre-planned return-to-launch maneuver).

* ### USS-A updates its OIR state to Ended to reflect the early termination of the flight.

 validation of the end-to-end operational lifecycle in Field Test 2

### **4.x.2.3** BR-UTM Third Operational Evaluation

objective \- validate contingency procedures, dynamic restrictions integration and evaluate the providers reaction to simulated events.

operational tests

check-in/ check-out \- standardize process

alerts and flight geography \- Automatic notification when leaving the flight area (evaluate use of Remote ID).

Identification of drones with Remote ID entering the area.  
Operational response from the provider in these situations.  
Dynamic Restrictions  
Creation of partial restriction with active OIR → possible actions:  
Leave the area, cancel flight, or react in a timely manner.  
Helicopter landing simulation → automatic temporary restriction.  
Evaluate providers' reaction time (timing) to act after an emergency.  
Operating Conditions  
Prohibit landing at the same takeoff point in case of restriction.  
Test Geo Fence → verify that providers comply with restrictions and that all OIRs are within the UTM Zone.  
Assess response to flights outside the UTM Zone.  
If drone leaves OIR → verify that provider creates new OIR or declares contingency.  
Extra Features to Test  
Define a list of standard procedures when ending an operation for different types of restrictions (do not just assume “Return to Home”).  
Test non-nominal volumes:  
How providers handle their creation and management.  
\[NOT PRIORITIZED\] \- Inclusion of details in restrictions (degree of severity, mandatory actions, permitted safe maneuvers).  
BRAC Requirements  
Flight in non-nominal volume is not permitted.  
If the drone leaves the OIR, the possible area must be calculated and a non-nominal volume automatically created.  
General Observations  
Need for more organic testing (“fly and I will evaluate the requirements”).  
Focus on real-time observation of providers’ reactions.

1\. Introduction & Vision

Third Field Test will shift focus to real-time contingency management and provider responsiveness. The vision is to move beyond pre-planned scenarios and evaluate how USS platforms and operators react to dynamic, unexpected events in a more organic operational environment.

This test aims on validation of advanced contingency procedures, the integration of dynamic constraints on active flights, and the automated handling of in-flight deviations.

1.1. New Features for Validation

This test will validate all previously tested features, with a specific focus on the following new capabilities:

Dynamic Constraint Integration: The ability for the system and participants to manage airspace restrictions that are created or modified after a flight has been activated.

Geo-Fencing and Automated Alerts: Real-time detection and notification of deviations from the approved 4D operational volume (OIR).

Non-Nominal Volume Management: The automated creation and management of non-nominal volumes in response to an in-flight deviation, as per BRAC requirements.

Provider Reaction Time: Measurement and evaluation of the time taken for a USS to detect a conflict or deviation, process it, and deliver actionable instructions to the operator.

**Core Objectives**

The primary goals of this field test are to:

* Validate Real-Time Contingency Response: Demonstrate that USSs can detect dynamic constraints affecting an active flight and guide the operator through appropriate, timely mitigation measures.  
* Test Geo-Fence Compliance and Deviation Handling: Verify that USSs can automatically detect when a drone exits its authorized OIR and trigger the appropriate operational response (e.g., alerts, a contingency declaration, or the creation of a non-nominal volume).  
* Evaluate Non-Nominal Volume Procedures: Ensure that in case of a deviation, USSs correctly calculate and create a non-nominal volume, and that flights cannot be activated within one.  
* Measure USS Performance: Quantitatively measure the reaction time of USS providers in responding to simulated emergencies and dynamic changes in the airspace.  
* Standardize Contingency Maneuvers: Test the implementation of specific, pre-defined contingency procedures beyond the default "Return to Home," based on information provided in dynamic constraints.

**Test Scenarios**

The field test will focus on dynamic scenarios designed to assess real-time decision-making and system responsiveness.

**Scenario 1: Dynamic Constraint on an Active Flight**

**Objective**: To validate the USS's ability to manage a new constraint that appears during flight and measure its reaction time.

**Execution**:

* A USS activates an OIR, and the corresponding drone begins its mission.  
* A test coordinator creates a new, high-priority Constraint that partially overlaps the active OIR (e.g., simulating a helicopter landing zone). The constraint will contain detailed instructions.  
* The USS must detect the conflict in near real-time. The time from constraint publication to USS action will be measured.  
* The USS must instruct its operator to take appropriate action based on its safety procedures (e.g., immediately exit the restricted area, hold position, or land at an alternate location).

**Scenario 2: OIR Deviation and Non-Nominal Volume Creation**

**Objective**: To validate the automated response to a drone breaching its approved flight geometry (Geo-Fence).

**Execution**:

* A drone is operating under a valid, Activated OIR.  
* The operator intentionally flies the drone outside the lateral and/or vertical boundaries of the OIR.  
* The managing USS must automatically detect the deviation via Remote ID data or other tracking means.  
* The USS must issue an immediate alert to the operator.  
* Per BRAC requirements, the USS must then calculate the potential flight area and automatically create a non-nominal volume in the DSS to represent the contingency.

**Scenario 3: Response to Flight Outside UTM Zone**

**Objective**: To evaluate the system's response to an operation that deviates outside the designated UTM test zone.

**Execution**:

* An operator flies a drone near the boundary of the defined UTM Zone.  
* The drone then proceeds to fly outside this zone.  
* The managing USS and the overall system must detect this breach and initiate the appropriate alert and contingency procedures.

**Scenario 4: Standardized Check-in / Check-out**

**Objective**: To validate a formal, standardized electronic procedure for flight check-in and check-out.

**Execution**:

* Before activating an OIR, a USS must perform a formal "check-in" using a defined digital process. Informal communications (phone, etc.) are not permitted.  
* Upon normal completion or early termination of the flight, the USS must perform a formal "check-out" to close the operation.

 The trial was conducted with three active UTM service providers, in scenarios proposed by the providers themselves and according to their respective capabilities. In addition, the first experiment was conducted by a supplementary service provider, focusing on surveillance through integration with a drone detection system.  
On December 17, a Proof of Concept (POC) was conducted, demonstrating operational advances.

Measures of Effectiveness

| \# | Name | Reason | Definition | Measurement | Example | Rationale |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |

# **5     Proposed System Operational Overview** 

*This OCD section provides an overview of the operations and operational context of the proposed system, supporting the description of the operations in Section A.7. The operational overview is provided from the users’ perspective(s) and within the system operational environment. The system operational environment is that environment in which the user performs his tasks, and is the subject of this section of the OpsCon. The information in this section of the OpsCon provides a static description of the relationship of the system with the environment.* 

*This section summarizes, in a prose style with graphics, information regarding the mission of the system, its operational environment, and a characterization of the personnel. Where an OCD is influenced by other operational information, such as other OCDs, ConOps documents, doctrine and/or procedures, that information should be referenced here. In some cases, particularly where the OCD is part of a hierarchy of operational documents, traceability should be provided to higher level documents.* 

The OCD proposes a baseline for future integration of non-segregated airspace, dissecting UTM and UAM state of the art regulatory and technological states. 

## **5.1    Missions**

*This OCD subsection should describe the applicable primary and secondary mission(s) that the system will address. It should state the overall purpose and intent of operations and should describe, if applicable, potential risks and issues, for example associated with geography or location of operations, strategies used to accomplish the mission, and specific tactics, methods or techniques employed to accomplish the mission. Where there are multiple missions, these should be prioritized where possible.* 

*This section should describe “what” the system is intended to do, and, to some extent, “how” and “when” it is expected to do it. It is important to explain key operational terms and operational jargon in a language that will be clearly understood by a wider audience.* 

*→ falar q ao invés de ser dois sistemas de controle de tráfego, é apenas 1 que integra UTM+AAM.* 

*→ falar novamente q a função deles é para a segurança do uso desses modais de baixa altitude*

*→ falar que a integração vai aumentar a consciência situacional em baixa altitude*

Rather than maintaining two disparate control frameworks, the herein proposed architecture intends to converge into a singular, unified traffic management system that seamlessly integrates UTM and AAM. This holistic approach replaces traditional siloed structures with a federated environment where UAS Service Suppliers (USS) and Providers of Service for UAM (PSU) operate under an interoperable governance model. 

Integrating low-altitude flights through a singular air traffic control system, hence assimilating the data of current and future flights, increasing situational awareness across operators. 

By consolidating these ecosystems into a unified infrastructure, the system ensures a cohesive transition toward the "ATM of the future," facilitating the management of diverse vehicle performance profiles—from small drones to eVTOLs—within a shared airspace.

The primary functional objective of this integrated system is to ensure the operational safety of low-altitude flight modalities by implementing systemic safety protocols, such as automated strategic de-confliction and dynamic geofencing, the architecture mitigates risks inherent to high-tempo, high-density operations in urban and regional environments. 

The integration of UTM and AAM frameworks significantly enhances shared situational awareness across the low-altitude stratum through a networked exchange of high-fidelity digital information. By digitizing flight intent, real-time position reporting, and meteorological advisories, the system provides a comprehensive and transparent operational picture to all stakeholders—including operators, regulators, and traditional ATC. This enhanced visibility is a critical enabler for cooperative separation practices and Digital Flight Rules (DFR), allowing for greater operational flexibility and the safe scalability of innovative air services in previously unmanaged or complex airspace volumes.

## **5.2    Operational Policies and Constraints** 

*This OCD subsection should reference the policies and standards governing the mission and describe the use and applicability of the system. It should also describe any other operational constraints that govern or limit operations (e.g., personnel availability and acceptable weather).* 

*This OCD section also helps define “where” the system will operate in a sociopolitical or economic sense.* 

*→ aqui falar que nao há uma norma unificada pra o xTM q integraria o UTM com AAM, e que apesar de ter requisitos, policies, contraints para UTM nao há o mesmo nível de documentação para o AAM.*

*→ falar que esse documento pode servidr de base para futuras legislações que considerem os dois como um unico elemento e talvez uma integração completa.* 

Currently there’s not an unified regulation or even requirements to a system integrating UTM to AAM, viewing airspace as a whole, and not a compilation of segmented volumes. 

Despite having requirements, policies and constraints for UTM operations, the AAM system lacks this formal documentation and regulations. This is a probable product of a quick implementation of UAS to controlled airspace, whereas eVTOL aircrafts are still in development stages. Nonetheless, eVTOLs should be addressed in regulatory form, so as to not put human life at risk. 

## **5.3    Operational Environment** 

*This OCD section should describe the physical operational environment(s). This may include discussion of the following, for example:* 

·       t*emperature, humidity, contaminants, noise, shock, vibration;* 

·       *facilities, equipment, computing hardware and software;* 

·       *interoperating systems;* 

·       *the social, geopolitical, and economic environments affecting operations; and* 

·       *elements that threaten, challenge, or cooperate with the system.* 

*This section also describes any changes to the environment that are likely to occur within the lifetime of the proposed system, including those caused by the introduction and use of the system itself. This section defines “where” the system will operate.* 

*→ explicar que são operações de baixa altitude e talvez uma figura q tem tanto no do decea/faa que sao os locais onde a gente tá falando.* 

### **5.3.1    Organizational Structure** 

*This OCD subsection should identify and describe the organizational structure(s) of the personnel. It should state the charter of each organizational element and describe any reporting and other relationships where they are relevant to the system of interest.* 

 → falar que tem um lado governo e o lado industrial, sendo q a fronteira do sistema sao os usuários (publico, serviços públicos, usuarios (utm/aam), vertiportos) \- toda a infra de xSS/sdsp/fims/etc … sao decomposições para entregar uma segurança de voo. 

The organizational structure is composed of government and the aircraft/UAS industries, both meaning to establish efficient regulatory structure. Government aims to 


 ~~![][image6]~~

~~![][image7]~~

~~![][image8]~~

~~![][image9]~~

~~![][image10]~~

 

# 

# **6     System Overview** 

*The intent of this OCD section is to provide an overview of the system, rather than a detailed description of system architecture, functions and other characteristics. Where appropriate, detailed information may be referenced, but should not be included here. The section should include a discussion of the system scope, system boundaries (both physical and operational), personnel involved, system states and modes, capabilities, the system architecture and external interfaces (and any significant internal interfaces). The system overview is written from the perspective(s) of the system operators and maintainers, in their operational environment, and is defined for the system of interest.* 

*The system overview should only be detailed enough to provide the information needed to understand the other sections of the Operational Concept Document. Early in the development activity, the system overview describes the conceptual system. As development progresses, this section is updated, finally describing the actual system operational concept at the end of the development effort.* 

## **6.1    System Scope** 

*This OCD subsection should describe the scope of the system within the context of the mission. It should describe the primary use(s) of the system within the context of the operational environment.*

## **6.2    System Goals and Objectives** 

*This OCD subsection should describe the system's goals and the objectives and expectations for it, quantified where possible, and the key performance attributes for the system. These should include the system quality factors (e.g., affordability, availability, reliability, maintainability, transportability, flexibility, and expansion).* 

*The goals and objectives will define “why” the system exists and should be related to the missions described in Section A.5.1.* 

## **6.3    Users and Operators** 

This OCD subsection should identify the various users and operators of the system, relating them to the personnel described in Section A.5.4. 

It is important to clearly describe the difference between the *users* and the *operators* of the system. Both points of view, while potentially very different, are needed to ensure a well-designed system. 

The users and operators section will discuss “who” is involved in the use of the system and their responsibilities, authorities, and accountabilities. 

\#\# The stakeholders of the system should be hre.. explaining the architecture

### **6.3.x System-Level / Infrastructure Parts**

#### **6.3.x.1 Connected Service \[0..\*\]**

#### **6.3.x.2 FIMS – Flight Information Management System**

|  | Flight Information Management System/FIMS FIMS is an interface for data exchange between FAA systems and UTM participants. FIMS enables exchange of airspace constraint data between the FAA and the USS Network. The FAA also uses this interface as an access point for information on active UTM operations. FIMS also provides a means for approved FAA stakeholders to query and receive post-hoc/archived data on UTM operations for the purposes of compliance audits and/or incident or accident investigation. FIMS is managed by the FAA and is a part of the UTM ecosystem.   (FAA UTM CONOPs V2) |
| :---- | :---- |
|  | — not covered (FAA UAM CONOPs V2) |
|  |  |
|  |   |

#### **6.3.x.1 Rules \[0..\*\]**

#### **6.3.x.2 Operational Volumes \[0..\*\]**

|  | Priority access demands for airspace may overlap with UTM Operational Volumes. In the event of a public safety incident (e.g., EMS or first responders must access airspace), FAA-authorized entities (e.g., law enforcement, fire department) can request UVRs to alert UTM participants of the public safety activity. UVRs do not exclude UTM participants from the airspace, however, Operators/RPICs are expected to exercise caution if they continue their operations, as they are responsible for the overall safety of their flight and are accountable for their actions.     (FAA UTM CONOPs V2) |
| :---- | :---- |
|  | UAM Corridors        As described earlier, initial UAM operations are expected to make use of the flexibility in the current regulatory framework (e.g., VFR, IFR) to meet their operational and mission needs. Over time, the number of UAM operations are expected to increase, the specific areas/locations where operators desire to conduct the operations may expand, and aircraft capabilities (e.g., equipage, performance) could advance. Corridors may offer the opportunity to respond to what could be new levels and types of service demands while taking advantage of the aircraft’s capabilities without adversely impacting current service levels.         The concept of UAM Corridors envisions safe and efficient UAM operations that may not require traditional ATC services in certain situations, are available to any aircraft appropriately equipped to meet the performance requirements, and would be created/implemented when operationally advantageous. The UAM Corridors could help support the increasing operational tempo through increased capabilities (e.g., aircraft performance), UAM Corridor structure, and UAM procedures. At increased UAM traffic levels, UAM Corridors could be a mechanism for distinguishing and keeping separate the different regulatory frameworks—those applicable to UAM operations versus those operating under the current (e.g., IFR, VFR) or UTM regulations.         UAM Corridors would be designed consistent with applicable environmental considerations and may be implemented in areas where it is operationally advantageous. The UAM Corridors may transit all airspace classes. It is anticipated that UAM Corridors may exist simultaneously at locations and in airspace classes with constructs (e.g., VFR flyways/corridors, IFR) leveraged for initial UAM operations.        Operations within UAM Corridors may have operational performance and participation (e.g., UAM Operational Intent sharing, deconfliction within the UAM Corridor) requirements. The performance and participation requirements for a UAM Corridor may vary between UAM Corridors. In addition, performance requirements and UAM Corridor definition (e.g., volume, location) support accommodations for most UAM off-nominal operations where the UAM aircraft can complete the operation safely. Any operator meeting the UAM Corridor performance and participation requirements may operate within or crossing the UAM Corridor. The crossing of a UAM Corridor by an aircraft/operator not participating in the cooperative environment (e.g., general aviation) remains an area of exploration as the UAM Corridor concept, specific features, uses, and requirements mature. As UAM Corridor geometry is better understood, the foundational elements of UAM Corridor crossings may be analyzed by stakeholders.          UAM Corridor definitions are available to stakeholders for planning and operational use. ATC will be involved in the implementation and execution of UAM Corridors for the airspace for which ATC is responsible. Other NAS users will be aware of UAM Corridors through airspace familiarization associated with flight planning or ATC flight plan approval or advisories. UAM Corridor design considerations should include:          1\. Minimal impact to existing ATS and UTM operations while maintaining equity for all operators.          2\. Public interest stakeholder needs (e.g., local environmental and noise, safety, security).          3\. Stakeholder utility (e.g., customer need). UAM Corridor availability (e.g., open, closed) would be in accordance with ATC operational design (e.g., nearby airport configurations/change).         UAM Corridor availability may be communicated through the federated service network to PSUs and UAM operators. In addition to UAM Corridor availability established by ATC, PSUs determine UAM Corridor status that identifies if one or more UAM operations are occurring somewhere within the UAM Corridor. UAM Corridor usage information may be used by the FAA or other stakeholders for situational awareness.          Initially, the UAM Corridors may support point-to-point UAM operations. As UAM operations evolve, UAM Corridors may be segmented and connected to form more complex and efficient networks of available routing between points (e.g., vertiports). Figure 3 shows a small number of point-to-point UAM Corridors. (FAA UAM CONOPs V2) |
|  | PVR \- RESERVA DE VOLUME DO ESPAÇO AÉREO PRIORITÁRIO Procedimento de reserva do espaço aéreo, resultando no estabelecimento de um volume prioritário, temporariamente autorizado e em atendimento às atividades, no solo ou no ar, dentro do ambiente UTM. As PVR são estabelecidas para apoiar a segurança de operações tripuladas e não tripuladas e relacionadas dentre outras, a atividades tais como: resposta a emergências; segurança e calamidade pública; e operações militares. (DECEA DCA 351-6) |
|  | Art. 108\. Os novos volumes de espaço aéreo definidos para operação UAM poderão ser usados pelos demais usuários desde que sejam atendidos os requisitos de capacidade e performance estabelecidos. (DECEA PCA 351-7) |

#### **6.3.x.3 SDSP Supplemental Data Service Providers // Provedor De Serviço De Dados Suplementares**

|  | UAS SUPPLEMENTAL DATA SERVICE PROVIDERS  Operators and USSs can access Supplemental Data Service Providers (SDSPs) for essential or enhanced services \- including terrain and obstacle data, specialized weather data, surveillance, and constraint information. SDSPs may connect to the USS Network or directly to Operators through other means (e.g., public/private internet sites).  (FAA UTM CONOPs V2) |
| :---- | :---- |
|  | Supplemental Data Service Provider (SDSP) UAM operators and PSUs use supplemental data services to access supporting data including, but not limited to, terrain, obstacle, and specialized weather. PSUs are also able to serve as SDSPs for subscribed UAM operators. SDSPs may be accessed via the federated service network or directly by UAM operators. (FAA UAM CONOPs V2) |
|  | PROVEDOR DE SERVIÇO DE DADOS SUPLEMENTARES UAS Os operadores e os USS podem acessar os Provedores de Serviços de Dados Suplementares (SDSP) para serviços essenciais ou aprimorados – incluindo dados de terrenos e obstáculos, dados meteorológicos especializados, vigilância e informações de restrição. SDSP podem se conectar à Rede USS ou diretamente às Operadoras por outros meios (por exemplo, sites de internet públicos/privados). (DECEA DCA 351-6) |
|  | PROVEDOR DE SERVIÇO DE DADOS SUPLEMENTARES – SDSP Art. 189\. O SDSP é o provedor de serviços de dados que apoiam operadores de frota, PSU, administradores de vertiporto e/ou o ECO-UAM no fornecimento de informações para o gerenciamento, coordenação e programação de operações de voo. Art. 190\. Demandas do serviço de informações aeronáuticas para a escalabilidade das operações aéreas dentro do ambiente UAM: I \- definir os serviços SDSP; II \- disponibilizar o intercâmbio dos dados originados pelo SDSP e as aeronaves; III \- implementar progressivamente o SWIM integrando ambientes UAM adjacentes; IV \- regulamentar os serviços dos provedores de serviço AIS dentro do ambiente UAM; e V \- analisar a utilização dos benefícios da implementação do conceito FF-ICE voltado para o ambiente UAM. (DECEA PCA 351-7) |

#### **6.3.x.4 xSU \[1..\*\] (USS / U-space Service / UAM)**

|  | UAS Service Supplier/USS A USS is an entity that assists UAS Operators with meeting UTM operational requirements that enable safe and efficient use of airspace. A USS (1) acts as a communications bridge between federated UTM actors to support Operators’ abilities to meet the regulatory and operational requirements for UAS operations, (2) provides the Operator with information about planned operations in and around a volume of airspace so that Operators can ascertain the ability to safely and efficiently conduct the mission, and (3) archives operations data in historical databases for analytics, regulatory, and Operator accountability purposes. In general, these key functions allow for a network of USSs to provide cooperative management of low altitude operations without direct FAA involvement.      USS services support operations planning, intent sharing, strategic and tactical de-confliction, conformance monitoring, RID, Airspace Authorization, airspace management functions, and management of off-nominal situations. They exchange information with one another over the internet to enable UTM services (e.g., exchange of intent information, notification of airspace changes, and automated query exchanges). USSs work with local municipalities and communities, as needed, to gather, incorporate, and maintain airspace reservations into airspace data repositories that may be accessed by Operators.       USSs may provide (1) Services that enable authorized UTM stakeholders to discover active USSs and their available services within the USS Network, (2) Services that provide the ability for vehicle owners to register data related to their UAS, (3) Services for USS registration, and (4) Services for message security to ensure data is secured and exchanged only with the authorized users. USSs may also provide other value-added services to support UTM participants as market forces create opportunity to meet business needs.  (FAA UTM CONOPs V2) |
| :---- | :---- |
|  | A PSU is an entity that supports UAM operators with meeting UAM operational requirements that enable safe, efficient, and secure use of the airspace. A PSU is the primary service and data provider for UAM stakeholders and the interface between the UAM ecosystem and the FAA. A PSU can be a separate entity from the UAM operator, or an operator can act as its own PSU. When confirming the UAM Operational Intent, a PSU may act on behalf of an operator who has subscribed to its offered services within the updated regulatory framework established by the FAA for instances when an operator does not act as its own PSU.  A PSU:  1\. Provides a communication bridge between federated UAM actors, from PSU to PSU via the network, to support its subscribing UAM operator’s ability to meet the regulatory and operational requirements for UAM operations.  2\. Provides its UAM operators with information gathered from the network about planned UAM operations in a UAM Corridor so that UAM operators can ascertain the ability to conduct safe and efficient missions.  3\. Analyzes and confirms that a submitted UAM Operational Intent is complete, consistent with current advisories and restrictions, and strategically deconflicted considering previously confirmed UAM Operational Intents, COPs, UAM Corridor capacity, airspace restrictions, vertiport resource availability, and adverse environmental conditions.  4\. Provides the confirmed UAM Operational Intent to the federated service network.  5\. Distributes notifications (e.g., constraints, restrictions) for the intended area of operation.  6\. Distributes FAA operational data and advisories, weather, and supplemental data.  7\. Supports cooperative separation management services (e.g., conformance monitoring, advisory services). a. Assists with coordinating UAM Corridor use status; UAM Corridor use status (e.g., occupied, unoccupied) is an indication that UAM operations are being conducted or not.  8\. Archives operational data in historical databases for analytics, regulatory, and UAM operator accountability purposes.  9\. Negotiates airport access through the airport’s sponsor. These key functions allow a PSU to support cooperative management for UAM operations without direct FAA involvement on a per flight basis.  PSU services support operations planning, UAM Operational Intent sharing, deconfliction, airspace management functions, and off-nominal operations that UAM operators may encounter. PSUs may provide value-added services to subscribers that optimize operations or provide SDSP services in support of UAM operations. PSUs exchange information with other PSUs via the federated service network to enable UAM services (e.g., exchange of UAM Operational Intent information, notification of UAM Corridor status, information queries). PSUs also support local municipalities and communities as needed to gather, incorporate, and maintain information that may be accessed by UAM operators.  (FAA UAM CONOPs V2) |
|  | O USS é uma entidade que auxilia os operadores de UAS no atendimento aos requisitos operacionais do UTM que permitem o uso seguro e eficiente do espaço aéreo. Um USS realiza as seguintes funções: a) atua como uma ponte de comunicação entre atores do UTM para apoiar os Operadores no cumprimento dos requisitos regulatórios e operacionais; b) fornece ao operador informações sobre operações planejadas dentro e em torno de um volume de espaço aéreo, para que os operadores possam verificar a capacidade de conduzir a missão com segurança e eficiência; e c) arquivamento de dados de operações em bancos de dados históricos para fins de análise, regulação e prestação de contas do Operador. Em geral, essas funções-chave permitem que uma rede de USS forneça uma gestão cooperativa de operações de baixa altitude sem envolvimento direto do DECEA. Os serviços do USS apoiam o planejamento de operações, o compartilhamento de intenções, o desconflito estratégico e tático, o monitoramento de conformidade, RID, autorização do espaço aéreo, funções de gerenciamento do espaço aéreo e gerenciamento de situações extras. Os USS trabalham com municípios e comunidades locais, conforme necessário, para coletar, incorporar e manter reservas de espaço aéreo em repositórios de dados que podem ser acessados pelos operadores.  Os USS podem fornecer ainda: serviços que permitem que as partes interessadas autorizadas do UTM descubram USS ativos e seus serviços disponíveis dentro da rede USS; serviços de registro de USS; e serviços de segurança de mensagens para garantir que os dados são protegidos e trocados apenas com os usuários autorizados. O USS também pode fornecer outros serviços de valor agregado para apoiar os participantes do UTM à medida que o mercado crie oportunidades para atender às necessidades dos negócios. (DECEA DCA 351-6) |
|  | Art. 61\. O termo PSU refere-se à entidade responsável pelo provimento de serviços dentro do ambiente UAM. Art. 62\. O PSU deverá ser certificado pelo DECEA segundo regras que serão publicadas em norma específica. Art. 63\. Múltiplos PSU poderão operar em uma mesma área geográfica específica. Art. 64\. Os PSU podem depender da contratação de serviços dos SDSP. Art. 65\. O PSU fornecerá os serviços aos operadores dentro do ambiente UAM levando em consideração os requisitos de capacidade e performance estabelecidos. Parágrafo único. O PSU poderá fornecer outros serviços de valor agregado para apoiar os participantes do UAM à medida que o mercado crie oportunidades para atender às necessidades dos negócios. Art. 66\. A função de PSU poderá ser exercida pelo DECEA ou outra entidade, seja pública ou privada, a ser estabelecida em legislação específica para cada área de operação. Art. 67\. Critérios objetivos deverão ser estabelecidos para determinar em quais espaços aéreos deverá haver a designação de um PSU. Art. 68\. Os PSU deverão atender aos protocolos de organizações internacionalmente reconhecidas para a padronização de processos relativos a sistemas, produtos e serviços aplicáveis. Art. 69\. Para um mesmo volume de espaço aéreo, num cenário operacional, poderá haver um ou mais PSU autorizados a operar. Parágrafo único. Independentemente da quantidade, deverá haver um sistema central sincronizado e interoperável com cada PSU. Art. 70\. Os PSU serão utilizados pelos operadores aéreos para receber ou compartilhar informações durante as operações das aeronaves dentro do ambiente UAM e deverão ser capazes de compartilhar informações com os USS. Art. 71\. O sistema central poderá ser gerido pelo DECEA ou outra instituição por ele delegada. Art. 72\. Exemplos de serviços prestados pelo PSU: gestão de intenções de voo, compartilhamento de informações operacionais, desconflito de tráfego, gestão de slots em vertiportos, balanceamento entre capacidade e demanda (DCB), controle de fluxo, monitoramento de conformidade, coordenação de acesso a aeroportos, vertiportos, serviços de meteorologia, serviços de cartografia, informações aeronáuticas etc. Art. 73\. Os serviços providos por cada PSU poderão variar de acordo com a quantidade de movimentos e da complexidade do espaço aéreo. Art. 74\. Este item aborda uma listagem, não exaustiva, de ações de responsabilidade do PSU: I \- interagir com outros PSU a fim de manter a eficiência das operações; II \- analisar e confirmar se a intenção de voo de um operador aéreo está completa, consistente com os avisos e restrições aplicáveis, estrategicamente separada de outros tráfegos (considerando as intenções de todos os demais voos), com disponibilidade de horário para pousar e decolar e informada das condições de voo; III \- inserir a intenção de voo aprovada na rede de PSU; IV \- emitir aos demais usuários impactados notificações sobre a autorização emitida, suas restrições e horários de operação; V \- prover suporte colaborativo para os serviços de separação (estratégica e tática) e emissão de alertas a outros PSU envolvidos; e VI \- registrar e armazenar os dados de todas as operações para fins de análise, regulação e governança.  (DECEA PCA 351-7) |

#### **6.3.x.5 Vertiport \[1..\*\]**

|  |  \- not covered  (FAA UTM CONOPs V2) |
| :---- | :---- |
|  |       Vertiports, used as a collective term, are expected to be a diverse system of public and private vertiports and vertistops. These facilities are categorized to identify the variety of aircraft they can support based on facility design and operations. Vertiports and vertistops support passenger and cargo operations for aircraft operating in VFR, IFR, and AFR.         UAM operators are expected to utilize whichever vertiport configuration meets their operational needs.         A vertiport is a designated area that meets the capability requirements to support UAM departure and arrival operations. The UAM vertiport provides current and future resource availability information for UAM operations (e.g., open/closed, pad availability) to support UAM operator planning and PSU strategic deconfliction. UAM vertiport information is accessible by the operator via the federated service network and supplemental vertiport information may be available via the SDSP. The vertiport information is used by UAM operators and PSUs for UAM operation planning including strategic deconfliction and DCB; however, the vertiports do not provide strategic deconfliction or DCB services. (FAA UAM CONOPs V2) |
|  | not covered (DECEA DCA 351-6) |
|  | XV \- Vertiporto: a) área delimitada em terra, na água ou em uma estrutura destinada para uso, no todo ou em parte, para pouso, decolagem e movimentação em superfície de aeronaves VTOL (ex.: helicópteros e eVTOL); e b) embora haja muitas outras definições mais detalhadas sobre os tipos de locais de operação de aeronaves eVTOL, no contexto deste documento, o termo Vertiporto será aplicado em todos os casos; (DECEA PCA 351-7) |

#### **6.3.x.1 Public Safety \[0..\*\]**

|  |   Other stakeholders can also access information and/or utilize UTM services via the USS Network. Stakeholders include public safety entities and the general public. Public safety entities, when authorized, can access UTM operations data as a means to ensure safety of the airspace and persons and property on the ground, security of airports and critical infrastructure, and privacy of the general public. Data can be accessed through dedicated portals or can be routed directly by service providers to public safety entities, local/tribal/state law enforcement agencies, and other relevant federal agencies (e.g., Department of Homeland Security (DHS)) on an as-needed basis. The general public can access data that is determined or required to be publicly available.    (FAA UTM CONOPs V2) |
| :---- | :---- |
|  | Public interest stakeholders are entities declared by governing processes (e.g., COPs) to be able to access UAM operational information and notifications. This access may support activities including, but not limited to, public right to know, government regulatory, government assured safety and security, and public safety. Examples of public interest stakeholders are local law enforcement and United States federal agencies.  (FAA UAM CONOPs V2) |
|  | Outras partes interessadas também podem acessar informações ou utilizar serviços UTM por meio da Rede USS. Entre as partes interessadas estão as entidades de segurança pública e o público em geral. As entidades de segurança pública, quando autorizadas, podem acessar os dados das operações do UTM como forma de garantir a segurança do espaço aéreo e das pessoas e propriedades no terreno, a segurança dos aeroportos e da infraestrutura crítica e a privacidade do público em geral. Os dados podem ser acessados em portais dedicados ou podem ser encaminhados diretamente por prestadores de serviços para entidades de segurança pública e outros órgãos públicos conforme a necessidade. O público em geral pode acessar dados determinados ou necessários que estejam disponíveis publicamente. (DECEA DCA 351-6) |
|  | As operações aéreas específicas como policiais, atendimento a emergências, segurança pública e atividades militares também serão integradas a esse novo ecossistema.  (DECEA PCA 351-7) |

#### **6.3.x.1 UTM Users**

#### **6.3.x.2 UASx \[1..\*\] (UAS / drones)**

|  | BVLOS and VLOS UAS Operators are responsible for separating from and remaining well clear of all other aircraft. Because the risks associated with different areas of operation can vary, the requirements for onboard DAA systems for UAS also vary. In airspace where risk to life in the air and on the ground is low, a relatively higher risk of UAS-to-UAS collision may be accepted, and thus the FAA may not require DAA technologies. Conversely, operations in more heterogeneous environments (e.g., mix of manned and unmanned aircraft, controlled airspace) could impose increased risk to manned aircraft due to the higher criticality of collision, therefore, increased performance requirements may be imposed (e.g., onboard systems, real-time avoidance equipment, network-based solutions).    (FAA UTM CONOPs V2) |
| :---- | :---- |
|  | not covered  (FAA UAM CONOPs V2) |
|  | Sistema de Aeronave Não Tripulada UAS Qualquer aparelho que possa sustentar-se na atmosfera a partir de reações que não sejam as reações do ar contra a superfície da terra e que pretenda operar sem piloto a bordo. (DECEA DCA 351-6) |
|  | Sistema de Aeronave Não Tripulada (Unmanned Aircraft System)            Art. 29\. O foco no ambiente UTM é a operação de aeronaves sUAS remotamente pilotadas ou autônomas e que possuam, na maioria dos casos, massa e dimensões significativamente menores se comparadas às aeronaves eVTOL.            Art. 31\. No ambiente UTM as aeronaves UAS irão operar atendendo a diversas finalidades, entretanto, sem transporte de passageiros. (DECEA DCA 351-7) |

#### **6.3.x.3 UAS Operator x \[1..\*\]**

|  | The Operator is the person or entity responsible for the overall management of their operation. The Operator meets regulatory responsibilities, plans flight/operations, shares operation intent information, and safely conducts operations using all available information. Use of the term ‘Operator’ in this document is inclusive of airspace users electing to participate in UTM, including manned aircraft Operators, except when specifically referred to as a manned or UAS/UTM Operator.  (FAA UTM CONOPs V2) |
| :---- | :---- |
|  | not covered  (FAA UAM CONOPs V2) |
|  | O Operador é a pessoa ou entidade responsável pela gestão geral de sua operação. Além disso, cumpre responsabilidades regulatórias, planeja voo/operações, compartilha informações de intenção de operação e conduz com segurança as operações usando todas as informações disponíveis. O uso do termo ‘Operador’ neste documento inclui os usuários do espaço aéreo que optam por participar do UTM, incluindo operadores de aeronaves tripuladas, exceto quando especificamente referido como operador tripulado ou UAS/UTM. (DECEA DCA 351-6) |
|  | not covered (DECEA DCA 351-7) |

#### **6.3.x.4 Remote Pilot in Command/RPIC \[1..\*\]**

|  | The remote pilot in command (RPIC) is the person responsible for the safe conduct of each UAS flight. An individual may serve as both the Operator and the RPIC. The RPIC adheres to operational rules of the airspace in which the unmanned aircraft (UA) is flying; avoids other aircraft, terrain and obstacles; assesses and respects airspace constraints and flight restrictions; and avoids incompatible weather/environments. The RPIC monitors the flight performance and location of the UA. If safety of flight is compromised, due to system/equipment degradation or environmental vulnerabilities, the RPIC is aware of these factors and intervenes appropriately. More than one RPIC may take control of the aircraft during the flight, provided one person is responsible for the operation at any given time. (FAA UTM CONOPs V2) |
| :---- | :---- |
|  | not covered  (FAA UAM CONOPs V2) |
|  | O Piloto Remoto em Comando (RPIC) é o responsável pela condução segura de cada voo de UAS. Uma pessoa pode atuar como um operador e como um RPIC. O RPIC adere às regras de operação do espaço aéreo em que a aeronave não tripulada voa; evita outras aeronaves, terrenos e obstáculos, avalia e respeita limitações do espaço aéreo e restrições de voo; evita condições climáticas e ambientes incompatíveis; e também monitora o desempenho do voo e localização da aeronave. Se a segurança do voo estiver comprometida, devido à degradação do sistema/equipamento ou às vulnerabilidades do ambiente, o RPIC estará ciente desses fatores e poderá intervir adequadamente. Mais de um RPIC pode suceder no controle da aeronave durante o voo, desde que uma única pessoa seja responsável pela operação em um determinado momento e seja identificada. (DECEA DCA 351-6) |
|  | not covered (DECEA DCA 351-7) |

## **6.3.x UAM Users**

#### **6.3.x.2 UAM Vehicle x \[1..\*\]**

|  | not covered (FAA UTM CONOPs V2) |
| :---- | :---- |
|  | UAM Aircraft – An aircraft that chooses to participate in UAM operations.  (FAA UAM CONOPs V2) |
|  | not covered (DECEA DCA 351-6) |
|  | Art. 33\. As principais características das aeronaves eVTOL são: I \- as aeronaves eVTOL são um novo tipo de aeronave elétrica que possuem a capacidade de pousar e decolar na vertical de forma semelhante a um helicóptero, transportando pessoas (piloto e/ou passageiros) e cumprindo os requisitos de capacidade e performance requeridos; II \- são projetadas, em geral, para voos em baixas altitudes e sem pressurização e, por isso, permitem o uso de materiais mais apropriados para esse tipo de operação; III \- embora os eVTOL tenham a capacidade de decolar e pousar na vertical, alguns modelos comportam-se de forma muito similar às aeronaves de asa fixa durante a fase em rota; IV \- as aeronaves eVTOL, em decorrência da limitação atual das baterias, possuem expectativa de alcance reduzido em comparação com os helicópteros e, por esse motivo, será necessário um controle de fluxo mais eficiente, a fim de gerenciar melhor o uso do espaço aéreo; e V \- quando comparada à aviação tradicional, será na IHM que, com a evolução tecnológica, bem como o progresso na área da automação, tornará a forma de pilotagem mais precisa, eficiente e simplificada. § 1° As aeronaves que possuem a capacidade de pousar e decolar na vertical são classificadas como VTOL, a exemplo dos tradicionais helicópteros, e, por isso, às aeronaves VTOL com propulsão elétrica, dá-se o nome de eVTOL. § 2° Existem projetos de aeronaves com a mesma capacidade VTOL, porém com energia obtida de forma híbrida, ou seja, por combustíveis fósseis e baterias. § 3° Algumas empresas possuem projetos em andamento de aeronaves com a capacidade adicional de pousar e decolar em pista de tamanho reduzido, semelhante a uma aeronave de asa fixa e, nesse caso, a classificação é STOL. Art. 34\. Existem diversas empresas no mundo atuando direta ou indiretamente no desenvolvimento das aeronaves eVTOL considerando diferentes tipos de design. Art. 35\. Durante a operação de eVTOL, é indispensável que sejam gerenciados pontos de pouso alternativos ao longo da rota, a fim de garantir a segurança em situações de contingência relacionadas à autonomia, em virtude das limitações das baterias. (DECEA DCA 351-7) |

#### **6.3.x.3 UAM Operator x \[1..\*\]**

|  | The Operator is the person or entity responsible for the overall management of their operation. The Operator meets regulatory responsibilities, plans flight/operations, shares operation intent information, and safely conducts operations using all available information. Use of the term ‘Operator’ in this document is inclusive of airspace users electing to participate in UTM, including manned aircraft Operators, except when specifically referred to as a manned or UAS/UTM Operator.  (FAA UTM CONOPs V2) |
| :---- | :---- |
|  | not covered  (FAA UAM CONOPs V2) |
|  | O Operador é a pessoa ou entidade responsável pela gestão geral de sua operação. Além disso, cumpre responsabilidades regulatórias, planeja voo/operações, compartilha informações de intenção de operação e conduz com segurança as operações usando todas as informações disponíveis. O uso do termo ‘Operador’ neste documento inclui os usuários do espaço aéreo que optam por participar do UTM, incluindo operadores de aeronaves tripuladas, exceto quando especificamente referido como operador tripulado ou UAS/UTM. (DECEA DCA 351-6) |
|  | not covered (DECEA DCA 351-7) |

## **6.4    System Interfaces and Boundaries** 

*This OCD subsection should identify and describe the various internal and external interfaces of the system. It should also identify the relationships between systems in which the organization (enterprise) is a FoS/SoS. The system interfaces section defines, in part, “where” the system is operated and supported. The placement of the system boundary is normally accomplished once the external interfaces are understood and such subtle interfaces as those associated with system operators and users are also clarified and understood. This section should complement the discussion conducted in Section A.5.3 by relating the defined interfaces and boundaries to the Operational Environment.* 

### **FIMS ⇄ Services**

The FIMS ⇄ Connected Service interface **SHALL** provide the means by which operational information is exchanged between air traffic authority systems and external services participating in the ecosystem. This interface **SHALL** enable regulatory oversight of airspace operations while allowing industry-operated services to perform operational planning, coordination, and execution functions in a distributed environment.

FIMS **SHALL** function as the authoritative interface for the receipt, dissemination, and controlled access to operational data. Connected Services **SHALL** use this interface to supply operational data required by policy and to receive regulatory information necessary to ensure compliance with applicable regulations and operational constraints.

The interface **SHALL** support the separation of responsibilities between the air traffic authority systems and Connected Services. Connected Services **SHALL** retain responsibility for operational coordination and service provision, while the authority **SHALL** retain responsibility for regulation, compliance monitoring, and post-operation analysis. The interface **SHALL not** be used to provide direct tactical control of airspace operations by the authority.

The FIMS ⇄ Connected Service interface **SHALL** enable approved stakeholders to query and retrieve archived operational data for the purposes of compliance audits, incident investigation, accident investigation, and system performance assessment. This capability **SHALL** support traceability and accountability across the airspace environment without requiring continuous real-time intervention by the authority.

The interface **SHALL** support interoperability among multiple Connected Services operating within the same airspace by enabling standardized data exchange through a federated architecture. This interoperability **SHALL** allow Connected Services to coexist and evolve independently while operating within a common regulatory and information framework.

As low altitude airspace operations scale in volume and complexity, the FIMS ⇄ Connected Service interface **SHALL** remain a critical enabler for safe integration, regulatory oversight, and information consistency across the ecosystem.

| ID | Producer | Consumer | Data Element | Description |
| ----- | ----- | ----- | ----- | ----- |
|  | Connected Service | FIMS | Service Data | External service-provided operational data |
|  | FIMS | Connected Service | FIMS Data | Flight and flow related data for connected services |

### **FIMS ⇄ SDSP**

### **FIMS ⇄ xSU**

The FIMS ⇄ xSU ( UTM / UAM ) interface shall provide the means by which Access Service Providers supply operational and status information to the Airspace Authority for oversight, monitoring, and regulatory purposes. This interface shall support the authorities’ ability to maintain situational awareness of operations conducted within the unified traffic management architecture without assuming responsibility for tactical control.

The FIMS ⇄ xSU ( UTM / UAM ) interface shall provide the primary access mechanism through which operators and external systems interact with traffic management services across unmanned, urban air mobility, and advanced air mobility environments. This interface shall enable a common entry point for operational participation while supporting multiple traffic management domains.

The xSS shall function as an abstraction layer between operators and the underlying traffic management services. Through this abstraction, the interface shall allow UTM, UAM, and AAM services to evolve independently while preserving a consistent access model for operators and external stakeholders.

The interface shall support the exchange of operational intent, constraints, advisories, and situational awareness data necessary for safe and coordinated operations across heterogeneous airspace environments. UTM, UAM, and AAM services shall rely on this interface to receive operational data required for planning, deconfliction, and coordination functions appropriate to each domain.

The FIMS ⇄ xSU ( UTM / UAM ) interface shall enable interoperability across traffic management domains by ensuring that data relevant to cross-domain operations is shared in a controlled and standardized manner. This capability shall support transitions between UTM, UAM, and/or AAM environments without requiring operators to interact directly with multiple domain-specific services.

The interface shall preserve separation of concerns by ensuring that xSS entities provide access, aggregation, and mediation functions, while UTM, UAM, and AAM services retain responsibility for traffic management, safety assurance, and domain-specific operational rules. The interface shall not assign tactical traffic separation responsibilities to the xSU.

As operations scale in volume, autonomy, and complexity, the FIMS ⇄ xSU ( UTM / UAM ) interface shall remain a critical enabler for federated access, cross-domain interoperability, and scalable integration of current and future air mobility services.

| ID | Producer | Consumer | Data Element | Description |
| ----- | ----- | ----- | ----- | ----- |
|  | FIMS | xSU | Constraints | Airspace and regulatory constraints |
|  | FIMS | xSU | RFI | Requests for additional information |
|  | FIMS | xSU | Authority Information | Regulatory and policy data |
|  | FIMS | xSU | Responses | Responses to USS queries |
|  | FIMS | xSU | Flow Management Information | Strategic traffic flow data |
|  | xSU | FIMS | Responses | Answers to FIMS RFIs |
|  | xSU | FIMS | Notifications | Operational alerts |
|  | xSU | FIMS | Flight Plans | Planned operations |
|  | xSU | FIMS | Flight Information | Active flight states |
|  | xSU | FIMS | Flow Management Information | Tactical flow data |

### **xSU ⇄ Public Safety**

### **xSU ← SDSP**

The xSU ← SDSP interface shall provide the means by which supplementary data services supply environmental, surveillance, and performance-related information to Access Service Providers. This interface shall support the safe planning and execution of operations across unmanned, urban air mobility, and advanced air mobility domains.

SDSP entities **shall** provide terrain data through this interface to support altitude management, obstacle clearance, and route planning. Terrain information **shall** be suitable for the operational context and performance characteristics of the supported vehicles.

The interface **shall** support the provision of localized weather information, including micro-weather effects, to enable xSUs to assess environmental conditions that may impact operational safety and performance. Micro-weather data **shall** support both pre-flight planning and in-flight awareness functions.

SDSP entities **shall** provide surveillance data through this interface to support situational awareness of cooperative and non-cooperative airspace users and other relevant objects. Surveillance information **shall** be used by xSUs to augment planning-level coordination and safety monitoring. The interface **shall not** be used to assign centralized tactical separation authority to SDSP entities.

The interface **shall** support the provision of vehicle performance data, including performance envelopes and operational limitations, to enable xSUs to assess feasibility, compliance, and safety margins of planned and active operations. Performance data **shall** be used to support decision-making without transferring vehicle control authority to SDSP entities.

SDSPx entities **shall** provide obstacle data, including static and dynamic obstacles, to support hazard identification and risk mitigation. Obstacle information **shall** enable xSUs to account for known hazards during planning and execution phases.

The xSU ← SDSP interface **shall** preserve separation of responsibilities. SDSP entities **shall** provide data services only, while xSUs **shall** retain responsibility for operational decision-making, coordination, and execution. The interface **shall** support federation by allowing multiple SDSP entities to coexist and evolve independently.

The xSU ← SDSP interface **shall** be applicable across unmanned, urban air mobility, and advanced air mobility environments, allowing domain-specific data sources to be integrated under a common architectural pattern. This interface **shall** remain a critical enabler for scalability, safety, and resilience of the unified traffic management architecture.

| ID | Producer | Consumer | Data Element | Description |
| :---- | :---- | :---- | :---- | :---- |
|  | SDSP | xSU | Terrain | Digital terrain models |
|  | SDSP | xSU | Micro-Weather | Localized weather |
|  | SDSP | xSU | Surveillance | Tracking information |
|  | SDSP | xSU | Performance | Vehicle performance models |
|  | SDSP | xSU | Obstacles | Static & dynamic obstacles |

### 

### **xSU ⇄ xSU**

| ID | Producer | Consumer | Data Element | Description |
| :---- | :---- | :---- | :---- | :---- |
| ICD-4.1 | xSU | Partner xSU | Operation Intent | Planned operations |
| ICD-4.2 | Partner xSU | xSU | Operation Intent | Planned operations |

### 

### **xSU ⇄ UTM Users**

The xSU ⇄ UTM Users interface shall provide the mechanism by which Access Service Providers communicate authorized operational information to UTM Users. This interface shall support the execution of unmanned aircraft operations in accordance with applicable airspace, regulatory, and service constraints. This interface **shall** support coordinated planning, monitoring, and management of unmanned aircraft operations within the unified traffic management architecture.

xSUs **shall** provide operational instructions and status information through this interface to enable UTM Users to understand the authorization state, scope, and conditions of their operations. Operational information **shall** reflect the outcome of planning, coordination, and authorization processes performed within the unified traffic management architecture.

UTM Users **shall** submit operation intent information through this interface to describe planned or intended operations, including scope, timing, and operational parameters. Operation intent information **shall** enable xSUs to perform coordination, constraint evaluation, and authorization support functions.

The interface **shall** support the provision of airspace, temporal, and regulatory constraints applicable to user operations. Constraint information **shall** enable UTM Users to maintain compliance with operational limitations and applicable rules throughout the operation lifecycle.

The interface **shall** support the provision of real-time operational information, including live status updates and telemetry summaries, to enable xSUs to maintain awareness of active operations. Real-time information **shall** support monitoring, conformance assessment, and safety-related services.

xSUs **shall** provide notifications through this interface to convey alerts, advisories, and operational messages relevant to safety, coordination, or compliance. Notifications **shall** support timely user awareness of conditions affecting planned or active operations.

The interface **shall** support the transmission of modifications to approved operations, including updates or amendments resulting from coordination, constraint changes, or evolving operational conditions. Modifications **shall** be communicated in a clear and traceable manner to enable UTM Users to adjust operations accordingly.

The xSU ⇄ UTM Users interface **shall** preserve separation of responsibilities. xSUs **shall** provide coordination and service-level guidance, while UTM Users **shall** retain responsibility for the execution of operations and compliance with applicable rules and procedures. The interface **shall not** be used to provide tactical control or direct vehicle maneuvering instructions.

The xSU ⇄ UTM Users interface **shall** function as a primary communication channel within the unified traffic management architecture, enabling safe, compliant, and scalable unmanned aircraft operations without introducing centralized air traffic control authority. The xSU ⇄ UTM Users interface **shall** function as a critical input channel within the unified traffic management architecture, enabling scalable, cooperative, and transparent unmanned aircraft operations.

| ID | Producer | Consumer | Data Element | Description |
| :---- | :---- | :---- | :---- | :---- |
|  | xSU | UTM Users | Others Operations Intents | Authorized operational instructions and status |
|  | xSU | UTM Users | Constraints | Airspace, temporal, or regulatory constraints |
|  | xSU | UTM Users | Notifications | Alerts, advisories, and operational messages |
|  | xSU | UTM Users | Modifications | Updates or amendments to approved operations |
|  | UTM Users | xSU | Operation Intent | Declared planned or intended operations |
|  | UTM Users | xSU | Real-Time Information | Live operational status and telemetry summaries |

### **xSU ⇄ UAM Users**

The xSU ⇄ UAM Users interface **shall** provide the mechanism by which Access Service Providers communicate operational clearances, guidance, and coordination information to UAM Users. This interface **shall** support the safe execution of UAM operations in accordance with applicable airspace, infrastructure, and regulatory requirements.

xSUs **shall** provide operational clearance and guidance information through this interface to enable UAM Users to understand the authorization state, conditions, and limitations of planned and active operations. Operational guidance **shall** reflect coordination outcomes within the unified traffic management architecture.

The interface **shall** support the provision of operational and airspace constraints applicable to UAM operations, including constraints associated with corridors, vertiports, terminal areas, and surrounding airspace. Constraint information **shall** enable UAM Users to maintain compliance throughout all phases of operation.

xSUs **shall** provide notifications through this interface to convey alerts, advisories, and safety-relevant messages. Notifications **shall** support timely awareness of conditions affecting UAM operations, including infrastructure status, traffic conditions, and environmental factors.

The interface **shall** support the transmission of modifications to approved UAM operations, including changes resulting from coordination outcomes, constraint updates, or evolving operational conditions. Modifications **shall** be communicated in a clear and traceable manner to enable UAM Users to respond appropriately.

The xSU ⇄ UAM Users interface **shall** preserve separation of responsibilities. xSUs **shall** provide coordination, authorization support, and information services, while UAM Users **shall** retain responsibility for operational execution and compliance with applicable procedures. The interface **shall not** be used to provide tactical air traffic control or direct vehicle maneuvering instructions.

The xSU ⇄ UAM Users interface **shall** function as a primary operational communication channel within the unified traffic management architecture, enabling safe, scalable, and passenger-capable urban and advanced air mobility operations without introducing centralized control authority.

| ID | Producer | Consumer | Data Element | Description |
| :---- | :---- | :---- | :---- | :---- |
|  | xSU | UAM Users | Operations | Operational clearances and guidance |
|  | xSU | UAM Users | Constraints | Operational and airspace constraints |
|  | xSU | UAM Users | Notifications | Alerts and advisories |
|  | xSU | UAM Users | Modifications | Changes to approved UAM operations |
|  | UAM Users | xSU | Operation Intent | Intended UAM missions and trajectories |
|  | UAM Users | xSU | Real-Time Information | Current operational and vehicle state data |

### 

### **xSU ⇄ Vertiport**

### **SDSP ⇄ SDSP**

### **SDSP ⇄ Vertiport**

The SDSP ⇄ Vertiport interface shall provide a mechanism by which supplementary data services deliver environmental, surveillance, performance, and aerodrome-related information directly to vertiport systems. This interface shall support the safe conduct of approach, departure, ground, and terminal-area operations associated with urban and advanced air mobility.

SDSP entities **shall** provide terrain data through this interface to enable vertiport systems to assess approach and departure surfaces, terrain clearance, and surrounding topography relevant to UAM operations. Terrain data **shall** support safety assessments and operational planning in the vicinity of the vertiport.

The interface **shall** support the provision of localized meteorological information, including time-sensitive and micro-scale weather phenomena, to enable vertiport operators to assess conditions impacting landing, takeoff, ground handling, and passenger operations. Micro-weather data **shall** support operational decision-making without introducing centralized traffic control functions.

SDSP entities **shall** provide surveillance data through this interface to enhance vertiport awareness of cooperative and non-cooperative traffic operating in the immediate vicinity of the vertiport. Surveillance information **shall** support situational awareness and safety monitoring. The interface **shall not** be used to provide tactical separation or air traffic control services.

The interface **shall** support the provision of performance-related data, including environmental and infrastructure constraints, to enable vertiport systems to assess operational limits, infrastructure availability, and compatibility with planned vehicle operations. Performance data **shall** inform local operational decisions without transferring authority over vehicle control.

SDSP entities **shall** provide obstacle data, including static and dynamic obstacles, to support hazard identification and mitigation in the vertiport vicinity. Obstacle data **shall** be suitable for integration with vertiport safety management and monitoring systems.

The interface **shall** support the provision of aerodrome information, including published vertiport characteristics, declared capacities, operational constraints, and status information. Aerodrome information **shall** enable coordination between vertiport operations, UAM Users, and Access Service Providers.

The SDSP ⇄ Vertiport interface **shall** preserve separation of responsibilities. SDSPx entities **shall** provide data services only, while vertiport operators **shall** retain responsibility for local infrastructure operations, safety management, and compliance with applicable regulations. The interface **shall** support federation by allowing multiple SDSPx entities to provide complementary data services.

The SDSP ⇄ Vertiport interface **shall** function as a critical supporting capability within the unified traffic management architecture, enabling safe terminal-area operations without introducing centralized traffic control or authority conflicts.

| ID | Producer | Consumer | Data Element | Description |
| :---- | :---- | :---- | :---- | :---- |
|  | SDSPx | Vertiport | Terrain | Surrounding terrain models for approach/departure safety |
|  | SDSPx | Vertiport | Micro-Weather | Local weather conditions impacting vertiport operations |
|  | SDSPx | Vertiport | Surveillance | Traffic awareness near vertiport airspace |
|  | SDSPx | Vertiport | Performance | Environmental or infrastructure performance constraints |
|  | SDSPx | Vertiport | Obstacles | Obstacle data in the vertiport vicinity |
|  | SDSPx | Vertiport | Aerodrome Information | Published aerodrome/vertiport data and operational constraints |

### 

### **SDSP ⇄ UTM Users**

The SDSP ⇄ UTM Users interface shall provide a mechanism by which supplementary data services deliver environmental, surveillance, and performance-related information directly to UTM Users. This interface shall support informed decision-making by users participating in low-altitude and cooperative traffic management operations.

SDSP entities **shall** provide terrain data through this interface to enable UTM Users to assess altitude constraints, obstacle clearance, and surface-related hazards during mission planning and execution. Terrain data **shall** be appropriate for the operational context and resolution required for low-altitude operations.

The interface **shall** support the provision of localized meteorological information, including micro-weather effects, to enable UTM Users to evaluate environmental conditions that may affect flight safety, performance, or mission feasibility. Micro-weather data **shall** support both pre-flight planning and operational awareness.

SDSP entities **shall** provide surveillance data through this interface to enhance UTM User awareness of cooperative and non-cooperative traffic and other relevant objects. Surveillance information **shall** be used to support situational awareness and risk assessment. The interface **shall not** be used to provide tactical separation services or to assume air traffic control responsibilities.

The interface **shall** support the provision of performance-related data to enable UTM Users to assess operational feasibility, environmental constraints, and safety margins. Performance data **shall** inform user decisions without transferring operational control authority to SDSPx entities.

SDSPx entities **shall** provide obstacle data, including static and dynamic obstacle information, to support hazard identification and avoidance during planning and execution phases. Obstacle data **shall** be suitable for integration with user planning tools and displays.

The SDSP ⇄ UTM Users interface **shall** preserve separation of responsibilities. SDSP entities **shall** provide data services only, while UTM Users **shall** retain responsibility for operational decisions and compliance with applicable rules and procedures. The interface **shall** support federation by allowing multiple SDSP entities to coexist and provide complementary data services.

The SDSP ⇄UTM Users interface **shall** remain a supporting capability within the unified traffic management architecture, enabling transparency, situational awareness, and safety without introducing centralized control or authority conflicts.

| ID | Producer | Consumer | Data Element | Description |
| :---- | :---- | :---- | :---- | :---- |
|  | SDSP | UTM Users | Terrain | Digital elevation and surface models supporting UTM planning and safety |
|  | SDSP | UTM Users | Micro-Weather | Localized meteorological data affecting low-altitude operations |
|  | SDSP | UTM Users | Surveillance | Cooperative and non-cooperative traffic awareness data |
|  | SDSP | UTM Users | Performance | Vehicle or environment performance-related parameters |
|  | SDSP | UTM Users | Obstacles | Static and dynamic obstacle databases |
|  | UTM Users | SDSP | Requests | Request of data |

### **SDSP ⇄ UAM Users**

The SDSP ⇄ UAM Users interface shall provide a mechanism by which supplementary data services deliver environmental, surveillance, performance, and aerodrome-related information directly to UAM Users. This interface shall support safe and efficient execution of UAM operations, including vertiport-based and corridor-based flight profiles.

SDSPx entities **shall** provide terrain data through this interface to enable UAM Users to assess route feasibility, obstacle clearance, and terrain-related risks along planned trajectories. Terrain data **shall** be suitable for the altitude, speed, and performance characteristics of UAM vehicles.

The interface **shall** support the provision of high-resolution meteorological information, including localized and time-sensitive weather phenomena, to support vertiport operations and corridor management. Micro-weather data **shall** enable UAM Users to evaluate operational constraints affecting departure, arrival, and en-route phases.

SDSPx entities **shall** provide surveillance data through this interface to enhance UAM User awareness of cooperative and non-cooperative traffic operating within or near UAM corridors and terminal areas. Surveillance information **shall** support situational awareness and risk assessment. The interface **shall not** be used to provide centralized air traffic control or tactical separation services.

The interface **shall** support the provision of performance-related data to enable UAM Users to assess vehicle capabilities, environmental limitations, and safety margins relevant to planned and active operations. Performance data **shall** inform operational decisions without transferring control authority to SDSPx entities.

SDSP entities **shall** provide obstacle data, including static and dynamic obstacles, to support hazard identification along UAM trajectories and in the vicinity of vertiports. Obstacle data **shall** be suitable for integration with UAM planning and monitoring tools.

The interface **shall** support the provision of aerodrome information, including vertiport operational status, infrastructure characteristics, and availability constraints. Aerodrome information **shall** enable UAM Users to assess operational readiness and compatibility with planned operations.

The SDSP ⇄ UAM Users interface **shall** preserve separation of responsibilities. SDSPx entities **shall** provide data services only, while UAM Users **shall** retain responsibility for operational decision-making and compliance with applicable regulations and procedures. The interface **shall** support federation by allowing multiple SDSP entities to coexist and provide complementary data services.

The SDSP ⇄ UAM Users interface **shall** function as a supporting capability within the unified traffic management architecture, enabling informed user decisions and enhanced situational awareness without introducing centralized control or authority conflicts.

| ID | Producer | Consumer | Data Element | Description |
| :---- | :---- | :---- | :---- | :---- |
|  | SDSP | UAM Users | Terrain | Terrain data for UAM route planning and risk assessment |
|  | SDSP | UAM Users | Micro-Weather | High-resolution weather data for vertiport and corridor operations |
|  | SDSP | UAM Users | Surveillance | Traffic awareness supporting separation and situational awareness |
|  | SDSP | UAM Users | Performance | Performance-affecting parameters (environmental or vehicle) |
|  | SDSP | UAM Users | Obstacles | Obstacle information relevant to UAM trajectories |
|  | SDSP | UAM Users | Aerodrome Information | Vertiport and aerodrome operational status and characteristics |
|  | UAM Users | SDSP | Requests | Request of data |

### 

### **UAS Operator ⇄ UAS**

The UAS Operator ⇄ UAS interface shall provide a mechanism for bidirectional information exchange between unmanned aircraft vehicles and UTM Operators. This interface shall support human awareness of vehicle state and mission execution while preserving vehicle autonomy and operator responsibility boundaries.

UAS entities **shall** provide telemetry data through this interface to enable UTM Users to maintain awareness of vehicle position, velocity, and health status. Telemetry information **shall** support monitoring, supervision, and post-operation analysis. The interface **shall not** be used to provide centralized traffic separation or air traffic control functions.

UTM Operators **shall** provide authorized operation intent and mission parameters to UAS entities through this interface. Operation intent information **shall** reflect approved operational scope and constraints and **shall** enable vehicles to execute missions in accordance with authorization and coordination outcomes.

Information exchanged through the UAS Operator ⇄ UAS interface **shall** support situational awareness, conformance monitoring, and mission execution without transferring tactical control of vehicles to UTM Users. UTM Users **shall** retain responsibility for mission supervision and compliance, while UASx entities **shall** retain responsibility for vehicle-level control and autonomous execution.

The interface **shall** preserve separation of responsibilities among humans, services, and vehicles. Human users **shall** not be required to issue continuous control inputs, and vehicles **shall** not depend on continuous human intervention for safe operation.

The UAS Operator ⇄ UAS interface **shall** function as a supporting coordination and awareness channel within the unified traffic management architecture, enabling scalable human supervision of autonomous operations without introducing centralized control or authority conflicts.

| ID | Producer | Consumer | Data Element | Description |
| :---- | :---- | :---- | :---- | :---- |
| ICD-13.1 | UAS | UTM Users | Telemetry | Position, velocity, and health information |
| ICD-13.2 | UTM Users | UASx | Operation Intent | Authorized intent and mission parameters |

### 

### **UAS Operator ⇄ UAS Operator**

### **UAS ⇄ UAS**

The interface **shall** support vehicle-to-vehicle (V2V) communication between UASx entities to enable cooperative coordination, collision avoidance support, and local autonomy functions. V2V communication **shall** be limited to coordination and safety-related exchanges and **shall not** convey centralized command authority from UTM Users or service providers.

| ID | Producer | Consumer | Data Element | Description |
| :---- | :---- | :---- | :---- | :---- |
| ICD-13.3 | UASx | UASx | V2V Communication | Vehicle-to-vehicle coordination messages |

### 

### **UAM Users ⇄ Vertiport**

### **UAM Operator ⇄ UAM Vehicle**

The UAM Operator ⇄ UAM Vehicle interface **shall** provide a mechanism for bidirectional information exchange between UAM Vehicle and UAM Operator. This interface **shall** support piloted, supervised, or highly automated UAM operations while maintaining clear authority and responsibility boundaries.

UAM Vehicle (manned or unmanned) **shall** provide telemetry data through this interface to enable UAM Operators to maintain awareness of vehicle state, flight progress, and system health. Telemetry information **shall** support supervision, decision-making, and post-operation analysis. The interface **shall not** be used to provide centralized traffic separation or air traffic control services.

UAM Operators **shall** provide operation intent and mission commands through this interface to communicate approved flight intent, routing, and mission-level directives to UAM Vehicles. Operation intent **shall** be consistent with authorizations, constraints, and coordination outcomes established within the unified traffic management architecture.

Information exchanged through the UAM Operator ⇄ UAM Vehicle Aircraft interface **shall** support safe mission execution without transferring responsibility for tactical separation or airspace management to individual UAM Operators. UAM Operators **shall** retain responsibility for operational supervision and compliance, while UAM Vehicle **shall** retain responsibility for vehicle-level control and execution.

The interface **shall** preserve separation of responsibilities between humans, services, and vehicles. UAM Operators **shall not** be required to provide continuous manual control inputs unless explicitly defined by the operational concept, and UAM Vehicle **shall** be capable of maintaining safe operation in accordance with approved autonomy or piloting modes.

The UAM Operator ⇄ UAM Vehicle interface **shall** function as a critical human–vehicle coordination channel within the unified traffic management architecture, enabling safe, scalable, and passenger-capable urban and advanced air mobility operations without introducing centralized control or authority conflicts.

| ID | Producer | Consumer | Data Element | Description |
| :---- | :---- | :---- | :---- | :---- |
|  | UAM Vehicle | UAM Users | Telemetry | Vehicle state and flight data |
|  | UAM Users | UAM Vehicle | Operation Intent | Flight intent and mission commands |

### 

### **UAM Vehicle ⇄ UAM Vehicle**

The interface **shall** support vehicle-to-vehicle (V2V) communication between UAM aircraft to enable cooperative coordination, spacing, and safety-related interactions. V2V communication **shall** support local autonomy and cooperative behavior and **shall not** be used to convey centralized command authority from UAM Users or service providers.

| ICD-14.3 | UAM Vehicle | UAM Vehicle | V2V Communication | Cooperative coordination messages |
| :---- | :---- | :---- | :---- | :---- |

### 

### **UAS ⇄ UAM Vehicle**

### 

### 

### **6\. SDSPx → UTM Users**

### **7\. SDSPx → UAM Users**

### **8\. SDSPx → Vertiport**

### 

### **11\. xSU → UAM Users**

### **12\. UAM Users → xSU**

### **13\. UTM Users ⇄ UASx**

### **15\. UTM Users ⇄ UAS Operator**

The UTM Users ⇄ UAS Operator interface **shall** provide a mechanism for peer-to-peer communication between UAS Operators and UTM Users to support organizational coordination, mission management, and operational oversight of unmanned aircraft operations.

UAS Operators **shall** use this interface to communicate coordination messages, dispatch information, and operational guidance to UTM Users. These communications **shall** support mission planning, resource allocation, and operational oversight responsibilities assigned to the UAS Operator role.

UTM Users **shall** use this interface to provide operational updates, status messages, and coordination information to UAS Operators. Such communications **shall** enable the UAS Operator to maintain situational awareness of mission progress and operational status.

The interface **shall** support bidirectional peer-to-peer communication appropriate for human and organizational coordination. The interface **shall not** be used to exchange airspace authorizations, traffic separation instructions, or service-level coordination messages, which are the responsibility of Access Service Providers and Airspace Authorities within the UTM ecosystem.

Information exchanged through the UTM Users ⇄ UAS Operator interface **shall** be limited to organizational, dispatch, and operational coordination functions. This interface **shall not** bypass or replace interfaces defined for UTM service coordination, regulatory oversight, or vehicle control.

The UTM Users ⇄ UAS Operator interface **shall** preserve separation of responsibilities. UAS Operators **shall** retain responsibility for organizational management, fleet oversight, and mission coordination, while UTM Users **shall** retain responsibility for operational supervision and execution. Neither party **shall** assume traffic management or air traffic control authority through this interface.

The UTM Users ⇄ UAS Operator interface **shall** function as a supporting organizational communication channel within the unified traffic management architecture, enabling coordinated unmanned aircraft operations without introducing authority conflicts or centralized control.

| ID | Producer | Consumer | Data Element | Description |
| ----- | ----- | ----- | ----- | ----- |
| ICD-15.1 | UAS Operator | UTM Users | P2P Communication | Operator coordination and messaging |
| ICD-15.2 | UTM Users | UAS Operator | P2P Communication | Operational coordination messages |

### **16\. UAM Users ⇄ UAM Operator**

The UAM Users ⇄ UAM Operator interface **shall** provide a mechanism for direct peer-to-peer communication between UAM Operators and UAM Users. This interface **shall** support operational coordination, dispatch, and organizational communication required for UAM mission execution.

UAM Operators **shall** use this interface to communicate dispatch instructions, coordination messages, and operational guidance to UAM Users. Such communications **shall** support mission planning, resource allocation, and fleet-level coordination without assuming traffic management or airspace control responsibilities.

UAM Users **shall** use this interface to provide operational updates, status messages, and coordination inputs to UAM Operators. These communications **shall** support situational awareness, mission progress tracking, and organizational decision-making.

The interface **shall** support bidirectional, peer-to-peer communication appropriate for human and organizational coordination. The interface **shall not** be used to exchange traffic separation instructions, airspace authorizations, or service-level coordination messages that are the responsibility of Access Service Providers or Airspace Authorities.

Information exchanged through the UAM Users ⇄ UAM Operator interface **shall** be limited to organizational, dispatch, and operational coordination functions. This interface **shall not** replace or bypass interfaces defined for xSU coordination, regulatory oversight, or vehicle control.

The UAM Users ⇄ UAM Operator interface **shall** preserve separation of responsibilities. UAM Operators **shall** retain responsibility for organizational management, dispatch, and fleet oversight, while UAM Users **shall** retain responsibility for mission supervision and operational execution. Neither party **shall** assume air traffic control or traffic management authority through this interface.

The UAM Users ⇄ UAM Operator interface **shall** function as a supporting organizational communication channel within the unified traffic management architecture, enabling coordinated UAM operations without introducing authority conflicts or centralized control.

| ID | Producer | Consumer | Data Element | Description |
| ----- | ----- | ----- | ----- | ----- |
| ICD-16.1 | UAM Operator | UAM Users | P2P Communication | Operator coordination and dispatch communication |
| ICD-16.2 | UAM Users | UAM Operator | P2P Communication | Operational and status messaging |

## **6.5    System States and Modes** 

*This OCD subsection should describe, at a high level, the operational states and modes and relate them to the various operational processes and user activities. Definition of all normal operational and support states and modes, and significant off-design states and modes, will lead to completeness in the selection of operations defined in the OCD.* 

*The states and modes section will help define “how” the system operates.* 

## **6.6    System Capabilities** 

*This OCD subsection should identify and describe the capabilities to be supplied by the system as a whole. It should relate system capabilities and characteristics to specific mission and personnel needs.* 

*The capabilities section defines “what” the system will do.* 

## **6.7    System Architecture** 

*This OCD subsection should provide an overview of the system architecture, identifying the various significant system elements and their interrelationships.* 

*The system architecture section defines “what” the system consists of.* 

The unified architecture shall provide a single integrated service framework to support safe, secure, and scalable operations for uncrewed aircraft systems, eVTOL operations, and other advanced air mobility operations across applicable airspace environments.

The architecture shall comprise complementary service environments, including ATS and cooperative traffic management services, and shall support operations that transition between service environments without requiring operators to adopt incompatible service providers or information models.

The architecture shall be extensible and shall support multiple operational profiles (e.g., UTM, UAM/AAM) through configuration of domain-specific rules, service performance requirements, and cooperative operating practices, while maintaining a consistent access and interoperability model.

The architecture shall preserve separation of concerns such that:

* Service providers shall provide access, information exchange, and cooperative services consistent with approved practices; and

* the airspace authority shall retain regulatory oversight, compliance monitoring, and safety governance functions.

The architecture shall not require centralized tactical control as a prerequisite for scalability; however, it shall support escalation mechanisms and authority intervention pathways for off-nominal conditions and safety-critical events.

![][image11]

 

# 

# **7     Operational Processes** 

*This OCD section should be written from an operations point of view, describing the missions and operations as they are likely to exist, using the proposed system.* 

*This OCD section summarizes, in a prose style, the operational processes, providing a process model describing the operations which take place, the operational flow and sequence of operations, inputs and outputs and other potential risks including dependencies and concurrencies. The information in this section will, therefore, provide a dynamic description of the system characteristics and how the system will perform to accomplish the operations. Detailed scenarios for each process should be presented in Appendix B of the OCD. However, critical operational threads should be discussed in detail in this section of the OCD.* 

*The processes should normally describe the following for each operation, as applicable:* 

·       *variations in the operations for different situations, including why, when, where, who, what, and how;* 

·       *the nature and objective(s) of each operation (or activity or task);* 

·       *when an operation may occur, including the order of tasks and activities within an operation, time sequences and the likely duration(s) of the operation;* 

·       *what tasks and activities occur, what methods and techniques are used;* 

·       *the system states and modes, and configurations, for each operational process;* 

·       *how the system is used, and how it responds to achieve the objectives of the operation;* 

·       *relationships to and interactions with other operations;* 

·       *what inputs are needed for the operation;* 

·       *what outputs or outcomes are expected;* 

·       *who is involved in the operation, and who does what, including interactions between different personnel; and* 

·       *where the operation occurs.* 

*Additional information that may be included in the operational process description is:* 

·       *the level of preparedness needed (i.e., the initial state of personnel, equipment, and information) to perform the operation successfully;* 

·       *the time responses to different stimuli, especially those that stress the system; and* 

·       *why an operation may occur, including the stimulus for the operation, and rationale for specific sequences of activities or tasks including, where appropriate, references to business rules, strategy and/or tactics.* 

*The scope of the operations should include all activities in which the system will be employed, including the primary and secondary missions, various levels of maintenance, and supporting or enabling operations (which support or enable the system to be used in its missions).* 

*An indication should also be given of the importance of each operation, and the relative importance of different operations.* 

*Processes may be decomposed from high level to lower level processes.* 

*This OCD section should be structured in accordance with the needs of the OCD audience. It could be hierarchically structured, or it could just be a list of processes. Regardless of the structure chosen, the contents of this section must be related to the scenarios and the operational needs.* 

*The operations section defines “what” the system does, and, to some extent, “how” it will do it.* 

 

# 

# **8     Other Operational Needs** 

*This OCD section provides a comparison of the user/operator/customer needs with the operational capability provided by the system. It is not a description of the operational requirements, as those requirements are derived from the OCD (and other sources) subsequent to its endorsement by the customer, and derivation of those operational requirements involves a good deal more analytical activity than required to prepare the OCD.*

*For example, the identification and quantification of system performance may require extensive operational analysis and system modeling that may only be initiated in other phases of the development stage of the lifecycle.* 

*This OCD section may also contain descriptions of operational needs that complement the operations but do not readily fit into the preceding section on Operational Processes. That is, those needs which are operational but are difficult to describe in terms of process activities. Such needs may relate to security and other important quality factors.* 

*The priority of the operational needs should be documented in this section. This OCD section should provide a transition between the description of operations (Section A.7) to the system overview Section A.6, stating the mission and personnel needs that drive the requirements for the system.* 

## **8.1    Mission Needs** 

*This OCD subsection should summarize the mission needs that the system will seek to satisfy. In the event that a Mission Needs Statement or Initial Capabilities Document has already been prepared, this section provides a brief summary of that document’s contents and refers the reader to it as a source document.* 

## **8.2    Personnel Needs**

### **8.2.1    Personnel Type**

*For each type, this subsection should describe the personnel needs that the system will seek to satisfy.* 

## **8.3    Quality Factors**

*This OCD section will include a discussion of important system quality factors such as:* 

·       *Usability;* 

·       *Operability; and* 

·       *Human performance/error balance* 

*The OCD section will also discuss additional system needs such as security and privacy attributes and how the conceptual system addresses them.* 

 

# 

# **9     Analysis of the Proposed System** 

## **9.1    Summary of Advantages** 

*This OCD section provides a qualitative and quantitative summary of the advantages to be obtained from the proposed system, including new capabilities, enhanced capabilities, and improved performance, as applicable, and their relationship to any deficiencies identified in A.5.6.* 

## **9.2    Summary of Disadvantages/Limitations** 

*This OCD section provides a qualitative and quantitative summary of disadvantages or limitations of the proposed system. These disadvantages may include, as applicable, degraded or missing capabilities, degraded or less-than-desired performance, greater-than-desired use of resources, undesirable operational impacts, conflicts with user assumptions, and other constraints. Limitations may result from decisions taken during development or doctrinal inputs to the development activities.* 

*This OCD section should also discuss any adverse impacts on the environment, including the social, geopolitical, and economic environment. It should anticipate the effect of those emergent characteristics that will arise from introduction and use of the system in the environment.* 

## **9.3    Alternatives and Tradeoffs Considered** 

*This OCD section identifies and describes major alternatives considered to the system or its characteristics, the tradeoffs among them, and rationale for the decisions reached. It is not intended to be a recapitulation of the trade studies nor a report on new trade studies, but rather a summary of the findings.* 

## **9.4    Summary of Impact by Classes of Users** 

*For each class of user, this section provides a qualitative and quantitative summary of the impact of the system on that particular class of user.* 

## **9.5    Regulatory Impacts** 

*This OCD section describes any potential regulatory risks and how the system addresses or handles (mitigates) these risks. This section needs to provide an overview of the regulatory risks including who the regulators are and the scope of their authority. This section should enumerate the potential risks a regulator may have and how they relate to the system and its development, operation, and maintenance. For example, in the case of a Foreign Military Sale, this section would enumerate what the critical technologies are, where and how they are used and/or may be protected, why they are needed, who has access to them, and when they will be exported.* 

## **9.6    Other Impacts** 

*Impacts not covered in any other part of OCD Section 9 should be documented here.* 

 

# 

# **Appendix A: Acronyms, Abbreviations, and Glossary** 

*The Operational Concept Document should be written in conformance with a program-specific list of acronyms, abbreviations, and with definitions incorporated in a program-specific glossary. Should the OCD use terms not incorporated in those references, or should the references not exist at the time of the OCD creation, then document-specific acronyms, abbreviations, and a glossary should be provided here.* 

# **Appendix B: Requirements**

## **ASTM UAS Traffic Management (UTM) UAS Service Supplier (USS) Interoperability Requirements (F3548 − 21, 2025).**

| ID | Requirement |
| ----- | ----- |
| **ACM** | **The system shall follow Aggregate Operational Intent Conformance Monitoring requirements** |
| ACM0005 | For every flight conducted by an operator, within 1 day(s) of the end of the flight, a USS shall evaluate all operational intents for flights conducted by that operator either within the last 7 days of the time of evaluation or that comprise the most recent 10 flight hours by the operator, whichever includes a greater number of flights, to determine whether the conformance requirements (OPIN0005, OPIN0010) were met by the operator in aggregate over this period. |
| ACM0010 | Whenever a period of aggregate non conformance is detected (in accordance with requirement (ACM0005), the USS shall send a notification to the operator (a performance notification) within the period of time required by regulation (if applicable) or within 6 hours. |
| ACM0015 | A performance notification shall include, at a minimum, the period of time the performance notification addresses and the aggregate performance against each applicable conformance requirement (OPIN0005, OPIN0010). |
| **CMSA** | **The system shall follow Conformance Monitoring for Situational Awareness requirements** |
| CMSA0005 | A USS performing CMSA for an operational intent shall also provide Strategic Coordination for the operational intent. |
| CMSA0010 | When performing CMSA for an operational intent, a USS shall  begin conformance monitoring upon notification from UAS personnel or the operator’s automation system of commencement of flight or detection of flight in progress, whichever occurs first. |
| CMSA0015 | When conformance monitoring begins, the managing USS performing CMSA shall transition an operational intent to the Activated state if the UA is in conformance. |
| CMSA0020 | When conformance monitoring begins, the managing USS performing CMSA shall transition an operational intent to the Nonconforming state if the UA is not in conformance. |
| CMSA0025 | The managing USS performing CMSA shall provide a means for UAS personnel or the operator’s automation system to indicate that the operational intent should be transitioned from the Accepted, Activated, or Nonconforming states to the Contingent state and, for cases where UAS personnel or the operator’s automation system, or both, provides the operational intent to the USS, simultaneously supply the updated operational intent that includes appropriate off-nominal 4D volumes. |
| CMSA0030 | Upon becoming aware that an operation corresponding to an operational intent in the Activated, Nonconforming, or Contingent state has completed, the managing USS performing CMSA shall terminate conformance monitoring, transition the operational intent to the Ended state, and render the operational intent non-discoverable within 5 seconds, 95 % of the time. |
| CMSA0035 | The managing USS performing CMSA shall retain the unmodified, coordinated 4D volumes comprising an operational intent when it is transitioned to the Nonconforming state and communicate uncoordinated behavior only through off-nominal 4D volumes. |
| CMSA0040 | The managing USS performing CMSA shall  continue to provide conformance monitoring for an operational intent until the operational intent transitions to the Ended state. |
| CMSA0100 | When using position report-based detection of non conformance, a managing USS performing CMSA shall provide UAS personnel or the operator’s automation system the ability to specify the intended position reporting frequency for an operation. |
| CMSA0105 | When using position report-based detection of non conformance, a managing USS performing CMSA shall be able to ingest position data at the position reporting frequency specified by UAS personnel or the operator’s automation system. |
| CMSA0110 | When using position report-based detection of non conformance, a managing USS performing CMSA shall provide UAS personnel or the operator’s automation system the ability to specify the maximum missing position data period for an operation after which the UA must be transitioned to the Nonconforming state. |
| CMSA0115 | When performing position report-based detection of non conformance, a managing USS performing CMSA shall transition an operational intent from the Activated state to the Nonconforming state and send a notification to UAS personnel or the operator’s automation system associated with the operational intent if no position data is received from the UA for a period exceeding the operator maximum missing position data period specified by UAS personnel or the operator’s automation system within 5 seconds, 95% of the time. |
| CMSA0200 | If a managing USS performing CMSA supports an approved operator-reported method for detection of non conformance, the USS shall provide UAS personnel or the operator’s automation system a means to indicate the method is to be used for a designated operational intent. |
| CMSA0205 | If a managing USS performing CMSA supports an approved operator-reported method for detection of non conformance, for an operational intent in the Accepted or Activated states, the USS shall provide UAS personnel or the operator’s automation system a means to indicate that the operational intent should be transitioned to the Nonconforming state and simultaneously supply an updated operational intent that includes appropriate off-nominal 4D volumes. |
| CMSA0215 | If a managing USS performing CMSA supports an approved operator-reported method for detection of non conformance, the USS shall provide UAS personnel or the operator’s automation system a means to indicate the UA has reestablished conformance with the pre-nonconforming operational intent. |
| CMSA0300 | For an operational intent in the Activated state, when the managing USS performing CMSA becomes aware that the UA is outside its operational intent, the managing USS shall send a notification to UAS personnel or the operator’s automation system, add one or more off-nominal 4D volumes to the operational intent to encompass the area and time of anticipated nonconformance, and transition the operational intent to the Nonconforming state within 5 seconds, 95% of the time. |
| CMSA0305 | For an operational intent in the Nonconforming state, when the USS becomes aware that the current off nominal 4D volumes previously added to the operational intent no longer encompass the anticipated area and time of nonconformance, the managing USS performing CMSA shall update the off-nominal 4D volumes to encompass the anticipated area and time of nonconformance within 5 seconds, 95 % of the time. |
| CMSA0310 | For an operational intent in the Nonconforming state, if the managing USS performing CMSA becomes aware that the UA has reestablished conformance with the pre-nonconforming operational intent, the managing USS performing CMSA shall remove the off-nominal 4D volumes from the operational intent and attempt to reestablish it as a coordinated operational intent and transition it to the Activated state within 5 seconds, 95 % of the time. |
| CMSA0315 | If an operational intent remains in the Nonconforming state for more than 60 consecutive seconds, the managing USS performing CMSA shall transition the operational intent to the Contingent state within 5 seconds, 95 % of the time. |
| CMSA0320 | For an operational intent in the Contingent state, when the managing USS performing CMSA becomes aware that the current off-nominal 4D volumes previously added to the operational intent no longer encompasses the anticipated area and time of contingency, the USS shall update the off-nominal 4D volumes to encompass the anticipated area of and time of contingency within 5 seconds, 95 % of the time. |
| CMSA0325 | The managing USS performing CMSA shall send a notification to relevant USSs for all operational intent state transitions and all changes to the 4D volumes associated with an operational intent within 5 seconds, 95 % of the time. |
| CMSA0330 | For an operational intent in the Nonconforming or Contingent states, if the most recent position information is available for the operational intent, the managing USS performing CMSA shall respond to a request for the position information from a requesting USS with the most recent position report and the expected time at which updated position information may be available for the operational intent within 5 seconds, 95 % of the time. |
| **CSTM** | **The system shall follow Constraint Management requirements** |
| CSTM0005 | A USS performing the Constraint Manager role shall have authorization granted by a competent authority for the region. |
| CSTM0010 | A USS performing the Constraint Manager role shall only accept constraints from authorized constraint providers. |
| CSTM0015 | A USS performing the Constraint Manager role shall enable an authorized constraint provider to create a new constraint, including the type of constraint and 4D volume(s). |
| CSTM0020 | The total number of vertices across all volumes comprising a constraint shall not exceed  1000\. |
| CSTM0025 | The area across all volumes comprising a constraint shall not exceed 10000 square kilometers. |
| CSTM0030 | A USS performing the Constraint Manager role shall enable an authorized constraint provider to modify an existing constraint. |
| CSTM0035 | A USS performing the Constraint Manager role shall reject an attempt to create a constraint that restricts airspace access if the start time for any 4D volume comprising the constraint is not at least 10 minutes in the future. |
| CSTM0040 | A USS performing the Constraint Manager role shall reject an attempt to modify a constraint that restricts airspace access if any component of the modification is within 10 minutes and may invalidate strategic deconfliction performed by a relevant USS. |
| CSTM0045 | A USS performing the Constraint Manager role shall reject an attempt to create or modify a constraint if the start time for any 4D volume comprising the constraint is greater than 56 days in the future. |
| CSTM0050 | A USS performing the Constraint Manager role shall reject an attempt to create or modify a constraint if the duration of the constraint is greater than 24 hours. |
| CSTM0055 | A USS performing the Constraint Manager role shall enable an authorized constraint provider to delete designated constraints. |
| CSTM0060 | A USS performing the Constraint Manager role shall only enable the authorized constraint provider that created a constraint to modify or delete the constraint. |
| CSTM0065 | Upon becoming aware of a relevant USS performing the Constraint Processing role, a USS performing the Constraint Management role shall send the details of a new, modified, or deleted constraint to the relevant USS within 5 seconds, 95% of the time. |
| CSTM0070 | Upon receipt of a properly formed request for constraint details from a USS, a USS performing the Constraint Management role shall send the response in no more than 5 seconds, 95% of the time. |
| CSTM0075 | USS performing the Constraint Management role for constraints shall maintain an availability of 99.9%. |
| CSTM0080 | USS performing the Constraint Management role shall render constraints non-discoverable within 5 seconds following the constraint end time or an early deletion of the constraint by the authorized constraint provider. |
| CSTM0085 | A USS performing the Constraint Management role shall  send a notification to the authorized constraint provider of each instance where it could not successfully send the details of a constraint to a relevant USS within 5 seconds, 95 % of the time |
| CSTM0090 | A  USS performing the Constraint Management role shall send a notification to the authorized constraint provider following the successful creation or modification of a constraint and notification of all relevant USSs within 5 seconds, 95 % of the time |
| CSTM0095 | A USS performing the Constraint Management role shall only modify a constraint or transition a constraint to the Valid state if the USS makes the resulting constraint discoverable by relevant USSs. |
| **CSTP** | **The system shall follow Constraint Processing requirements** |
| CSTP0005 | Before a managing USS performing the Constraint Processing role creates or modifies an operational intent, the USS shall notify UAS personnel or the operator’s automation system, providing the details of all constraints that intersect that operational intent. |
| CSTP0010 | When a managing USS performing the Constraint Processing role is unable to provide UAS personnel or the operator’s automation system with the details of all relevant constraints that intersect an operational intent, the USS shall send a user notification within 5 seconds, 95 % of the time. |
| CSTP0015 | For the entire time an operational intent is in the Activated, Nonconforming, or Contingent states, a managing USS performing the Constraint Processing role shall maintain awareness of new or modified constraints relevant to that operational intent. |
| CSTP0020 | When a managing USS performing the Constraint Processing role is notified of a constraint that intersects an operational intent it manages, the USS shall send a user notification providing the details of the intersecting constraint within 5 seconds, 95 % of the time. |
| CSTP0025 | Before a USS performing the Constraint Processing role creates or modifies an area of interest defined by the end user, the USS shall notify the end user providing the details of all constraints that intersect with that area of interest. |
| CSTP0030 | When a USS performing the Constraint Processing role is unable to provide the end user with the details of all relevant constraints that intersect an area of interest defined by the end user, the USS shall send a notification to the end user within 5 seconds, 95 % of the time. |
| CSTP0035 | When a USS performing the Constraint Processing role is notified of a constraint that intersects an area of interest defined by the end user, the USS shall send a notification to the end user providing the details of the intersecting constraint within 5 seconds, 95 % of the time. |
| **DSS** | **The system shall follow DSS requirements** |
| DSS0005 | A DSS implementation supporting the services defined in this specification shall, at a minimum, include the following interfaces for use by USSs, in accordance with the DSS portion of the OpenAPI specification presented in [utm.yaml](https://github.com/astm-utm/Protocol/blob/v1.0.0/utm.yaml): (1) createOperationalIntentReference / updateOperationalIntentReference /  getOperationalIntentReference / deleteOperationalIntentReference — these interfaces enable a USS to create, update, retrieve, or delete an operational intent entity reference in the DSS. (A USS can only change operational intent entity references it created.) (2) searchOperationalIntentReferences — this interface enables a USS to query a specified geographic area and time range of interest. All relevant operational intent entity references are returned. (3) createConstraintReference / updateConstraintReference / getConstraintReference / deleteConstraintReference — these interfaces enable a USS to create, update, retrieve, or delete a constraint entity reference in the DSS. (A USS can only change constraint entity references it created.) (4) queryConstraintReferences — this interface enables a USS to query a specified geographic area and time range of interest. All relevant constraint entity references are returned. (5) createSubscription / updateSubscription / getSubscription, deleteSubscription — these interfaces enable a USS to create, update, retrieve, or delete a subscription for a specified geographic area and time range of interest, and returns all operational intent references and constraint references relevant to that subscription at the time of the call. (A USS can only change or view subscriptions it created.) |
| DSS0010 | After mapping and storing operational intent or constraint entity reference information into the DSS Airspace Representation, the DSS shall not store or otherwise retain the precise geographical extents of the associated 4D volume(s) |
| DSS0015 | A DSS instance shall authenticate USSs using an industry-standard authentication mechanism. |
| DSS0020 | Communication between a USS and DSS instances shall be encrypted using an industry-standard encryption mechanism with a minimum encryption strength of 128 bits. |
| DSS0030 | A DSS implementation shall minimally include the following interfaces for use by Net-RID Service Providers and Display Providers, in accordance with the DSS portion of the OpenAPI specification presented in [astm\_rid\_api\_2.1](https://github.com/uastech/standards/tree/astm_rid_api_2.1): (a) PUT Identification Service Area — this interface enables a Net-RID Service Provider to create or modify an ISA entity summary in the DSS. (b) DELETE Identification Service Area — this interface enables a Net-RID Service Provider to delete an existing ISA entity summary from the DSS. (A Net-RID Service Provider can only delete ISAs it created.) (c) PUT Subscription—this interface creates a subscription for new or modified ISAs within a 4-D volume, and returns the intersecting ISAs resident in the DSS at the time of the call. (d) DELETE Subscription—this interface enables a Net-RID Display Provider to delete a subscription from the DSS. (A Net-RID Display Provider can only delete subscriptions it created.) (e) GET Subscription—this interface enables a Net-RID Display Provider to retrieve the details of a specific existing subscription to verify its existence and composition. (A Net- RID Display Provider can only retrieve subscriptions it created.) (f) GET Subscriptions—this interface enables a Net-RID Display Provider to retrieve the details of all existing subscriptions it created. |
| DSS0040 | After mapping and storing ISA summary information into the DSS Airspace Representation, the DSS shall not store or otherwise retain the precise geographical extents of the associated 4D volume. |
| DSS0050 | The DSS shall not allow more than 10 subscriptions per USS in a given area of the DSS Airspace Model. |
| DSS0060 | The DSS shall limit the duration of subscriptions to no more than 24 hours. |
| DSS0070 | The DSS shall be implemented in a manner that allows a USS to access any instance of a DSS pool and obtain the same results |
| DSS0100 | A DSS implementation shall minimally include the following interfaces, in accordance with the DSS portion of the OpenAPI specification presented in [utm.yaml](https://github.com/astm-utm/Protocol/blob/v1.0.0/utm.yaml): (1) setUssAvailability / getUssAvailability — these interfaces enable a USS performing availability arbitration to indicate the availability status of a USS to the DSS, or check the current DSS understanding of the availability of a USS. (2) makeDssReport — this interface enables a USS to report a problem to the DSS that might otherwise go unnoticed. |
| DSS0110 | When synchronizing data, a DSS instance shall authenticate with other DSS instances in the same region using an industry-standard authentication mechanism. |
| DSS0120 | Communication between DSSs in the same region shall be encrypted using an industry-standard encryption mechanism with a minimum encryption strength of 128 bits. |
| DSS0200 | When synchronizing data, a DSS instance shall authenticate with other DSS instances in the same pool using an industry-standard authentication mechanism. |
| DSS0205 | Communication between DSSs shall be encrypted using an industry-standard encryption mechanism with a minimum encryption strength of 128 bits. |
| DSS0210 | DSS implementations shall store and synchronize the following data: (**1**) For each subscription: (a) A unique ID for the subscription; (b) The manager of the subscription; (c) A means by which a USS contacts the subscriber to inform them of new information; (d) The general area in which the subscription is relevant (perhaps by means of a set of DAR cell IDs); (e) Start and end time of the subscription; (f) Version of the subscription (to enable consistent read-modify-write operations); (g) An indication of what types of entity references are relevant to the subscription;  (h) An indication for whether this subscription was created automatically to support an operational intent; (i) The notification count for the subscription (used by a USS to detect missed notifications). (**2**) For each entity reference: (a) A unique ID for the entity, (b) The manager of the entity, (c) A means by which a USS contacts the managing USS to obtain the details of the entity, (d) The operational intent state, if the entity is an operational intent, (e) The general area in which the entity is located (perhaps by means of a set of DAR cell IDs), and (f) The start and end time of the entity. (**3**) For each USS with a known availability state as indicated by a USS performing availability arbitration: (a) The identity of the USS, (b) The availability state of the USS, and (c) The version of the availability state |
| DSS0215 | DSS implementations shall only respond to the USS after the transaction has been recorded in the DAR. |
| DSS0300 | DSS implementers shall provide a test instantiation of their DSS implementation for use by USSs when needed for interoperability testing. When not conducting a test of a new release candidate, this test instantiation must use the currently deployed version of the implementer’s DSS software and be configured to perform DSS-DSS synchronization with other DSS instances in the test environment DSS pool of a DSS region. |
| **GEN** | **The system shall follow general requirements.** |
| GEN0005 | USSs performing any of the roles identified in this specification shall be implemented and operated under an ISO/IEC 27001-compliant Information Security Management System or equivalent. |
| GEN0010 | USSs performing any of the roles identified in this specification shall be implemented and operated under an ISO/IEC27701-compliant Privacy Information Management System or equivalent. |
| GEN0015 | USSs performing any of the roles identified in this specification shall be implemented and operated under an ISO/IEC 9001-compliant Quality Management System, or equivalent. |
| GEN0100 | USSs shall synchronize their time to within 5 seconds of an industry recognized time source 99% of the time. |
| **GEN0105** | **USSs shall use synchronized time for all timestamps.** |
| GEN0200 | USSs shall permanently delete data received from other USSs within 24 hours except when the data is required to be retained by the competent authority for a longer period of time to support incident analysis or the archival of incident analysis packages. |
| GEN0300 | USS providers shall provide an interoperability test instance of their implementation for use by other USSs when needed for interoperability testing. |
| GEN0305 | An interoperability test instance shall use the currently deployed version of the implementer’s USS software except when testing an update to the implementer’s USS software. |
| GEN0310 | An interoperability test instance shall provide a means for injection or generation of test data in a geographic test location. |
| GEN0400 | If a USS is unable to perform its intended function, the USS shall send a user notification no more than 5 seconds, 95% of the time. |
| GEN0405 | A managing USS shall send a use notification to UAS personnel or an operator’s automation system associated with an operational intent for all state transitions of that operational intent within 5 seconds, 95 % of the time. |
| GEN0500 | For detecting conflicts between two operational intents or intersections between an operational intent and a constraint, a USS shall compute intersections of the 3D, geospatial components of 4D volumes with a precision such that two 3D volumes with more than 1 centimeters of true overlap are indicated as intersecting, and two 3D volumes separated by more than 1 centimeters at their closest points are indicated as not intersecting. |
| **LOG** | **Requirements specific to logging.** |
| LOG0005 | USSs shall timestamp all logged data in UTC time without local adjustments. |
| LOG0010 | Timestamps for logged data shall correspond to the time at which the associated event occurred. |
| LOG0015 | USSs shall log outgoing messages sent to other USSs and the DSS, and the responses to those messages. |
| LOG0020 | USSs shall log incoming messages received from other USSs and the responses to those messages. |
| LOG0025 | USSs shall log instances where an expected response to a request is not received. |
| LOG0030 | USSs shall log all instances of interaction required by this specification with UAS personnel, end users, or the operator’s automation. |
| LOG0035 | USSs shall be capable of exporting logged data applicable to the USS roles they perform to the common export formats described in Annex A3. |
| LOG0040 | USSs that manage operational intents shall log data that associates an operator with operational intents that are made discoverable. |
| LOG0045 | USSs shall log instances where an operational intent could not be planned or replanned due to conflicts with other operational intents or constraints. |
| LOG0050 | USSs performing conformance monitoring shall log all position data used for conformance monitoring that is ingested from the UA. |
| LOG0055 | USSs performing Constraint Management shall log data that allows the authorized constraint provider to be associated with all constraints that transition to the Valid state. |
| **OPIN** | **The system shall follow Operational Intents requirements** |
| OPIN0005 | Operational intents shall be constructed such that the UA’s actual position is outside an operational intent in the Activated state no more than 18 times per flight hour, each excursion having a duration of no more than 10 seconds. |
| OPIN0010 | Operational intents shall be constructed such that the UA’s actual position is inside an operational intent in the Activated state at least 95 percent of total flight time. |
| OPIN0015 | Operational intents in the Accepted and Activated states shall specify coordinated volumes only and must not include off-nominal 4D volumes. |
| OPIN0020 | The total number of vertices across all volumes comprising an operational intent shall be limited to 10000\. |
| OPIN0025 | The managing USS shall only modify an operational intent or transition an operational intent to the Accepted, Activated, Nonconforming, or Contingent states if the managing USS can make the resulting operational intent discoverable by relevant USSs. |
| OPIN0030 | An operational intent shall only transition to the Accepted state no more than 30 days of the start time of the operation. |
| OPIN0035 | A USS shall only modify or render non-discoverable operational intents that it created. |
| OPIN0040 | If an operational intent is canceled by the UAS personnel or an operator’s automation system prior to activation, the managing USS shall transition an operational intent from the Accepted state to the Ended state and render the operational intent non-discoverable no more than 5 seconds, 95% of the time. |
| **SCD** | **The system shall follow Strategic Conflict Detection requirements.** |
| SCD0005 | A managing USS shall apply the lowest bound priority status to any relevant operational intent in the Accepted state for which the relevant USS is determined to be down and does not respond to a request for the details of an operational intent. |
| SCD0010 | A managing USS shall apply the highest priority status defined by the regulator to any operational intent in the Activated, Nonconforming, or Contingent states for which the relevant USS is determined to be down and does not respond to a request for the details of the operational intent. |
| SCD0015 | A managing USS shall verify that an operational intent does not conflict with a higher priority operational intent before transitioning it to the Accepted state. |
| SCD0020 | A managing USS shall verify that an Accepted operational intent that is modified while remaining in the Accepted state does not conflict with higher priority operational intents before the modification is executed. |
| SCD0025 | A managing USS shall verify that before transitioning an operational intent to the Activated state, it does not conflict with a higher priority operational intent. |
| SCD0030 | A managing USS shall verify that an Activated operational intent that is modified while remaining in the Activated state does not conflict with a higher priority operational intent before the modification is executed unless the conflict already existed at the time the modification was initiated. |
| SCD0035 | A managing USS shall verify that before transitioning an operational intent to the Accepted state, it does not conflict with an equal priority operational intent when regulation does not allow conflicts within the same priority level. |
| SCD0040 | A managing USS shall verify that an Accepted operational intent that is modified while remaining in the Accepted state does not conflict with an equal priority operational intent before the modification is executed when regulation does not allow conflicts within the same priority level. |
| SCD0045 | A managing USS shall verify that an operational intent does not conflict with an equal priority operational intent before transitioning it to the Activated state when regulation does not allow conflicts within the same priority level. |
| SCD0050 | A managing USS shall verify that an Activated operational intent that is modified while remaining in the Activated state does not conflict with an equal priority operational intent before the modification is executed when regulation does not allow conflicts within the same priority level unless the conflict already existed at the time the modification was initiated. |
| SCD0055 | When a managing USS creates a new operational intent and detects a conflict with an operational intent of the same priority, and regulation allows conflicts within that same priority level, that USS that manages the conflicting operational intent within 1 second, 95 % of the time. |
| SCD0060 | When a managing USS modifies an Accepted operational intent that remains in the Accepted state and detects a conflict with an operational intent of the same priority and regulations allow conflicts within that same priority level, that USS shall send a notification to the USS that manages the conflicting operational intent within 1 second, 95 % of the time. |
| SCD0065 | When a managing USS transitions an operational intent to the Activated state and detects a conflict with an operational intent of the same priority, and regulations allow conflicts within that same priority level, that USS shall send a notification to the USS that manages the conflicting operational intent within 1 second, 95 % of the time. |
| SCD0070 | When a managing USS modifies an Activated operational intent that remains in the Activated state and detects a conflict with an operational intent of the same priority, and regulations allow conflicts within that same priority level, that USS shall send a notification to the USS that manages the conflicting operational intent within 1 second, 95 % of the time. |
| SCD0075 | Upon receipt of a properly-formed request for the details of an operational intent from another USS, the relevant managing USS shall send the requested data in no more than 1 second, 95 % of the time. |
| SCD0080 | For the entire time an operational intent is in the Activated, Nonconforming, or Contingent states, the managing USS shall maintain awareness of new or modified operational intents relevant to the managed operational intent. |
| SCD0085 | Upon receipt of a notification that an operational intent may be relevant to a subscription, the managing USS shall send the data for the operational intent to the subscribing USS in no more than 5 second, 95% of the time. |
| SCD0090 | When a managing USS creates or modifies an operational intent that conflicts with another operational intent, that USS shall send a notification reporting the conflict to UAS personnel or the operator’s automation system associated with the new or modified operational intent within 5 seconds, 95% of the time. |
| SCD0095 | When a managing USS becomes aware that a new or modified operational intent conflicts with an existing operational intent it manages, that USS shall send a notification reporting the conflict to UAS personnel or the operator’s automation system associated with the operational intent within 5 seconds, 95% of the time. |
| SCD0100 | A managing USS shall only transition an operational intent to the Nonconforming and Contingent states if it is also serving the role of CMSA. |
| **USS** | **The system shall follow UAS service supplier requirements** |
| USS0005 | A USS shall make entities discoverable using the DSS. |
| USS0105 | USS performing the Strategic Coordination role shall, at a minimum, support the following interfaces for use by peer USS, in accordance with the peer-to-peer (P2P) portion of the OpenAPI specification provided in [utm.yaml](https://github.com/astm-utm/Protocol/blob/v1.0.0/utm.yaml): (1) getOperationalIntentDetails — this interface enables a USS to request the details of operational intents from the managing USS. (2) getOperationalIntentTelemetry — this interface enables a USS to request position data, if available, for off-nominal UAS operations (that is, operational intents in the Nonconforming or Contingent states) from the managing USS. |
| USS0110 | A USS performing the Constraint Management role shall, at a minimum, support the following interfaces for use by USSs performing the Constraint Processing role, in accordance with the P2P portion of the OpenAPI specification provided in [utm.yaml](https://github.com/astm-utm/Protocol/blob/v1.0.0/utm.yaml): (1) getConstraintDetails — this interface is called by a relevant USS when it needs details of a specified constraint entity from the managing USS. (2) notifyConstraintDetailsChanged — this interface is called by a managing USS after the DSS informs it that a peer USS has a subscription relevant to a new, modified, or deleted constraint entity. (3) makeUssReport — this interface is called by a USS when the requesting USS encounters an issue with the hosting USS that might otherwise go unnoticed or unreported. |

## **ASTM Remote ID and Tracking Requirements (F3411− 22a, 2025\)** 

| ID | Requirement |
| ----- | ----- |
| **BB4** | **The system shall follow** **specific Bluetooth Legacy (4.x compatible) Requirements** |
| BB40010 | These broadcast messages shall be “un-coded” and conform to Bluetooth Core Specification 5.0, Volume 6, Part B, Sections 2.1 and 2.3.1. |
| BB40030 | Legacy Advertising Frames shall be encoded as illustrated and Table 14\.  |
| **BB5** | **The system shall follow specific Bluetooth 5 Long Range Requirements** |
| BB50010 | If implementing this specification using Bluetooth 5 Long Range, Legacy (ADV\_NONCONN\_IND) advertisements must be sent, as described in Bluetooth Legacy (4.x compatible) Transport Method, for backwards compatibility with less capable receivers. |
| BB50020 | Bluetooth 5 Extended Advertisements (ADV\_EXT\_IND \+ AUX\_ADV\_ IND) must be sent as well at the same rate as Dynamic Data (see Update Rates).  |
| BB50030 | Bluetooth 5 Extended Advertisements must be sent on a LE Coded (S=8) PHY. |
| BB50040 | These messages shall conform to Bluetooth Core Specification 5.0, Volume 6, Part B, Section 2.2 (LE Coded PHY, S=8). |
| BB50050 | The Bluetooth 5 Extended Advertisement Primary Packet shall be broadcast through all 3 beacon channels, followed by the Secondary packet on the remaining channels. |
| BB50060 | The Pointer Frame shall be encoded as described in Fig. 8 and Table 15\. |
| BB50070 | The Aux Ptr Field in the Primary Packet shall be implemented in accordance with Bluetooth Core Specification 5.0, Volume 6, Part B, Section 2.3.4.5 with the following guidance in Table 16\. |
| BB50100 | This packet shall be encoded according to the Common Extended Advertising Format described in Bluetooth Core Specification 5.0, Volume 6, Part B, Section 2.3.4 with the values included in Fig. 9 and Table 17\. |
| BB50110 | Additionally this packet Adv Data payload shall use the “Message Pack” (Message Type 0xF) format described in 5.4.5.22, Fig. 9, and in Table 13\. |
| BB50120 | No more than 9 messages shall be included in a single Message Pack. |
| **BMG** | **The system shall follow specific to broadcast messages Requirements.** |
| BMG0010 | Each message shall be 25 bytes in length (padded with nulls as needed).  |
| BMG0020 | Each message shall begin with a 1 byte header followed by 24 bytes of data. |
| BMG0030 | Non-magnitude values, strings, or IDs that may be or may not be numerical (such as the Unique ID) shall be expressed in Network Byte Order which reads in a left to right, most significant byte (MSB) to least significant byte (LSB) order.  |
| BMG0040 | Magnitude values expressed as 16 or 32 bit integers (such as Latitude, Longitude, Altitude, etc.) shall be expressed as “little endian” (marked as “LE” in the “Message Details” tables below), where the LSB is on the left and the MSB is on the right |
| BMG0050 | Optional fields within messages being sent shall be filled in as stated in the corresponding block message format and if opting out, or the value is unknown, shall be filled with nulls (0s) for string values or 0 for numeric unless an alternate default/unknown value representation is stated in Table 1\. |
| BMG0060 | All ASCII Strings shall be filled with nulls in the unused portion of the field. |
| BMG0065 | Table 2 shall be used to encode to those enumerations. |
| BMG0070 | The message header includes the Message Type and Protocol Version and shall be sent in each message. |
| BMG0080 | Unique ID shall default to the Manufacturer Serial number. |
| BMG0090 | Once the UA is provisioned, the UAS ID shall be one of the following: |
| BMG0091 | The UAS ID shall be Manufacturer Serial Number expressed in the ANSI/ CTA-2063-A Serial Number format. |
| BMG0092 | The UAS ID shall be a Civil Aviation Authority (CAA) issued Registration ID for the UA formatted as described in Table 1\. |
| BMG0093 | The UAS ID shall be a UTM Assigned ID if operating within a UTM system (128-bit UUID) binary encoded, Network Byte Order. |
| BMG0094 | The UAS ID shall be a Specific Session ID according to the registered Session ID Type (see Annex A5). |
| BMG0095 | The first byte of the Specific Session ID must be the Specific Session ID Type (1–255) where 0 is reserved, 1–224 is the registered type, and 225–255 are available for private experimental use only |
| BMG0100 | The transmitted data shall be encoded according to Table 7\. |
| BMG0110 | Any fields that require a flag bit to be set shall be set according to Table 7\. |
| BMG0120 | If no authentication is used, and this message is still being sent (which is not required), the Auth Type shall be set to 0 and the Signature shall be empty. |
| BMG0130 | When a signature is required, the signature produced by a UAS shall be encoded to match the signature format expected by the verifier. |
| BMG0135 | If the AuthType is 5 (Specific Authentication Method), then the first byte of the first page of authentication data must be the Specific Authentication Method Type (1-255) where 0 is reserved, 1-224 is the registered type, and 225-255 are available for private experimental use only. |
| BMG0140 | When UAS ID (1) or Operator ID (2) is set as the AuthType, then the Message Signature shall include the corresponding data and TimeStamp from the Authentication message in the signature |
| BMG0150 | If the AuthType is set to Message Set (3), then the Signature shall include the concatenation (in message type order) of all other transmitted message types (excluding this Authentication message), and TimeStamp from this Authentication message. |
| BMG0160 | The Data Page shall be incremented (starting from 0\) for each additional message required to complete the oversized message. |
| BMG0161 | The Length field shall specify the exact length in bytes of the authentication payload data. |
| BMG0170 | AuthType 3 (Message Set) shall only be used when the transport media can send all of the pages together, such as Bluetooth 5 or Wi-Fi. |
| BMG0180 | If the AuthType is 4 (Network Remote ID), then the Authentication Data/Signature shall be empty (all nulls). |
| BMG0190 | If the GCS has a dynamic location source (for example, GNSS), then the Operator Location fields shall be the current location information of the GCS as acquired from the dynamic source. |
| BMG0200 | If the GCS cannot obtain dynamic location data, then the Operator Location fields shall be the aircraft’s takeoff location. |
| BMG0210 | Minimum update frequency shall be the same as static messages. |
| BMG0220 | If a group of aircraft is being represented, the number of aircraft, radius of flight area centered on the Location/Vector Message latitude/longitude, and group operations ceiling and floor shall be expressed in this message using the Area fields. |
| BMG0230 | If one or more UA are non-equipped, the Area fields shall be used to declare (by means of broadcast messages compliant with this section) a volume of operation by a device external to the UA (such as a ground station) centered on the Location/Vector Message latitude/longitude. |
| BMG0240 | If the value for one or more fields is unknown, that field shall be filled as specified in Table 1\. |
| BMG0250 | When using the message pack, all message types being sent shall be sent together in one or more message packs and shall be sent at a periodicity of at least the dynamic message rate in accordance with Update Rates for message packs that contain dynamic data |
| **BUR** | **The system shall follow specific Broadcast Update Rate Requirements.** |
| BUR0005 | Update requirements shall be applied to each sector. |
| BUR0010 | For broadcast messages, dynamic messages (as indicated in the block message section) shall be sent at least every 1 second(s). |
| BUR0020 | Static messages (as indicated in the block message section) shall be sent at least every 3 second(s) |
| BUR0030 | the maximum potential time elapsed since the time of applicability of the dynamic fields in the Location/Vector Message shall be no older than 1 second. |
| BUR0040 | the system shall make a “best effort” to transmit when the saturation level allows. |
| BUR0050 | the Message Counter (for that message type) shall be incremented and reset to 0 after 0xFF is reached. |
| BUR0060 | the Message Counter shall be the same for each page in the page set. |
| **BWF** | **The system shall follow specific connectionless broadcast mechanisms that can be implemented using Wi-Fi Management Frames encapsulating Open Drone ID messages requirements.** |
| BWF0010 | For better interoperability with handheld device SDKs, Messages shall be encoded within the Service Discovery Frame based on the Neighbor Awareness Networking (NAN) Specification. |
| BWF0020 | For UAS implementing this protocol broadcast frame, a “management” (type 0), ”beacon” (subtype 8), and “action” (subtype 13\) frame as prescribed by the IEEE 802.11-2016 Part 11 Wi-Fi specification shall be encoded as NAN Service Discovery Frames as described in the NAN Specification. |
| BWF0030 | The values shall be filled as described in the NAN Service Discovery Frame Diagram in Fig. 10 and NAN Service Discovery Frame Details Table 18\. |
| BWF0032 | Beacon frames called NAN Synchronization beacons shall be transmitted at 6 Mbps inside NAN Discovery Windows (DWs) used for NAN timing synchronization. |
| BWF0034 | The values of each beacon frame field shall be filled as described in Table 19\. |
| BWF0036 | NAN Synchronization beacon frames shall be followed by Vendor Specific Public Action frames encoded as NAN Service Discovery Frames (SDF) within the DWs. |
| BWF0040 | All message types being sent shall be sent using message pack(s) described in 5.4.5.22, Fig. 9, and in Table 13\. |
| BWF0050 | the Cluster ID (defined in NAN Specification) shall be a static value of “50-6F-9A-01-00-FF”. This is to facilitate the receiver to get Remote ID messages from multiple UAS in parallel. |
| BWF0060 | The mandatory NAN Service Descriptor Attribute shall ) be included in the NAN SDF frames. |
| BWF0070 | The field value of Master Performance shall be 0xFE |
| BWF0080 | Random Factor shall be 0xEA to allow multiple receivers to receive DRI messages in parallel. |
| BWF0090 | In order to allow operation of NAN Discovery, broadcasting shall  operate in channel 6 (2.437 GHz) in the 2.4 GHz frequency band and may optionally operate in channel 149 (5.745 GHz) in the 5 GHz band. |
| BWF0100 | The transmission interval of the consecutive NAN Service Discovery frames shall meet the requirements of the update rate for dynamic or static messages. |
| BWFB | Requirements Specification on a connectionless broadcast mechanism can be implemented using Wi-Fi Management Frames encapsulating Open Drone ID messages. |
| BWFB0010 | in implementing the Remote ID Wi-Fi Beacon Transport method, either a single channel (channel 6\) or any beacon channels shall be used. |
| BWFB0020 | For UAS implementing this protocol, a standard 802.11 Beacon frame, which is a “management” (type 0), “beacon” (subtype 8), frame as prescribed by the IEEE 802.11-2016 Part 11 specification shall encode the Remote ID message pack as a vendor-specific information element IE221 (using OUI: FA-0B-BC, Vendor Type: 0x0D) payload as described in Fig. 12 and Table 20\. |
| BWFB0030 | The broadcast message shall be transmitted on any Wi-Fi channel of the 2400 MHz to 2483 MHz band; and according to the beacon frame standard as defined in the IEEE 802.11 standard. |
| BWFB0032 | The broadcast message shall be transmitted on any Wi-Fi channel of the 5150 MHz to 5895 MHz band; and according to the beacon frame standard as defined in the IEEE 802.11 standard. |
| BWFB0034 | The broadcast message shall be transmitted on a single “social” Wi-Fi Channel on 2.4 G band (Channel 6\) or 5 GHz band (Channel 149). |
| BWFB0040 | The message broadcast interval shall be \<= 200 TU. |
| BWFB0050 | The message broadcast interval shall be \<= 200 TU. |
| BWFB0060 | The broadcast message broadcast interval shall meet the minimum requirements of the update rate for dynamic and static messages. |
| **DSS** | **The system shall follow DSS requirements.** |
| DSS0015 | A DSS instance shall authenticate USSs using an industry-standard authentication mechanism. |
| DSS0020 | Communication between a USS and DSS instances shall be encrypted using an industry-standard encryption mechanism with a minimum encryption strength of 128 bits. |
| DSS0030 | A DSS implementation shall minimally include the following interfaces for use by Net-RID Service Providers and Display Providers, in accordance with the DSS portion of the OpenAPI specification presented in https://github.com/uastech/standards/tree/astm\_rid\_api\_2.1: (a) PUT Identification Service Area — this interface enables a Net-RID Service Provider to create or modify an ISA entity summary in the DSS. (b) DELETE Identification Service Area — this interface enables a Net-RID Service Provider to delete an existing ISA entity summary from the DSS. (A Net-RID Service Provider can only delete ISAs it created.) (c) PUT Subscription—this interface creates a subscription for new or modified ISAs within a 4D volume, and returns the intersecting ISAs resident in the DSS at the time of the call. (d) DELETE Subscription—this interface enables a Net-RID Display Provider to delete a subscription from the DSS. (A Net-RID Display Provider can only delete subscriptions it created.) (e) GET Subscription—this interface enables a Net-RID Display Provider to retrieve the details of a specific existing subscription to verify its existence and composition. (A Net- RID Display Provider can only retrieve subscriptions it created.) (f) GET Subscriptions—this interface enables a Net-RID Display Provider to retrieve the details of all existing subscriptions it created. |
| DSS0040 | After mapping and storing ISA summary information into the DSS Airspace Representation, the DSS shall not store or otherwise retain the precise geographical extents of the associated 4D volume. |
| DSS0050 | The DSS shall not allow more than 10 subscriptions per USS in a given area of the DSS Airspace Model. |
| DSS0060 | The DSS shall limit the duration of subscriptions to no more than 24 hours. |
| DSS0070 | The DSS shall be implemented in a manner that allows a USS to access any instance of a DSS pool and obtain the same results |
| DSS0205 | Communication between DSSs shall be encrypted using an industry-standard encryption mechanism with a minimum encryption strength of 128 bits. |
| **NET** | **The system shall follow specific network requirements** |
| NET0010 | UAS shall authenticate with Net-RID Service Providers using an industry-standard authentication mechanism.  |
| NET0020 | Communication between UAS and Net-RID Service Providers shall be encrypted using an industry standard encryption mechanism with a minimum encryption strength of 128 bits. |
| NET0030 | The Net-RID Service Provider shall notify the operator of a Networked UAS if the UAS is not providing necessary data to participate in Network Remote ID. |
| NET0040 | If dynamic data (for example, position updates) are not being received from a UAS at a frequency of 1 Hz at least 20% of the time, the Net-RID Service Provider shall notify the operator.  |
| NET0110 | Net-RID Service Providers that support Intent-Based Network Participants shall provide the ability for the operator of an Intent-Based Network Participant to submit, modify, or delete an operation plan. |
| NET0120 | Net-RID Service Providers shall require authentication of operators using an industry-standard authentication mechanism when operation plans are submitted for Intent-Based Network Participants.  |
| NET0130 | Communications between the Intent-Based Network Participants operator interface and a Net-RID Services Pro vider shall be encrypted using an industry-standard encryption mechanism with a minimum encryption strength of 128 bits. |
| NET0210 | Net-RID Display Providers shall authenticate with Net-RID Service Providers using an industry standard authentication mechanism. |
| NET0220 | Communications between Net-RID Display Providers and Net-RID Services providers shall be encrypted using an industry-standard encryption mechanism with a minimum encryption strength of 128 bits.  |
| NET0230 | A Net-RID Display Provider shall request Remote ID data from a Net-RID Service Provider only for areas in which end users are currently requesting information by means of the Remote ID Display Applications services.  |
| NET0240 | A Net-RID Display Provider shall request relevant UAS Remote ID information from a Net-RID Service Provider by specifying a rectangular area with a diagonal no greater than 7 km. |
| NET0250 | A Net-RID Service Provider shall provide an error code or message and no Remote ID data in response to a request when the diagonal specifying the rectangular area is greater than 7 km. |
| NET0260 | When the diagonal for the requested area is within the limit, the Net-RID Service Provider(s) shall provide relevant Remote ID data for the requested rectangular area in no more than 1 second 95% of the time and in 3 seconds 99% of the time. |
| NET0270 | For each applicable UA, near-real-time position information shall include: (a) All position reports in the requested area up to 60 seconds in the past.  (b) For each time a UA entered the requested area during 60 seconds, the last position report received outside of the request area.  (c) For each time a UA exits the requested area during 60 seconds, the first position report received outside of the requested area.  |
| NET0280 | If a networked UAS temporarily loses network connectivity, a Net-RID Service Provider may derive and supply location information from UAS operation plan extrapolation to Net-RID Display Providers until network connectivity is reestablished and updated location information is received from the UAS. |
| NET0290 | Net-RID Service providers shall not provide extrapolated location information to Net-RID Display Providers for a UAS if network connectivity with the UAS exists and location information is being received.  |
| NET0300 | The Net-RID Service Provider shall inform Net-RID Display Providers when flight plan extrapolation is being used to supply position information for a UAS. |
| NET0310 | When flight plan extrapolation is used to supply position information for a UAS, the Net-RID Service Provider shall characterize the accuracy of the extrapolated location data using the Vertical Accuracy and Horizontal Accuracy of Position data fields. |
| NET0320 | If a networked UAS loses connectivity and the associated Net-RID Service Provider is unable to provide extrapolated position data, the Net-RID Service Provider shall provide to a requesting Net-RID Display Provider the most recent position report and an indication that current data is not being received. |
| NET0330 | Net-RID Display Providers shall retain data obtained from Net-RID Service Providers for no longer than 86,400 seconds. |
| NET0410 | Communications between Net-RID Display Providers and Remote ID Display Applications shall be encrypted using an industry-standard encryption mechanism with a minimum encryption strength of 128 bits. |
| NET0420 | A Net-RID Display Provider shall respond to the initial request from a Remote ID Display Application for position data for all UAS in an area with a diagonal no greater than 7 km in 1 seconds 95% of the time and in 3 seconds 99% of the time. |
| NET0430 | A Net-RID Display Provider shall provide an error code or message and no Remote ID data in response to a request from a Remote ID Display Application for an area with a diagonal greater than 7 km. |
| NET0440 | A Net-RID Display Provider shall respond to subsequent requests (that is, requests after the initial request) from a Remote ID Display Application for UAS Remote ID for an area previously requested within the past 5 seconds with a diagonal no greater than 7 km in 1 seconds 95 % of the time and in 3 seconds 99 % of the time. |
| NET0450 | When responding to valid requests for Remote ID data from a display application, a Net-RID Display Provider shall provide the most recent data available that is relevant, aggregated from all applicable Net-RID Service Providers. Relevant data includes information consistent with the common data dictionary described in Table 1 and, if requested by the Net-RID Display Application, near-real-time position information for UAs that are currently in the requested area or that were in the area up to 60 seconds prior, including Intent-Based Network Participants.  |
| NET0460 | A Net-RID Display Provider shall respond to requests from a Display Application for flight details for a specific UAS within an area with a diagonal equal to or less than 2 km in 2 seconds 95% of the time and in 6 seconds 99% of the time. |
| NET0470 | A Net-RID Display Provider shall provide access to required and optional fields defined in Table 1 to Remote ID Display Applications. |
| NET0480 | For a display area with a diagonal greater than 7 km and less than 2 km, a Net-RID Display Provider shall cluster UAs in close proximity to each other using a circular or polygonal area covering no less than 15% percent of the display area size and associating a count of the UAs in the cluster.  |
| NET0490 | For a display area with a diagonal greater than 7 km and less than 2 km, a Net-RID Display Provider shall reduce the precision of location information for individual UAs that are not included in a cluster. This is to be accomplished using a circular or polygonal area with a radius or distance to the polygon edge of no less than 300 m, randomly offset from the actual UA location (but always encompassing the UA location), and associating a UA count of 1 with the area.  |
| NET0610 | A Net-RID Service Provider shall make all UAS operations discoverable for Network Remote ID purposes by means of one or more ISAs in the DSS for the complete duration of each operation plus 60 seconds. |
| NET0620 | If a Net-RID Service Provider is unable to make a UAS operation discoverable through the creation of an ISA in the DSS, the Net-RID Service Provider shall notify the operator. |
| NET0630 | A Net-RID Display Provider shall obtain ISA information from the DSS (including creating or maintaining an ISA subscription) only for areas in which an end user is currently requesting information by means of the Remote ID Display Applications it services. |
| NET0710 | A Net-RID Service Provider shall minimally support the following interfaces for use by Net-RID Display Providers, in accordance with the P2P (peer-to-peer) portion of the OpenAPI specification provided in [https://github.com/uastech/standards/tree/astm\_rid\_api\_2.1](https://github.com/uastech/standards/tree/astm_rid_api_2.1): (1) GET flights: this interface enables a Net-RID Display Provider to request the position-related Remote ID data (if any) for UAS operating in one or more volumes. (2) GET flight details: this interface enables a Net-RID Display Provider to request the additional non-position-related details (for example, UAS ID, UAS type, etc.) for a specific UAS operation. |
| NET0720 | A Net-RID Display Provider shall query a Net-RID Service Provider for flights only for areas in which end users have requested information by means of the Remote ID Display Applications it services. |
| NET0730 | Net-RID Display Provider shall (NET0730) minimally support the following interface for use by Net-RID Service Providers, in accordance with the P2P (peer-to-peer) portion of the OpenAPI specification provided in https://github.com/uastech/standards/tree/astm\_rid\_api\_2.1: (1) POST Identification Service Area: this interface is called by a Net-RID Service Provider when the DSS informs it that a Net-RID Display Provider has a subscription for an area intersecting a new, modified, or deleted ISA |
| NET0740 | When a Net\_RID Service Provider is informed by the DSS that a Net-RID Display Provider has a subscription for an area intersecting a new, modified, or deleted ISA, the Net-RID Service Provider shall send the details of the ISA to the Net-RID Display Provider (by invoking the Post Identification Service Area interface) in 1 second 95 % of the time and in 3seconds 99 % of the time. |
| **VF** | **Requirements specific to Verifier Service** |
| VF0010 | The verifier service shall implement the signature verification algorithm that matches the agreed signature format that will be sent by the broadcaster. |
| VF0020 | The verifier service shall set up a web service |
| VF0030 | The response time of the verifier shall be less than 1 seconds 95 % of the time from receipt of the verified request message to the transmission of the result. |
| VF0040 | The Verifier API shall implement a RESTful/JSON protocol on a web server with a TLS secured endpoint as described by the Verifier API OpenAPI Description in https://github.com/opendroneid/authentication-verifier-api/tree/auth\_1.1. |
| VF0050 | The verifier shall maintain a testing end-point. |
| VF0060 | The ResultCode and ResultString values shall be set in the verifier response given the conditions in Table A1.2. |

## **ASTM Detect and Avoid System Performance Requirements (F3442−25, 2025\)**

| ID | Requirement |
| ----- | ----- |
| 5.1.1 | This section identifies the set of objectives that the DAA system, including the human pilot if required to be “in the loop,” shall satisfy as a complete unit. |
| 5.2.1 | If required by the CAA, the proponent shall provide to the CAA or CAA-approved test organization, or both, evidence of physical verification demonstrating the DAA system meets all required performance criteria identified or generated in response to this specification. |
| 5.2.3 | When physical performance is impractical (for example, difficult corner cases, extensive time-based testing, or sheer volume of test case permutations) the analysis or simulation shall still be substantiated using a sampling of physical test data to establish validity. |
| 5.3.6.2 | The manufacturer shall be responsible for a hazard/ risk assessment specifically for their DAA\_SS as showing in Fig. 2\. |
| 5.3.6.3 | The manufacturer’s documentation shall include the mitigations identified in the DAA\_SS hazard and risk assessment. |
| 5.3.7.2 | The DAA system integrator shall complete a safety analysis that encompasses all types of failure modes that can adversely impact the effectiveness of the system, such as those listed in Table X4.8. |
| 5.3.7.3  | The DAA systems integrator shall ensure the OHRA mitigations are included in the documentation provided to the operator. |
| 5.4.3 | The RR and LR performance requirements in this section shall be verified using a statistically significant number of encounters that are representative of the operational environment airspace. |
| 5.4.3.1 | Limitations on the DAA equipment shall be identified based on limitations of the encounter set(s) used to verify the performance requirements. |
| 5.4.4.1 | For encounters with intruders equipped with ADS-B Out, the DAA system RR shall be ≤0.18. |
| 5.4.4.2 | For encounters with non-cooperative or transponder-only intruders, the DAA system RR shall be ≤0.30. |
| 5.4.5.1 | For intruders equipped with ADS-B Out, the DAA system LR shall be ≤0.40. |
| 5.4.5.2 | For non-cooperative or transponder-only intruders, the DAA system LR shall be ≤0.50. |
| 5.5.2.1 | The approach to system availability here is derived from the JARUS process for SORA V2.0 Annex D, section 5.4 (TMPR (Tactical Mitigation Performance Requirement) Robustness (Integrity and Assurance) Assignment). |
| 5.5.2.2 | For Class 1 equipment (to be used in operational volumes with low air risk), the allowable loss of function and performance shall be less than 1 per 100 flight hours (1E-2 Loss/FH). |
| 5.5.2.3 | For Class 2 equipment (to be used in operational volumes with medium air risk), the allowable loss of function and performance shall be less than 1 per 1000 flight hours (1E-3 Loss/FH). |
| 5.5.3.1 | The approach to system assurance here is derived from the JARUS process for SORA. |
| 5.5.3.2 | For Class 1 equipment (to be used in operations in low air risk airspace), the allowable introduction of hazardously misleading information shall be less than 1 per 1000 flight hours (1E-3 Loss/FH). |
| 5.5.3.3 | For Class 2 equipment (to be used in operations in medium air risk airspace), the allowable introduction of hazardously misleading information shall be less than 1 per 10000 flight hours (1E-4 Loss/FH). |
| 5.5.5.1 | The DAA system shall employ a consistent time basis across all functions for marking the time of applicability of measurements and calculated parameters (for example, GPS, UTC). |
| 5.5.5.2 | The DAA system timing, if based on GPS, shall be resilient to GPS failures. |
| 5.6.1.1 | If required, the DAA system shall have a maintenance plan and maintenance schedule in accordance with the maintenance instructions provided by the manufacturer. |
| 5.6.1.1.1 | The maintenance instructions shall provide direction as to verification of proper installation and calibration of the system to ensure continued performance is met in the field. |
| 5.6.2 | The DAA system shall have a test function for detecting foreseeable “static” system failures. |
| 5.6.3 | The DAA system shall detect and notify the PIC of any degradation or loss of function that requires PIC action or take predefined automated contingency action to mitigate the risk if required by the operational safety case, within a timeframe appropriate for the alerting condition. |
| 5.6.3.1 | Failures without means of detection should be identified during system design, and the DAA system as a whole shall comply with the requirements for availability (5.5.2) and assurance (5.5.3). |
| 5.6.3.2 | The DAA system shall persist the notification of degradation or loss of function until the functionality is fully restored. |
| 5.7.1 | The PIC shall be notified of any changes to DAA software, hardware, or configuration. |
| 5.7.2 | Making any changes to DAA software, hardware, or configuration shall be restricted to authorized and qualified personnel. |
| 5.7.3 | Any changes to DAA software, hardware, or configuration shall require confirmation that the modified information is correct and uncorrupted. |
| 5.7.4 | There shall be a means to prevent any changes to the DAA software, hardware, or configuration from inadvertently or maliciously occurring, or a suitable preflight check to detect such changes and prevent takeoff if such changes were to occur. |
| 5.7.5 | The DAA system architecture shall prevent unauthorized access to the DAA system during operation. |
| 5.8.1 | The DAA system shall satisfy performance requirements across the range of environmental conditions as defined by the manufacturer and communicated to the customer. |
| 5.8.2 | The DAA system integrator shall identify all environmental limitations of the system where it does not meet the performance requirements and document them in the operator’s manual and technical specifications documents. |
| 6.1 | The DAA system integrator shall perform a timing analysis that identifies the timing elements for the DAA system. |
| 6.2 | The timing elements shall be reflected in the test methods used to show that the DAA system supports the required risk ratios when operated in accordance with the DAA System CONOPS in the representative airspace defined in Generalized Air Risk Assessment Descriptions (5.3.4). |
| 7.2.2 | Upon detecting the presence of an intruder, the DF shall determine the track of the intruder as required by the alert function (A1F) to identify and prioritize hazards. |
| 7.2.3  | The DF shall output the track(s) of all detected intruders to the A1F. |
| 7.2.4.2 | If track coasting is implemented in the DF, the DF shall designate any track for which the intruder was not detected in the last surveillance cycle as a coasted track and report the time coasted (that is, the time since the last known detection). |
| 7.2.4.2.1 | Else, the DF shall drop the track for any track that was not detected in the current surveillance cycle. |
| 7.2.4.3 | If track coasting is implemented in the DF, the DF shall drop tracks whose coasting time is longer than a configurable parameter set by the DAA integrator. |
| 7.2.5.1 | The DF track output shall include the computed uncertainty parameters (often a covariance matrix) for each report of each track. |
| 7.2.5.2 | The DF uncertainty shall be computed as the accumulated uncertainty of the track estimation, the measurement uncertainty and, if implemented, track coasting. |
| 7.3.1 | The maximum number of targets that can be tracked simultaneously without violating the DF timing budget, as described in Timing Appendix, shall be identified. |
| 7.3.1.1 | The maximum number of aircraft tracks passed on to the A1F so as not to violate assumptions concerning PIC workloads nor violate good human factors engineering considerations shall be identified. |
| 7.3.1.2 | This maximum number shall be demonstrated to be sufficient to meet LR and RR requirements given the air vehicle traffic rates in the operational environment, the rates for false tracks (for example, sensor noise and ground clutter), and the rates for tracks of non-interest (for example, real tracks on non-aircraft objects such as cars, birds, clouds). |
| 7.3.2  | The FOV/FOR of each sensor shall be identified in terms of azimuth and minimum/maximum angular elevation or coverage volume. |
| 7.3.2.1 | This coverage shall be demonstrated to meet the overall DAA system RR and LR performance requirements, and that the FOV/FOR meet any operational minimum coverage requirements. |
| 7.3.3 | The detection and usable track range(s) needed from the DF for relevant intruders (as defined by the encounter models) to provide sufficient detection performance to meet overall system RR and LR requirements shall be identified. |
| 7.3.3.1 | The DF shall detect intruders out to the range(s) identified above for each sensor across its full FOV/FOR. |
| 7.3.4 | The DF shall be demonstrated to acquire and maintain an intruder track of acceptable quality to meet LR and RR requirements for the relevant intruders (as defined by the encounter models) expected in the operational volume. |
| 7.3.4.1 | This detection sensitivity shall be demonstrated across the combined FOV/FOR and range(s) of the DF. |
| 7.3.5 | The precision of the track necessary to meet LR and RR requirements shall be identified and demonstrated. |
| 7.3.5.1 | This precision shall be included in the determination of the maximum detection ranges required of each sensor, as defined in Range. |
| 7.3.6 | The aggregate accuracy of the sensor(s) shall be identified and demonstrated to be sufficient to ascertain the position and velocity of an intruder to the level necessary to meet the required LR and RR.  |
| 7.3.7 | The DF shall meet all the performance requirements of this specification in the presence of interference, noise, and clutter sources found within the operational environment as specified in interference, ambient noise and clutter. |
| 7.3.7.1 | Possible sources of interference, ambient noise, and clutter, based on the sensor modalities used, shall be identified and documented. |
| 7.3.8.1 | The effects of the false alarms on the risk ratios RR and LR shall be included in the determination of the risk ratios LR and RR. |
| 7.3.8.2 | The manufacturer shall define all common sources of false alarms and should minimize the contribution of each alarm to overall performance. |
| 7.4.1 | The DF shall provide an indication when BITs and configuration checks are complete, and detection/tracking of intruders is available or, conversely, when the system is not available. |
| 7.4.2 | In the event of a midflight restart, the A1F shall be continuously alerted to the loss of function until such time as the DF resumes detection of intruders. |
| 8.2.1 | The A1F shall issue an alert for an intruder if it determines that the UA must maneuver to remain well clear from that intruder. |
| 8.2.1.1 | At a minimum, this alert shall be declared early enough to permit resolution of the hazard (within the appropriate LoWC and MAProxy risk ratio thresholds) and no later than the occurrence of loss of well clear. |
| 8.2.1.2 | For a pilot-in-the-loop system, this alert shall be annunciated as a warning-level alert in accordance with AC 25.1322-1, Section 6(b), indicating that immediate pilot awareness is required, and immediate pilot action is required. |
| 8.2.2.1 | If implemented a lower-priority alert for a pilot-in-the-loop system, these alerts shall be annunciated as advisory or caution-level alerts in accordance with AC 25.1322-1. |
| 8.2.2.2 | A high-priority determines that the UA must maneuver to avoid MACproxy with that intruder. If implemented, this alert shall be declared early enough to permit resolution of the hazard (within the appropriate MACproxy risk ratio threshold) and no later than the occurrence of MACproxy.  |
| 8.2.2.2.1 | If implemented for a pilot-in-the-loop system, this alert shall be annunciated as a warning-level alert in accordance with AC 25.1322-1, indicating that pilot action is required but distinguished in some manner from the minimum A1F alert. |
| 8.2.3.1 | At a minimum, the A1F shall pass the alert status (on/off or alert level for systems implementing multiple alert levels) of each intruder to the A2F. |
| 8.2.4 | For an ownship not flying according to a pre-determined flight plan or forced to temporarily deviate from its flight plan, the A1F shall calculate the alerts using the current position and velocity vector of the ownship. |
| 8.2.5 | The A1F shall calculate warning-level alerts using the stated estimates (for example, position and velocity) of the intruder derived solely on data received from the DF up to the current time. |
| 8.2.6 | The A1F shall update alerts and targets in the following prioritized order consistent with AC 25.1322-1 Flightcrew Alerting: (1) Warning-level alerts; (2) Caution-level alerts (if implemented); (3) Advisory alerts (if implemented); (4) Other detected traffic. |
| 8.2.7 | For alerts of the same priority level, the A1F shall further prioritize the alerts by a criterion associated with reduced collision risk, such as by increasing order of time to Closest Point of Approach (CPA). |
| 8.2.8 | For an intruder meeting the criteria of multiple alerts (for example, both caution and warning-level alert criteria), the A1F shall assign the highest priority alert to the intruder based on the priority rules in this section. |
| 8.2.9.2 | If the A1F implements track coasting, the A1F shall not use an intruder’s registered flight plan for extrapolation because the intruder could deviate from the flight plan at any time. |
| 8.2.9.3 | If the A1F implements track coasting, a maximum coasting time shall be identified such that the appropriate MACproxy and LoWC risk ratios are still achieved. |
| 8.2.9.4 | The A1F shall provide alerts on any tracks that have been coasted for less than the identified maximum coast time in the same manner as current tracks (that is, in accordance with prioritized order). |
| 8.2.9.5 | The A1F shall generate no alerts on coasted tracks exceeding the maximum coast time. |
| 8.2.9.6 | The A1F shall pass no information on coasted tracks exceeding the maximum coast time to the A2F. |
| 8.3 | The A1F shall output the updated alert status of an intruder no later than tClassify \+ tNotify (as discussed in Appendix X2) after receiving new data on the intruder from the DF and subject to the timing analysis required in System Timing (6.1). |
| 8.4.2 | At a minimum, all traffic meeting the alerting conditions in a lower-priority alert and, if implemented, additional levels of alerting shall be displayed as appropriate for the mission CONOPS. |
| 8.4.3 | The DAA traffic display shall provide traffic information appropriate to the DAA system CONOPS for each displayed traffic element. |
| 8.4.4 | The traffic display shall not display traffic coasted beyond the maximum coasting time in accordance with Alerting on Coasted Tracks requirements. |
| 8.4.5 | The traffic display shall use the following colors to present alert information (see AC 25.1322-1). |
| 8.4.8 | Warning-level alerts shall include distinct aural indications (also known as “aural alert”). |
| 8.4.8.1 | If implemented, caution-level alerts shall include an aural indication distinct from that for a warning-level alert. |
| 8.4.8.2 | If the capability to inhibit or suppress aural alerts has been implemented, the display shall indicate to the PIC when the aural alerts have been inhibited or suppressed. |
| 8.4.10 | If the DAA implementation includes a traffic display for the operator, the DAA system shall coast the tracks for the current alerting cycle to a consistent time reference.  |
| 9.2.2 | In the presence of one or more actionable alerts, the A2F shall calculate maneuver guidance to increase horizontal or vertical minimum separation, or both, from the identified intruder(s) with the goal of separating by at least the well clear boundary from each intruder. |
| 9.2.2.1  | If well clear, the A2F shall identify a maneuver or succession of maneuvers that will reduce the likelihood of loss of well clear. |
| 9.2.2.2 | If well clear separation is lost or cannot be maintained, the A2F shall identify a maneuver or succession of maneuvers that will reduce the likelihood of MACproxy and will regain well clear separation. |
| 9.2.2.3 | If a MACproxy occurs or cannot be avoided, the A2F shall identify a maneuver or succession of maneuvers that will reduce the likelihood of MAC and will regain well clear. |
| 9.2.2.4 | In computing avoidance maneuvers, the A2F shall take into account the performance capabilities of the ownship aircraft. |
| 9.2.3 | Any information necessary for the pilots to perform A2F tasks expected of them in accordance with the CONOPS shall be displayed, even if the A2F function is automatic. |
| 9.3.1 | The A1F and A2F shall update provided information at a rate commensurate with the timing analysis. |
| 9.3.2 | At a minimum, the A2F shall identify an avoidance maneuver in a time sufficient for the maneuver to be executed such that loss of well clear and MACproxy are avoided within the respective risk ratio thresholds. |
| 10.1 | The system shall recreate the events leading up to a MACproxy or other incident and to ascertain how the DAA system affected the incident. |
| 10.2.1 | The DAA system shall include a log generation function for post-incident analysis. |
| 10.2.2 | At a minimum, the DAA system shall log all intruders that have entered the alert threshold during operation of the DAA system. |
| 10.2.3 | The DAA system shall update the data in the log no less than 1 per second. |
| 10.2.4 | The DAA system shall record in the log all parameters supplied by the DF regarding the intruder (see 8.2.3 for the minimum set of parameters the DF must capture for each detected target). |
| 10.2.6 | The DAA system shall timestamp each logged entry so as to establish the exact chronology of events. |
| 10.2.7 | For each logged entry, the DAA system shall record enough data to establish a precise chronology of events to support incident investigation as well as continued maturation of the DAA System. |
| 10.2.8 | The DAA system shall record the Incident log in a non-volatile memory such that all parameters are easily recovered when disconnected from its power source. |

## **ASTM Performance for Weather Information Reports, Data Interfaces, and Weather Information Providers (WIPs) Requirements (F3673− 23, 2025\)**

| ID | Requirement |
| ----- | ----- |
| **4** | **Significance and Use** |
| 4,3 | Providers publishing weather data or services for sale or for use by users shall be qualified. |
| **5** | **Weather Data Performance Requirements** |
| 5.2.1 | Data exchange formats shall be JSON/GeoJSON compliant. |
| 5.2.2 | WIPs shall meet cyber-security requirements in accordance with ISO/IEC 27001\. |
| 5.2.3 | WIPs shall use OpenAPI to define data exchange requirements. |
| **5.3** | **Standard of Performance for Weather Data Tiering** |
| 5.3.1 | The industry shall use standard industry methods for detecting thunderstorms and lightning. |
| 5.3.1.4 | All Tier 3 data shall have metadata with quantification of accuracy tier for use in risk management. |
| 5.3.1.4.1 | Lightning detection and strike information shall meet prescribed accuracy in 5.3.1.4(1) and 5.3.1.4(2). |
| 5.3.2 | All Tier 2 data shall have metadata with quantification of accuracy rates for use in risk management. |
| 5.3.3 | All Tier 1 data shall have metadata with quantification of accuracy rates for use in risk management. |
| **5.3.6** | **Point Weather Data Sets** |
| 5.3.6.1 | Each point data set shall have metadata with quantification of accuracy rates for use in risk management. |
| 5.3.6.2 | Each point data set shall have a time stamp associated with each data parameter. |
| **5.3.7** | **Area or Volume Weather Analysis** |
| 5.3.7.1 | The area or volume weather analysis shall annotate a time stamp associated with each data parameter with the earliest time of the first data measurement used in the weather analysis for each parameter. |
| 5.3.7.2 | If the area or volume weather analysis is model based, the time stamp shall be the time when the weather model analysis is complete. |
| **5.4** | **WIP Service Reliability Performance Requirements** |
| 5.4.1 | WIPs shall provide weather information that is up to date and reliable to support the user consistent with the standard of performance per this specification. |
| **5.4.2** | **Weather Information Updates** |
| 5.4.2.1 | Upon receipt of updated weather information related to current weather, the WIP shall make it available to the user. |
| 5.4.2.2 | If regularly scheduled weather information reports are unavailable for more than 15 min past scheduled time, the WIPs shall inform the user that the information is not up to date. |
| 5.4.2.3 | The WIP shall ensure the data being shared are the latest or most recent available dataset from the source. |
| **5.4.3** | **Weather Data and Service Reliability** |
| 5.4.3.1 | The WIP shall notify all users of outages or if falling outside of weather data tier tolerance in any component of the WIP services if unresolved within 15 min, or unless end users decide to opt out of notifications based on a service level agreement. |
| 5.4.3.2 | At the request of the user, the WIP shall inform the user of the source of the data if the WIP is not the originating source. |
| 5.4.3.3 | The WIP shall provide a confidence level for weather data originating from sensors or derived weather analysis products to capture and validate accuracy rates. |
| 5.4.3.4 | The WIP that provides weather alert and notification services |
| 5.4.3.4.1 | Shall provide weather alerts in accordance with user agreements |
| 5.4.3.4.2 | Shall provide a weather alert that exceeds weather event thresholds within 5 min. |
| 5.4.4 | The WIP shall implement appropriate procedures to guarantee the integrity of the data to the user and adhere to them. |
| 5.5 | The location of the observation shall be indicated using one of the following methods:The ICAO designator, the location based on World Geodetic System 1984 coordinates, or the proper vertiport designator. |
| 5.6 | Shall be indicated in UTC time. |
| **6** | **Quality Control Measures and Metrics** |
| 6.1 | WIPs shall maintain quality control measures and metrics to ensure data sets generated by the WIP and made available to other WIPs and users. |
| 6.1.1 | The WIP shall implement a continuous data health and monitoring system to identify weather data, aggregated by parameter, which falls outside the required targeted accuracy under the data tier published by the WIP. |
| 6.1.2 | The WIP continuous data health and monitoring system checks shall include time, location, parameters, and representativeness to surrounding information within the area. |
| 6.1.3 | The WIP continuous data health and monitoring system shall identify when a regularly published weather information report is late to dissemination by more than 15 min. |
| 6.1.4 | The WIP continuous data health and monitoring system shall identify when a weather alert for a user threshold is late to dissemination by more than 5 min. |
| 6.1.5 | The WIP shall complete a report weekly that quantifies the overall confidence level of each weather data parameter for the specified one-week period for the data tier published by the WIP. |
| 6.1.6 | The WIP shall compile and publish a quarterly report, publicly. |
| 6.1.6.1 | The WIP report shall document the number of events the continuous health and monitoring system identified in which weather data, aggregated by parameter, did not meet the required target accuracy for the advertised weather data tier; |
| 6.1.6.2 | The WIP report shall document the percent of instances when weather data sets, aggregated by parameter, did not meet the required target accuracy for the advertised weather data tier; |
| 6.1.6.3 | The WIP report shall document the percent of instances a regularly published weather information report was late to dissemination by more than 15 min |
| 6.1.6.4 | The WIP report shall document the percent of instances when a weather alert meeting a user threshold was late to dissemination by more than 5 min |
| 6.1.6.5 | The WIP report shall document weekly metric reports that quantified the overall confidence level of each weather data parameter for each specified one-week period for the data tier published by the WIP |
| 6.1.6.6 | The WIP report shall publish the methodology used to measure required target accuracy and determining confidence level for all weather data sets. |
| **7** | **Qualifying Weather Data Sets** |
| 7.1 | Any WIP that provides weather data sets from any sources other than ASOS and AWOS, PIREPS, and government weather radar data sets, available in the NAS, shall comply with the standard of weather data performance parameters in 7.3 – 7.6. |
| 7.2 | Any WIP that produces weather analysis models shall comply with the standard of weather data performance parameters in 7.3 – 7.6 |
| 7.3 | Weather data sets used by WIPs shall demonstrate their ability to meet one of the three-tiered performance criteria or be rated non-tiered. |
| 7.3.1 | The data associated with each weather parameter from a data source shall be categorized into Tiers 1, 2, or 3 and include a metadata stamp to provide proof of quantification demonstrating its tier. |
| 7.3.2 | Once the data source is entered into the system with a performance tier, the WIP shall ensure that the data source is validated and ensure that data from the data source continue to meet the accuracy performance requirements of its data performance tier. |
| 7.4 | Government and commercial models shall have for each grid box associated metrics that describe the data tier of the data used for the weather analysis. |
| 7.4.2 | Each grid point shall have metadata depicting what sensor or sensor type was used to quantify the accuracy of the data with a confidence level.  |
| 7.4.2.1 | An inability to quantify a grid point because of no sensor data available shall have accompanying metadata indicating the accuracy of the grid point and confidence level is unknown and stamped as non-tiered data. |
| **7.5** | **Time Synchronization** |
| 7.5.1 | The WIP shall synchronize their system time to within 1 s with a Stratum-1 time server as described in IETF RFC 5905\. |
| 7.5.2 | WIPs shall use synchronized time to 1 s or better for all timestamps |
| 7.6 | Data that are derived through various methods shall undergo testing and demonstration using the methods described in 7.3 – 7.5. |
| 7,7 | Data that are obtained via remote sensing shall undergo testing and demonstration using scientific methods appropriate to the type of remotely sensed data provided. |
| 7.7.1 | Measurements from remotely sensed data sets that are affected by differing atmospheric conditions shall include metadata descriptions of atmospheric conditions that will degrade accuracy and confidence level. |
| **8** | **Data Retention** |
| 8.1 | WIPs that use commercial datasets within the WIP service offerings shall have service level agreements with third-party service providers that ensure the third-party service provider retains the proprietary data that are used within the WIPs services for three months or the WIP retains the third-party proprietary data for three months. |
| 8.1.1 | At a minimum, WIPs shall arrange to retain any data used by users to make flight management decisions.  |

## **ASTM Operational Risk Assessment of Unmanned Aircraft Systems Requirements (F3178 − 24, 2025\)**

| Id | Text |
| :---- | :---- |
| 6.2 | Hazards shall be identified and documented through a process that fits the needs of the organization |
| **7** | **Safety Risk Analysis** |
| 7.1 | Following hazard identification, a safety risk analysis shall be performed. |
| 7.2 | Likelihood and severity definitions shall be appropriate for the system and operation, and are commonly adopted from approved CAA sources (for example, FAA Order 8040.4C, FAA Order 8040.6A). |

## **ASTM Vertiport Design Requirements (F3423/F3423M− 22, 2025\)**

| ID | Requirements |
| ----- | ----- |
| **5** | **Vertiport General Requirements** |
| 5.1 | A vertiport site shall consider the need to ensure safe approaches and departures of all aircraft for which it is designed to support. |
| 5.1.1 | Vertiports shall have an appropriate written Emergency Action Plan (EAP) in place. |
| 5.1.2 | Each facility shall have a functioning wind cone in the case of any manned operations or an alternative means of communicating real-time active winds to the operator of an unmanned aircraft or directly to the controlling operations system of an autonomous aircraft. |
| 5.1.2.1 | The wind cone shall provide the onboard pilot with valid wind direction and speed information in the vicinity of the vertiport under normal and typical wind conditions during approach, landing, and ground operations. |
| 5.1.2.3 | To avoid presenting an obstruction hazard, the wind cone shall be located outside the safety area, so it does not penetrate the approach/departure or transitional surfaces. |
| 5.1.2.4 | At a vertiport intended for night operations, the wind cone shall be illuminated, either internally or externally, to ensure it is clearly visible. |
| 5.1.4 | Grading of the vertiport, that is, the slope of a vertiport’s surface, shall be designed so as to protect, that is, slope down and away from, at a minimum, the primary egress path, passenger holding area, rooftop hangars, and fire protection activation systems such that in the event of a fuel spill the fuel will flow away from these areas. |
| 5.1.4.7 | All load-bearing surfaces that an aircraft will rest on or traverse across shall meet International Building Code, 6 International Fire Code, 6 and NFPA9 standards. Due to its malleability and susceptibility to deformation in high-temperature environments, asphalt susceptible to this type of deformation should be avoided as a load-bearing surface.  |
| 5.1.5 | The TLOF shall be designed and constructed to support the static and dynamic loads of the design aircraft and the static weight of any ground support vehicles or equipment. |
| 5.1.5.1 | Areas outside the TLOF area to be utilized for the purposes of aircraft parking, aircraft movement, aircraft refueling, and aircraft recharging shall be designed to support the static weight of the design aircraft.  |
| 5.1.6 | A vertiport shall have smooth, well-drained, operational areas with sufficient stability to permit the safe movement of aircraft along all adjoining surfaces that an aircraft may need to transition. |
| 5.2 | All vertiport construction shall be communicated to the authority having jurisdiction prior to construction commencing. |
| 5.4 | All Vertiports shall be assigned a permanent identifier in accordance with aviation authority policy for identification in the airspace system for all recognized operational and management purposes. |
| 5.5 | At a minimum, VFR Vertiports shall be accurately referenced through accepted survey practices by latitude and longitude to within 620 ft \[6 m\] horizontal accuracy and 63 ft \[1 m\] vertical accuracy. |
| 5.5.1 | In accordance with aviation authority policy, all IFR vertiports shall be accurately referenced through governing and applicable survey practices by latitude and longitude in accordance with the IFR procedures to be associated with the Vertiport. |
| 5.6 | All Vertiport information shall be checked, evaluated, and updated by the owner as appropriate as new information becomes available or old information is changed. |
| 5.6.1 | At a minimum, all vertiport information shall be verified and updated on an annual basis or more frequently if required by the civil aviation authority. |
| 5.8 | For simultaneous operations to be conducted, the following criteria shall be met: |
| 5.8.1 | The distance between independent landing/takeoff positions shall be sufficient to provide for safe operations, taking into account aircraft wake turbulence, airspace protection, aircraft emergency operations, and traffic avoidance. |
| **6** | **Vertiport Dimensional Standards** |
| 6.3 | Given the variability in aircraft and aircraft design reflecting the latest technological advancements in the aviation industry, specifically VTOL platforms, the dimensional criteria should be based on the largest CD, for example, overall length or overall width, whichever is greater. This shall also include making accommodations for the unfolding/folding of wings, rotors, or combinations thereof, associated with normal operations. |
| 6.3.1 | Minimum TLOF shall be no less than 1.0 × CD of the largest design aircraft. |
| 6.3.2 | Minimum FATO shall be no less than 1.5 × CD of the largest design aircraft. This dimension does not include a rejected takeoff area. |
| 6.3.3 | Minimum Safety Area shall be at least 1⁄3 CD of the largest design aircraft but not less than 10 ft \[3 m\]. |
| 6.3.4.1 | In a situation where a VTOL aircraft creates a downward flow of exhaust gases that impact the vertiport surface, the surface shall be noncombustible and resistant to deformation and heat stress. |
| 6.3.5 | All applicable building and fire codes shall be followed as it applies to electrical systems, wiring, grounding, charging, storage, and human interaction. |
| 6.3.6 | If it is not feasible to provide adequate separation and coverage for the prevailing winds through multiple approach/departure paths, operational limitations shall be developed and implemented as needed. |
| **6.3.7** | **Airspace Availability** |
| 6.3.7.1 | In identifying a vertiport’s approach/departure paths, TLOF, FATO, and Safety Areas, all obstructions in the vicinity of the Vertiport shall be evaluated for compliance. |
| 6.3.7.1.1 | Obstruction shall not penetrate any of the aforementioned imaginary surfaces. |
| 6.3.8 | Vertiport owners shall work to protect all “imaginary surfaces” and airspace as defined in this section from penetration and encroachment. |
| 6.3.8.2 | The approach surface shall begin at each end of the Vertiport primary surface (FATO) with the same width as the primary surface and extends outward and upward for a horizontal distance of 4000 ft \[1219 m\] where its width is 500 ft \[152 m\].  |
| 6.3.8.2.1 | The slope of the approach surface shall be 8:1 for civil VTOL aircraft. |
| 6.3.8.3 | These surfaces shall extend outward and upward from the lateral boundaries of the primary surface and from the approach surfaces at a slope of 2:1 for a distance of 250 ft \[76 m\] measured horizontally from the centerline of the primary and approach surfaces.  |
| **6.4** | **TLOF Design and Marking** |
| 6.4.1 | The TLOF perimeter shall be identified with a 12 in. \[30.5 cm\] solid white line. |
| 6.4.1.1 | Vertiport Symbol shall be centered on TLOF. |
| **6.4.2** | **Load Bearing** |
| 6.4.2.1 | The TLOF and any load-bearing surfaces shall be designed and constructed to support the loads imposed simultaneously by the design aircraft and any ancillary ground support vehicles and equipment. |
| 6.4.2.2 | For design purposes, the design static load shall be equal to the aircraft’s maximum takeoff weight applied through the total contact area of the aircraft’s wheels or skids. |
| 6.4.2.3 | For design purposes, the dynamic load shall be assumed to be 150 percent, 1.5 × the maximum takeoff mass (MTOM) of the design aircraft. |
| 6.4.2.3.1 | When specific loading data is not available, 75 percent of the weight of the design aircraft shall be used and applied equally through the contact area of the two rear wheels (or the pair of rear wheels of a dual-wheel configuration) of wheel-equipped aircraft. |
| 6.4.2.3.2 | For a skid-equipped aircraft, 75 percent of the weight of the design aircraft shall be applied equally through the aft contact areas of the two skids of a skid-equipped aircraft. |
| **6.5** | **Taxiway Design and Marking** |
| 6.5.3 | If the vertiport operator intends for the facility to support night operations, it shall be lighted as described in 6.5.3.1 – 6.5.3.6. |
| 6.5.3.4 | A minimum of three light fixtures per side of a square or rectangular TLOF shall be incorporated. |
| 6.5.3.4.1 | A light shall be located at each corner, with additional lights uniformly spaced between the corner lights.  |
| 6.5.3.4.2 | A circular TLOF shall be defined by using an even number of lights, with a minimum of eight, uniformly spaced around the TLOF |
| **6.6** | **FATO Placement** |
| **6.6.3** | **Elevated Vertiports** |
| 6.6.3.1 | Parking positions shall be designed to provide a minimum distance of no less than 1⁄4 the controlling dimension between the outermost structure of the largest design aircraft that a particular position is designed to support and any object, building, safety area, or other parking position. |
| 6.6.3.1.4 | The passenger approach to the aircraft shall be clearly identified to prevent passengers from contact with rotors, propellers, or other moving aircraft parts. |
| 6.6.3.1.5 | For night operations, adequate illumination shall be maintained for passengers, crew, and ground personnel operating around the aircraft. |
| 6.7 | A FATO shall be located such that there are no intrusions of the FATO or its adjoining safety area by any building or parking position. |
| 6.9 | Fuel and Fuel Storage |
| 6.9.1.2 | If fuel is provided at a Vertiport, applicable fire, environmental, and zoning regulations shall be complied with for the local municipality and authority having jurisdiction. |
| 6.9.1.3 | For vertiports that only service those aircraft that rely solely on electrical propulsion without any form of liquid fuel or fuel cell technology, applicable fire, environmental, and zoning regulations shall be complied with for the local municipality and authority having jurisdiction. |
| 6.9.1.4 | In those cases where an energy storage system is incorporated to provide an auxiliary power source for the charging of aircraft to compensate for peak power grid utilization, these devices shall meet all applicable regulations and fire code requirements as set forth by local building and fire codes and be accepted by the local authority having jurisdiction. This includes the standards in NFPA 855\. |
| **6.9.1.5** | **Charging Stations** |
| 6.9.1.5.1 | Charging stations shall not be located within the TLOF, FATO, Safety Area, or Taxiway so as to constitute an obstruction or hazard to ground or flight operations. |
| 6.9.1.5.2 | Each individual charging station shall incorporate an emergency shut-off capability. Each individual charging station shall incorporate fire safety equipment commensurate with applicable fire codes and accepted best practices for such systems. |
| 6.9.1.6 | If it is discovered that an electromagnetic vulnerability is present at a TLOF/FATO location that has been shown to interfere with aircraft navigational instrumentation, warning placards shall be placed on the landing surface in conjunction with warning information being placed in all published documentation to alert pilots and aircraft operators of the potential issue. |
| 6.9.1.7 | Landing/Takeoff surfaces, parking areas, taxiways, walkways, access points, passenger areas, and crew areas that are elevated greater than 30 in. \[76.2 cm\] shall provide adequate fall protection. |
| 6.9.1.7.1 | Construction materials that are inherently susceptible to degradation due to weather, ultraviolet light exposure, heat and/or cold exposure as well as any materials that do not meet the ASTM definition of noncombustible materials shall not be used. |
| 6.9.1.7.1.1 | Woven metal safety netting or fencing that has been coated with nylon, vinyl, or plastic shall be avoided due to their combustible nature. |
| 6.9.1.7.2 | Safety nets shall be designed to have a minimum load carrying capability of 25 lb ⁄sq ft \[122 kg ⁄sq m\] as specified in FAA AC 150/5390-2C, Heliport Design Guide. |
| 6.9.1.8 | All edges of the safety net shall be securely fastened to solid structure. |

## **ASTM Training for Public Safety Remote Pilot of Unmanned Aircraft Systems (UAS) Endorsement  Requirements (F3379− 20, 2025\)**

| ID | Requirement |
| ----- | ----- |
| **4** | **Significance and Use** |
| 4.1 | Every person who is identified as a PS-RP shall have met the requirements of this guide. |
| 5 | Program Management |
| 5.1 | A PS-RP training program shall be developed as described by Specification F3330. |
| 5.3 | A PS-RP training program shall use Table 1 when establishing requirements. |
| **6** | **General Knowledge** |
| 6.1 | The following subject, performance, and task knowledge areas shall be assessed by levels (see Table 1\) of competency in the exam items: |
| 6.2 | A PS-RP shall meet the general knowledge requirements of Guide F3266 for endorsement as a RPIC. |
| 6.3 | A PS-RP shall complete the following FEMA and National Incident Management System (NIMS) training, or equivalent: IS-100: Introduction to the Incident Command System, ICS-100;  S-200: Incident Command System for Single Resource and Initial Action Incident;  IS-700: National Incident Management System, An Introduction;  IS-800: National Response Framework, An Introduction. |
| **7** | **Public Safety Remote Pilot Skills** |
| 7.2 | A PS-RP shall demonstrate the ability to complete the public safety remote pilot competency lane described in Annex A1. |
| 7.4 | A PS-RP shall demonstrate the ability to perform, to the trainer’s satisfaction, a sufficient number and variety of actual or mock UAS incidents that are likely to occur in their normal area of operations, including the selection and dispatch of appropriate resources, conduct of the flight operations, and follow-up reports. |
| 8 | Public Safety Remote Pilot in Command Skills |
| 8.1 | A PS-RPIC shall meet the skills requirements of Guide F3266 for endorsement as a RPIC. |
| 8.2 | A PS-RPIC shall demonstrate the ability to complete the public safety remote pilot competency lane described in Annex A1, indoors and outdoors, and in day and night conditions. |
| 8.3 | A PS-RPIC shall know the six phases of UAS operations: Pre-planning, Notification, Planning and Strategy, Tactics and Techniques, Suspension, and After action review or critique. |
| 8.4 | To the extent determined by the AHJ, PS-RPIC shall know the roles of other agencies or organizations, at the following levels, that coordinate, provide resources, provide services, or perform other functions in search and rescue for the AHJ: National, State or Provincial, Tribal, and Local. |
| **9** | **Public Safety Remote Pilot Instructor Skills** |
| 9.1 | PS-RP instructor shall meet the skills requirements of Section 8 (Public Safety Remote Pilot in Command Skills) and Section 9 (Public Safety Remote Pilot Instructor Skills) for endorsement as a PS-RPIC. |
| 9.2 | All instructors shall be thoroughly knowledgeable about the unmanned aircraft environment and with the working environment of public safety. |
| 10 | Incident-Specific Knowledge and Skills |
| 10.1 | Personnel shall be trained to recognize visible and potential hazards or environments associated with a UAS support to public safety (see Table 1, Level C: knows analysis). |
| 10.2 | Personnel shall be trained to recognize the appropriate PPE selections for eyes, face, head, extremities, and respiratory tract based on the environmental conditions and task to be completed (see Table 1, Level C: knows analysis). |
| 10.3 | Personnel shall have an understanding of how and where to report potential hazard(s) (see Table 1, Level C: knows analysis). |
| 10.4 | Personnel shall be trained to recognize when a hazard presents a risk that exceeds their training or PPE, or both (see Table 1, Level C: knows analysis). |
| 10.5 | Personnel shall be trained to recognize when there is a need for specialized resources (including mutual aid) at the outset of a UAS operation and notify search management when these conditions are present (see Table 1, Level C: knows analysis). |
| 10.6 | Personnel shall be trained to describe, identify, and communicate relevant information to search management for the activation of emergency response systems (see Table 1, Level C: knows analysis). |
| 10.7 | Personnel shall be trained to recognize the additional hazards associated with a structural collapse incident (see Table 1, Level B: knows principles). |
| 10.8 | Personnel shall be trained to recognize the additional hazards associated with a water rescue incident (see Table 1, Level B: knows principles). |
| **11** | **Communications** |
| 11.1 | PS-RPs shall demonstrate the ability to verbally communicate information clearly, effectively, and accurately (see Table 1, Level 3b: competent performance, knows procedures). |
| 11.2 | PS-RPs shall know the radio communications procedures and protocols used in search missions in the field, as determined by the AHJ (see Table 1, Level 3b: competent performance, knows procedures). |
| 11.3 | PS-RPs shall demonstrate the ability to operate the radio equipment used for search missions in the field, as determined by the AHJ (see Table 1, Level 3b: competent performance, knows procedures). |
| 11.4 | PS-RPs shall demonstrate the ability to correctly send and receive position coordinates by radio (see Table 1, Level 3b: competent performance, knows procedures). |
| **12** | **Personal Fitness** |
| 12.1 | UAS team members shall demonstrate annually that they meet the requirements of a medical fitness standard determined by the AHJ. |
| 12.2 | UAS team members shall demonstrate annually that they meet the requirements of a physical performance standard determined by the AHJ. |
| **13** | **Training Course Administration** |
| 13.2 | The following records shall be maintained: |
| 13.2.1 | Factual and accurate student attendance records; |
| 13.2.2 | Factual and accurate student performance records, including comments regarding need for improvement in skills or knowledge; |
| 13.2.3 | Identity and qualifications of the instructor(s); |
| 13.2.4 | Records of the evaluation of instructor(s) performance; |
| 13.2.5 | Records of course content evaluations. |
| **14** | **Continuing Qualification Curriculum Requirements** |
| 14.3.1 | UAS teams and those instructors and evaluators who conduct flight training or flight evaluations shall complete proficiency training designed for their respective duty position. |
| 14.4.1 | Continuing qualification shall include validation/ evaluation in all events and major subjects required for original qualification |
| **A1** | **PUBLIC SAFETY REMOTE PILOT COMPETENCY LANE** |
| A1.2.3 | Organizations shall time all iterations of the public safety remote pilot competency lane. Iterations that are not timed shall be recorded and documented as “UNTIMED.” |
| **A1.3** | **Basic Maneuvering Lane** |
| A1.3.1 | A PS-RPIC shall demonstrate the ability to perform, to the trainer’s satisfaction, a sufficient number and variety of actual or mock UAS incidents that are likely to occur in their area of operations, including the selection and dispatch of appropriate resources, conduct of the flight operations, and follow-up reports. |
| A1.3.2 | A PS-RPIC shall demonstrate the ability to perform flight tasks in a variety of personal protective equipment, as determined by the organization. |
| **A1.4** | **Basic Payload Lane (Electronic Search)** |
| A1.4.1 | A PS-RPIC shall demonstrate the ability to perform flight tasks in a variety of personal protective equipment, as determined by the organization. |
| **A1.10** | **Alternatives** |
| A1.10.2 | Organizations that offer PS-RP training courses shall include the public safety remote pilot competency lane described in Guide F3379 to market or advertise as compliant with Guide F3379. |

## **ASTM Verification of Lightweight Unmanned Aircraft Systems (UAS)  Requirements (F3657, 2025\)** 

| ID | Requirements |
| ----- | ----- |
| 5.1.1 | Each applicant who claims compliance to this specification shall be able to show compliance with the applicable requirements of this specification. |
| **6** | **Operating Limitation and Information** |
| 6.1 | During the verification process, the applicant shall determine and document in the aircraft flight manual appropriate operating limitations and other information necessary for safe operation of the system. |
| 6.1.1 | This shall include any wind limitations as well as features of the control station and the C2 link functions of the system. |
| 6.2.1 | During the verification process, the applicant shall determine and document weight and loading distribution, including the maximum certificated weights and the CG range. |
| 6.2.2 | The applicant shall determine the location of the reference datum used in balance computations. |
| **7** | **Documentation** |
| 7.1.2 | The manufacturer shall retain documentation of appropriate verification results including data showing compliance with this specification. |
| 7.1.4.1  | All verification shall be recorded and available at the applicant’s location for future reference for UAS that will receive type certification by a CAA, or (as appropriate) self or third-party determinations of airworthiness for UAS. |
| 7.2.1 | The applicant shall adhere to Specification F2908 for the unmanned aircraft flight manual. |
| 7.2.2 | The applicant shall determine and document in the unmanned aircraft flight manual appropriate operating limitations and other information necessary for safe operation of the system. |
| 7.2.2.1 | This shall include any wind limitations as well as features of the control station and the CNPC link functions of the system. |
| 7.2.5.3 | For those systems that might have components capable of causing injury, the UA shall have a warning/caution statement added to the unmanned aircraft flight manual alerting the crew to the risk. |
| 7.2.5.4 | If removing/adding ballast is permitted, the unmanned aircraft flight manual shall include instructions with respect to loading, marking, and securing of removable ballast and ensuring the center of gravity remains within limits that can be controlled by the control system and ensures adequate aerodynamic stability. |
| 7.2.5.5 | The aircraft flight manual shall have a method to verify or calculate CG location. |
| 7.2.5.6 | The manufacturer shall develop and provide instructions to ensure any damage caused by shipping or handling are identified prior to flight. |
| 7.2.6.1 | The UFM shall include the specific external HIRF environments for the UAS intended operational envelope. |
| 7.2.6.2 | If the UAS design did not consider a specific HIRF, or did not verify the HIRF protection of the UAS, the UFM shall include a caution statement. |
| 7.2.7.1 | The emergency procedures section shall include checklists describing the recommended procedures and air-speeds for coping with various types of emergencies or critical situations. |
| 7.2.8.2 | The section shall include several checklists that may include preflight inspection, before starting procedures, starting engine, before taxiing, taxiing, before takeoff, climb, cruise, descent, before landing, balked landing, after landing, and post flight procedures. |
| 7.2.8.3 | All specializations and limitations shall be those determined from the preceding relative design criteria. |
| 7.3.2 | The maintenance manual shall include maximum damage and wear limits for the propellers. |
| 7.3.3 | The maintenance manual shall provide instructions for continued airworthiness that are in compliance with Practice F2909. |
| 7.3.4 | Applicants shall provide the CAA with a written, self-certifying statement that they have an established inspection and maintenance program for the continued airworthiness of the aircraft. |
| 8 | This specification requires the manufacturer to complete functional verification prior to achieving compliance. |
| 8.1.2 | If sufficient operational reliability is not demonstrated, the manufacturer shall levy initial operational restrictions until an acceptable level of demonstrated reliability is reached. |
| 8.1.3 | UAS design and construction requirements shall be verified with a combination of analysis, inspections, demonstrations or tests. |
| 8.1.3.2 | UAS demonstrations, testing, analysis, or simulations, or combinations thereof, shall be conducted to verify that the design requirements have been satisfied and the results recorded and available for future reference. |
| 8.2.1 | The applicant shall verify the proper completion of each ready-to-fly UAS by conducting a final system test in accordance with the requirements below. |
| 8.2.2 | The following ground check and flight test procedures shall be conducted and documented for each ready-to-fly UAS using one or more of the following methods: analysis, inspection, demonstrations and test. |
| 8.2.2.2 | The control station and other associated elements required for remote operations shall be inspected during the on site inspection. |
| 8.2.2.3 | The applicant shall complete a minimum of 25 hours of flight time for UAS, to demonstrate that the aircraft and all required on-board subsystems, payload, control station, other required off-board subsystems, any required launch and recovery equipment, all required crew members, and command and control (C2) links between UA and the control station perform as designed in the intended configuration. |
| 8.3.1 | An organization complying with this specification shall manage under configuration control all life cycle data which are generated by applying this specification. |
| 8.3.2 | The organization shall keep a record of the documentation used to show compliance of each approved system configuration produced to all applicable consensus specifications and regulatory requirements in effect at the time of manufacture or major change. |
| **9** | **Best Practices** |
| 9.1.1.1 | Flight operations shall be conducted within the visual line of sight of the remote pilot/observer.  |
| 9.1.1.1.1 | Multi-engine UAS shall include verification of VXSE, VYSE, VMC. |
| 9.1.1.1.2 | The aircraft shall have no hazardous operating characteristics or design features. |
| 9.1.1.1.3 | Following satisfactory completion of initial flight testing, the applicant shall certify in the UA records that the UA has been shown to comply with this specification with the following, or a similarly worded, statement: I certify that the prescribed flight test has been completed and the aircraft is controllable throughout its normal range of speeds and throughout all maneuvers to be executed, has no hazardous operating characteristics or design features, and is safe for operation.  |
| 9.1.1.1.4 | Test shall be conducted at maximum gross weight, with minimum of in-flight turbulence. |
| 9.1.2.1 | The aircraft shall be safely controllable and maneuverable during takeoff, climb, level flight (cruise), approach, and landing (power off and on) with primary controls of turn and throttle and the possibility of combined turn displacement for flare. |
| 9.1.2.2 | Demonstrate a smooth transition between all flight conditions shall be possible without exceptional pilot skills. |
| 9.1.2.3 | Longitudinal control of the aircraft shall be demonstrated by performing two minutes of flight without control input for three conditions: maximum power setting climb, reduced power descent and cruise setting power level flight. |
| 9.1.2.3.1 | The aircraft shall not enter into dangerous or unusual attitudes. |
| 9.1.2.4 | Lateral control shall be demonstrated by maintaining the controls in a neutral position, which shall initially give an unaccelerated level flight condition. |
| 9.1.2.4.1 | The aircraft shall not enter into a dangerous attitude during the 2 min that the flight controls are fixed. |
| 9.1.2.4.2 | Demonstration shall be conducted at maximum takeoff weight, with minimum of in-flight turbulence. |
| 9.1.2.5 | Directional control shall be demonstrated by a separate and full deflection of each directional flight control for three full turns of 360° without the aircraft entering any dangerous flight attitude during the maneuver in each direction. |
| 9.1.2.5.1 | Test shall be conducted at minimum flight weight, with minimum of in-flight turbulence. |
| 9.1.2.5.2 | The demonstrated turn rate shall not be less than 12°⁄s (30 s for a 360° turn) in both directions. |
| 9.1.2.5.3 | These turns shall be in alternating directions (that is, left-right-left). |
| 9.1.3.1 | Flight testing shall not reveal, by pilot observation, heavy buffeting (except as associated with a stall), excessive airframe or control vibrations, flutter (with proper attempts to induce it), or control divergence, at any speed from VS0 to VDF. |
| 9.2.1.1 | Primary structure strength shall be verified by analysis, or test. |
| 9.2.1.2 | Systems structure such as control surfaces and associated linkages, motor/engine mounts, and others strength shall be verified by analysis, inspection, or test. |
| 9.2.1.3.1 | The applicant shall describe the process used to determine that the airframe structure can withstand expected flight loads throughout the flight envelope. |
| 9.2.1.3.2 | The applicant shall include any test data or stress analysis that demonstrates positive structural margins of safety during flight. |
| 9.2.2.1 | The empty weight and corresponding center of gravity shall be determined by weighing the aircraft with: (1) Fixed ballast; (2) Unusable fuel; and (3) Full operating fluids, including other fluids required for normal operation of the UA. |
| 9.2.3.1 | Compliance with the limit load requirements of this part shall be shown by tests in which: (1) The direction of the test loads produces the most severe loading in the control system; and (2) Each fitting, pulley, and bracket used in attaching the system to the main structure is included. |
| 9.2.3.2 | Compliance shall be shown (by analyses or individual load tests) with the special factor requirements for control system joints to angular motion. |
| 9.2.4.1 | It shall be shown by operation tests that, when the controls are operated from the control system the system is free from: (1) Jamming; (2) Excessive friction; and (3) Excessive deflection. |
| 9.3.1 | The engine(s) thrust shall be verified by either the manufacturer’s published thrust to RPM numbers or by actual measurements. |
| 9.3.1.1 | The fuel and oil systems shall be shown capable of supplying adequate grade fuel and oil to the propulsion system throughout the entire flight envelope at the required rate and pressure specified by the propulsion system supplier if those specifications are available. |
| 9.3.1.3 | The propulsion system shall be shown to support normal operations throughout the anticipated lifecycle of the system. |
| 9.3.2 | For UA with multiple propulsion systems, the applicant shall determine the minimum number of operational propulsion systems required to maintain controlled flight through analysis or demonstration. |
| 9.3.2.1 | For UA with multiple propulsion systems, the UAS shall be shown to perform one of the following actions in the event of propulsion system failure: (1) The aircraft remains capable of controlled flight, or (2) The descent flight path can be controlled from the control system, or (3) The system defaults to a safe automated recovery procedure. |
| 9.4.1 | Propellers shall be shown to have satisfactory endurance as well as stresses that do not exceed values shown to be safe for continuous operation in accordance with the applicable requirements of Section 14\. |
| 9.5.1.1 | The C2 System shall be shown to present the information required for UA operations in a timely and unambiguous fashion to the remote pilot at all times. |
| 9.5.1.2 | The airspeed instruments shall be shown to provide true airspeed with a minimum practicable instrument calibration error. |
| 9.5.1.3 | Any static pressure system shall be calibrated to indicate pressure altitude (with a standard atmosphere) with a minimum practicable instrument calibration error. |
| 9.5.1.4 | If the pressure altitude system is not reliant on static pressure, it shall be shown to be equivalent to or better than pressure-based systems in all operating conditions. |
| 9.5.2.1 | For touch screen or other control devices, a human factors evaluation of the suitability for pilot/aircraft interface shall be performed. |
| 9.5.2.1.2 | The UAS shall be required to demonstrate compliance to general controllability and maneuverability, directional and lateral control, minimum control speed, rate of roll, trim, wings level stall, turning flight and accelerated turning stalls, directional stability and control, flap interconnection. |
| 9.5.2.1.3 | The permissible operating and environmental conditions and capabilities for the control station shall be specified and verified. |
| 9.5.2.1.4 | The functioning of the control station and associated UA shall be tested and demonstrated in an integrated manner. |
| 9.5.2.1.5 | The C2 System shall be shown to provide the remote pilot the ability to adequately command and control the trajectory of the UA under normal operating conditions. |
| 9.5.2.2 | The AFCS shall be shown to provide the remote pilot with clear indications of any commanded flight parameter (for example, airspeed, altitude), flight path (way points), or both, and the UA performance with respect to them. |
| 9.5.2.2.1 | The AFCS shall be shown to allow remote pilot intervention during all normal procedures. This restriction does not apply to UA operating under lost link procedures, even though the remote pilot may be technically considered out-of-the-loop. |
| 9.5.2.3 | Datalink compliance with this specification shall be verified (at a minimum) by analysis. |
| 9.5.2.3.1 | Datalink performance during the operational envelope shall be demonstrated and documented. |
| 9.5.2.4 | An electrical load analysis shall be performed to ensure that electrical bus loads and capacity shall be adequate to power all aircraft systems and installed payloads. |
| 9.5.2.4.1 | The electrical system shall be demonstrated to operate safely. |
| 9.5.2.5 | All lighting shall be inspected for compliance with this specification. |
| 9.5.2.5.1 | All lighting shall be shown to provide adequate illumination by analysis, inspection or demonstration. |
| 9.5.2.6 | The landing gear, if any, shall be shown to accommodate landing loads without damage to the structure. This does not apply to frangible components. |
| 9.5.2.6.1 | Frangible landing gear, if any, shall be shown to accommodate landing loads without unintended damage to the structure. |
| 9.5.2.7 | The means of demonstrating and validating the flight termination system shall be determined by the UAS designer/manufacturer.  |
| 9.5.2.7.1 | There shall be sufficient documented testing and analysis to demonstrate and verify the reliability and functionality of the system. |
| 9.5.2.7.2 | In cases where flight termination results in destruction of the UA, the designer/manufacturer shall conduct and document sufficient testing to prove the reliability of the system. |
| 9.5.2.7.3 | For systems designed to preserve the UA following flight termination, verification may occur through periodic demonstrations of the system. |
| 9.6.1 | Any required launch and recovery system shall be demonstrated to operate safely. |
| 9.6.2 | Any required tethering system shall be demonstrated to operate safely. |
| 9.7.1 | Any installed payload shall be demonstrated to operate safely. |
| 9.7.2.1 | If the operation of the UAS includes flight in areas where HIRF are probable, the UAS electrical and electronic systems that perform functions whose failure would prevent the continued safe flight and recovery of the UA shall be designed to mitigate this risk. |
| 9.7.2.2 | Any RF emissions by the UAS shall be evaluated according to applicable regulations, and any findings or approvals gained, or both, shall be included in the type design. |
| 9.8.1.1 | Wing level stalling speeds VS0 and VS should be determined by flight test at a rate of speed decrease of 1 knot/s or less, throttle closed, with maximum takeoff weight, and most unfavorable CG. |
| 9.8.1.1.1 | Compliance with this section shall be demonstrated under the following conditions: (a) Wing flaps in any condition, (b) Landing gear retracted and extended, (c) With the engine at idle and 90 % of maximum continuous power, and (d) During launch with the UA pitch 30° above the horizontal. |
| 9.8.1.2 | The UA shall demonstrate a full-throttle climb gradient at 1.3 VS0 which shall exceed 1⁄30 within 5 s of power application from aborted landing. |
| 9.8.1.2.1 | Balked landing performance shall be demonstrated considering minimum remaining available ESD power. |
| 9.8.1.3 | If there is any tendency for a spin to turn into a spiral dive, the UA should be able to recover from this condition without exceeding either the limiting air speed or the limiting maneuvering factor for the UA. |
| 9.8.1.4 | It shall be demonstrated that the UA is safely controllable and that all maneuvers and operations necessary to effect a safe landing following any probable powered trim system runaway that reasonably might be expected in service. |
| 9.8.2.1 | The applicant shall predict the limit loads by analysis or flight test to determine the limit loads on the UA and systems required for continued safe flight encountered throughout the operating envelope to include atmospheric gusts or maneuvering loads, or both. |
| 9.8.2.1.1 | Each critical load requirement shall be investigated either by conservative analysis or tests (static, component, or flight), or a combination of both. |
| 9.8.2.1.2 | The strength of stressed-skin wings shall be proven by load tests or by combined structural analysis and load tests. |
| 9.8.2.1.3 | The positive limit maneuvering load factor shall be shown to equal or exceed 2.1. |
| 9.8.2.1.4 | The negative limit maneuvering load factor shall be shown to equal or exceed 0.84. |
| 9.8.2.1.5 | The structure shall be shown capable of withstanding a vertical gust of \>12 fps. |
| 9.8.2.1.6 | The structure should be shown capable of withstanding a vertical gust of 25 fps. |
| 9.9.1.1 | Propellers shall be shown to have satisfactory endurance as well as stresses that do not exceed values shown to be safe for continuous operation in accordance with the applicable requirements of Section 14, Documentation. |
| 9.9.1.2 | The chordwise balance of the blades shall be such that: The blades cannot be induced to flutter or weave in all flying conditions. |
| 9.9.1.2.1 | The chordwise balance of each blade in a pair shall be the same. |
| **A1** | **ADDITIONAL REQUIREMENTS FOR UAS INTENDED FOR EXPANDED OPERATIONS** |
| A1.1.1 | The system shall be constructed so that the aircraft remains controllable or automatically initiates a predictable and safe maneuver in the event of the failure of any flight-critical component or system. |
| A1.1.2 | Applicant shall provide a method to ensure the dynamic area-of-operation is properly evaluated for potential hazards, and the risks presented to non-participating person and property by those hazards are controlled or eliminated. |
| A1.1.3 | Applicant shall provide a method to increase conspicuity of the UA when operating with visibility less than 3 statute miles or during expanded operations. |
| A1.1.4 | Applicant shall provide a method for the remote pilot to maintain visual line of sight with the UA when operating with visibility less than 3 statute miles. |
| A1.2.1 | The UAS, if intended for operation over people or in airspace where it may encounter other aircraft, shall have features that help mitigate the potential risk to people or property on the ground, and other aircraft. |
| A1.2.3.1 | UA used during operations with reduced cloud clearance shall be painted in a manner that is highly visible to the unaided eye. |
| A1.2.3.1.1 | The high visibility modification shall consist of large areas of the aircraft painted the safety orange color or safety yellow, equivalent to ANSI standard Z535.1-1998. |
| A1.2.3.1.2 | UA used during operations with reduced cloud clearance shall have a calculated visible distance greater than one statute mile using the following formula \[Visible Distance (feet) \= 3438 × Side View Height (feet)\] listed within the Operating Limitations of the AFM distance. |
| A1.3.1.1 | The UA shall be verified so that in the event of propulsion system failure: (1) The flight path can be controlled, or (2) The system defaults to a safe automated recovery procedure. |
| A1.3.2 | For UA with multiple propulsion systems, the UA shall be constructed so that in the event of a singular or multiple propulsion system failure:  (1)The aircraft remains capable of controlled flight, or  (2)The descent flight path can be controlled from the control station, or (3)The system defaults to a safe automated recovery procedure. |
| A1.3.3 | The propulsion system shall minimize failure for reasons other than insufficient fuel or electrical power and to support normal operations throughout the anticipated lifecycle of the system. |
| **A1.4** | **Required Equipment/On-Board Systems** |
| A1.4.1 | The control station shall demonstrate compliance with Specification F3298 10.2.1.1 within all critical phases of flight. |
| A1.4.1.1 | Information required for UA operations shall be presented in a timely and unambiguous fashion. |
| A1.4.1.2 | The control station shall provide the pilot with all information required for accurate control and monitoring of the UAS and ensure operation within its limits. |
| A1.4.1.2.1 | This information shall include: (a) UA present position. (b) UA altitude (type and units). (c) UA heading (type and units). (d) UA speed (type and units). (e) Fuel or other indication of remaining flight time UA operating status (that is, degraded operation, normal operation, modes of flight, etc.). (f) Any parameters at a resolution and accuracy level sufficient to allow compliance with air navigation system requirements as mandated operational requirements. |
| A1.4.1.3 | The propulsion system onboard the UA shall be designed to provide in-flight fuel quantity indication for combustion propulsion or state of charge indication for electric propulsion. |
| A1.4.1.4 | For UA that are not equipped with automatic stall protection, a means shall be provided to warn the pilot when the aircraft is approaching the stall. |
| A1.4.1.4.1 | For UAS equipped with a geo-fence system and associated flight control systems, a means shall be provided for visual alerts if any UA under the remote pilots control contact any geo-fence boundary. |
| A1.4.1.5 | There shall be a means to synchronize and positively transfer control between control stations and remote pilots in command if multiple control stations are in use. |
| A1.4.1.5.1 | For UAS capable of simultaneously controlling multiple UA from a single control station: (a) The system shall present information to the remote pilot in command in an unambiguous fashion so that the status and situation of each UA can be readily discerned and acted on, under both normal and emergency operations, as required |
| A1.4.1.5.2 | For UAS capable of simultaneously controlling multiple UA from a single control station: (b) The system shall permit the remote pilot in command to direct commands to any or all of the multiple UA without undue attention or effort. |
| A1.4.1.6 | The Control Station shall demonstrate compliance with F3298 10.5.8.3 while in a moving vehicle. |
| A1.4.1.6.1 | The Control Station shall demonstrate compliance with Specification F3298 10.2.1.1 while in a moving vehicle. |
| A1.4.1.6.2 | The Control Station should be capable of an illumination setting that minimizes degradation of night vision. |
| A1.4.1.6.3 | The Control Station shall demonstrate compliance with Specification F3298 10.5.6 while in a moving vehicle. |
| A1.4.1.7 | The UAS shall demonstrate a radio communication Datalink installed as specified in Specification F3298 10.4.1. |
| A1.4.1.7.1 | The Lost Link procedures shall demonstrate compliance with Specification F3298 10.6.3.1 with a dynamically positioned remote pilot. |
| A1.4.2.1 | The UA shall have an anti-collision light system that consists of one or more anti-collision lights located so that their light will not impair the flight crew members’ vision or detract from the conspicuity of the position lights. |
| A1.4.2.2 | The UA shall have lighted anti-collision lighting visible for at least 1 statute mile. |
| A1.4.2.3 | UA intended for operations at night shall have lighted anti-collision lighting visible for at least 3 statute miles. |
| A1.4.2.4 | UA intended for beyond visual line of sight operations shall have lighted anti-collision lighting visible for at least 3 statute miles. |
| A1.4.3.1 | UA intended for beyond visual line of sight operations, operations at night or during other conditions of reduced visibility shall have lighted anti-collision lighting visible for at least three statute miles. |
| A1.4.3.2  | Left and right position lights shall consist of a red and a green light spaced laterally as far apart as practicable and installed on the UA such that, with the UA in the normal flying position, the red light is on the left side and the green light is on the right side. |
| A1.4.3.3 | The rear position light shall be a white light mounted as far aft as practicable on the tail or on each wing tip. |
| A1.4.3.4 | Each light color shall have the applicable International Commission on Illumination chromaticity coordinates as follows: (1) Aviation Red — y is not greater than 0.335; and z is not greater than 0.002. (2) Aviation Green — x is not greater than 0.440 – 0.320 y; x is not greater than y – 0.170; and y is not less than 0.390 – 0.170 x. (3) Aviation White — x is not less than 0.300 and not greater than 0.540; y is not less than “x – 0.040” or “y0 – 0.010”, whichever is the smaller; and y is not greater than “x \+ 0.020” nor “0.636 – 0.400x” where y0 is the y coordinate of the Planckian radiator for the value of x considered. (4) The minimum light intensities in any vertical plane, measured with the red filter (if used) and expressed in terms of “effective” intensities is 80 candles. |
| A1.4.5.1 | If intended for flight within atmospheric icing conditions, the UAS shall comply with one of the following: |
| A1.4.5.2 | A means shall be provided to allow the UAS to avoid potential icing conditions (clouds and precipitation at an ambient temperature below \+5 °C); or The UAS can detect and safely exit icing conditions. |
| A1.4.5.3 | Critical detect and exit ice accretions shall be based on three minutes plus: (1) Two minutes if ice detection is based on visual cues of ice accretion; (2) Detection time defined in Specification F3120/F3120M if an ice detection system that complied with the qualification requirements in Specification F3120/F3120M is installed. |
| A1.5.2.2 | The UA shall broadcast its own ADS-B information during BVLOS/EVLOS operation. (ADS-B Out). |
| A1.5.2.3 | The UA shall broadcast its own ADS-B information. (ADS-B Out). |
| A1.6.1 | The POH or Unmanned Aircraft Flight Manual, or both, shall include Normal and Emergency procedures for operations in a moving vehicle. |
| A1.6.2 | The POH or Unmanned Aircraft Flight Manual, or both, shall include Operating Limitations for the UAS during operations from a moving vehicle. |
| A1.6.3 | The POH or Unmanned Aircraft Flight Manual, or both, shall include Normal and Emergency procedures for night operations. |
| A1.6.4 | The POH or Unmanned Aircraft Flight Manual, or both, shall include Operating Limitations for the UAS during night operation. |
| A1.6.5 | The POH or Unmanned Aircraft Flight Manual, or both, shall include Normal and Emergency procedures for beyond visual line of sight or extended visual line of sight operations, or both. |
| A1.6.6 | The POH or Unmanned Aircraft Flight Manual, or both, shall include Operating Limitations for the UAS during beyond visual line of sight or extended visual line of sight operations. |
| A1.6.7 | The POH or Unmanned Aircraft Flight Manual, or both, shall include Normal and Emergency procedures for operations over people. |
| A1.6.8 | The POH or Unmanned Aircraft Flight Manual, or both, shall include Operating Limitations for the UAS during operations over people. |
| A1.6.9 | The POH or Unmanned Aircraft Flight Manual, or both, shall include Normal and Emergency procedures for contacting ATC in the absence of an aviation-band radio transceiver. |
| A1.6.10 | The POH or Unmanned Aircraft Flight Manual, or both, shall include Normal and Emergency procedures for operations in certain airspace. |
| A1.6.11 | The POH or Unmanned Aircraft Flight Manual, or both, shall include Operating Limitations for the UAS during operations within certain airspace. |
| A1.6.12 | The POH or Unmanned Aircraft Flight Manual, or both, shall include Normal and Emergency procedures for operations above 100 mph. |
| A1.6.12.1 | This shall include methods for contacting ATC in the absence of an aviation-band radio transceiver. |
| A1.6.13 | The POH or Unmanned Aircraft Flight Manual, or both, shall include Normal and Emergency procedures for operations above 400 ft AGL. |
| A1.6.13.1 | This shall include methods for contacting ATC and other aircraft in the absence of an aviation-band radio transceiver. |
| **X2** | **ACCEPTABLE METHODS FOR VERIFICATION BY INSPECTION** |
| X2.1 | Before flight-testing, the manufacturer shall conduct a thorough ground inspection of each UAS produced to verify at least the following: |
| X2.3 | The proper function of all switches and circuits, instrumentation, brakes, and any other appropriate systems shall be verified |
| X2.4 | All flight controls shall be checked for smooth and proper function and proper maximum deflections. |
| X2.4.1 | The safe operating range of C2 link(s) shall be verified in accordance with Specification F3002. |
| X2.5 | Propulsion system checks and procedures shall be performed, as applicable to the design, to verify: 1- Proper propulsion system installation, (for example, spark ignition, turbine, electric); 2- Proper servicing of any propulsion system fluids; 3- No apparent fuel, oil, or coolant leaks; 4- Propeller installation and pitch adjustment; 5- Performance of a propulsion system run-in with adjustments; 6- Tachometer indicates propulsion system idle revolutions per minute and maximum static revolutions per minute are within supplier/manufacturer published limits; 7- Proper function of propulsion system instrumentation or speed control, or both; 8- Proper function of ignition system(s); and 9- Proper function of all battery system(s). |
| X2.6 | The UAS shall be checked to verify that all placards and switch markings are in place, as applicable. |
| X2.7 | The following shall be verified: |
| X2.7.1 | All required documentation shall be available at the control station. |
| X2.7.2 | Shall be verified: All visible surfaces are free of deformation, distortion, or other evidence of failure or damage. |
| X2.7.3 | Shall be verified: Inspection of all visible fittings and connections for defective or unsecure attachment. |
| X2.7.4 | Shall be verified: Complete walk-around/pre-flight inspection in accordance with the aircraft flight manual. |
| X2.7.5 | Shall be verified: All panels are closed and locked. |
| X2.8 | After completion of the ground check, a taxi test, if appropriate, shall be conducted to verify as applicable: (1) Brake function, (2) Landing gear tracking and steering, and (3) Proper compass readings, to be verified by a reference, and corrected. |
| X3.1 | Safe flight operation of each completed UAS shall be verified, as applicable, to include acceptable handling and control characteristics, stall characteristics, propulsion system operation, airspeed indications, and overall suitability for normal flight in accordance with the aircraft flight manual. |
| X3.1.1 | The flight test procedure, at a minimum, shall include recorded verification of the following: (1) Takeoff runway wind, outside air temperature, and pressure altitude; (2) Demonstration of safe takeoff for the operating conditions specified for the UAS; (3) Demonstration of safe climb out; (4) Appropriate response to flight controls in all configurations; (5) Demonstration of safe recovery from stall, including verification of appropriate stall warning and stall recovery characteristics; (6) Demonstration that there are not any unexpected or abnormal performance or handling characteristics; and (7) Proper propulsion system operating temperatures. |

## **ASTM F3623-23 Standard Specification for Surveillance Supplementary Data Service Provider**

# **Appendix C: System Operational Scenarios** 

*This OCD Appendix will provide detailed information for a number of key scenarios that best describe how the system is used in its operational context by the users, operators, and maintainers. The scenarios are stated in terms of, and related, to the operational elements defined in Sections A.5.1 through A.5.5.* 

*The OCD section should provide typical usage scenarios for each of the operational processes served by the system, as documented in Section 7 of the OCD. Scenarios describe typical detailed sequences of user, system, and environment events. Based on the motivations for preparing an OCD, this section is by far the most important and should receive substantial emphasis. Details on the development of the scenarios are provided in Section 7.3.5 of this Guide.* 

## **Appendix C.1.x Scenario: Nominal UAM Corridor Passenger Operation**

This use case represents routine passenger transport operations conducted by multiple eVTOL aircraft within a cooperative xTM environment. Operators submit 4D trajectory intents through service suppliers, which perform strategic deconfliction and demand-capacity balancing prior to departure. Aircraft enter a defined UAM corridor via coordinated entry points, maintain separation using cooperative mechanisms (e.g., V2V/V2I exchanges), and operate under automated traffic management rather than direct ATC control. The objective is to model steady-state high-density corridor operations, evaluate throughput and separation performance, and assess system scalability under increasing traffic demand while maintaining safety constraints.

## **Appendix C.2.x Scenario: Off-Nominal Conformance & Conflict Escalation**

This use case examines system behavior under abnormal or degraded conditions within the xTM environment. Scenarios include loss of communication, trajectory nonconformance, unauthorized airspace entry, degraded navigation performance, or emergency diversion due to energy constraints. The system must detect deviations, trigger automated mitigation strategies such as re-planning or tactical avoidance, and escalate to human or ATC intervention if required. The objective is to evaluate resilience, response latency, and recovery mechanisms under off-nominal conditions, ensuring that cooperative traffic management maintains safety margins even when automation or participants behave unpredictably.

## **Appendix C.3.x Scenario: Public Safety Volume Reservation (Emergency Response)**

This use case represents a public safety emergency scenario in which a dynamic airspace restriction (e.g., UAS Volume Reservation or equivalent geofence) is established to support search and rescue operations. A drone swarm conducts low-altitude search operations under UTM management, while an eVTOL aircraft transports rescue personnel and equipment within the UAM layer above. The xTM system redistributes or reroutes civil traffic, enforces geofencing constraints, and monitors conformance in real time. The objective is to evaluate the system’s ability to support prioritized emergency operations, manage multi-layered traffic (UAS and UAM), and maintain safe separation while adapting dynamically to time-critical mission demands.

## **Appendix C.2.x Scenario: Cross-Environment Transition**

This use case models the operational interaction between low-altitude UTM-managed drone traffic and higher-altitude UAM-managed eVTOL traffic within an integrated xTM environment. An eVTOL operating in a UAM corridor must coordinate trajectory intent and separation assurance with concurrent drone operations occurring below or within intersecting volumes of airspace. The scenario captures shared information exchange between UTM and UAM service providers, vertical separation management, conflict detection across traffic classes, and coordinated deconfliction strategies when trajectories overlap. The objective is to evaluate interoperability between the two traffic management layers, ensure safe coexistence of heterogeneous aircraft types with different performance envelopes, and assess the effectiveness of shared situational awareness and cooperative coordination mechanisms in maintaining system-wide safety and efficiency.

![][image12]

*![][image13]*

*![][image14]*

*![][image15]*

## **Appendix B.1 Operational Processes** 

*This OCD subsection should describe the scenarios for the operational process(s) described in Section 7 of the OCD.* 

## **Appendix B.1.x Scenario** 

*This OCD subsection should provide, for each operational process, the sequence of user and system operations/tasks. Each scenario should be related to specific users and system elements.* 

*Several different types of scenarios should be considered, including those that address normal mission modes, anomaly/exception handling, mission critical activities, safety critical modes/activities, and maintenance modes. Detailed scenarios should be provided for each Design Reference Mission (DRM) identified for the system.* 

*Section 7.3.5 of this Guide provides direction for development of an appropriate and quality set of scenarios. Typical content for a scenario is listed in the following outline.* 

**Overview** 

*Summary of what the system is (context), what it is to do in general (mission), and how it will do it* 

**Sequence** 

·       *Data flow* 

·       *State and mode transitions* 

·       *Decision points (particularly human interactions)* 

**Performance** 

·       *Response time* 

·       *Delay points / times* 

·       *Throughput / turnaround times expected* 

·       *Reliability, availability, maintainability* 

·       *Survivability*

·       *Supportability*

·       *Key technical performance measures* 

·       *Key measures of effectiveness (MoE).* 

**User and Organizational Potential Risks** 

·       *User types and technical expertise* 

·       *User training constraints,* 

·       *User / operator responsibilities and decision authority*

·       *User workload and period over which operators/users can function effectively* 

·       *Operator/user comfort and convenience* 

·       *Situational awareness.* 

**System Environment and Existing Facilities** 

·       *Environment in which system must operate, including all physical environments* 

·       *Geographical-related risks* 

·       *Safety, security, system integrity needs* 

·       *Interfacing systems description and data flows* 

·       *Operational aspects which will affect the needs for system growth capabilities, including flexibility and expansion* 

·       *HAZMAT and disposal risks.* 

## **Appendix B .2 Common Scenarios and Conditions** 

*Various scenarios may share common sections and common conditions. It would be appropriate to document them in this section and then reference them from the scenario descriptions.* 
