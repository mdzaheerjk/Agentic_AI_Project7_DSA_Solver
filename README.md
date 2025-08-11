# 🧮 Agentic AI Project 7: DSA Solver

![Python](https://img.shields.io/badge/Python-3.12%2B-brightgreen)
![Agentic AI](https://img.shields.io/badge/Agentic%20AI-DSA%20Solver-blue)
![DSA Solver](https://img.shields.io/badge/AI-DSA%20Solver-orange)
![License](https://img.shields.io/badge/License-GPL--3.0-orange)

A powerful, agentic, end-to-end AI platform for solving Data Structures & Algorithms (DSA) problems. This project integrates modular multi-agent design and code execution tools to solve, explain, and evaluate DSA challenges using LLMs and real-time code execution. Built for extensibility, learning, and competitive programming.

> 📁 **Repository:** `Agentic_AI_Project7_DSA_Solver`

---

## 🚀 Project Highlights

- 🧩 **AI DSA Problem Solving:**  
  Automatically solves DSA problems, generates explanations, and tests solutions.
- 🤖 **Agentic AI Architecture:**  
  Modular agent system for code generation, debugging, and evaluation.
- ⚙️ **Live Code Execution:**  
  Executes generated code in isolated Docker containers for safety and accuracy.
- 📊 **Evaluation & Feedback:**  
  Provides output, error logs, and step-by-step explanations.
- 🧩 **Extensible:**  
  Add new agent roles, problem types, or evaluation strategies easily.

---

## 🧠 Technical Stack

- **Python 3.12+**
- **Agentic AI Patterns**
- **Docker (for code execution)**
- **LLMs for code & explanation generation**
- **Modular agent, team, and tool abstractions**

---

## 🏗️ Project Structure

```bash
Agentic_AI_Project7_DSA_Solver/
├── app.py                          # Main entry point
├── main.py
├── requirements.txt
├── LICENSE
├── README.md
├── 1. Project Structure.ipynb
├── Autogen Projects.excalidraw
├── diagram-export-6-12-2025-11_40_32-PM.png
├── example.py
├── team_example.py
├── agent-be.py
├── agent-be enhanced.py
├── autogen_backend.py
├── streamlit_app.py                # Optional web UI
├── output-1.lua
├── output-2.lua
├── output-3.lua
├── AlgoGenie/
│   └── ...                         # Additional AlgoGenie modules
├── agents/
│   ├── __init__.py
│   ├── code_executor_agent.py
│   └── problem_solver.py
├── config/
│   ├── constant.py
│   ├── docker_executor.py
│   ├── docker_utils.py
│   └── settings.py
├── team/
│   └── dsa_team.py
├── temp/
│   └── ...                         # Temporary code and results
├── Project Unstructured/
│   └── ...                         # Unstructured assets
├── tests/
│   └── ...                         # (if present)
└── __pycache__/
```

---

## ⚡ Installation & Usage

### 1. Clone the repository
```bash
git clone https://github.com/mdzaheerjk/Agentic_AI_Project7_DSA_Solver.git
cd Agentic_AI_Project7_DSA_Solver
```

### 2. Set up a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Configure Docker for code execution
- Ensure Docker is installed and running for safe code evaluation.

### 5. Run the DSA solver
```bash
python app.py
```
or (for the web UI):
```bash
streamlit run streamlit_app.py
```
or (alternate entry):
```bash
python main.py
```

---

## 🧪 Example Usage

- **Solve DSA Problems:**  
  Input a DSA question and receive a generated solution, explanation, and test case analysis.
- **Live Execution & Feedback:**  
  View output, error logs, and stepwise reasoning for each generated solution.
- **Extend Easily:**  
  Add new agent types for hints, optimization, or multi-language support.

---

## 🧩 Extensibility

- **Add More Agents:**  
  Implement agents for specific DSA domains (graphs, DP, etc.), test generation, or peer review.
- **Custom Evaluation:**  
  Expand with new scoring, plagiarism detection, or code style checks.

---

## 📚 Documentation

See comments in source files and agent/team modules for extension instructions and workflow details.

---

## ✍️ Author

**Mohammed Zaheeruddin**  
🎓 First-Year B.Tech Student | AI/ML & GenAI Enthusiast  
🏫 Shetty Institute of Technology, Gulbarga  
📧 info.zaheerjk@gmail.com

---

## 📜 License

This project is licensed under the **GPL-3.0 License** – see the LICENSE file for details.

---

#### Key Features:
1. Multi-agent, LLM-powered DSA problem solving and code execution
2. Modular, extensible Python codebase for rapid learning and research
3. Add new agent roles, problem types, or evaluation strategies
4. Designed for competitive programming, education, and self-study
