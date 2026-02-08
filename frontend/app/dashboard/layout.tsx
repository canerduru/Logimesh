export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex h-screen bg-gray-100 dark:bg-zinc-900">
      <aside className="w-64 bg-white dark:bg-zinc-800 border-r border-gray-200 dark:border-zinc-700">
        <div className="p-6">
          <h2 className="text-xl font-bold">LogisticsMesh</h2>
        </div>
        <nav className="mt-6 px-6 space-y-2">
          <a href="/dashboard" className="block py-2.5 px-4 rounded transition duration-200 hover:bg-gray-200 dark:hover:bg-zinc-700 hover:text-blue-600">
            Overview
          </a>
          <a href="/dashboard/fleets" className="block py-2.5 px-4 rounded transition duration-200 hover:bg-gray-200 dark:hover:bg-zinc-700 hover:text-blue-600">
            My Fleets
          </a>
          <a href="/dashboard/loads" className="block py-2.5 px-4 rounded transition duration-200 hover:bg-gray-200 dark:hover:bg-zinc-700 hover:text-blue-600">
            Active Loads
          </a>
          <a href="/dashboard/routes" className="block py-2.5 px-4 rounded transition duration-200 hover:bg-gray-200 dark:hover:bg-zinc-700 hover:text-blue-600">
            Route Simulator
          </a>
          <a href="/dashboard/settings" className="block py-2.5 px-4 rounded transition duration-200 hover:bg-gray-200 dark:hover:bg-zinc-700 hover:text-blue-600">
            Settings
          </a>
        </nav>
      </aside>
      <main className="flex-1 p-10 overflow-y-auto">
        {children}
      </main>
    </div>
  )
}
