import { configureStore } from '@reduxjs/toolkit';
import formReducer from '../features/formSlice';
import chatReducer from '../features/chatSlice';

export const store = configureStore({
  reducer: {
    form: formReducer,
    chat: chatReducer,
  },
});
