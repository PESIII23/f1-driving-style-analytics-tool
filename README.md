# Cadillac F1: Driving Style Analytics Tool

## Business Need  
In the high-stakes environment of Formula 1, performance optimization hinges on understanding not just the car, but the driver's interaction with it. While lap time remains the ultimate metric, it is influenced by numerous external factors—car performance, tire compound, track conditions, and traffic.  

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
  - Real-time telemetry (`gm-staging.pitrho.com`)  

### Tools & Frameworks  
- Which tools are preferred for analysis and visualization?  
  - Plotly, Streamlit, PowerBI, Jupyter Notebook

### Role of AI/ML in Motorsport  
- How should a motorsports AI/ML scientist think?  
  - How to translate data into racing terminology?  
  - Can you handle handle ambiguity well?  
  - Prioritizing data quality over flashy UIs given time constraints and solo-approach ("garbage in, garbage out")  

### Beyond Dashboards  
- What differentiates a meaningful solution? 
  - Tangible racing explanations ("these two drivers show similar braking patterns because…")  
  - Timeboxing ideas to avoid rabbit holes  
  - Innovating even if at 70% completion
  - Well-defined deliverables

### End-of-Project Value  
- How will results be reviewed and integrated into real F1 decision-making?  
  - GM Motorsports team open to reviewing results once ready
 
---

## How This Repo Fits In  
This repository represents my **practical answer to the project and discovery questions above**.  
By combining clustering, anomaly detection, and telemetry-based analysis, I demonstrate how those insights translate into an end-to-end solution for understanding and comparing driver styles in Formula 1.  
