# Copilot Coding Agent Instructions

> This file provides instructions for GitHub Copilot Coding Agent when working on this repository.

## Environment Setup

- Python 3.12+ required
- Install dependencies: `pip install -e ".[dev]"`
- Azure CLI and azd must be available for infrastructure tasks
- Run tests: `pytest tests/ -v`
- Lint: `ruff check src/ tests/`
- Format: `ruff format src/ tests/`

## Working on This Repository

### Adding a New Specialist Agent

When asked to add a new agent:

1. **Determine the category**: intake, market_intelligence, analysis, decision, communication, or coaching
2. **Create the agent file** at `src/agents/<category>/<agent_name>.py`:
   ```python
   """
   Insurance Competitive Quote Intelligence — <Agent Name>
   
   <One-line description of what this agent does.>
   
   Azure Services: <List Azure services this agent uses>
   """
   
   from typing import Any
   from agent_framework import Agent, AgentContext
   
   
   class <AgentClassName>(Agent):
       """<Docstring explaining the agent's role in the pipeline>"""
   
       name = "<kebab-case-name>"
       description = "<One sentence>"
       model = "gpt-4o-mini"  # Use gpt-4o for complex reasoning, gpt-4o-mini for simpler tasks
   
       system_prompt = """<System prompt instructions>"""
   
       async def run(self, context: AgentContext) -> Any:
           """Execute the agent's primary task."""
           # Implementation here
           pass
   ```

3. **Add Pydantic schemas** if the agent has new input/output types → `src/models/schemas.py`
4. **Register in agent.yaml**:
   ```yaml
   - name: <kebab-case-name>
     entry_point: src.agents.<category>.<module>:<ClassName>
     model: gpt-4o-mini
   ```
5. **Add to workflow** in `src/workflows/` if it's part of the main pipeline
6. **Write tests** in `tests/unit/agents/test_<agent_name>.py`

### Adding a New Tool

When asked to add a tool or Azure service integration:

1. **Create the tool module** at `src/tools/<category>/<tool_name>.py`
2. **Register in agent.yaml** under `tools:`:
   ```yaml
   - name: <tool_name>
     module: src.tools.<category>.<tool_name>
   ```
3. **Add Bicep infrastructure** if a new Azure resource is needed → `infra/modules/<category>/`
4. **Update main.bicep** to include the new module (with conditional deployment if appropriate)
5. **Recompile ARM**: `az bicep build --file infra/main.bicep --outfile infra/main.json`

### Adding a Competitor Data Source

When asked to add a competitor or market data source:

1. Add configuration in `src/tools/market/competitor_api.py`
2. If API requires authentication, add Key Vault reference in the tool
3. Configure APIM backend policy in `infra/modules/integration/apim.bicep`
4. Update the Price Collection agent's system prompt if source-specific instructions needed

### Modifying Infrastructure

When asked to change Azure resources:

1. Edit the relevant Bicep module in `infra/modules/<category>/`
2. If adding a new resource, create a new module and reference from `main.bicep`
3. Use conditional deployment: `module x '...' = if (deployFlag) { ... }`
4. Always recompile: `az bicep build --file infra/main.bicep --outfile infra/main.json`
5. Commit both `.bicep` and `.json` files

### Customizing for a Line of Business

When asked to adapt for a specific insurance line:

1. Update `ProductType` enum in `src/models/schemas.py`
2. Adjust `SubmissionRecord` fields for the line's specific data requirements
3. Modify agent system prompts to reflect line-specific terminology
4. Update sample data in `data/` directory
5. Adjust coverage comparison dimensions in the Coverage Comparison agent

## Code Quality Requirements

- All functions must have type hints
- All agents must have docstrings
- Pydantic models must have Field descriptions
- Tests must cover: happy path, error cases, edge cases
- No secrets in code — use Key Vault references or environment variables
- All Azure service calls must use managed identity (no connection strings with keys)

## Testing Standards

```bash
# Run all tests
pytest tests/ -v

# Run specific category
pytest tests/unit/agents/ -v
pytest tests/contract/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing
```

Test file naming: `test_<module_name>.py`
Test class naming: `Test<ClassName>`
Test method naming: `test_<behavior_being_tested>`

## Pull Request Standards

- PR title: `<type>: <short description>` (feat, fix, docs, chore, test, infra)
- Include tests for any new agent or tool
- Update `agent.yaml` if agent/tool registration changes
- Update `docs/AGENTS.md` if agent behavior changes
- Recompile ARM JSON if Bicep changes
- Ensure all existing tests pass before merging

## Do Not

- Remove or weaken the Compliance Guardrail agent's `approval_mode: always_require`
- Store secrets, API keys, or credentials in source code
- Skip Pydantic validation between agents
- Deploy infrastructure without conditional flags
- Use synchronous blocking calls in agent `run()` methods
- Hardcode competitor names or proprietary pricing data
