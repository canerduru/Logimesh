-- Seed Companies (Idempotent)
INSERT INTO companies (id, name, country, fleet_size, reputation_score)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'Anatolia Logistics', 'Turkey', 12, 4.8),
    ('22222222-2222-2222-2222-222222222222', 'Bosphorus Express', 'Turkey', 8, 4.5),
    ('33333333-3333-3333-3333-333333333333', 'Rhine Freight GMBH', 'Germany', 25, 4.9),
    ('44444444-4444-4444-4444-444444444444', 'Berlin Trans', 'Germany', 15, 4.7),
    ('55555555-5555-5555-5555-555555555555', 'Sofia Haulers', 'Bulgaria', 10, 4.6)
ON CONFLICT (id) DO UPDATE
SET
    name = EXCLUDED.name,
    country = EXCLUDED.country,
    fleet_size = EXCLUDED.fleet_size,
    reputation_score = EXCLUDED.reputation_score;
