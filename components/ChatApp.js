import React, { useState, useEffect } from 'react';
import { createClient } from '@supabase/supabase-js';

// Supabase Configuration
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseAnonKey);

export default function LovingMessageApp() {
  const [activeTab, setActiveTab] = useState('messages'); // search, messages, profile
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [profile, setProfile] = useState({ name: 'User', avatar: null });

  // 1. Fetch Real-time Messages from Supabase
  useEffect(() => {
    fetchMessages();
    
    // Subscribe to real-time changes
    const channel = supabase
      .channel('schema-db-changes')
      .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'messages' }, (payload) => {
        setMessages((prev) => [...prev, payload.new]);
      })
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, []);

  const fetchMessages = async () => {
    const { data, error } = await supabase.from('messages').select('*').order('created_at', { ascending: true });
    if (!error && data) setMessages(data);
  };

  // 2. Send Message
  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    const { error } = await supabase.from('messages').insert([
      { text: newMessage, sender: profile.name, created_at: new Date() }
    ]);

    if (!error) setNewMessage('');
  };

  // 3. Profile Image Upload
  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (file) {
      const fileExt = file.name.split('.').pop();
      const fileName = `${Math.random()}.${fileExt}`;
      const filePath = `avatars/${fileName}`;

      let { error: uploadError } = await supabase.storage.from('avatars').upload(filePath, file);

      if (!uploadError) {
        const publicUrl = supabase.storage.from('avatars').getPublicUrl(filePath).data.publicUrl;
        setProfile((prev) => ({ ...prev, avatar: publicUrl }));
      }
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 max-w-md mx-auto border shadow-lg">
      
      {/* Header Board */}
      <header className="bg-pink-600 text-white p-4 text-center shadow-md">
        <h1 className="text-xl font-bold tracking-wide">Connect Your Love 💕</h1>
        <p className="text-xs text-pink-200">Loving Message Portal</p>
      </header>

      {/* Main Body Area */}
      <main className="flex-1 overflow-y-auto p-4">
        
        {/* SEARCH TAB */}
        {activeTab === 'search' && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-gray-700">Search Partners</h2>
            <input
              type="text"
              placeholder="Search user or ID..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500"
            />
            <div className="text-sm text-gray-500">Searching for: {searchQuery}</div>
          </div>
        )}

        {/* MESSAGING TAB (Real-time Chat) */}
        {activeTab === 'messages' && (
          <div className="flex flex-col h-full justify-between">
            <div className="flex-1 overflow-y-auto space-y-3 mb-4">
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`p-3 rounded-lg max-w-[80%] ${
                    msg.sender === profile.name
                      ? 'bg-pink-500 text-white ml-auto text-right'
                      : 'bg-white text-gray-800 border'
                  }`}
                >
                  <p className="text-xs text-pink-200 font-semibold">{msg.sender}</p>
                  <p className="text-sm">{msg.text}</p>
                </div>
              ))}
            </div>

            <form onSubmit={handleSendMessage} className="flex gap-2">
              <input
                type="text"
                placeholder="Type a loving message..."
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500"
              />
              <button type="submit" className="bg-pink-600 text-white px-4 py-2 rounded-lg font-bold">
                Send
              </button>
            </form>
          </div>
        )}

        {/* PROFILE TAB */}
        {activeTab === 'profile' && (
          <div className="flex flex-col items-center space-y-4 pt-6">
            <div className="relative w-24 h-24 rounded-full bg-gray-300 overflow-hidden border-2 border-pink-500 flex items-center justify-center">
              {profile.avatar ? (
                <img src={profile.avatar} alt="Profile" className="w-full h-full object-cover" />
              ) : (
                <span className="text-gray-500 text-xs">No Photo</span>
              )}
            </div>

            {/* Photo Upload Button */}
            <label className="cursor-pointer bg-pink-600 text-white px-4 py-2 rounded-lg text-sm font-semibold">
              Add / Change Picture
              <input type="file" accept="image/*" onChange={handleImageUpload} className="hidden" />
            </label>

            <div className="w-full space-y-2 mt-4">
              <label className="text-xs font-semibold text-gray-600">Profile Name</label>
              <input
                type="text"
                value={profile.name}
                onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                className="w-full p-2 border rounded-lg"
              />
            </div>
          </div>
        )}
      </main>

      {/* Bottom Navigation Bar (3 Buttons) */}
      <nav className="bg-white border-t flex justify-around py-3">
        <button
          onClick={() => setActiveTab('search')}
          className={`flex flex-col items-center ${activeTab === 'search' ? 'text-pink-600 font-bold' : 'text-gray-500'}`}
        >
          🔍
          <span className="text-xs">Search</span>
        </button>

        <button
          onClick={() => setActiveTab('messages')}
          className={`flex flex-col items-center ${activeTab === 'messages' ? 'text-pink-600 font-bold' : 'text-gray-500'}`}
        >
          💬
          <span className="text-xs">Messaging</span>
        </button>

        <button
          onClick={() => setActiveTab('profile')}
          className={`flex flex-col items-center ${activeTab === 'profile' ? 'text-pink-600 font-bold' : 'text-gray-500'}`}
        >
          👤
          <span className="text-xs">Profile</span>
        </button>
      </nav>

    </div>
  );
}

