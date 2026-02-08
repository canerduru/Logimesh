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
import { Plus } from "lucide-react"

interface Load {
  id: string
  origin_lat: number
  origin_lng: number
  destination_lat: number
  destination_lng: number
  weight_tons: number
  deadline: string
  status: string
  price_offered: number
}

export default function LoadsPage() {
  const [loads, setLoads] = useState<Load[]>([])
  const [loading, setLoading] = useState(true)
  const supabase = createClientComponentClient()

  useEffect(() => {
    async function fetchLoads() {
      const { data, error } = await supabase
        .from('loads')
        .select('*')
        .limit(20)

      if (error) {
        console.error("Error fetching loads:", error)
      } else {
        setLoads(data || [])
      }
      setLoading(false)
    }

    fetchLoads()
  }, [supabase])

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">Load Board</h2>
        <Button>
          <Plus className="mr-2 h-4 w-4" /> Post Load
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Active Loads</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Route (Lat/Lng)</TableHead>
                <TableHead>Weight</TableHead>
                <TableHead>Price</TableHead>
                <TableHead>Deadline</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                 <TableRow>
                   <TableCell colSpan={6} className="text-center py-4">Loading loads...</TableCell>
                 </TableRow>
              ) : loads.length === 0 ? (
                <TableRow>
                   <TableCell colSpan={6} className="text-center py-4">No active loads.</TableCell>
                </TableRow>
              ) : (
                loads.map((load) => (
                  <TableRow key={load.id}>
                    <TableCell>
                      {load.origin_lat.toFixed(2)},{load.origin_lng.toFixed(2)} → {load.destination_lat.toFixed(2)},{load.destination_lng.toFixed(2)}
                    </TableCell>
                    <TableCell>{load.weight_tons}t</TableCell>
                    <TableCell>${load.price_offered}</TableCell>
                    <TableCell>{new Date(load.deadline).toLocaleDateString()}</TableCell>
                    <TableCell>
                      <Badge variant={load.status === 'PENDING' ? 'default' : 'secondary'}>
                        {load.status}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <Button variant="ghost" size="sm">Details</Button>
                    </TableCell>
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
