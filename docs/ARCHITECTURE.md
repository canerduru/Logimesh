# LogisticsMesh Architecture

This document describes the high-level architecture of the LogisticsMesh platform.

## System Components

- **Frontend (Next.js 14):**
  - Handles user authentication and UI interactions.
  - Communicates directly with Supabase (via PostgreSQL and Realtime).
  - Displays dashboards and simulation results.
  - Hosted on Vercel.

- **Backend (Python / LangGraph):**
  - Executes AI agent workflows (Negotiation, Simulation, Orchestration).
  - Uses LangGraph for state management and graph traversal.
  - Interfaces with database via Supabase client.
  - Mocks LLM calls (Claude) for Phase 1/2.
  - Deployed as serverless functions (Modal/Railway).

- **Database (Supabase / PostgreSQL):**
  - Core data store for Companies, Fleets, Loads, Routes.
  - Authentication via Supabase Auth.
  - Row Level Security (RLS) policies for multi-tenancy.
  - Realtime subscriptions for agent messages.

- **Workflow Automation (n8n):**
  - Scheduled jobs (e.g., daily reports).
  - Webhook handlers for external events.
  - Integration with email/Slack.

## Data Flow

1. **User Interaction:**
   - User logs in via Frontend -> Supabase Auth.
   - User views Dashboard -> Fetches data from Supabase (RLS enforced).

2. **Agent Negotiation:**
   - Fleet Agent broadcasts capacity -> Writes to `agent_messages`.
   - Load Agent detects message via Realtime -> Evaluates fit -> Responds.
   - Negotiation proceeds via message exchange until agreement or timeout.
   - Master Orchestrator monitors for deadlocks.

3. **Route Simulation:**
   - User requests simulation -> Backend triggers Route Agent.
   - Agent runs Monte Carlo simulation -> Writes result to `routes` table.
   - Frontend displays result.

## Security Model

- **Authentication:** Supabase Auth (Email/Password).
- **Authorization:** RLS policies based on `user_profiles` table linking users to companies.
- **API Security:** Backend uses Service Role key for privileged operations; Frontend uses Anon key with RLS.
