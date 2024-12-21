import api from '../utils/apiClient';
import { User } from '../models';

interface LoginResponse {
  token: string;
  user: User;
}

export async function login(email: string, password: string): Promise<LoginResponse> {
  const { data } = await api.post('/auths/users/login', { email, password });
  return data;
}

export async function register(email: string, first_name: string, last_name: string, password: string): Promise<LoginResponse> {
  const { data } = await api.post('/auths/users/register', { email, first_name, last_name, password });
  return data;
}
