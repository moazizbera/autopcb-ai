# AutoPCB-AI

Constraint-Based Circuit Design Engine (MVP)

---

## 🚀 Overview

AutoPCB-AI is a backend system that simulates a simplified Electronic Design Automation (EDA) engine.

It converts electrical requirements into basic circuit designs using deterministic rules and engineering logic.

---

## 🧠 Purpose

This project demonstrates:

- Backend system design (FastAPI)
- Clean architecture separation
- Engineering-style problem decomposition
- Basic circuit reasoning using Ohm’s Law

It is NOT a UI project or AI demo — it is a structured backend engineering prototype.

---

## 🏗️ Architecture

The system is structured into clear layers:

- API Layer → request handling (FastAPI)
- Service Layer → orchestration logic
- Engine Layer → core circuit computation
- Schema Layer → validation and contracts
- Domain Layer → circuit models

---

## ⚙️ Current Functionality (MVP)

Input:
- Voltage
- Target component (LED)

Output:
- Resistor value (calculated using Ohm’s Law)
- Simple circuit connection

---

## 🔌 Example

### Request

```json
{
  "voltage": 5,
  "target_component": "LED"
}
```

### Response

```json
{
  "resistor_value": "150 Ohm",
  "circuit": "VCC -> 150 Ohm -> LED -> GND"
}
```

## 🧪 Run Project

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
```
open 

http://localhost:8000/docs

---

## 🧠 Design Principles

- Separation of concerns  
- Stateless engine logic  
- Clean service orchestration  
- Extensible architecture for future EDA expansion  

---

## 📌 Future Direction

- Multi-component circuits  
- Graph-based circuit representation  
- Constraint validation engine  
- Optimization layer (cost, efficiency, power)  
---
