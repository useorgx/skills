You are launching a new initiative from a single goal statement.

## Quick Start

1. Confirm the goal, scope, and any timeline hints.
2. Check for existing initiatives to avoid duplicates.
3. Create the initiative, milestones, workstreams, and starter tasks.
4. Launch the initiative if the user wants execution to start immediately.

## Input

The user provides a one-line goal describing what they want to accomplish. Examples:

- "Launch our mobile app in the App Store by Q2"
- "Migrate our infrastructure to Kubernetes"
- "Build an AI-powered customer support chatbot"

## Process

### Step 1: Parse the Goal

Extract from the goal statement:

- **Core objective**: What is the primary outcome?
- **Domain signals**: Which teams/domains are involved? (engineering, product, marketing, sales, operations, design)
- **Timeline hints**: Any dates or quarters mentioned?
- **Success indicators**: What would "done" look like?

### Step 2: Create the Initiative

Use `mcp__orgx__create_entity` with type="initiative" to create:

- **title**: Clear, action-oriented title (e.g., "Mobile App Launch Q2 2025")
- **description**: 2-3 sentence summary including:
  - What we're building/achieving
  - Why it matters (business impact)
  - Key constraints or dependencies
- **priority**: "high" for strategic goals, "medium" for operational improvements

### Step 3: Define Milestones (3-5)

Create milestones that represent major checkpoints. Each milestone should be:

- **Time-bound**: Include realistic due_date (YYYY-MM-DD format)
- **Measurable**: Clear definition of done
- **Sequential**: Earlier milestones enable later ones

Typical milestone pattern:

1. **Discovery/Planning** (Week 1-2): Requirements, research, architecture decisions
2. **Foundation** (Week 3-4): Core infrastructure, setup, initial builds
3. **Core Development** (Week 5-8): Main feature implementation
4. **Integration/Testing** (Week 9-10): QA, bug fixes, integration testing
5. **Launch/Delivery** (Final week): Go-live, monitoring, handoff

Use `mcp__orgx__create_entity` with type="milestone" for each, linking to the initiative_id.

### Step 4: Create Workstreams

Workstreams organize work by domain. Based on the goal, create relevant workstreams:

| Domain          | When to Create                      | Example Tasks                     |
| --------------- | ----------------------------------- | --------------------------------- |
| **engineering** | Technical implementation needed     | Architecture, coding, DevOps      |
| **product**     | Product decisions/specs needed      | PRD, user stories, prioritization |
| **marketing**   | External communication needed       | Messaging, launch plan, content   |
| **sales**       | Revenue impact or customer outreach | Enablement, pricing, demos        |
| **operations**  | Process/workflow changes needed     | Runbooks, training, support       |
| **design**      | UI/UX work needed                   | Wireframes, prototypes, assets    |

Use `mcp__orgx__create_entity` with type="workstream" for each, linking to the initiative_id.

### Step 5: Assign Agents to Workstreams

For each workstream, use `mcp__orgx__spawn_agent_task` to assign the appropriate agent:

- Match agent type to workstream domain
- Provide clear context about the initiative and their responsibilities
- Include the initiative_id for tracking

Agent types: product, engineering, marketing, sales, operations, design, orchestrator

### Step 6: Configure Agent Autonomy (Optional)

If the user specifies trust preferences, use `mcp__orgx__configure_agent` to set:

- **trust_level**: "strict" (approve everything), "balanced" (approve key decisions), "autonomous" (minimal oversight)
- **focus_areas**: Specific areas the agent should prioritize
- **approval_required**: Actions that need human sign-off
- **skip_approval**: Actions that can proceed automatically

### Step 7: Launch the Initiative

After all components are created, use `mcp__orgx__launch_entity` with type="initiative" to activate it.

## Output

Provide a summary to the user including:

1. **Initiative created**: Title and ID
2. **Milestones**: List with due dates
3. **Workstreams**: List with assigned agents
4. **Next steps**: What the user should expect (agent activity, first decisions)

## Guidelines

- Ask clarifying questions if the goal is ambiguous (timeline, scope, priority)
- Default to 2-week sprints for milestone spacing if no timeline given
- Always create at least engineering and product workstreams for technical goals
- Include an orchestrator agent task to coordinate cross-functional work
- Keep descriptions concise but specific; avoid generic filler text

## Failure Handling

- If a similar initiative already exists, pause and ask whether to update it or create a new one.
- If OrgX MCP tools are unavailable, explain what is missing and stop rather than guessing.
