# Backend - LogisticsMesh Agent System

This directory contains the Python-based backend for the LogisticsMesh platform, featuring multi-agent orchestration powered by LangGraph.

## Setup

1.  **Install Dependencies:**
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

2.  **Environment Variables:**
    Copy the example file and fill in your credentials.
    ```bash
    cp ../.env.example ../.env
    ```
    Required variables:
    - `SUPABASE_URL`: Your Supabase project URL.
    - `SUPABASE_KEY`: Your Supabase anonymous key.
    - `ANTHROPIC_API_KEY`: API key for Claude (optional if using mock mode).
    - `DRY_RUN`: Set to `true` to skip database writes and use mock data.

3.  **Running Tests:**
    Run the test suite using pytest.
    ```bash
    pytest backend/tests/
    ```

4.  **Running the Demo (Phase 2 & 3):**
    Simulate agent-to-agent communication without a database.

    *Phase 2 (Basic Communication):*
    ```bash
    python -m backend.demo_phase2
    ```

    *Phase 3 (Negotiation & Transaction):*
    ```bash
    python -m backend.demo_phase3
    ```

    *Phase 4 (Route Simulation & Risk Analysis):*
    ```bash
    python -m backend.demo_phase4
    ```

5.  **Running the Frontend Dashboard (Phase 5):**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```
    Access at `http://localhost:3000/dashboard`

6.  **Running n8n Automation (Phase 6):**
    ```bash
    cd n8n
    docker-compose up -d
    ```
    Access at `http://localhost:5678`

## Directory Structure

- `agents/`: Core logic for each agent type (Fleet, Load, Negotiation, etc.).
- `models/`: Pydantic models for state, messages, and data schemas.
- `utils/`: Helper functions for LLM interaction, mocking, and message routing.
- `tests/`: Unit and integration tests.

## Development

- Agents are built using `langgraph`.
- Communication happens via Supabase Realtime (or mocked in DRY_RUN).
- Use `mock_llm.py` for deterministic testing of agent decisions.
