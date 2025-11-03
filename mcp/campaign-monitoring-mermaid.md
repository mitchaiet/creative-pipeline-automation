# Campaign Monitoring - Mermaid Visualizations

This document provides visual diagrams for the Campaign Monitoring Agent using Mermaid syntax.

---

## 1. Automated Workflow Sequence

```mermaid
sequenceDiagram
    participant User
    participant UI as Gradio UI
    participant Load as Load JSON
    participant Trans as Translate
    participant Env as Generate Environments
    participant Prod as Generate Products
    participant Preview as Preview Tab

    User->>UI: Select campaign_config.json
    UI->>Load: load_campaign_config_from_json()
    Load->>UI: Populate all fields
    Note over Load: Campaign ID: YYYYMMDD_HHMMSS

    Load->>Trans: .then(translate_message)
    Note over Trans: 2-5 seconds
    Trans->>Trans: Generate 4 language translations
    Trans->>UI: Update translations display

    Trans->>Env: .then(generate_environments)
    Note over Env: 30-60 seconds
    Env->>Env: Generate 4 background images
    Env->>UI: Update environment gallery

    Env->>Prod: .then(generate_product_views)
    Note over Prod: 60-120 seconds per product
    Prod->>Prod: Generate 6 views per product
    Prod->>UI: Update product gallery

    Prod->>Preview: .then(switch to preview tab)
    Preview->>User: Display all generated assets
    Note over Preview: Total: 2-3 minutes
```

---

## 2. Campaign Data Structure

```mermaid
graph TB
    Campaign[Campaign Configuration]

    Campaign --> Brief[Campaign Brief]
    Campaign --> GenConfig[Generation Config]
    Campaign --> AdSettings[Ad Settings]
    Campaign --> Assets[Asset Inventory]
    Campaign --> Status[Campaign Status]

    Brief --> ID[Campaign ID<br/>YYYYMMDD_HHMMSS]
    Brief --> Target[Targeting<br/>Region + Audience]
    Brief --> Message[Messaging<br/>Primary + Translations]

    GenConfig --> EnvPrompt[Environment Prompt]
    GenConfig --> Products[Product Slugs]
    GenConfig --> Mode[Product Mode<br/>separate/combined]
    GenConfig --> Logos[Logo Paths]

    AdSettings --> Ratios[Aspect Ratios<br/>1:1, 9:16, 16:9]
    AdSettings --> Local[Localization<br/>Per Format]
    AdSettings --> IncLogo[Include Logo<br/>Per Format]

    Assets --> Environments[Environments<br/>4 images]
    Assets --> ProductViews[Product Views<br/>6 per product]
    Assets --> Ads[Ad Creatives<br/>3 aspect ratios]

    Status --> Phase[Phase<br/>configuration/generation/complete]
    Status --> Progress[Progress %]
    Status --> Errors[Errors/Warnings]

    style Campaign fill:#e1f5ff
    style Brief fill:#fff4e1
    style GenConfig fill:#f0f0f0
    style AdSettings fill:#e8f5e9
    style Assets fill:#fce4ec
    style Status fill:#f3e5f5
```

---

## 3. Monitoring Decision Flow

```mermaid
flowchart TD
    Start([Campaign Loaded]) --> CheckID{Valid Campaign ID?<br/>YYYYMMDD_HHMMSS}

    CheckID -->|No| Alert1[⚠️ Invalid ID Format]
    CheckID -->|Yes| CheckBrief{Campaign Brief<br/>Complete?}

    CheckBrief -->|No| Alert2[❌ Missing Region/Audience/Message]
    CheckBrief -->|Yes| CheckTrans{Translations<br/>Available?}

    CheckTrans -->|No & Localization=true| Alert3[❌ Missing Translations]
    CheckTrans -->|Yes| CheckEnv{Environments<br/>Generated?}

    CheckEnv -->|Count = 0| Alert4[❌ No Environments Generated]
    CheckEnv -->|Count < 3| Warn1[⚠️ Low Environment Count]
    CheckEnv -->|Count >= 3| CheckProd{Products<br/>Generated?}

    CheckProd -->|Missing Views| Alert5[❌ Incomplete Product Views]
    CheckProd -->|6 Views Each| CheckAds{Ads<br/>Generated?}

    CheckAds -->|Count = 0| Alert6[❌ No Ad Creatives]
    CheckAds -->|Count < Expected| Warn2[⚠️ Low Ad Variant Count]
    CheckAds -->|Count = Expected| CheckQuality{Quality<br/>Checks Pass?}

    CheckQuality -->|Errors Found| Alert7[❌ Generation Errors]
    CheckQuality -->|Warnings Found| Warn3[⚠️ Review Recommended]
    CheckQuality -->|All Pass| Success[✅ Campaign Ready]

    Alert1 --> End([Agent Alert])
    Alert2 --> End
    Alert3 --> End
    Alert4 --> End
    Alert5 --> End
    Alert6 --> End
    Alert7 --> End
    Warn1 --> End
    Warn2 --> End
    Warn3 --> End
    Success --> End

    style Start fill:#e1f5ff
    style Success fill:#c8e6c9
    style Alert1 fill:#ffcdd2
    style Alert2 fill:#ffcdd2
    style Alert3 fill:#ffcdd2
    style Alert4 fill:#ffcdd2
    style Alert5 fill:#ffcdd2
    style Alert6 fill:#ffcdd2
    style Alert7 fill:#ffcdd2
    style Warn1 fill:#fff9c4
    style Warn2 fill:#fff9c4
    style Warn3 fill:#fff9c4
    style End fill:#f0f0f0
```

---

## 4. Asset Generation Pipeline

```mermaid
graph LR
    JSON[campaign_config.json] --> Load[Load Configuration]

    Load --> Trans[Translation Service]
    Trans --> TransOut[4 Language Variants]

    Load --> Env[Environment Generator]
    Env --> Gemini1[Google Gemini 2.5 Flash]
    Gemini1 --> EnvOut[4 Background Images]

    Load --> Prod[Product Generator]
    Prod --> Gemini2[Google Gemini 2.5 Flash]
    Gemini2 --> ProdOut[6 Views × N Products]

    TransOut --> Compose[Ad Compositor]
    EnvOut --> Compose
    ProdOut --> Compose

    Compose --> Ad1[1:1 Ads<br/>1080×1080]
    Compose --> Ad2[9:16 Ads<br/>1080×1920]
    Compose --> Ad3[16:9 Ads<br/>1920×1080]

    Ad1 --> Output[outputs/YYYYMMDD_HHMMSS/]
    Ad2 --> Output
    Ad3 --> Output

    style JSON fill:#e1f5ff
    style Load fill:#f0f0f0
    style Trans fill:#fff4e1
    style Env fill:#e8f5e9
    style Prod fill:#fce4ec
    style Gemini1 fill:#ffe0b2
    style Gemini2 fill:#ffe0b2
    style Compose fill:#f3e5f5
    style Output fill:#c8e6c9
```

---

## 5. Alert Severity Levels

```mermaid
graph TB
    Alerts[Campaign Alerts]

    Alerts --> Critical[❌ CRITICAL ALERTS]
    Alerts --> Warning[⚠️ WARNING ALERTS]
    Alerts --> Info[ℹ️ INFO ALERTS]

    Critical --> C1[No Assets Generated<br/>Immediate Action Required]
    Critical --> C2[Incomplete Product Views<br/>Missing Camera Angles]
    Critical --> C3[Generation Failure<br/>API/System Error]
    Critical --> C4[Missing Translations<br/>Localization Enabled]

    Warning --> W1[Low Variant Count<br/>< 3 per aspect ratio]
    Warning --> W2[Insufficient Environment Diversity<br/>< 3 backgrounds]
    Warning --> W3[Single Product + Combined Mode<br/>Consider separate mode]
    Warning --> W4[Long Generation Time<br/>> 10 minutes]
    Warning --> W5[Invalid Campaign ID Format<br/>Not YYYYMMDD_HHMMSS]

    Info --> I1[Campaign Complete<br/>Ready for Review]
    Info --> I2[Generation In Progress<br/>Current Phase: X%]
    Info --> I3[Assets Refreshed<br/>New variants available]

    style Alerts fill:#e1f5ff
    style Critical fill:#ffcdd2
    style Warning fill:#fff9c4
    style Info fill:#c8e6c9
    style C1 fill:#ef5350
    style C2 fill:#ef5350
    style C3 fill:#ef5350
    style C4 fill:#ef5350
    style W1 fill:#ffeb3b
    style W2 fill:#ffeb3b
    style W3 fill:#ffeb3b
    style W4 fill:#ffeb3b
    style W5 fill:#ffeb3b
    style I1 fill:#66bb6a
    style I2 fill:#66bb6a
    style I3 fill:#66bb6a
```

---

## 6. File System Organization

```mermaid
graph TB
    Root[outputs/]

    Root --> C1[20251103_150000/]
    Root --> C2[20251103_153045/]
    Root --> C3[20251104_090000/]

    C1 --> C1Config[campaign_config.json]
    C1 --> C1Env[environments/]
    C1 --> C1Prod[products/]
    C1 --> C1Ads[ads/]

    C1Env --> E1[env_001.png]
    C1Env --> E2[env_002.png]
    C1Env --> E3[env_003.png]
    C1Env --> E4[env_004.png]

    C1Prod --> P1[eco-cleaner_front.png]
    C1Prod --> P2[eco-cleaner_back.png]
    C1Prod --> P3[eco-cleaner_left.png]
    C1Prod --> P4[eco-cleaner_right.png]
    C1Prod --> P5[eco-cleaner_top-down.png]
    C1Prod --> P6[eco-cleaner_bottom-up.png]

    C1Ads --> A1[1_1/]
    C1Ads --> A2[9_16/]
    C1Ads --> A3[16_9/]

    A1 --> A1E[ad_en.png]
    A1 --> A1S[ad_es.png]
    A1 --> A1F[ad_fr.png]

    style Root fill:#e1f5ff
    style C1 fill:#fff4e1
    style C2 fill:#f0f0f0
    style C3 fill:#f0f0f0
    style C1Config fill:#e8f5e9
    style C1Env fill:#fce4ec
    style C1Prod fill:#f3e5f5
    style C1Ads fill:#ffe0b2
```

---

## 7. Campaign Status State Machine

```mermaid
stateDiagram-v2
    [*] --> Configuration

    Configuration --> EnvironmentGeneration: Load JSON

    EnvironmentGeneration --> ProductGeneration: 4 Environments Created
    EnvironmentGeneration --> Failed: API Error

    ProductGeneration --> AdComposition: All Product Views Complete
    ProductGeneration --> Failed: Missing Views

    AdComposition --> GenerationComplete: All Ads Created
    AdComposition --> Failed: Composition Error

    GenerationComplete --> [*]
    Failed --> [*]

    note right of Configuration
        Phase: configuration
        Progress: 0%
    end note

    note right of EnvironmentGeneration
        Phase: environment_generation
        Progress: 25%
        Time: 30-60s
    end note

    note right of ProductGeneration
        Phase: product_generation
        Progress: 60%
        Time: 60-120s per product
    end note

    note right of AdComposition
        Phase: ad_composition
        Progress: 90%
        Time: 30-60s
    end note

    note right of GenerationComplete
        Phase: generation_complete
        Progress: 100%
    end note

    note right of Failed
        Phase: failed
        Check errors array
    end note
```

---

## 8. Expected Asset Counts

```mermaid
graph LR
    Campaign[Campaign]

    Campaign --> Env[Environments]
    Campaign --> Prod[Products]
    Campaign --> Ads[Ad Creatives]

    Env --> Env4[4 Images<br/>Required]

    Prod --> ProdCount{Product Count}
    ProdCount --> P1[1 Product<br/>6 Views]
    ProdCount --> P2[2 Products<br/>12 Views]
    ProdCount --> PN[N Products<br/>6×N Views]

    Ads --> Ratios{Aspect Ratios}
    Ratios --> R1[1:1 Square]
    Ratios --> R2[9:16 Vertical]
    Ratios --> R3[16:9 Landscape]

    R1 --> Local1{Localization?}
    Local1 -->|Yes| L1[4 Languages<br/>4 Ads]
    Local1 -->|No| NL1[1 Ad]

    R2 --> Local2{Localization?}
    Local2 -->|Yes| L2[4 Languages<br/>4 Ads]
    Local2 -->|No| NL2[1 Ad]

    R3 --> Local3{Localization?}
    Local3 -->|Yes| L3[4 Languages<br/>4 Ads]
    Local3 -->|No| NL3[1 Ad]

    style Campaign fill:#e1f5ff
    style Env fill:#fce4ec
    style Prod fill:#f3e5f5
    style Ads fill:#e8f5e9
    style Env4 fill:#ffcdd2
    style L1 fill:#c8e6c9
    style L2 fill:#c8e6c9
    style L3 fill:#c8e6c9
```

---

## 9. Region and Language Mapping

```mermaid
graph TB
    Regions[Target Regions]

    Regions --> NA[North America]
    Regions --> EU[Europe]
    Regions --> AP[Asia Pacific]
    Regions --> LA[Latin America]
    Regions --> MEA[Middle East & Africa]
    Regions --> OC[Oceania]

    NA --> NAL[Languages: en, es, fr]
    EU --> EUL[Languages: en, de, fr, es, it]
    AP --> APL[Languages: en, zh-CN, ja, ko, th]
    LA --> LAL[Languages: es, pt, en]
    MEA --> MEAL[Languages: ar, en, fr]
    OC --> OCL[Languages: en]

    style Regions fill:#e1f5ff
    style NA fill:#fff4e1
    style EU fill:#f0f0f0
    style AP fill:#e8f5e9
    style LA fill:#fce4ec
    style MEA fill:#f3e5f5
    style OC fill:#ffe0b2
    style NAL fill:#c8e6c9
    style EUL fill:#c8e6c9
    style APL fill:#c8e6c9
    style LAL fill:#c8e6c9
    style MEAL fill:#c8e6c9
    style OCL fill:#c8e6c9
```

---

## 10. Monitoring Agent Architecture

```mermaid
graph TB
    Agent[Monitoring Agent]

    Agent --> Input[Input Layer]
    Agent --> Process[Processing Layer]
    Agent --> Output[Output Layer]

    Input --> ReadJSON[Read campaign_config.json]
    Input --> ReadFiles[Scan File System]
    Input --> ReadLogs[Check Generation Logs]

    Process --> Validate[Validate Configuration]
    Process --> Count[Count Assets]
    Process --> Compare[Compare Expected vs Actual]
    Process --> Analyze[Analyze Metrics]

    Validate --> V1[Campaign ID Format]
    Validate --> V2[Required Fields]
    Validate --> V3[Path Existence]

    Count --> C1[Environment Images]
    Count --> C2[Product Views]
    Count --> C3[Ad Creatives]

    Compare --> CP1[Expected Translations]
    Compare --> CP2[Expected Environments]
    Compare --> CP3[Expected Product Views]
    Compare --> CP4[Expected Ad Variants]

    Analyze --> A1[Generation Time]
    Analyze --> A2[File Sizes]
    Analyze --> A3[Variant Diversity]

    Output --> Alert[Generate Alerts]
    Output --> Report[Generate Report]
    Output --> Notify[Notify User]

    Alert --> Critical2[Critical Issues]
    Alert --> Warning2[Warnings]
    Alert --> Info2[Informational]

    style Agent fill:#e1f5ff
    style Input fill:#fff4e1
    style Process fill:#e8f5e9
    style Output fill:#fce4ec
    style Critical2 fill:#ffcdd2
    style Warning2 fill:#fff9c4
    style Info2 fill:#c8e6c9
```

---

Each diagram visualizes a different aspect of the campaign monitoring system:
1. **Sequence Diagram** - Temporal flow of automated workflow
2. **Data Structure** - Hierarchical organization of campaign data
3. **Decision Flow** - Monitoring logic and alert triggers
4. **Pipeline** - Asset generation technical architecture
5. **Alert Levels** - Categorization of monitoring alerts
6. **File System** - Directory structure and organization
7. **State Machine** - Campaign status transitions
8. **Asset Counts** - Expected output calculations
9. **Region Mapping** - Language translation requirements
10. **Agent Architecture** - Monitoring agent internal structure
