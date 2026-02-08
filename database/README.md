# LogisticsMesh Database Setup

This directory contains the SQL migration files and seed data scripts for the LogisticsMesh platform. The database is powered by Supabase (PostgreSQL).

## Directory Structure

- `/migrations`: Schema definition files (tables, policies, indexes). Apply these in order.
- `/seeds`: Mock data scripts (companies, fleets, loads). Apply these after migrations.
- `/schemas`: ER diagrams and documentation.

## Setup Instructions

### 1. Create a Supabase Project

1. Go to [Supabase](https://supabase.com/) and create a new project.
2. Note your `Project URL` and `API Keys` (Anon/Public).

### 2. Apply Migrations (Schema)

Run the following SQL scripts in the Supabase SQL Editor in this order:

1. `migrations/001_create_core_tables.sql` - Creates the base tables.
2. `migrations/001_b_create_user_profiles.sql` - Adds user profile linkage.
3. `migrations/002_create_rls_policies.sql` - Enables security policies.
4. `migrations/003_create_indexes.sql` - Adds performance indexes.

### 3. Apply Seed Data

After the schema is created, populate the database with mock data:

1. `seeds/001_seed_companies.sql` - Creates 5 companies.
2. `seeds/002_seed_fleets.sql` - Creates 20 fleets.
3. `seeds/003_seed_loads.sql` - Creates 15 loads.

### 4. Verify Setup

Run the following query in the SQL Editor to verify data:

```sql
SELECT
    c.name,
    COUNT(f.id) as fleet_count,
    COUNT(l.id) as load_count
FROM companies c
LEFT JOIN fleets f ON c.id = f.company_id
LEFT JOIN loads l ON c.id = l.company_id
GROUP BY c.name;
```

You should see 5 companies with their respective fleet and load counts.

## RLS Policies Note

Row Level Security is enabled.
- **Service Role** key bypasses RLS (use for admin tasks).
- **Anon/Authenticated** keys are subject to RLS.
- Users are linked to companies via the `user_profiles` table.
