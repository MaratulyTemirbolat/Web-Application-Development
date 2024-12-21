import { useEffect, useState } from 'react';
import { View, Text, FlatList, Image, Button, StyleSheet } from 'react-native';
import { getCartItems, removeFromCart } from '../../../services/cartService';
import { CartItem } from '../../../models';
import { useRouter } from 'expo-router';

export default function CartScreen() {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const router = useRouter();

  async function fetchCart() {
    const data = await getCartItems();
    setCartItems(data);
  }

  useEffect(() => {
    fetchCart();
  }, []);

  async function handleRemove(productId: number) {
    await removeFromCart(productId);
    fetchCart();
  }

  const total = cartItems.reduce((acc, ci) => acc + ci.product.price * ci.quantity, 0);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Your Cart</Text>
      <FlatList
        data={cartItems}
        keyExtractor={(_, index) => String(index)}
        renderItem={({item}) => (
          <View style={styles.cartItem}>
            <Image source={{uri:item.product.photo_url}} style={styles.image}/>
            <View style={{flex:1, marginLeft:10}}>
              <Text>{item.product.name}</Text>
              <Text>Quantity: {item.quantity}</Text>
              <Text>Subtotal: ${item.quantity * item.product.price}</Text>
              <Button title="Remove" onPress={() => handleRemove(item.product.id)} />
            </View>
          </View>
        )}
      />
      <View style={styles.footer}>
        <Text style={styles.total}>Total: ${total}</Text>
        <Button title="Checkout" onPress={() => router.push('/(shop)/checkout')} />
      </View>
    </View>
  )
}

const styles = StyleSheet.create({
  container: { flex:1, padding:10 },
  title: { fontSize:24, marginBottom:20 },
  cartItem: { flexDirection:'row', marginBottom:20, alignItems:'center' },
  image: { width:80, height:80, borderRadius:8 },
  footer: { borderTopWidth:1, borderColor:'#ccc', paddingTop:10 },
  total: { fontSize:18, marginBottom:10 }
});
