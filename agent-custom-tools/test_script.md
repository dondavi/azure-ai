# Astronomy Agent Test Script

## Test Suite: Agent.py Functionality Tests

### Test Case 1: Find Next Visible Event and Calculate Observation Cost

**Objective:** Verify that the agent can retrieve the next visible astronomical event in a specified location and calculate telescope rental costs.

**User Input:**
```
Find me the next event I can see from South America and give me the cost for 5 hours of premium telescope time at normal priority.
```

**Function Calls Expected:**
- `next_visible_event(location="south_america")`
- `calculate_observation_cost(telescope_tier="premium", hours=5, priority="normal")`

**Expected Agent Response:**
```
The next astronomical event you can observe from South America is the Jupiter-Venus Conjunction, taking place on May 1st.
The cost for 5 hours of premium telescope time at normal priority for this observation will be $1,875.
```

**Assertions:**
- ✓ Event retrieved: Jupiter-Venus Conjunction
- ✓ Event date: May 1st
- ✓ Location: South America
- ✓ Cost calculated: $1,875
- ✓ Telescope tier: Premium
- ✓ Duration: 5 hours
- ✓ Priority: Normal

---

### Test Case 2: Generate Observation Report

**Objective:** Verify that the agent can generate a formal observation report for a given organization.

**User Input:**
```
Generate that information in a report for Bellows College.
```

**Function Calls Expected:**
- `generate_observation_report(event_name="Jupiter-Venus Conjunction", location="South America", telescope_tier="premium", hours=5, priority="normal", observer_name="Bellows College")`

**Expected Agent Response:**
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

**Assertions:**
- ✓ Report generated successfully
- ✓ Report includes event name
- ✓ Report includes observation location
- ✓ Report includes telescope specifications
- ✓ Report includes cost information
- ✓ Report formatted for organization (Bellows College)