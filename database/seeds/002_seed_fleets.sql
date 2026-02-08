-- Seed Fleets
-- Company 1 (Anatolia) - Turkey
INSERT INTO fleets (company_id, vehicle_type, capacity_tons, current_location_lat, current_location_lng, status)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'Tautliner', 24.0, 41.0082, 28.9784, 'IDLE'), -- Istanbul
    ('11111111-1111-1111-1111-111111111111', 'Refrigerated', 22.0, 39.9334, 32.8597, 'IN_TRANSIT'), -- Ankara
    ('11111111-1111-1111-1111-111111111111', 'Tautliner', 24.0, 38.4192, 27.1287, 'IDLE'), -- Izmir
    ('11111111-1111-1111-1111-111111111111', 'Mega Trailer', 25.0, 40.9833, 29.1167, 'IDLE'); -- Gebze

-- Company 2 (Bosphorus) - Turkey
INSERT INTO fleets (company_id, vehicle_type, capacity_tons, current_location_lat, current_location_lng, status)
VALUES
    ('22222222-2222-2222-2222-222222222222', 'Tautliner', 24.0, 41.6772, 26.5557, 'IDLE'), -- Edirne (Border)
    ('22222222-2222-2222-2222-222222222222', 'Box Trailer', 20.0, 41.0082, 28.9784, 'IN_TRANSIT'), -- Istanbul
    ('22222222-2222-2222-2222-222222222222', 'Tautliner', 24.0, 37.0000, 35.3213, 'IDLE'); -- Adana

-- Company 3 (Rhine Freight) - Germany
INSERT INTO fleets (company_id, vehicle_type, capacity_tons, current_location_lat, current_location_lng, status)
VALUES
    ('33333333-3333-3333-3333-333333333333', 'Tautliner', 24.0, 50.9375, 6.9603, 'IDLE'), -- Cologne
    ('33333333-3333-3333-3333-333333333333', 'Refrigerated', 22.0, 48.1351, 11.5820, 'IN_TRANSIT'), -- Munich
    ('33333333-3333-3333-3333-333333333333', 'Mega Trailer', 25.0, 53.5511, 9.9937, 'IDLE'), -- Hamburg
    ('33333333-3333-3333-3333-333333333333', 'Tautliner', 24.0, 50.1109, 8.6821, 'IDLE'), -- Frankfurt
    ('33333333-3333-3333-3333-333333333333', 'Box Trailer', 20.0, 52.5200, 13.4050, 'ASSIGNED'); -- Berlin

-- Company 4 (Berlin Trans) - Germany
INSERT INTO fleets (company_id, vehicle_type, capacity_tons, current_location_lat, current_location_lng, status)
VALUES
    ('44444444-4444-4444-4444-444444444444', 'Tautliner', 24.0, 52.5200, 13.4050, 'IDLE'), -- Berlin
    ('44444444-4444-4444-4444-444444444444', 'Tautliner', 24.0, 51.3397, 12.3731, 'IDLE'), -- Leipzig
    ('44444444-4444-4444-4444-444444444444', 'Refrigerated', 22.0, 51.0504, 13.7373, 'IN_TRANSIT'); -- Dresden

-- Company 5 (Sofia Haulers) - Bulgaria
INSERT INTO fleets (company_id, vehicle_type, capacity_tons, current_location_lat, current_location_lng, status)
VALUES
    ('55555555-5555-5555-5555-555555555555', 'Tautliner', 24.0, 42.6977, 23.3219, 'IDLE'), -- Sofia
    ('55555555-5555-5555-5555-555555555555', 'Mega Trailer', 25.0, 42.1354, 24.7453, 'IDLE'), -- Plovdiv
    ('55555555-5555-5555-5555-555555555555', 'Tautliner', 24.0, 43.2141, 27.9147, 'IN_TRANSIT'), -- Varna
    ('55555555-5555-5555-5555-555555555555', 'Box Trailer', 20.0, 43.8356, 25.9657, 'IDLE'), -- Ruse (Border)
    ('55555555-5555-5555-5555-555555555555', 'Tautliner', 24.0, 41.5727, 23.2842, 'IDLE'); -- Blagoevgrad
