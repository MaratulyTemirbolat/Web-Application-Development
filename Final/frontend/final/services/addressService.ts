import api from '../utils/apiClient';
import { Address } from '../models';

export async function addAddress(city: string, street_name: string, zip_code: string): Promise<Address> {
  const { data } = await api.post('/addresses/create', { city, street_name, zip_code });
  return data;
}
