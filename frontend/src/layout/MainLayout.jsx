import React from 'react';
import InteractionForm from '../components/InteractionForm';
import ChatPanel from '../components/ChatPanel';

const MainLayout = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans text-gray-900">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <h1 className="text-xl font-bold text-blue-900">Log HCP Interaction</h1>
      </header>

      {/* Content */}
      <main className="flex-1 flex overflow-hidden p-6 gap-6">
        {/* Left Panel - Form */}
        <div className="flex-1 overflow-hidden">
          <InteractionForm />
        </div>

        {/* Right Panel - Chat */}
        <div className="w-[400px] flex flex-col overflow-hidden">
          <ChatPanel />
        </div>
      </main>
    </div>
  );
};

export default MainLayout;
