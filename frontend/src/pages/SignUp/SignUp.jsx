import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

// Импортируем Header
import Header from "../../components/Header/Header";

import styles from "./SignUp.module.css";

export default function SignUp() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    last_name: "",
    first_name: "",
    email: "",
    password: "",
  });

  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");

    if (
      !form.last_name ||
      !form.first_name ||
      !form.email ||
      !form.password
    ) {
      setError("Заполните все поля");
      return;
    }

    try {
      await axios.post("http://localhost:8000/api/users/register/", form);

      navigate("/login");
    } catch (err) {
      setError("Не удалось зарегистрироваться");
      console.log(err);
    }
  };

  return (
    <div className={styles.container}>
      {/* === 1. HEADER === */}
      <Header />

      {/* === 2. ОСНОВНОЙ КОНТЕНТ === */}
      <div className={styles.page}>
        <div className={styles.sparkle1}>✦</div>
        <div className={styles.sparkle2}>✦</div>
        <div className={styles.sparkle3}>✦</div>

        <div className={styles.card}>
          <div className={styles.cardSparkle}>✦</div>

          <h1>Регистрация</h1>

          <form onSubmit={handleSubmit}>
            <label>Фамилия</label>
            <input
              name="last_name"
              placeholder="Бакуго"
              value={form.last_name}
              onChange={handleChange}
            />

            <label>Имя</label>
            <input
              name="first_name"
              placeholder="Кацуки"
              value={form.first_name}
              onChange={handleChange}
            />

            <label>Email</label>
            <input
              type="email"
              name="email"
              placeholder="bakugo@yandex.ru"
              value={form.email}
              onChange={handleChange}
            />

            <label>Пароль</label>
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
            />

            {error && <p className={styles.error}>{error}</p>}

            <button type="submit">
              Зарегистрироваться
            </button>
          </form>

          <p className={styles.login}>
            Уже есть аккаунт?
            <Link to="/login"> Войти</Link>
          </p>
        </div>
      </div>
    </div>
  );
}