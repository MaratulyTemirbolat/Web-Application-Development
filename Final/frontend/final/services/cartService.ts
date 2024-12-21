import api from '../utils/apiClient';
import { CartItem } from '../models';

export async function addToCart(productId: number, quantity: number): Promise<void> {
  await api.post('/cart/add', { product_id: productId, quantity });
}

export async function removeFromCart(productId: number): Promise<void> {
  await api.delete(`/cart/remove/${productId}`);
}

export async function getCartItems(): Promise<CartItem[]> {
  const { data } = await api.get('/cart/');
  return data;
}
