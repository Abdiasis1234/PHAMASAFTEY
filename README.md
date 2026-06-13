https://github.com/a2anet/a2a-hackathon-template
# Pharma Safety Tri-Agent System

A multi-agent customer support and research system built for the Google A2A Hackathon.

This project explores how three specialised agents can communicate over the Agent-to-Agent protocol to handle pharmaceutical safety reports, such as adverse drug reaction reports, missing patient details, medicine-related complaints, and regulatory escalation cases.

## Problem

Pharmaceutical companies receive large volumes of safety-related messages from patients, doctors, pharmacists, and support teams. These reports often contain incomplete, emotional, or unstructured information.

In regulated healthcare environments, missing important details can delay escalation, risk patient safety, and create compliance issues.

## Solution

The Pharma Safety Tri-Agent System uses three cooperating agents:

1. **Personal Agent**
2. **Customer Service Agent**
3. **Research Agent**

Together, they transform an unstructured customer message into a structured safety case, research the relevant medical and regulatory context, and recommend the correct next action.

## Agent Roles

### 1. Personal Agent

The Personal Agent receives the original customer or patient message.

Its role is to understand and structure the message before passing it to the Customer Service Agent.

It extracts:

- Patient concern
- Medicine name
- Symptoms
- Dosage
- Timeline
- Severity
- Missing information
- Emotional tone
- Urgency level

Example output:

```json
{
  "case_type": "adverse_drug_reaction",
  "medicine": "ExampleMed",
  "symptoms": ["dizziness", "nausea"],
  "severity": "moderate",
  "missing_fields": ["dosage", "patient_age"],
  "urgency": "high",
  "summary": "Patient reports dizziness and nausea after taking ExampleMed."
}
