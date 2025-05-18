# IUFlowGen 🧠📄➡️📊

**IUFlowGen** is a thesis experiment tool that demonstrates how AI can process procedural documents and automatically transform them into interactive flowcharts. This system provides multiple visualization levels to explore the structural logic of a document in both overview and detailed modes.

---

## 🧪 Project Purpose

This application is part of a thesis experiment aimed at evaluating the effectiveness of AI-based document understanding and flowchart generation. The system is designed to:

- Parse procedural documents
- Extract hierarchical steps and relations
- Visualize them as Graphviz-based flowcharts
- Support interactive exploration with multiple detail levels (Level 1 to Level 4)

---

## 🚀 Features

- 📄 Document input: Procedural text files (`level1.txt`, `level2.txt`, etc.)
- 🧠 AI Processing: Parses and cleans Graphviz DOT representations
- 📊 Visualization: Renders interactive flowcharts using D3.js + Graphviz
- 🧭 Modes: Supports `overview` and `detailed` chart rendering
- ⏱️ Time tracking: Marks experiment time per level
- ⚙️ Settings: Choose rank direction (`LR`, `TB`) and chart visibility

---


## 📂 File Structure

```text
.
├── app.py              # Streamlit frontend
├── backend.py          # Logic for dot parsing and rendering
├── level1.txt          # Sample input for Level 1
├── level2.txt          # Sample input for Level 2
├── level3.txt          # Sample input for Level 3
├── level4.txt          # Sample input for Level 4
├── main.css            # Custom styles for flowchart display
├── requirements.txt    # Dependencies
└── README.md           # You're here
```

---

## 🧰 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🖥️ Run the App

Start the Streamlit app:

```bash
streamlit run app.py
```
Then open your browser at http://localhost:8501

## 📄 License

This project is developed as part of a thesis at **International University – VNU-HCM**. © 2025.
