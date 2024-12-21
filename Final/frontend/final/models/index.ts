export interface User {
    id: number;
    email: string;
    first_name: string;
    last_name: string;
}

export interface Category {
    id: number;
    name: string;
    created_at: string;
    updated_at: string;
}

export interface Product {
    id: number;
    name: string;
    description: string;
    price: number;
    photo_url: string;
    category: Category;
    created_at: string;
    updated_at: string;
}

export interface CartItem {
    product: Product;
    quantity: number;
}

export interface Order {
    id: number;
    purchaser: User;
    total_price: number;
    status: number;
    products: Product[];
    created_at: string;
    updated_at: string;
}

export interface Address {
    id: number;
    city: string;
    street_name: string;
    zip_code: string;
    created_at: string;
    updated_at: string;
}

export interface Payment {
    id: number;
    order: Order;
    amount: number;
    payment_method: number; // 0: Cash, 1: Card
    created_at: string;
    updated_at: string;
}
