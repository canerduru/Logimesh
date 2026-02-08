# End-to-End System Test: LogisticsMesh

This document describes the manual test procedure to verify the complete functionality of the LogisticsMesh platform, from load creation to invoice generation.

## Prerequisites

1.  **Backend:** Python environment set up (`backend/requirements.txt`), `DRY_RUN=true`.
2.  **Frontend:** Next.js dev server running (`npm run dev`).
3.  **Database:** Supabase project active (or mocked).
4.  **Automation:** n8n running via Docker (`docker-compose up`).

## Test Scenario: "The Happy Path"

### Step 1: User Posts a Load (Frontend)
1.  Navigate to `http://localhost:3000/dashboard/loads`.
2.  Click **"Post Load"**.
3.  Fill in: Origin "Berlin", Destination "Munich", Price "2500".
4.  **Expected Result:** Load appears in the "Active Loads" table with status `PENDING`.

### Step 2: System Broadcasts Load (n8n & Backend)
1.  **n8n Trigger:** The mock webhook at `http://localhost:5678/webhook/new-load` receives the load data.
2.  **Notification:** Check mock email inbox or logs for "New Load Available: Berlin -> Munich".
3.  **Backend Agent:** Run `python -m backend.demo_phase4`.
    - Observe `LoadAgent` broadcasting `LOAD_REQUEST`.
    - Observe `FleetAgent` receiving the request.

### Step 3: Agent Negotiation (Backend)
1.  **Route Simulation:** Observe `FleetAgent` triggering `RouteSimulationAgent`.
    - Log should show: "Simulation complete. Profit: X, Risk: Y".
2.  **Decision:** `FleetAgent` accepts the offer (assuming low risk scenario).
3.  **Negotiation:** Agents exchange `NEGOTIATION_START`, `COUNTER_OFFER`, `ACCEPT` messages.
4.  **Transaction:** Log should show "Transaction created: ...".

### Step 4: Live Monitoring (Frontend)
1.  Navigate to `http://localhost:3000/dashboard/agents`.
2.  **Expected Result:** The chat window updates in real-time with the messages exchanged in Step 3.
    - You should see `LOAD_REQUEST`, `CAPACITY_OFFER`, `ACCEPT` messages appearing.

### Step 5: Transaction Finalization & Invoice (n8n)
1.  **Backend:** The demo script finalizes the transaction (`status=COMPLETED`).
2.  **n8n Trigger:** The mock webhook at `http://localhost:5678/webhook/transaction-completed` triggers.
3.  **Invoice:** Check mock email/logs for "Invoice for Transaction #...".
4.  **Frontend:** Navigate to `http://localhost:3000/dashboard`.
    - "Recent Activity" card should show "Load Matched: Berlin -> Munich".

## Troubleshooting

- **Agents not talking?** Check `backend/utils/message_router.py` log output.
- **Frontend not updating?** Check browser console for WebSocket connection errors.
- **n8n not triggering?** Ensure Docker container is running and webhook URLs match.
