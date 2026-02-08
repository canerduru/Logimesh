"use client"

import { useEffect, useState, useRef } from "react"
import { createClientComponentClient } from "@supabase/auth-helpers-nextjs"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Bot, User, Clock, CheckCircle2, XCircle, RefreshCw } from "lucide-react"

interface AgentMessage {
  id: string
  sender_agent_type: string
  receiver_agent_type: string
  message_type: string
  payload_json: any
  timestamp: string
  conversation_id: string
}

export default function AgentsPage() {
  const [messages, setMessages] = useState<AgentMessage[]>([])
  const [activeConversation, setActiveConversation] = useState<string | null>(null)
  const supabase = createClientComponentClient()
  const scrollRef = useRef<HTMLDivElement>(null)

  // Fetch initial messages
  useEffect(() => {
    async function fetchMessages() {
      const { data, error } = await supabase
        .from('agent_messages')
        .select('*')
        .order('timestamp', { ascending: false })
        .limit(50)

      if (data) {
        setMessages(data.reverse()) // Show oldest first in chat
      }
    }

    fetchMessages()

    // Realtime Subscription
    const channel = supabase
      .channel('agent-activity')
      .on(
        'postgres_changes',
        { event: 'INSERT', schema: 'public', table: 'agent_messages' },
        (payload) => {
          console.log('New message:', payload.new)
          setMessages((prev) => [...prev, payload.new as AgentMessage])
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [supabase])

  // Auto-scroll to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  // Group messages by conversation
  const conversations = Array.from(new Set(messages.map(m => m.conversation_id).filter(Boolean)))

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">Live Agent Monitor</h2>
        <Badge variant="outline" className="text-green-600 border-green-600 animate-pulse">
          <span className="w-2 h-2 bg-green-600 rounded-full mr-2"></span>
          System Active
        </Badge>
      </div>

      <div className="grid grid-cols-12 gap-6 h-full">
        {/* Sidebar: Active Conversations */}
        <Card className="col-span-3 h-full overflow-hidden flex flex-col">
          <CardHeader>
            <CardTitle className="text-sm uppercase tracking-wider text-muted-foreground">Active Threads</CardTitle>
          </CardHeader>
          <CardContent className="flex-1 overflow-y-auto space-y-2 p-2">
            {conversations.length === 0 && <p className="text-sm text-muted-foreground text-center py-4">No active threads</p>}
            {conversations.map((convId) => (
              <div
                key={convId}
                onClick={() => setActiveConversation(convId)}
                className={`p-3 rounded-lg cursor-pointer transition-colors ${activeConversation === convId ? 'bg-primary/10 border-l-4 border-primary' : 'hover:bg-muted'}`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono truncate w-24">...{convId.slice(-8)}</span>
                  <Badge variant="secondary" className="text-[10px]">Active</Badge>
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  Last msg: {new Date(messages.filter(m => m.conversation_id === convId).pop()?.timestamp || '').toLocaleTimeString()}
                </p>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Main Chat Area */}
        <Card className="col-span-9 h-full overflow-hidden flex flex-col">
          <CardHeader className="border-b bg-muted/20 py-4">
             <div className="flex items-center space-x-4">
                <Avatar>
                  <AvatarFallback><Bot className="h-5 w-5" /></AvatarFallback>
                </Avatar>
                <div>
                  <CardTitle className="text-lg">
                    {activeConversation ? `Conversation ${activeConversation.slice(0, 8)}` : "Select a thread"}
                  </CardTitle>
                  {activeConversation && (
                    <p className="text-xs text-muted-foreground">Monitoring agent negotiation protocol...</p>
                  )}
                </div>
             </div>
          </CardHeader>

          <CardContent
            ref={scrollRef}
            className="flex-1 overflow-y-auto p-6 space-y-4 bg-slate-50 dark:bg-slate-900/50"
          >
            {messages
              .filter(m => !activeConversation || m.conversation_id === activeConversation)
              .map((msg) => {
                const isFleet = msg.sender_agent_type === 'FLEET_AGENT' || msg.sender_agent_type.includes('FLEET')
                const isLoad = msg.sender_agent_type === 'LOAD_AGENT'

                return (
                  <div key={msg.id} className={`flex w-full ${isFleet ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[70%] rounded-lg p-4 shadow-sm border ${
                      isFleet
                        ? 'bg-blue-50 border-blue-100 dark:bg-blue-900/20 dark:border-blue-800'
                        : 'bg-white border-gray-200 dark:bg-gray-800 dark:border-gray-700'
                    }`}>
                      <div className="flex items-center space-x-2 mb-2">
                        <Badge variant="outline" className="text-[10px] h-5">
                          {msg.sender_agent_type}
                        </Badge>
                        <span className="text-xs text-muted-foreground">
                          {new Date(msg.timestamp).toLocaleTimeString()}
                        </span>
                      </div>

                      <div className="text-sm font-medium mb-1">
                        {msg.message_type.replace('_', ' ')}
                      </div>

                      <div className="bg-black/5 dark:bg-white/5 rounded p-2 text-xs font-mono overflow-x-auto">
                        <pre>{JSON.stringify(msg.payload_json, null, 2)}</pre>
                      </div>
                    </div>
                  </div>
                )
              })}

            {messages.length === 0 && (
                <div className="flex flex-col items-center justify-center h-full text-muted-foreground">
                    <Bot className="h-12 w-12 mb-4 opacity-20" />
                    <p>Waiting for agent activity...</p>
                </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
