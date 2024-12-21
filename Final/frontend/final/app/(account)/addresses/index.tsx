import { useEffect, useState } from 'react';
import { View, Text, Button } from 'react-native';
import { Link, useRouter } from 'expo-router';
import { Address } from '../../../models';
import api from '../../../utils/apiClient';

export default function AddressesScreen() {
  const [addresses, setAddresses] = useState<Address[]>([]);
  const router = useRouter();

  async function fetchAddresses() {
    const { data } = await api.get('/addresses/');
    setAddresses(data);
  }

  useEffect(() => {
    fetchAddresses();
  }, []);

  return (
    <View style={{flex:1, padding:20}}>
      <Text style={{fontSize:24, marginBottom:20}}>Your Addresses</Text>
      {addresses.map((addr) => (
        <View key={addr.id} style={{marginBottom:10}}>
          <Text>{addr.street_name}, {addr.city}, {addr.zip_code}</Text>
        </View>
      ))}
      <Button title="Add Address" onPress={() => router.push('/(account)/addresses/add')} />
    </View>
  );
}
