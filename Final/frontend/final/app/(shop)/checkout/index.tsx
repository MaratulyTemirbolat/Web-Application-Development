import { useState } from 'react';
import { View, Text, Button, StyleSheet, TextInput, Alert } from 'react-native';
import { createOrder } from '../../../services/orderService';
import { createPayment } from '../../../services/paymentService';

export default function CheckoutScreen() {
  const [paymentMethod, setPaymentMethod] = useState<'card'|'cash'>('cash');
  const [cardNumber, setCardNumber] = useState('');
  
  async function handleCheckout() {
    try {
      const order = await createOrder();
      const amount = order.total_price; 
      const payment_method = paymentMethod === 'cash' ? 0 : 1;
      await createPayment(order.id, amount, payment_method);
      Alert.alert('Success', 'Order placed successfully!');
    } catch (err: any) {
      console.error(err);
      Alert.alert('Error', 'Something went wrong!');
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Payment Method</Text>
      <View style={styles.radioGroup}>
        <Button 
          title="Cash" 
          color={paymentMethod === 'cash' ? 'green' : 'gray'} 
          onPress={() => setPaymentMethod('cash')} 
        />
        <Button 
          title="Card" 
          color={paymentMethod === 'card' ? 'green' : 'gray'} 
          onPress={() => setPaymentMethod('card')} 
        />
      </View>
      {paymentMethod === 'card' && (
        <TextInput 
          placeholder="Card Number" 
          value={cardNumber} 
          onChangeText={setCardNumber} 
          style={styles.input}
          keyboardType="numeric"
        />
      )}
      <Button title="Place Order" onPress={handleCheckout} />
    </View>
  )
}

const styles = StyleSheet.create({
  container: { flex:1, padding:20 },
  title: { fontSize:24, marginBottom:20 },
  radioGroup: { flexDirection:'row', justifyContent:'space-around', marginBottom:20 },
  input: { borderWidth:1, borderColor:'#ccc', padding:10, borderRadius:5, marginBottom:20 }
});
