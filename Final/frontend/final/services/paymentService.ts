import api from '../utils/apiClient';
import { Payment } from '../models';

export async function createPayment(orderId: number, amount: number, payment_method: number): Promise<Payment> {
  const { data } = await api.post('/payments/create', { order_id: orderId, amount, payment_method });
  return data;
}
