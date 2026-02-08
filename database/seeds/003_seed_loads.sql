-- Seed Loads
-- Company 1 (Anatolia) - Exporting textiles
INSERT INTO loads (company_id, origin_lat, origin_lng, destination_lat, destination_lng, weight_tons, deadline, status, price_offered)
VALUES
    ('11111111-1111-1111-1111-111111111111', 41.0082, 28.9784, 52.5200, 13.4050, 18.5, NOW() + INTERVAL '3 days', 'PENDING', 2200), -- Istanbul -> Berlin
    ('11111111-1111-1111-1111-111111111111', 38.4192, 27.1287, 48.1351, 11.5820, 20.0, NOW() + INTERVAL '4 days', 'PENDING', 2500), -- Izmir -> Munich
    ('11111111-1111-1111-1111-111111111111', 40.1885, 29.0610, 42.6977, 23.3219, 15.0, NOW() + INTERVAL '2 days', 'PENDING', 900); -- Bursa -> Sofia

-- Company 2 (Bosphorus) - Exporting automotive parts
INSERT INTO loads (company_id, origin_lat, origin_lng, destination_lat, destination_lng, weight_tons, deadline, status, price_offered)
VALUES
    ('22222222-2222-2222-2222-222222222222', 40.7667, 29.9167, 48.7758, 9.1829, 22.0, NOW() + INTERVAL '5 days', 'PENDING', 2800), -- Izmit -> Stuttgart
    ('22222222-2222-2222-2222-222222222222', 41.0082, 28.9784, 44.4268, 26.1025, 12.0, NOW() + INTERVAL '2 days', 'PENDING', 1100), -- Istanbul -> Bucharest
    ('22222222-2222-2222-2222-222222222222', 39.9334, 32.8597, 50.9375, 6.9603, 19.5, NOW() + INTERVAL '4 days', 'PENDING', 3000); -- Ankara -> Cologne

-- Company 3 (Rhine Freight) - Machinery & Chemicals
INSERT INTO loads (company_id, origin_lat, origin_lng, destination_lat, destination_lng, weight_tons, deadline, status, price_offered)
VALUES
    ('33333333-3333-3333-3333-333333333333', 50.9375, 6.9603, 41.0082, 28.9784, 15.0, NOW() + INTERVAL '5 days', 'PENDING', 2400), -- Cologne -> Istanbul (Return load opportunity!)
    ('33333333-3333-3333-3333-333333333333', 53.5511, 9.9937, 52.2297, 21.0122, 21.0, NOW() + INTERVAL '3 days', 'PENDING', 1200), -- Hamburg -> Warsaw
    ('33333333-3333-3333-3333-333333333333', 48.1351, 11.5820, 45.4642, 9.1900, 18.0, NOW() + INTERVAL '2 days', 'PENDING', 800); -- Munich -> Milan

-- Company 4 (Berlin Trans) - Consumer Goods
INSERT INTO loads (company_id, origin_lat, origin_lng, destination_lat, destination_lng, weight_tons, deadline, status, price_offered)
VALUES
    ('44444444-4444-4444-4444-444444444444', 52.5200, 13.4050, 48.8566, 2.3522, 10.0, NOW() + INTERVAL '2 days', 'PENDING', 1500), -- Berlin -> Paris
    ('44444444-4444-4444-4444-444444444444', 51.3397, 12.3731, 50.0755, 14.4378, 23.0, NOW() + INTERVAL '1 day', 'PENDING', 600), -- Leipzig -> Prague
    ('44444444-4444-4444-4444-444444444444', 51.0504, 13.7373, 50.0614, 19.9366, 22.0, NOW() + INTERVAL '2 days', 'PENDING', 950); -- Dresden -> Krakow

-- Company 5 (Sofia Haulers) - Agriculture
INSERT INTO loads (company_id, origin_lat, origin_lng, destination_lat, destination_lng, weight_tons, deadline, status, price_offered)
VALUES
    ('55555555-5555-5555-5555-555555555555', 42.1354, 24.7453, 48.1351, 11.5820, 20.0, NOW() + INTERVAL '3 days', 'PENDING', 1800), -- Plovdiv -> Munich
    ('55555555-5555-5555-5555-555555555555', 43.2141, 27.9147, 44.4268, 26.1025, 24.0, NOW() + INTERVAL '1 day', 'PENDING', 450), -- Varna -> Bucharest
    ('55555555-5555-5555-5555-555555555555', 42.6977, 23.3219, 40.6401, 22.9444, 16.0, NOW() + INTERVAL '2 days', 'PENDING', 500); -- Sofia -> Thessaloniki
