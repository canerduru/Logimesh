-- Enable Row Level Security on all tables
ALTER TABLE companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE fleets ENABLE ROW LEVEL SECURITY;
ALTER TABLE loads ENABLE ROW LEVEL SECURITY;
ALTER TABLE routes ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_states ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- Helper function to check company membership
CREATE OR REPLACE FUNCTION is_member_of_company(_company_id UUID)
RETURNS BOOLEAN AS $$
  SELECT EXISTS (
    SELECT 1 FROM user_profiles
    WHERE id = auth.uid() AND company_id = _company_id
  );
$$ LANGUAGE sql SECURITY DEFINER;

-- USER_PROFILES Policies
CREATE POLICY "Users can view their own profile" ON user_profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile" ON user_profiles
  FOR UPDATE USING (auth.uid() = id);

-- COMPANIES Policies
CREATE POLICY "Users can view their own company" ON companies
  FOR SELECT USING (
    id IN (SELECT company_id FROM user_profiles WHERE id = auth.uid())
  );

CREATE POLICY "Users can update their own company" ON companies
  FOR UPDATE USING (
    id IN (SELECT company_id FROM user_profiles WHERE id = auth.uid() AND role = 'admin')
  );

-- FLEETS Policies
CREATE POLICY "Users can view their company's fleets" ON fleets
  FOR SELECT USING (is_member_of_company(company_id));

CREATE POLICY "Users can insert fleets for their company" ON fleets
  FOR INSERT WITH CHECK (is_member_of_company(company_id));

CREATE POLICY "Users can update their company's fleets" ON fleets
  FOR UPDATE USING (is_member_of_company(company_id));

CREATE POLICY "Users can delete their company's fleets" ON fleets
  FOR DELETE USING (is_member_of_company(company_id));

-- LOADS Policies
CREATE POLICY "Users can view their company's loads" ON loads
  FOR SELECT USING (is_member_of_company(company_id));

CREATE POLICY "Users can insert loads for their company" ON loads
  FOR INSERT WITH CHECK (is_member_of_company(company_id));

CREATE POLICY "Users can update their company's loads" ON loads
  FOR UPDATE USING (is_member_of_company(company_id));

CREATE POLICY "Users can delete their company's loads" ON loads
  FOR DELETE USING (is_member_of_company(company_id));

-- ROUTES Policies
CREATE POLICY "Users can view their company's simulated routes" ON routes
  FOR SELECT USING (is_member_of_company(company_id));

CREATE POLICY "Users can insert simulated routes" ON routes
  FOR INSERT WITH CHECK (is_member_of_company(company_id));

CREATE POLICY "Users can update simulated routes" ON routes
  FOR UPDATE USING (is_member_of_company(company_id));

-- AGENT_MESSAGES Policies
-- Messages are visible if the user belongs to sender OR receiver company
-- Note: sender_id and receiver_id might not directly map to company_id in all contexts,
-- but usually agents act on behalf of a company. Assuming sender_id/receiver_id are company_ids or agent_ids.
-- If they are agent_ids, we'd need to look up the agent owner.
-- For simplicity, let's assume sender_id/receiver_id refers to company_id or null (system).

CREATE POLICY "Users can view messages involving their company" ON agent_messages
  FOR SELECT USING (
    is_member_of_company(sender_id) OR is_member_of_company(receiver_id)
  );

CREATE POLICY "Users can insert messages from their company" ON agent_messages
  FOR INSERT WITH CHECK (is_member_of_company(sender_id));

-- TRANSACTIONS Policies
CREATE POLICY "Users can view transactions involving their company" ON transactions
  FOR SELECT USING (
    is_member_of_company(shipper_company_id) OR is_member_of_company(carrier_company_id)
  );

-- AGENT_STATES Policies
CREATE POLICY "Users can view their company's agent states" ON agent_states
  FOR SELECT USING (is_member_of_company(company_id));

CREATE POLICY "Users can update their company's agent states" ON agent_states
  FOR UPDATE USING (is_member_of_company(company_id));

CREATE POLICY "Users can insert agent states for their company" ON agent_states
  FOR INSERT WITH CHECK (is_member_of_company(company_id));
