import { Slot, Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { Platform, View, StyleSheet } from 'react-native';

export default function Layout() {
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarShowLabel: false,
        tabBarStyle: { height: 60 },
      }}
    >
      <Tabs.Screen 
        name="index" 
        options={{
          tabBarIcon: ({ color, size }) => <Ionicons name="home" size={size} color={color} />,
        }} 
      />
      <Tabs.Screen 
        name="(shop)/products/index" 
        options={{
          title: 'Products',
          tabBarIcon: ({ color, size }) => <Ionicons name="list" size={size} color={color} />,
        }}
      />
      <Tabs.Screen 
        name="(shop)/cart/index" 
        options={{
          title: 'Cart',
          tabBarIcon: ({ color, size }) => <Ionicons name="cart" size={size} color={color} />,
        }}
      />
      <Tabs.Screen 
        name="(shop)/checkout/index" 
        options={{
          title: 'Checkout',
          href: null,
          tabBarIcon: ({ color, size }) => <Ionicons name="checkbox-outline" size={size} color={color} />,
        }}
      />
      <Tabs.Screen 
        name="(auth)/login" 
        options={{
          title: 'Checkout',
          tabBarIcon: ({ color, size }) => <Ionicons name="log-in" size={size} color={color} />,
        }}
      />
      <Tabs.Screen 
        name="(auth)/register" 
        options={{
          title: 'Checkout',
          href: null,
          tabBarIcon: ({ color, size }) => <Ionicons name="log-in" size={size} color={color} />,
        }}
      />
      <Tabs.Screen 
        name="(account)/addresses/index" 
        options={{
          title: 'Account',
          tabBarIcon: ({ color, size }) => <Ionicons name="person" size={size} color={color} />,
        }}
      />
      <Tabs.Screen 
        name="(account)/addresses/add" 
        options={{
          title: 'Account',
          href: null,
          tabBarIcon: ({ color, size }) => <Ionicons name="person" size={size} color={color} />,
        }}
      />
    </Tabs>
  );
}
