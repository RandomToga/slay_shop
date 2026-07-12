import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Добавляем токен в заголовки, если он есть
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Обработка обновления токена
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem('refreshToken');
        const response = await axios.post(`${API_BASE_URL}/users/refresh/`, {
          refresh: refreshToken,
        });
        localStorage.setItem('accessToken', response.data.access);
        originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
        return api(originalRequest);
      } catch (e) {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// API методы
export const productApi = {
  // Получить список товаров с пагинацией
  getProducts: (page = 1) => api.get(`/products/?page=${page}`),
  
  // Получить товар по ID
  getProduct: (id) => api.get(`/products/${id}/`),
};

export const cartApi = {
  // Получить корзину
  getCart: () => api.get('/cart/'),
  
  // Добавить товар в корзину
  addToCart: (data) => api.post('/cart/items/', data),
  
  // Обновить количество товара в корзине
  updateCartItem: (itemId, data) => api.patch(`/cart/items/${itemId}/`, data),
  
  // Удалить товар из корзины
  removeFromCart: (itemId) => api.delete(`/cart/items/${itemId}/`),
  
  // Очистить корзину
  clearCart: () => api.delete('/cart/clear/'),
};

// API методы для пользователя
export const userApi = {
  // Получить профиль
  getProfile: () => api.get('/users/me/'),
  
  // Обновить профиль
  updateProfile: (data) => api.patch('/users/me/', data),
  
  // Вход
  login: (data) => api.post('/users/login/', data),
  
  // Регистрация
  register: (data) => api.post('/users/register/', data),
};

// API методы для заказов
export const orderApi = {
  // Получить заказы пользователя
  getOrders: (page = 1) => api.get(`/orders/?page=${page}`),
  
  // Получить детали заказа
  getOrder: (id) => api.get(`/orders/${id}/`),
  
  // Создать заказ
  createOrder: (data) => api.post('/orders/create/', data),
};

// API методы для адресов
export const addressApi = {
  // Получить адреса пользователя
  getAddresses: (page = 1) => api.get(`/users/addresses/?page=${page}`),
  
  // Получить адрес по ID
  getAddress: (id) => api.get(`/users/addresses/${id}/`),
  
  // Создать адрес
  createAddress: (data) => api.post('/users/addresses/', data),
  
  // Обновить адрес
  updateAddress: (id, data) => api.patch(`/users/addresses/${id}/`, data),
  
  // Удалить адрес
  deleteAddress: (id) => api.delete(`/users/addresses/${id}/`),
};


export const paymentApi = {
  // Получить способы оплаты
  getPaymentMethods: (page = 1) =>
    api.get(`/payment-methods/?page=${page}`),
};

export default api;