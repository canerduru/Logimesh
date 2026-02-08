"use client"

import { useState } from "react"
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Play, TrendingUp, AlertTriangle, CheckCircle2 } from "lucide-react"

interface SimulationResult {
  profit: number
  risk: number
  summary: string
  recommendation: string
}

export default function RoutesPage() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<SimulationResult | null>(null)

  const [origin, setOrigin] = useState("Berlin")
  const [destination, setDestination] = useState("Munich")
  const [price, setPrice] = useState(2500)

  // Mock server action to simulate backend delay + response
  const handleRunSimulation = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setResult(null)

    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 2000))

    // Mock response logic similar to Python backend
    const mockProfit = price - (Math.random() * 500 + 1200) // Mock cost
    const mockRisk = Math.random() * 100

    setResult({
      profit: parseFloat(mockProfit.toFixed(2)),
      risk: parseFloat(mockRisk.toFixed(2)),
      summary: mockRisk > 50
        ? "High risk detected. Return load probability is low (<30%)."
        : "Route is highly profitable with stable fuel costs.",
      recommendation: mockRisk > 50 ? "REJECT" : "ACCEPT"
    })

    setLoading(false)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">Route Simulation Engine</h2>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Input Form */}
        <Card>
          <CardHeader>
            <CardTitle>Simulation Parameters</CardTitle>
            <CardDescription>Enter route details to run Monte Carlo analysis.</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleRunSimulation} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="origin">Origin</Label>
                <Input id="origin" value={origin} onChange={(e) => setOrigin(e.target.value)} placeholder="City, Country" required />
              </div>

              <div className="space-y-2">
                <Label htmlFor="destination">Destination</Label>
                <Input id="destination" value={destination} onChange={(e) => setDestination(e.target.value)} placeholder="City, Country" required />
              </div>

              <div className="space-y-2">
                <Label htmlFor="price">Offered Price (€)</Label>
                <Input
                  id="price"
                  type="number"
                  value={price}
                  onChange={(e) => setPrice(Number(e.target.value))}
                  required
                  min={0}
                />
              </div>

              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? (
                  <>Running Analysis...</>
                ) : (
                  <><Play className="mr-2 h-4 w-4" /> Run Simulation</>
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Results Panel */}
        <Card className={`transition-opacity duration-500 ${result ? 'opacity-100' : 'opacity-50'}`}>
          <CardHeader>
            <CardTitle>Analysis Results</CardTitle>
            <CardDescription>
                {result ? "Simulation complete (1000 scenarios run)" : "Waiting for simulation input..."}
            </CardDescription>
          </CardHeader>
          <CardContent>
            {result ? (
              <div className="space-y-6">
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-slate-50 dark:bg-slate-900 p-4 rounded-lg text-center border">
                    <p className="text-sm text-muted-foreground mb-1">Projected Profit</p>
                    <p className={`text-2xl font-bold ${result.profit > 0 ? 'text-green-600' : 'text-red-600'}`}>
                      €{result.profit}
                    </p>
                  </div>
                  <div className="bg-slate-50 dark:bg-slate-900 p-4 rounded-lg text-center border">
                    <p className="text-sm text-muted-foreground mb-1">Risk Score (0-100)</p>
                    <div className="flex items-center justify-center space-x-2">
                        {result.risk > 50 ? <AlertTriangle className="h-5 w-5 text-orange-500" /> : <CheckCircle2 className="h-5 w-5 text-green-500" />}
                        <p className={`text-2xl font-bold ${result.risk > 50 ? 'text-orange-600' : 'text-green-600'}`}>
                        {result.risk}
                        </p>
                    </div>
                  </div>
                </div>

                <div className="bg-muted/30 p-4 rounded-md border-l-4 border-blue-500">
                    <h4 className="font-semibold mb-2 flex items-center">
                        <TrendingUp className="h-4 w-4 mr-2" />
                        AI Recommendation
                    </h4>
                    <p className="text-sm text-gray-700 dark:text-gray-300 mb-3">
                        {result.summary}
                    </p>
                    <Badge variant={result.recommendation === 'ACCEPT' ? 'default' : 'destructive'} className="text-sm px-3 py-1">
                        {result.recommendation}
                    </Badge>
                </div>
              </div>
            ) : (
              <div className="h-48 flex items-center justify-center text-muted-foreground border-dashed border-2 rounded-lg">
                Enter parameters to see profit forecast
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
