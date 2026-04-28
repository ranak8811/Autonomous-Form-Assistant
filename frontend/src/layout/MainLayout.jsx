import React from 'react';
import InteractionForm from '../components/InteractionForm';
import ChatPanel from '../components/ChatPanel';

const MainLayout = () => {
  return (
    <div className="h-screen bg-gray-50 flex flex-col font-sans text-gray-900 overflow-hidden">
      {/* Header - Fixed at top */}
      <header className="bg-white border-b border-gray-200 px-6 py-4 flex-shrink-0">
        <h1 className="text-xl font-bold text-blue-900">Log HCP Interaction</h1>
      </header>

      {/* Content - Fills remaining height */}
      <main className="flex-1 flex overflow-hidden p-6 gap-6">
        {/* Left Panel - Form (Independently Scrollable if content is long) */}
        <div className="flex-1 h-full overflow-hidden">
          <InteractionForm />
        </div>

        {/* Right Panel - Chat (Independently Scrollable) */}
        <div className="w-[450px] h-full flex flex-col overflow-hidden">
          <ChatPanel />
        </div>
      </main>
    </div>
  );
};

export default MainLayout;
