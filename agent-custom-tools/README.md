# Astronomy Agent with Custom Tools

An AI-powered agent that helps users explore astronomical events and calculate telescope rental costs using Azure AI Project SDK. The agent uses custom tool integration to access real-time event data and pricing information.

## Overview

This project demonstrates how to build an intelligent agent that:
- Provides information about upcoming astronomical events visible from specific locations
- Calculates telescope rental costs based on tier, duration, and priority level
- Generates professional observation reports for organizations

The agent is powered by Azure's Prompt Agent framework and uses three custom tools to interact with astronomical data.

---

## Project Structure

```
agent-custom-tools/
├── agent.py                      # Main agent application
├── functions.py                  # Custom tool implementations
├── requirements.txt              # Python dependencies
├── initdev.sh                    # Development environment setup script
├── test_script.md                # Test cases for agent functionality
├── data/                         # Data files for tools
│   ├── events.txt               # Astronomical events database
│   ├── telescope_rates.txt       # Pricing rates by telescope tier
│   └── priority_multipliers.txt  # Cost multipliers by priority level
└── reports/                      # Generated observation reports (created at runtime)
```

---

## Setup Instructions

### Prerequisites

- Python 3.10 or later
- Azure subscription with AI Projects resources
- Environment variables configured (see below)

### 1. Create Virtual Environment

```bash
cd /projects/agent-custom-tools
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `python-dotenv` - Environment variable management
- `azure-identity` - Azure authentication
- `azure-ai-projects` - Azure AI Project client
- `openai` - OpenAI API client (used by Azure)

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
PROJECT_ENDPOINT=<your-azure-project-endpoint>
MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

Obtain these values from your Azure AI Project resource in the Azure Portal.

---

## How It Works

### Step-by-Step Flow

#### 1. **Agent Initialization** (`agent.py` - lines 1-40)
   - Load environment variables from `.env`
   - Connect to Azure AI Project client using default Azure credentials
   - Create an OpenAI client for agent interactions

#### 2. **Define Custom Tools** (`agent.py` - lines 45-130)
   The agent is configured with three custom tools:

   **Tool 1: `next_visible_event`**
   - Located in: `functions.py` (lines 48-57)
   - Purpose: Find upcoming astronomical events visible from a given location
   - Input: continent name (e.g., "south_america")
   - Output: Event name, type, date, and visible locations
   - Example: "Find the next event visible from South America" → "Jupiter-Venus Conjunction on May 1st"

   **Tool 2: `calculate_observation_cost`**
   - Located in: `functions.py` (lines 60-82)
   - Purpose: Calculate telescope rental costs based on specifications
   - Inputs:
     - `telescope_tier`: "standard", "advanced", or "premium"
     - `hours`: Duration of observation (float)
     - `priority`: "low", "normal", or "high"
   - Output: Base cost, total cost with priority multiplier, and itemized breakdown
   - Formula: `total_cost = (hourly_rate × hours) × priority_multiplier`
   - Example: "5 hours of premium telescope at normal priority" → "$1,875"

   **Tool 3: `generate_observation_report`**
   - Located in: `functions.py` (lines 85-135)
   - Purpose: Create a formal observation report and save it to a file
   - Inputs: Event name, location, telescope tier, hours, priority, observer name
   - Output: Formatted report saved as `report_<event>_<timestamp>.txt`
   - Report includes: Event details, telescope specifications, cost breakdown, and professional formatting

#### 3. **Create Agent Configuration** (`agent.py` - lines 132-148)
   - Define agent name: `"astronomy-agent"`
   - Set system instructions for agent behavior
   - Register all three custom tools with the agent
   - Deploy agent using Azure AI Projects

#### 4. **Create Conversation Thread** (`agent.py` - line 152)
   - Initialize a chat conversation with unique session ID
   - Maintains context across multiple user interactions

#### 5. **User Interaction Loop** (`agent.py` - lines 155-170)
   - Accept user prompts via command line
   - Send prompts to agent for processing
   - Handle function call execution

#### 6. **Function Call Processing** (`agent.py` - lines 173-210)
   - **Wait for tool invocations**: Agent analyzes user input and determines which tools to call
   - **Execute tools**: 
     - If `next_visible_event` is called, fetch event data from `data/events.txt`
     - If `calculate_observation_cost` is called, lookup rates from `data/telescope_rates.txt` and multipliers from `data/priority_multipliers.txt`
     - If `generate_observation_report` is called, create and save a formatted report file
   - **Return results**: Send tool outputs back to agent for final response generation
   - **Loop**: Repeat until agent stops issuing function calls
   - **Display response**: Print final answer to user

#### 7. **Cleanup** (`agent.py` - lines 212-213)
   - Delete agent from Azure
   - Close connections

---

## Data Files

### `data/events.txt`
Database of astronomical events with format: `name|type|date|locations`

```
Jupiter-Venus Conjunction|conjunction|05-01|north_america;south_america;europe;asia;africa;australia
Perseids Meteor Shower|meteor_shower|08-12|north_america;europe;asia
```

- **Date format**: MM-DD (month-day)
- **Locations**: Semicolon-separated hemisphere/region codes
- **Available locations**: `north_america`, `south_america`, `europe`, `asia`, `africa`, `australia`, `antarctica`

### `data/telescope_rates.txt`
Hourly rental rates by telescope tier: `tier|hourly_rate`

```
standard|100.0
advanced|200.0
premium|375.0
```

### `data/priority_multipliers.txt`
Cost multipliers by observation priority: `priority|multiplier`

```
low|0.8
normal|1.0
high|1.5
```

---

## Example Usage

### Running the Agent

```bash
python agent.py
```

The agent enters an interactive loop accepting user prompts.

### Example Interaction 1

**User Input:**
```
Find me the next event I can see from South America
```

**Agent Process:**
1. Calls `next_visible_event(location="south_america")`
2. Searches `data/events.txt` for events >= today with south_america visible
3. Returns: Jupiter-Venus Conjunction on May 1st

**Agent Output:**
```
The next astronomical event you can observe from South America is the Jupiter-Venus Conjunction, taking place on May 1st.
```

### Example Interaction 2

**User Input:**
```
What would be the cost for 5 hours of premium telescope time at normal priority?
```

**Agent Process:**
1. Calls `calculate_observation_cost(telescope_tier="premium", hours=5, priority="normal")`
2. Calculates: ($375/hour × 5 hours) × 1.0 multiplier = $1,875
3. Returns itemized cost breakdown

**Agent Output:**
```
The cost for 5 hours of premium telescope time at normal priority for this observation will be $1,875.
```

### Example Interaction 3

**User Input:**
```
Generate that information in a report for Bellows College.
```

**Agent Process:**
1. Calls `generate_observation_report(event_name="Jupiter-Venus Conjunction", location="South America", telescope_tier="premium", hours=5, priority="normal", observer_name="Bellows College")`
2. Creates formatted report from templates
3. Saves to file: `report_jupiter-venus_conjunction_2026-03-19_1518.txt`

**Agent Output:**
```
Here is your report for Bellows College:

- Next visible astronomical event: Jupiter-Venus Conjunction
- Date: May 1st
- Visible from: South America
- Observation details:
    - Telescope tier: Premium
    - Duration: 5 hours
    - Priority: Normal
- Observation cost: $1,875

A formal report has been generated for Bellows College.
```

---

## Code Walkthrough

### `agent.py` - Agent Orchestration

**Main function flow:**

```python
def main():
    # 1. Load environment and connect to Azure
    load_dotenv()
    project_client = AIProjectClient(...)
    openai_client = project_client.get_openai_client()
    
    # 2. Define tool schemas
    event_tool = FunctionTool(name="next_visible_event", ...)
    cost_tool = FunctionTool(name="calculate_observation_cost", ...)
    report_tool = FunctionTool(name="generate_observation_report", ...)
    
    # 3. Create agent with tools
    agent = project_client.agents.create_version(
        definition=PromptAgentDefinition(
            model=model_deployment,
            tools=[event_tool, cost_tool, report_tool]
        )
    )
    
    # 4. Main conversation loop
    while True:
        user_input = input("USER: ")
        # Send to agent
        # Process function calls
        # Display response
```

### `functions.py` - Tool Implementations

**Three main functions:**

1. **`next_visible_event(location: str) -> str`**
   - Parses location parameter
   - Compares today's date against event dates in database
   - Returns JSON with event details

2. **`calculate_observation_cost(telescope_tier: str, hours: float, priority: str) -> str`**
   - Validates inputs against available tiers and priorities
   - Loads rates and multipliers from data files
   - Calculates: `base_cost × priority_multiplier`
   - Returns JSON with cost breakdown

3. **`generate_observation_report(...) -> str`**
   - Calls both `next_visible_event()` and `calculate_observation_cost()` internally
   - Formats data into professional report template
   - Saves to timestamped file
   - Returns JSON with file path

**Helper functions:**

- `_load_events()` - Reads and parses `events.txt`, sorts by date
- `_load_rates()` - Reads `telescope_rates.txt` and `priority_multipliers.txt`

---

## Testing

The project includes a test script documenting expected agent behavior:

```bash
cat test_script.md
```

Contains two test cases:
1. **Test Case 1**: Find next event + calculate cost
2. **Test Case 2**: Generate observation report

Run manual tests by following the user inputs in `test_script.md`.

---

## Troubleshooting

### Issue: `Cannot connect to Azure`
**Solution:** Verify `.env` file has correct `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME`. Ensure Azure credentials are configured (run `az login`).

### Issue: `Module not found: azure.ai.projects`
**Solution:** Ensure virtual environment is activated and dependencies installed:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Issue: `Data files not found`
**Solution:** Ensure you're running from project root directory:
```bash
cd /Users/davidsanchez/Projects/02-agent-custom-tools
```

### Issue: Function calls not executing
**Solution:** Verify tool definitions match function signatures in `functions.py`. Check tool parameter names and types.

---

## Architecture Diagram

```
User Input
    ↓
Agent (Azure AI Projects)
    ├─ Analyzes input
    ├─ Determines which tools to call
    └─ Executes function calls
        ↓
    Custom Tools
    ├─ next_visible_event()      → reads data/events.txt
    ├─ calculate_observation_cost() → reads data/telescope_rates.txt
    └─ generate_observation_report() → creates reports/
        ↓
    Results back to Agent
        ↓
    Generate Natural Language Response
        ↓
    Display to User
```

---

## Key Concepts

### Tool Definition
Each tool requires a JSON schema describing:
- `name`: Tool identifier
- `description`: What the tool does
- `parameters`: Input parameter schema with types
- `strict`: Whether to strictly enforce the schema

### Function Calls
The OpenAI API returns `response.output` containing:
- `item.type == "function_call"`: Tool invocation
- `item.name`: Which tool to call
- `item.arguments`: JSON parameters
- `item.call_id`: Unique identifier for this call

### Response Loop
After tool execution, the agent needs results back via:
```python
FunctionCallOutput(
    type="function_call_output",
    call_id=...,
    output=result
)
```

This allows the agent to incorporate tool results into its final response.

---

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `PROJECT_ENDPOINT` | Azure AI Project endpoint URL | `https://project-xyz.eastus.inference.ml.azure.com` |
| `MODEL_DEPLOYMENT_NAME` | LLM deployment name | `gpt-4-turbo` |

---

## References

- [Azure AI Projects SDK Documentation](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/develop/agents-reference)
- [Function Calling with OpenAI API](https://platform.openai.com/docs/guides/function-calling)
- [Azure Authentication](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme)
