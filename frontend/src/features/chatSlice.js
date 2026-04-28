import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { chatWithAgent } from "../services/api";
import { updateMultipleFields } from "./formSlice";
import { toast } from "react-toastify";

export const sendMessage = createAsyncThunk(
  "chat/sendMessage",
  async ({ message }, { getState, dispatch }) => {
    const { chat, form } = getState();

    dispatch(setLoading(true));

    try {
      const response = await chatWithAgent(message, chat.messages, form);

      if (response.form_data) {
        const changedFields = Object.keys(response.form_data).filter((key) => {
          const oldValue = JSON.stringify(form[key]);
          const newValue = JSON.stringify(response.form_data[key]);
          return newValue !== oldValue && response.form_data[key] !== null;
        });

        if (changedFields.length > 0) {
          dispatch(updateMultipleFields(response.form_data));

          // Trigger a separate toast for each changed field
          changedFields.forEach((field) => {
            const label = field.replace("_", " ").toUpperCase();
            const value = response.form_data[field];
            const displayValue = Array.isArray(value)
              ? value.join(", ")
              : value;

            toast.info(`${label} changed to: "${displayValue}"`, {
              icon: "🤖",
              autoClose: 10000,
            });
          });
        }
      }

      if (response.response.toLowerCase().includes("saved")) {
        toast.success("Interaction saved to database!");
      }

      return response;
    } catch (error) {
      toast.error("Failed to connect to AI");
      throw error;
    } finally {
      dispatch(setLoading(false));
    }
  },
);

const initialState = {
  messages: [
    {
      text: "Hello! I'm your AI Assistant. You can describe your interaction here, and I'll fill out the form for you.",
      role: "assistant",
      timestamp: new Date().toISOString(),
    },
  ],
  isLoading: false,
};

const chatSlice = createSlice({
  name: "chat",
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
  extraReducers: (builder) => {
    builder.addCase(sendMessage.fulfilled, (state, action) => {
      // The message is already in the history from the backend response
      state.messages = action.payload.history.map((m) => ({
        ...m,
        timestamp: new Date().toISOString(),
      }));
    });
  },
});

export const { addMessage, setLoading, clearChat } = chatSlice.actions;
export default chatSlice.reducer;
