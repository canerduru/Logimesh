# n8n Workflow Automation

This directory contains the n8n automation workflows for the LogisticsMesh platform. n8n is used to trigger notifications, generate invoices, and report daily metrics.

## Setup

1.  **Run n8n with Docker Compose:**
    ```bash
    docker-compose up -d
    ```

2.  **Access n8n:**
    Open `http://localhost:5678` in your browser.

3.  **Import Workflows:**
    Import the JSON files from the `workflows/` directory into your n8n instance.

4.  **Configure Credentials:**
    - **Supabase:** Add PostgreSQL credentials (host, user, password, database).
    - **SMTP:** Configure email settings for notifications.
    - **Slack:** Add Slack Webhook URL.

## Workflows

- **New Load Notification:** Triggers when a new load is posted. Filters by urgency and notifies carriers.
- **Invoice Generation:** Triggers when a transaction is completed. Generates an HTML invoice and emails it.
- **Daily Report:** Runs daily at 9:00 AM. Queries transaction volume and revenue.
