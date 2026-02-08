# LogisticsMesh

Multi-agent AI platform connecting competing logistics companies through anonymous agent-to-agent collaboration.

## Overview

LogisticsMesh enables logistics companies to share fleet capacity and load demands securely and anonymously. Using AI agents powered by Anthropic Claude (currently mocked), the system negotiates matches, optimizes routes, and executes transactions without revealing sensitive competitive data until a deal is struck.

## Key Features

- **Anonymous Collaboration:** Companies interact via agents, protecting their identity during initial negotiations.
- **Dynamic Pricing:** AI agents negotiate prices based on real-time market conditions.
- **Route Optimization:** "RouteForge" module simulates profitability for potential routes.
- **Automated Transactions:** Secure transaction recording and invoice generation.

## Project Structure

- `/frontend`: Next.js 14 application with Shadcn/UI components.
- `/backend`: Python backend for AI agents (LangGraph).
- `/database`: SQL migrations and seeds for Supabase (PostgreSQL).
- `/n8n`: Workflow automation definitions.
- `/docs`: Architecture and API documentation.

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.9+
- Docker (optional, for local Supabase)
- Supabase Account

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/canerduru/Logimesh.git
   cd Logimesh
   ```

2. **Database Setup:**
   Follow the instructions in `database/README.md` to set up your Supabase project and apply migrations.

3. **Backend Setup:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Environment Variables:**
   Copy `.env.example` to `.env.local` (frontend) and `.env` (backend) and fill in your keys.

## Phase 1 Status: COMPLETE
- Database Schema Design
- Initial SQL Migrations
- Mock Data Seeds
- Frontend Authentication Skeleton
