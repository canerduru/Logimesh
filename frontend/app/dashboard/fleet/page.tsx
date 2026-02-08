"use client"

import { useEffect, useState } from "react"
import { createClientComponentClient } from "@supabase/auth-helpers-nextjs"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

// Define Fleet Interface
interface Fleet {
  id: string
  company_id: string
  vehicle_type: string
  capacity_tons: number
  status: string
  current_location_lat: number
  current_location_lng: number
  available_from: string
}

export default function FleetPage() {
  const [fleets, setFleets] = useState<Fleet[]>([])
  const [loading, setLoading] = useState(true)
  const supabase = createClientComponentClient()

  useEffect(() => {
    async function fetchFleets() {
      // In a real app, filter by user's company_id
      const { data, error } = await supabase
        .from('fleets')
        .select('*')
        .limit(20)

      if (error) {
        console.error("Error fetching fleets:", error)
      } else {
        setFleets(data || [])
      }
      setLoading(false)
    }

    fetchFleets()
  }, [supabase])

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'IDLE':
        return <Badge variant="secondary" className="bg-yellow-100 text-yellow-800 hover:bg-yellow-200">Idle</Badge>
      case 'IN_TRANSIT':
        return <Badge className="bg-green-100 text-green-800 hover:bg-green-200">In Transit</Badge>
      case 'ASSIGNED':
        return <Badge variant="outline" className="border-blue-500 text-blue-500">Assigned</Badge>
      default:
        return <Badge variant="secondary">{status}</Badge>
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">Fleet Management</h2>
        <Button>Add Vehicle</Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Your Vehicles</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Vehicle Type</TableHead>
                <TableHead>Capacity (Tons)</TableHead>
                <TableHead>Location (Lat/Lng)</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Available From</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                 <TableRow>
                   <TableCell colSpan={5} className="text-center py-4">Loading fleets...</TableCell>
                 </TableRow>
              ) : fleets.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} className="text-center py-4">No fleets found.</TableCell>
                </TableRow>
              ) : (
                fleets.map((fleet) => (
                  <TableRow key={fleet.id}>
                    <TableCell className="font-medium">{fleet.vehicle_type}</TableCell>
                    <TableCell>{fleet.capacity_tons}</TableCell>
                    <TableCell>{fleet.current_location_lat.toFixed(4)}, {fleet.current_location_lng.toFixed(4)}</TableCell>
                    <TableCell>{getStatusBadge(fleet.status)}</TableCell>
                    <TableCell>{new Date(fleet.available_from).toLocaleDateString()}</TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}
