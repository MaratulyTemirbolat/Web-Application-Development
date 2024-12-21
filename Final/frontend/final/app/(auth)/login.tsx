import { useState } from 'react';
import { View, TextInput, Button, Text, StyleSheet } from 'react-native';
import { login } from '../../services/authService';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Link } from 'expo-router';

export default function LoginScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  async function handleLogin() {
    try {
      const data = await login(email, password);
      await AsyncStorage.setItem('auth_token', data.token);
    } catch (err: any) {
      setError('Invalid credentials');
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.heading}>Login</Text>
      {error ? <Text style={styles.error}>{error}</Text> : null}
      <TextInput placeholder="Email" value={email} onChangeText={setEmail} style={styles.input}/>
      <TextInput placeholder="Password" secureTextEntry value={password} onChangeText={setPassword} style={styles.input}/>
      <Button title="Login" onPress={handleLogin} />
      <Link href="/(auth)/register"><Text style={styles.link}>Don’t have an account? Register</Text></Link>
    </View>
  )
}

const styles = StyleSheet.create({
  container: { flex:1, justifyContent:'center', padding:20 },
  heading: { fontSize:24, marginBottom:20, textAlign:'center' },
  input: { borderWidth:1, borderColor:'#ccc', marginBottom:15, padding:10, borderRadius:5 },
  link: { textAlign:'center', marginTop:15, color:'blue' },
  error: { color:'red', marginBottom:10 }
});
