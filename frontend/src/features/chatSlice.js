import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  messages: [
    {
      text: "Hello! I'm your AI Assistant. You can describe your interaction here, and I'll fill out the form for you.",
      role: 'assistant',
      timestamp: new Date().toISOString(),
    },
  ],
  isLoading: false,
};

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    addMessage: (state, action) => {
      state.messages.push({
        ...action.payload,
        timestamp: new Date().toISOString(),
      });
    },
    setLoading: (state, action) => {
      state.isLoading = action.payload;
    },
    clearChat: (state) => {
      state.messages = initialState.messages;
    },
  },
});

export const { addMessage, setLoading, clearChat } = chatSlice.actions;
export default chatSlice.reducer;
