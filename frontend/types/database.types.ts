export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export interface Database {
  public: {
    Tables: {
      companies: {
        Row: {
          id: string
          name: string
          country: string
          fleet_size: number
          reputation_score: number
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          name: string
          country: string
          fleet_size?: number
          reputation_score?: number
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          name?: string
          country?: string
          fleet_size?: number
          reputation_score?: number
          created_at?: string
          updated_at?: string
        }
      }
      fleets: {
        Row: {
          id: string
          company_id: string
          vehicle_type: string
          capacity_tons: number
          current_location_lat: number
          current_location_lng: number
          status: 'IDLE' | 'IN_TRANSIT' | 'ASSIGNED'
          available_from: string
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          company_id: string
          vehicle_type: string
          capacity_tons: number
          current_location_lat?: number
          current_location_lng?: number
          status?: 'IDLE' | 'IN_TRANSIT' | 'ASSIGNED'
          available_from?: string
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          company_id?: string
          vehicle_type?: string
          capacity_tons?: number
          current_location_lat?: number
          current_location_lng?: number
          status?: 'IDLE' | 'IN_TRANSIT' | 'ASSIGNED'
          available_from?: string
          created_at?: string
          updated_at?: string
        }
      }
      loads: {
        Row: {
          id: string
          company_id: string
          origin_lat: number
          origin_lng: number
          destination_lat: number
          destination_lng: number
          weight_tons: number
          deadline: string
          status: 'PENDING' | 'MATCHED' | 'DELIVERED' | 'CANCELLED'
          price_offered: number
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          company_id: string
          origin_lat: number
          origin_lng: number
          destination_lat: number
          destination_lng: number
          weight_tons: number
          deadline: string
          status?: 'PENDING' | 'MATCHED' | 'DELIVERED' | 'CANCELLED'
          price_offered?: number
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          company_id?: string
          origin_lat?: number
          origin_lng?: number
          destination_lat?: number
          destination_lng?: number
          weight_tons?: number
          deadline?: string
          status?: 'PENDING' | 'MATCHED' | 'DELIVERED' | 'CANCELLED'
          price_offered?: number
          created_at?: string
          updated_at?: string
        }
      }
      user_profiles: {
        Row: {
          id: string
          company_id: string | null
          role: 'admin' | 'company_manager' | 'agent_operator' | null
          full_name: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          id: string
          company_id?: string | null
          role?: 'admin' | 'company_manager' | 'agent_operator' | null
          full_name?: string | null
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          company_id?: string | null
          role?: 'admin' | 'company_manager' | 'agent_operator' | null
          full_name?: string | null
          created_at?: string
          updated_at?: string
        }
      }
    }
  }
}
