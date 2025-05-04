# Botnet Detection Using Flow-Based Machine Learning

This repository contains the full pipeline for detecting botnet network traffic using flow-level features and classical machine learning models. The approach follows a two-phase structure: data preprocessing and feature engineering, followed by model training, evaluation, and optimization. The project leverages the ISOT Botnet dataset and highlights the effectiveness of flow-based detection using Random Forest classifiers.

## Dataset Reference

The ISOT Botnet dataset used in this project is available at:
[https://onlineacademiccommunity.uvic.ca/isot/2022/11/27/botnet-and-ransomware-detection-datasets/](https://onlineacademiccommunity.uvic.ca/isot/2022/11/27/botnet-and-ransomware-detection-datasets/)

The dataset consists of PCAP files containing both normal and malicious traffic generated from multiple botnet families.

---

## Project Phases

### Phase 1: Data Collection & Preprocessing

1. **PCAP to CSV Conversion**:
   - Used a Python wrapper over Tshark to convert PCAP files to CSVs.
   - Focused only on essential packet fields to reduce size and processing load.

2. **Cleaning**:
   - Dropped irrelevant fields such as MAC addresses and textual headers.
   - Removed rows with missing or corrupt values.

3. **Visualization**:
   - Used distribution plots (KDE) to study packet size and protocol skew.
   - Identified imbalances and anomalies in botnet vs. normal traffic.

4. **Encoding**:
   - Label encoding for protocol fields.
   - Normalization was skipped as tree-based models are scale-invariant.

---

### Phase 2: Feature Engineering & Modeling

1. **Flow-Based Feature Extraction**:
   - Created `flow_id` using 5-tuple (source IP, destination IP, protocol, source port, destination port).
   - Aggregated per-flow statistics:
     - Packet count
     - Total and average packet size
     - Standard deviation of packet size
     - Flow duration
     - Bytes per second
     - Packets per second
     - TCP flag count
     - Small packet count

2. **Handling Imbalanced Data**:
   - Applied SMOTE (Synthetic Minority Oversampling Technique) to balance the dataset before training.

3. **Model Training**:
   - Trained Decision Tree, Random Forest, and Extra Trees classifiers.
   - Fine-tuned Random Forest across tree depths (1 to 29) to examine overfitting vs. underfitting.

4. **Evaluation Metrics**:
   - Accuracy
   - Precision
   - Recall
   - F1 Score
   - ROC-AUC
   - MCC (Matthews Correlation Coefficient)

5. **Model Comparison & Visualizations**:
   - Plotted F1 vs. depth to visualize overfitting.
   - ROC Curve for final evaluation.
   - Feature importance graph for interpretability.

---

## Features Extracted

| Feature Name          | Description                                             |
|-----------------------|---------------------------------------------------------|
| packet_count          | Number of packets in the flow                           |
| total_bytes           | Total size of all packets in bytes                      |
| avg_packet_size       | Mean packet size within the flow                        |
| std_packet_size       | Standard deviation of packet sizes                      |
| flow_duration         | Time difference between first and last packet           |
| bytes_per_second      | Data rate in bytes/second                               |
| packets_per_second    | Packet rate in packets/second                           |
| tcp_flag_count        | Count of packets with TCP flags                         |
| small_packets         | Number of packets < 128 bytes                           |

---

## ROC Curve and Feature Importance

- ROC curves demonstrate the model's ability to distinguish between classes across thresholds.
- Feature importance plot reveals key contributors (e.g., flow duration, byte rate) to detection accuracy.

---
Install dependencies:
```
- Python 3.8+
- scikit-learn
- pandas, numpy
- seaborn, matplotlib
- imbalanced-learn
- tshark (CLI)
```

References
1) Stevanovic & Pedersen (2014): "An Efficient Flow-based Botnet Detection Using Supervised Machine Learning"
      Introduced minimal packet analysis for flow classification.
      Demonstrated Random Forest and Decision Trees as best-performing models.
   
2) Abrantes et al. (2022): "A dataset-centric analysis for botnet traffic classification using machine learning"
      Addressed pitfalls in feature leakage using IPs/ports.
      Emphasized per-botnet evaluation and SMOTE balancing.

ISOT Dataset:
https://onlineacademiccommunity.uvic.ca/isot/2022/11/27/botnet-and-ransomware-detection-datasets/

Papers:
<p><a href="https://www.sciencedirect.com/science/article/pii/S1877050921022213?ref=pdf_download&fr=RR-2&rr=93a8be554bb04418">Exploring Dataset Manipulation via Machine Learning for Botnet Traffic </a></p>
<p><a href="https://sci-hub.se/10.1109/ICCNC.2014.6785439">An efficient flow-based botnet detection using supervised machine learning </a></p>




