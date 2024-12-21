import api from '../utils/apiClient';
import { Product } from '../models';

export async function getProducts(): Promise<Product[]> {
  const { data } = await api.get('/products/');
  return data;
}
