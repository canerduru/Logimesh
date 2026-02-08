import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function Dashboard() {
  const supabase = createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return redirect('/login')
  }

  // Fetch company info (mock for now as we don't have the user link)
  // In real app, we'd query user_profiles -> companies

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Company Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-zinc-800 p-6 rounded-lg shadow">
          <h3 className="text-gray-500 text-sm font-medium uppercase">Active Fleets</h3>
          <p className="text-3xl font-bold mt-2">12</p>
          <span className="text-green-500 text-sm">4 in transit</span>
        </div>
        <div className="bg-white dark:bg-zinc-800 p-6 rounded-lg shadow">
          <h3 className="text-gray-500 text-sm font-medium uppercase">Pending Loads</h3>
          <p className="text-3xl font-bold mt-2">5</p>
          <span className="text-yellow-500 text-sm">2 expiring soon</span>
        </div>
        <div className="bg-white dark:bg-zinc-800 p-6 rounded-lg shadow">
          <h3 className="text-gray-500 text-sm font-medium uppercase">Revenue (MTD)</h3>
          <p className="text-3xl font-bold mt-2">€45,200</p>
          <span className="text-green-500 text-sm">+12% vs last month</span>
        </div>
      </div>

      <div className="mt-8">
        <h2 className="text-xl font-bold mb-4">Recent Activity</h2>
        <div className="bg-white dark:bg-zinc-800 rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-zinc-700">
            <thead className="bg-gray-50 dark:bg-zinc-900">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-zinc-800 divide-y divide-gray-200 dark:divide-zinc-700">
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">Load Match</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Istanbul -> Berlin (18.5t)</td>
                <td className="px-6 py-4 whitespace-nowrap"><span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">Completed</span></td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">2 hours ago</td>
              </tr>
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">Route Sim</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Paris -> Madrid Analysis</td>
                <td className="px-6 py-4 whitespace-nowrap"><span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">Processed</span></td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">5 hours ago</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
