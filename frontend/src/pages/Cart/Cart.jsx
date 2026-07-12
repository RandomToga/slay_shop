import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    cartApi,
    addressApi,
    paymentApi,
    orderApi,
} from "../../services/api";

import Header from "../../components/Header/Header";
import Footer from "../../components/Footer/Footer";
import styles from "./Cart.module.css";

const Cart = () => {

    const navigate = useNavigate();

    const isAuth = Boolean(localStorage.getItem("accessToken"));

    const [loading, setLoading] = useState(true);

    const [cart, setCart] = useState({
        items: [],
        total_amount: "0.00",
    });

    const [addresses, setAddresses] = useState([]);

    const [payments, setPayments] = useState([]);

    const [selectedAddress, setSelectedAddress] = useState("");

    const [selectedPayment, setSelectedPayment] = useState("");

    const [creatingOrder, setCreatingOrder] = useState(false);

    const [error, setError] = useState("");

    useEffect(() => {
        if (!isAuth) {
            navigate("/login");
            return;
        }
        loadData();
    }, [isAuth]);

    const loadData = async () => {
        setLoading(true);
        setError("");

        try {
            const cartResponse = await cartApi.getCart();
            const cartData = cartResponse.data;
            setCart(cartData);

            const [addressesResponse, paymentResponse] = await Promise.all([
                addressApi.getAddresses(),
                paymentApi.getPaymentMethods(),
            ]);
            setAddresses(addressesResponse.data.results || []);
            setPayments(paymentResponse.data.results || []);
        } catch (e) {
            console.error(e);
            setError("Не удалось загрузить корзину.");
        } finally {
            setLoading(false);
        }
    };

    const updateQuantity = async (item, quantity) => {
        if (quantity <= 0) {
            return removeItem(item.cart_item_id);
        }

        try {
            await cartApi.updateCartItem(
                item.cart_item_id,
                {
                    product_quantity: quantity,
                }
            );
            await loadData();
        } catch (e) {
            console.error(e);
        }
    };

    const removeItem = async (id) => {
        try {
            await cartApi.removeFromCart(id);
            await loadData();
        } catch (e) {
            console.error(e);
        }
    };

    const clearCart = async () => {
        try {
            await cartApi.clearCart();
            setCart({
                items: [],
                total_amount: "0.00",
            });
        } catch (e) {
            console.error(e);
        }
    };

    const createOrder = async () => {
        if (!selectedAddress) {
            alert("Выберите адрес доставки");
            return;
        }

        if (!selectedPayment) {
            alert("Выберите способ оплаты");
            return;
        }

        try {
            setCreatingOrder(true);
            await orderApi.createOrder({
                address_id: Number(selectedAddress),
                payment_method_id: Number(selectedPayment),
            });
            alert("Заказ успешно оформлен!");
            setCart({ items: [], total_amount: "0.00" });
            navigate("/profile");
        } catch (e) {
            console.error(e);
            alert("Не удалось оформить заказ.");
        } finally {
            setCreatingOrder(false);
        }
    };

    if (loading) {
        return (
            <div className={styles.container}>
                <Header />
                <div className={styles.loading}>
                    <div className={styles.spinner}></div>
                </div>
                <Footer />
            </div>
        );
    }

    if (error) {
        return (
            <div className={styles.container}>
                <Header />
                <div className={styles.emptyPage}>
                    <h1>Ошибка</h1>
                    <p>{error}</p>
                    <button
                        className={styles.mainButton}
                        onClick={loadData}
                    >
                        Повторить
                    </button>
                </div>
                <Footer />
            </div>
        );
    }

    if (cart.items.length === 0) {
        return (
            <>
                <div className={styles.container}>
                    <Header />
                    <div className={styles.emptyPage}>
                        <div className={styles.emptyContent}>
                            <div className={styles.emptyIcon}>🛒</div>
                            <h1>Корзина пуста</h1>
                            <p>Но это не повод расстраиваться! </p>
                            <p>Настоящая королева всегда знает, чем себя порадовать ✨</p>
                            <button
                                className={styles.mainButton}
                                onClick={() => navigate("/")}
                            >
                                В каталог за покупками
                            </button>
                        </div>
                    </div>
                    <Footer />
                </div>
            </>
        );
    }

    return (
        <div className={styles.container}>
            <Header />
            
            <div className={styles.bgText}>SHOP</div>
            <div className={styles.bgTextSecond}>CART</div>

            <div className={styles.contentWrapper}>
                <section className={styles.title}>
                    <div className={styles.note}>
                        beauty shopping ♡
                    </div>
                    <h1>CART</h1>
                    <p>your favorite products</p>
                </section>

                <main className={styles.wrapper}>
                    <section className={styles.cartSection}>
                        {cart.items.map((item) => (
                            <div
                                key={item.cart_item_id}
                                className={styles.cartItem}
                            >
                                <div className={styles.imageBlock}>
                                    <div className={styles.imagePlaceholder}>
                                        🧴
                                    </div>
                                </div>
                                <div className={styles.info}>
                                    <h3>{item.product_name}</h3>
                                    <p>{Number(item.price).toFixed(2)} ₽</p>
                                </div>
                                <div className={styles.quantity}>
                                    <button
                                        onClick={() =>
                                            updateQuantity(
                                                item,
                                                item.product_quantity - 1
                                            )
                                        }
                                    >
                                        −
                                    </button>
                                    <span>{item.product_quantity}</span>
                                    <button
                                        onClick={() =>
                                            updateQuantity(
                                                item,
                                                item.product_quantity + 1
                                            )
                                        }
                                    >
                                        +
                                    </button>
                                </div>
                                <div className={styles.total}>
                                    {Number(item.total_price).toFixed(2)} ₽
                                </div>
                                <button
                                    className={styles.remove}
                                    onClick={() =>
                                        removeItem(item.cart_item_id)
                                    }
                                >
                                    ✕
                                </button>
                            </div>
                        ))}
                    </section>

                    <section className={styles.summary}>
                        <div className={styles.summaryHeader}>
                            <h2>💖 Ваш заказ</h2>
                        </div>

                        <div className={styles.summaryRow}>
                        </div>

                        <div className={styles.summaryRow}>
                            <span>Сумма</span>
                            <strong className={styles.totalPrice}>
                                {Number(cart.total_amount).toFixed(2)} ₽
                            </strong>
                        </div>

                        <div className={styles.divider}></div>

                        <div className={styles.selectGroup}>
                            <label>
                                📍 Адрес доставки
                            </label>
                            <select
                                value={selectedAddress}
                                onChange={(e) =>
                                    setSelectedAddress(e.target.value)
                                }
                            >
                                <option value="">
                                    Выберите адрес
                                </option>
                                {addresses.map((address) => (
                                    <option
                                        key={address.address_id}
                                        value={address.address_id}
                                    >
                                        {address.city}, {address.street}, {address.house}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className={styles.selectGroup}>
                            <label>
                                💳 Способ оплаты
                            </label>
                            <select
                                value={selectedPayment}
                                onChange={(e) =>
                                    setSelectedPayment(e.target.value)
                                }
                            >
                                <option value="">
                                    Выберите способ оплаты
                                </option>
                                {payments.map((method) => (
                                    <option
                                        key={method.payment_method_id}
                                        value={method.payment_method_id}
                                    >
                                        {method.payment_method_name}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <button
                            className={styles.mainButton}
                            disabled={creatingOrder}
                            onClick={createOrder}
                        >
                            {creatingOrder ? "Оформление..." : "🌸 Оформить заказ"}
                        </button>

                        <button
                            className={styles.clearButton}
                            onClick={clearCart}
                        >
                            🗑 Очистить корзину
                        </button>
                    </section>
                </main>
            </div>

            <Footer />
        </div>
    );
};

export default Cart;