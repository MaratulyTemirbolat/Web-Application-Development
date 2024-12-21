import { useEffect, useState } from 'react';
import { View, Text, FlatList, Image, TouchableOpacity, StyleSheet } from 'react-native';
import { getProducts } from '../../../services/productService';
import { Product } from '../../../models';

export default function ProductsScreen() {
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    (async () => {
      const data = await getProducts();
      setProducts(data);
    })();
  }, []);

  return (
    <View style={styles.container}>
      <FlatList 
        data={products}
        keyExtractor={(item) => String(item.id)}
        numColumns={2}
        columnWrapperStyle={{ justifyContent:'space-between' }}
        renderItem={({item}) => (
          <View style={styles.productCard}>
            <Image source={{uri: item.photo_url}} style={styles.image}/>
            <Text style={styles.name}>{item.name}</Text>
            <Text>${item.price}</Text>
          </View>
        )}
      />
    </View>
  )
}

const styles = StyleSheet.create({
  container: { flex:1, padding:10 },
  productCard: { flexBasis:'48%', marginBottom:20, backgroundColor:'#fff', padding:10, borderRadius:8 },
  image: { width:'100%', height:100, resizeMode:'cover', borderRadius:8 },
  name: { fontSize:16, fontWeight:'600', marginVertical:5 }
});
