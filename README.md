# Cadillac F1: Driving Style Analytics Tool

## Business Need  
In the high-stakes environment of Formula 1, performance optimization hinges on understanding not only the car, but the driver's interaction with it. While lap time remains the ultimate metric, it is influenced by numerous external factors such as car performance, tire compound, track conditions, traffic, and more.  

## Objective  
To isolate and understand driver behavior, Cadillac F1 requires a telemetry-driven analytics tool that can cluster drivers by driving style, independent of lap time.  

## Key Research Questions  
- Is there a driving style that is faster overall?  
- Which style yields higher average speed?  
- Can tire wear be correlated to driving style?  
- How do we control for driver, compound, traffic, and weather?  

## Recommended Deliverables  
- Clustering algorithm for driving styles  
- Visual dashboard for style comparison  
- Anomaly detection module  
- Tire wear correlation model  

## Advanced Analytics Directions  
- What makes a lap fast for a given driver?  
- Detect anomalous laps, including:  
  - Outlier inputs (e.g., defending against another driver)  
  - Deviations from typical driving style  

---

## My Contribution: Piloting the Capstone Early  
This project is typically assigned as a **senior capstone**, but I am **piloting it a semester earlier**. Doing so allows me to:  
- Build foundational approaches before future teams take it on  
- Explore innovative solutions with fewer constraints  
- Establish early connections with GM Motorsports engineers  

---

## Discovery Questions to the GM Motorsports Team  
To better understand their context, workflows, and expectations, I asked guiding questions such as:  

### Systems & Applications  
- What platforms and architectural components drive motorsport analytics?  
  - Python microservices  
  - Kafka pipelines (big data messaging)
  - Modernizing apps using React (from CoffeeScript)  
  - Real-time telemetry integration (`gm-staging.pitrho.com`)  

### Tools & Frameworks  
- Which tools are preferred for analysis and visualization?  
  - Jupyter Notebook, Plotly, Streamlit, PowerBI  

### Key Considerations
- How would an experienced AI/ML Engineer approach the problem?
  - Prioritize data quality over flashy UI, given time constraints and solo-approach
  - Timeboxing ideas to avoid rabbit holes

### Beyond Dashboards  
- What differentiates a meaningful solution?
  - Tangible racing explanations ("these two drivers show similar braking patterns because…")  
  - Innovative even if at 70% completion

### End-of-Project Value  
- How will results be reviewed and integrated into real F1 decision-making?  
  - GM Motorsports team open to reviewing results once ready
 
---

## How This Repo Fits In  
This repository represents my **practical answer to the project and discovery questions above**.  
By combining clustering, anomaly detection, and telemetry-based analysis, I demonstrate how those insights translate into an end-to-end solution for understanding and comparing driver styles in Formula 1.  
