import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const chatWithAgent = async (message, history, formData) => {
  const response = await axios.post(`${API_BASE_URL}/chat/`, {
    message,
    history: history.map(m => ({ text: m.text, role: m.role })),
    form_data: formData
  });
  return response.data;
};

export const fetchHcps = async () => {
  const response = await axios.get(`${API_BASE_URL}/hcps/`);
  return response.data;
};

export const fetchProducts = async () => {
  const response = await axios.get(`${API_BASE_URL}/products/`);
  return response.data;
};
