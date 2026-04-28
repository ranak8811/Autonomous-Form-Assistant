import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { addMessage, sendMessage } from '../features/chatSlice';

const ChatPanel = () => {
  const [input, setInput] = useState('');
  const dispatch = useDispatch();
  const messages = useSelector((state) => state.chat.messages);
  const isLoading = useSelector((state) => state.chat.isLoading);

  const handleSend = () => {
    if (!input.trim() || isLoading) return;
    const userMessage = input;
    setInput('');
    dispatch(sendMessage({ message: userMessage }));
  };

  return (
    <div className="bg-white rounded-lg shadow-sm h-full flex flex-col border border-gray-200">
      <div className="p-4 border-b border-gray-200 flex items-center bg-blue-50">
        <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center mr-2">
            <span className="text-white text-xs">AI</span>
        </div>
        <div>
            <h2 className="font-bold text-blue-900">AI Assistant</h2>
            <p className="text-xs text-blue-600">Log interaction via chat</p>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] p-3 rounded-lg ${
              msg.role === 'user' 
                ? 'bg-blue-600 text-white rounded-br-none' 
                : 'bg-gray-100 text-gray-800 rounded-bl-none'
            }`}>
              <p className="text-sm">{msg.text}</p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 p-3 rounded-lg animate-pulse">
                <p className="text-sm text-gray-400 italic">Thinking...</p>
            </div>
          </div>
        )}
      </div>

      <div className="p-4 border-t border-gray-200">
        <div className="relative">
          <input 
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Describe interaction..."
            className="w-full border border-gray-300 rounded-full py-2 pl-4 pr-24 focus:ring-blue-500 focus:border-blue-500"
          />
          <button 
            onClick={handleSend}
            className="absolute right-1 top-1 bottom-1 bg-blue-600 text-white px-6 rounded-full text-sm font-medium hover:bg-blue-700 transition-colors"
          >
            Log
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatPanel;
