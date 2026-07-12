import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api, { cartApi } from "../../services/api";
import Header from "../../components/Header/Header";
import styles from "./SignIn.module.css";

export default function SignIn() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setIsLoading(true);

    if (!form.email || !form.password) {
      setError("Заполните все поля");
      setIsLoading(false);
      return;
    }

    try {
      // ✅ Получаем гостевую корзину из localStorage ПЕРЕД входом
      let guestCart = [];
      try {
        const storedCart = localStorage.getItem('guest_cart');
        if (storedCart) {
          const parsed = JSON.parse(storedCart);
          guestCart = parsed.items || [];
          console.log("=== Guest cart from localStorage:", guestCart);
        }
      } catch (e) {
        console.error("Error reading guest cart:", e);
      }

      // ✅ Вход
      const response = await api.post("/users/login/", form);
      
      const { access, refresh } = response.data;
      localStorage.setItem("accessToken", access);
      localStorage.setItem("refreshToken", refresh);

      // ✅ Если есть гостевые товары, отправляем на сервер
      if (guestCart.length > 0) {
        try {
          console.log("=== Merging guest cart with user cart ===");
          const mergeResponse = await cartApi.mergeGuestCart(guestCart);
          console.log("=== Merge result:", mergeResponse.data);
          
          // ✅ Сохраняем объединенную корзину
          localStorage.setItem('cart', JSON.stringify(mergeResponse.data));
          
          // ✅ Очищаем гостевую корзину
          localStorage.removeItem('guest_cart');
        } catch (mergeError) {
          console.error("Failed to merge cart:", mergeError);
        }
      }

      // ✅ Загружаем профиль
      const userResponse = await api.get("/users/me/", {
        headers: {
          Authorization: `Bearer ${access}`
        }
      });

      const userData = userResponse.data;
      localStorage.setItem("user", JSON.stringify(userData));

      if (userData.role_name && userData.role_name.toLowerCase() === "менеджер") {
        window.location.href = "http://localhost:8000/admin";
      } else {
        navigate("/");
      }
    } catch (err) {
      console.error("Login error:", err);
      
      if (err.response && err.response.status === 401) {
        setError("Неверный email или пароль");
      } else if (err.response && err.response.data) {
        const errorMessages = Object.values(err.response.data).flat();
        setError(errorMessages[0] || "Не удалось войти");
      } else {
        setError("Не удалось войти. Проверьте подключение к интернету.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <Header />
      <div className={styles.page}>
        <div className={styles.sparkle1}>✦</div>
        <div className={styles.sparkle2}>✦</div>
        <div className={styles.sparkle3}>✦</div>

        <div className={styles.card}>
          <div className={styles.cardSparkle}>✦</div>
          <h1>Вход</h1>
          <form onSubmit={handleSubmit}>
            <label>Email</label>
            <input
              type="email"
              name="email"
              placeholder="ivanov@example.com"
              value={form.email}
              onChange={handleChange}
              disabled={isLoading}
            />

            <label>Пароль</label>
            <input
              type="password"
              name="password"
              placeholder="Введите пароль"
              value={form.password}
              onChange={handleChange}
              disabled={isLoading}
            />

            {error && <p className={styles.error}>{error}</p>}

            <button type="submit" disabled={isLoading}>
              {isLoading ? "Вход..." : "Войти"}
            </button>
          </form>

          <p className={styles.register}>
            Нет аккаунта?
            <Link to="/register"> Зарегистрироваться</Link>
          </p>
        </div>
      </div>
    </div>
  );
}