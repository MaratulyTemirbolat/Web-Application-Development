import { useState } from 'react';
import { View, TextInput, Button, Text, StyleSheet } from 'react-native';
import { register } from '../../services/authService';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Link } from 'expo-router';

export default function RegisterScreen() {
  const [email, setEmail] = useState('');
  const [first_name, setFirstName] = useState('');
  const [last_name, setLastName] = useState('');
  const [password, setPassword] = useState('');

  async function handleRegister() {
    try {
      const data = await register(email, first_name, last_name, password);
      await AsyncStorage.setItem('auth_token', data.token);
    } catch (err: any) {
      console.error(err);
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.heading}>Register</Text>
      <TextInput placeholder="Email" value={email} onChangeText={setEmail} style={styles.input}/>
      <TextInput placeholder="First Name" value={first_name} onChangeText={setFirstName} style={styles.input}/>
      <TextInput placeholder="Last Name" value={last_name} onChangeText={setLastName} style={styles.input}/>
      <TextInput placeholder="Password" secureTextEntry value={password} onChangeText={setPassword} style={styles.input}/>
      <Button title="Register" onPress={handleRegister} />
      <Link href="/(auth)/login"><Text style={styles.link}>Already have an account? Login</Text></Link>
    </View>
  )
}

const styles = StyleSheet.create({
  container: { flex:1, justifyContent:'center', padding:20 },
  heading: { fontSize:24, marginBottom:20, textAlign:'center' },
  input: { borderWidth:1, borderColor:'#ccc', marginBottom:15, padding:10, borderRadius:5 },
  link: { textAlign:'center', marginTop:15, color:'blue' }
});
