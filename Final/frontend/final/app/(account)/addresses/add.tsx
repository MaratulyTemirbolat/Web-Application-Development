import { useState } from 'react';
import { View, TextInput, Button, StyleSheet, Alert } from 'react-native';
import { addAddress } from '../../../services/addressService';
import { useRouter } from 'expo-router';

export default function AddAddressScreen() {
  const [city, setCity] = useState('');
  const [street_name, setStreetName] = useState('');
  const [zip_code, setZipCode] = useState('');
  const router = useRouter();

  async function handleAdd() {
    try {
      await addAddress(city, street_name, zip_code);
      Alert.alert('Success', 'Address added!');
      router.back();
    } catch (err: any) {
      Alert.alert('Error', 'Could not add address.');
    }
  }

  return (
    <View style={styles.container}>
      <TextInput placeholder="City" value={city} onChangeText={setCity} style={styles.input}/>
      <TextInput placeholder="Street Name" value={street_name} onChangeText={setStreetName} style={styles.input}/>
      <TextInput placeholder="ZIP Code" value={zip_code} onChangeText={setZipCode} style={styles.input}/>
      <Button title="Add Address" onPress={handleAdd} />
    </View>
  )
}

const styles = StyleSheet.create({
  container: { flex:1, padding:20 },
  input: { borderWidth:1, borderColor:'#ccc', padding:10, borderRadius:5, marginBottom:15 }
});
