-- INDEXES: Optimizing frequent queries

-- COMPANIES
CREATE INDEX idx_companies_country ON companies(country);

-- FLEETS
CREATE INDEX idx_fleets_company_id ON fleets(company_id);
CREATE INDEX idx_fleets_status ON fleets(status);
CREATE INDEX idx_fleets_location ON fleets(current_location_lat, current_location_lng);

-- LOADS
CREATE INDEX idx_loads_company_id ON loads(company_id);
CREATE INDEX idx_loads_status ON loads(status);
CREATE INDEX idx_loads_deadline ON loads(deadline);
CREATE INDEX idx_loads_origin ON loads(origin_lat, origin_lng);
CREATE INDEX idx_loads_destination ON loads(destination_lat, destination_lng);

-- ROUTES
CREATE INDEX idx_routes_company_id ON routes(company_id);
CREATE INDEX idx_routes_profitability ON routes(profitability_score);

-- AGENT_MESSAGES
CREATE INDEX idx_messages_sender ON agent_messages(sender_id);
CREATE INDEX idx_messages_receiver ON agent_messages(receiver_id);
CREATE INDEX idx_messages_timestamp ON agent_messages(timestamp);
CREATE INDEX idx_messages_conversation ON agent_messages(conversation_id);

-- TRANSACTIONS
CREATE INDEX idx_transactions_shipper ON transactions(shipper_company_id);
CREATE INDEX idx_transactions_carrier ON transactions(carrier_company_id);
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_transactions_created_at ON transactions(created_at);

-- AGENT_STATES
CREATE INDEX idx_agent_states_company ON agent_states(company_id);
CREATE INDEX idx_agent_states_updated ON agent_states(last_updated);
