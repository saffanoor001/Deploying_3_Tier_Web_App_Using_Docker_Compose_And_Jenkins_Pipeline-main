import { createContext, useEffect, useState } from "react"; 
import axios from 'axios';
import { toast } from "react-toastify";
import { useNavigate } from 'react-router-dom';

export const ShopContext = createContext(); 

const ShopContextProvider = (props) => { 
    const currency = '$'; 
    const delivery_fee = 10; 
    const backendUrl = import.meta.env.VITE_BACKEND_URL.replace(/\/$/, ''); // remove trailing slash
    const [search, setSearch] = useState('');
    const [showSearch, setShowSearch] = useState(false);
    const [cartItems, setCartItems] = useState({});
    const [products, setProducts] = useState([]);
    const [token, setToken] = useState('');
    const navigate = useNavigate();

    // Add to cart
    const addToCart = async (itemId, size) => {
        if(!size){
            toast.error('Select Product Size');
            return;
        }

        let cartData = structuredClone(cartItems);
        if(cartData[itemId]){
            cartData[itemId][size] = (cartData[itemId][size] || 0) + 1;
        } else {
            cartData[itemId] = { [size]: 1 };
        }
        setCartItems(cartData);

        if(token){
            try{
                await axios.post(`${backendUrl}/api/cart/add`, { itemId, size }, { headers: { token } });
            }
            catch(error){
                console.error(error);
                toast.error(error.message);
            }
        }
    };

    // Update quantity
    const updateQuantity = async (itemId, size, quantity) => {
        let cartData = structuredClone(cartItems);
        if(quantity <= 0){
            delete cartData[itemId][size];
            if(Object.keys(cartData[itemId]).length === 0){
                delete cartData[itemId];
            }
        } else {
            if(!cartData[itemId]) cartData[itemId] = {};
            cartData[itemId][size] = quantity;
        }
        setCartItems(cartData);

        if(token){
            try{
                await axios.post(`${backendUrl}/api/cart/update`, { itemId, size, quantity }, { headers: { token } });
            }
            catch(error){
                console.error(error);
                toast.error(error.message);
            }
        }
    };

    const getCartCount = () => {
        let totalCount = 0;
        for(const items in cartItems){
            for(const size in cartItems[items]){
                totalCount += cartItems[items][size];
            }
        }
        return totalCount;
    };

    const getCartAmount = () => {
        let totalAmount = 0;
        for(const itemId in cartItems){
            const itemInfo = products.find(p => p._id === itemId);
            if(!itemInfo) continue;
            for(const size in cartItems[itemId]){
                totalAmount += itemInfo.price * cartItems[itemId][size];
            }
        }
        return totalAmount;
    };

    // Fetch products
    const getProductsData = async () => {
        try {
            const response = await axios.get(`${backendUrl}/api/product/list`);
            if(response.data.success){
                setProducts(response.data.products);
            } else {
                toast.error(response.data.message);
            }
        } catch(error){
            console.error(error);
            toast.error(error.message);
        }
    };

    // Fetch user cart
    const getUserCart = async (userToken) => {
        try{
            const response = await axios.post(`${backendUrl}/api/cart/get`, {}, { headers: { token: userToken } });
            if(response.data.success){
                setCartItems(response.data.cartData);
            }
        } catch(error){
            console.error(error);
            toast.error(error.message);
        }
    };

    useEffect(() => {
        getProductsData();
    }, [token]);

    useEffect(() => {
        if(!token && localStorage.getItem('token')){
            const storedToken = localStorage.getItem('token');
            setToken(storedToken);
            getUserCart(storedToken);
        }
    }, [token]);

    const value = { 
        products,
        currency,
        delivery_fee,
        search, setSearch,
        showSearch, setShowSearch,
        cartItems, setCartItems,
        addToCart,
        updateQuantity,
        getCartCount,
        getCartAmount,
        navigate,
        backendUrl,
        token, setToken,
        setProducts
    };

    return (
        <ShopContext.Provider value={value}>
            {props.children}
        </ShopContext.Provider>
    );
};

export default ShopContextProvider;
