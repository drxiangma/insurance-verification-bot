# Insurance Verification AI Agent

## Overview

This AI agent automates the insurance verification process for personal injury clients. It utilizes conversational AI and natural language processing (NLP) capabilities, deployed in the Microsoft Azure environment. The agent can process patient data, contact insurance companies, verify coverage details, and document interactions.

## Features

1. **Input Patient Data**: Accepts an Excel workbook containing patient and insurance company details.
2. **Automated Calling**: Uses Twilio API to initiate and manage phone calls with insurance companies.
3. **Conversational AI**: Leverages Azure Cognitive Services for NLP to:
   - Navigate automated phone systems.
   - Communicate with human representatives.
4. **Resilient Interaction**:
   - Handles dropped calls, incorrect information, and unresponsive systems.
5. **Documentation**:
   - Records, transcribes, and exports conversation details to another Excel workbook.
6. **Secure Operations**: Uses Azure Key Vault for managing secrets and encryption.

---

## Technology Stack

- **Microsoft Azure Services**:
  - Azure Bot Service
  - Azure Cognitive Services (Speech and Text Analytics)
  - Azure Functions
  - Azure SQL Database
  - Azure Key Vault
- **Twilio API**: For programmatic phone calls.
- **Programming Language**: Python

---

## Prerequisites

1. **Software Requirements**:
   - Python 3.8+
   - Microsoft Azure account
   - Twilio account
2. **Python Libraries**:
   - `twilio`
   - `azure-cognitiveservices-speech`
   - `azure-ai-textanalytics`
   - `openpyxl`
3. **Azure/Twilio Accounts**:
   - `AZURE_SPEECH_KEY`: Your Azure Speech service key.
   - `AZURE_REGION`: Your Azure region.
   - `AZURE_TEXT_KEY`: Your Azure Text Analytics key.
   - `TWILIO_SID`: Your Twilio Account SID.
   - `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token.
   - `TWILIO_PHONE_NUMBER`: Your Twilio phone number.

---

## Setup and Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/insurance-verification-ai.git
cd insurance-verification-ai
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Azure Services
- Set up Azure Cognitive Services for Speech and Text Analytics.
- Set up Azure SQL Database to store patient and insurance data.
- Configure Azure Key Vault to manage secrets.
### 4. Configure Twilio
- Obtain a Twilio account SID, auth token, and phone number.
- Add these to Azure Key Vault.
### 5. Input Data
Prepare an Excel file with patient and insurance company details in the following format:

Patient ID |	Patient Name |	Insurance Company	| Insurance Phone

Place this file in the `input/` directory.
### 6. Run the Application
```bash
python main.py
```
The application will process the input data, make calls, document interactions, and export results to the `output/` directory.
