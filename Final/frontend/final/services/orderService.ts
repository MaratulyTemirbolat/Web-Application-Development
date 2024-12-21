import api from '../utils/apiClient';
import { Order } from '../models';

export async function createOrder(): Promise<Order> {
  const { data } = await api.post('/orders/create');
  return data;
}
