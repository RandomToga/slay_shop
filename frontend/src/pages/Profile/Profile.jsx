import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

// Импорты компонентов
import Header from "../../components/Header/Header";
import Footer from "../../components/Footer/Footer";

// Импорт API
import { userApi, orderApi, addressApi } from "../../services/api";

// Импорт стилей
import styles from "./Profile.module.css";
import globalStyles from "../Home/Home.module.css";

const Profile = () => {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);

  const [user, setUser] = useState({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
  });

  const [orders, setOrders] = useState([]);
  const [addresses, setAddresses] = useState([]);

  const [editing, setEditing] = useState(false);

  const [showAddressForm, setShowAddressForm] = useState(false);

  const [newAddress, setNewAddress] = useState({
    city: "",
    street: "",
    house: "",
    apartment: "",
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [userRes, ordersRes, addressesRes] = await Promise.all([
          userApi.getProfile(),
          orderApi.getOrders(),
          addressApi.getAddresses(),
        ]);

        setUser(userRes.data);
        setOrders(ordersRes.data.results || []);
        setAddresses(addressesRes.data.results || []);
      } catch (err) {
        console.error(err);

        if (err.response?.status === 401) {
          navigate("/login");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [navigate]);

  const handleProfileUpdate = async (e) => {
    e.preventDefault();

    try {
      const res = await userApi.updateProfile(user);
      setUser(res.data);
      setEditing(false);
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddAddress = async (e) => {
    e.preventDefault();

    try {
      const res = await addressApi.createAddress(newAddress);

      setAddresses([...addresses, res.data]);

      setNewAddress({
        city: "",
        street: "",
        house: "",
        apartment: "",
      });

      setShowAddressForm(false);
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteAddress = async (id) => {
    try {
      await addressApi.deleteAddress(id);

      setAddresses(addresses.filter((a) => a.address_id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  const getStatusText = (status) => {
    if (!status) return "Неизвестно";
    return status.status_name || "Неизвестно";
  };

  const getStatusClass = (status) => {
    if (!status) return styles.unknown;
    
    const statusName = status.status_name?.toLowerCase() || "";
    
    const map = {
      "новый": styles.new,
      "в обработке": styles.processing,
      "обрабатывается": styles.processing,
      "отправлен": styles.shipped,
      "в пути": styles.shipped,
      "доставлен": styles.delivered,
      "выполнен": styles.completed,
      "отменён": styles.cancelled,
      "отменен": styles.cancelled,
    };
    
    return map[statusName] || styles.unknown;
  };

  const formatDate = (date) => {
    if (!date) return "—";
    return new Date(date).toLocaleDateString("ru-RU", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  };

  if (loading) {
    return (
      <div className={globalStyles.container}>
        <Header />
        <div className={styles.loading}>
          <div className={styles.spinner}></div>
          <p>Загрузка...</p>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className={globalStyles.container}>
      <Header />

      <div className={globalStyles.contentWrapper}>
        <div className={styles.background}></div>

        <section className={styles.titleBlock}>
          <div className={styles.note}>my account ♡</div>
          <h1>PROFILE</h1>
          <p>everything about your beauty journey</p>
        </section>

        <main className={styles.wrapper}>
          <section className={styles.profileCard}>
            <h2>Личная информация</h2>

            <form onSubmit={handleProfileUpdate}>
              <div className={styles.field}>
                <label>Фамилия</label>
                <input
                  value={user.last_name || ""}
                  disabled={!editing}
                  onChange={(e) =>
                    setUser({
                      ...user,
                      last_name: e.target.value,
                    })
                  }
                />
              </div>

              <div className={styles.field}>
                <label>Имя</label>
                <input
                  value={user.first_name || ""}
                  disabled={!editing}
                  onChange={(e) =>
                    setUser({
                      ...user,
                      first_name: e.target.value,
                    })
                  }
                />
              </div>

              <div className={styles.field}>
                <label>Почта</label>
                <input value={user.email || ""} disabled />
              </div>

              <div className={styles.field}>
                <label>Телефон</label>
                <input
                  value={user.phone || ""}
                  disabled={!editing}
                  placeholder="+7 (999) 123-45-67"
                  onChange={(e) =>
                    setUser({
                      ...user,
                      phone: e.target.value,
                    })
                  }
                />
              </div>

              <button
                className={styles.mainButton}
                type="submit"
                onClick={(e) => {
                  if (!editing) {
                    e.preventDefault();
                    setEditing(true);
                  }
                }}
              >
                {editing ? "Сохранить изменения" : "Редактировать профиль"}
              </button>

              {editing && (
                <button
                  type="button"
                  className={styles.cancelButton}
                  onClick={() => {
                    setEditing(false);
                    userApi.getProfile().then((res) => {
                      setUser(res.data);
                    });
                  }}
                >
                  Отмена
                </button>
              )}
            </form>
          </section>

          <section className={styles.ordersCard}>
            <h2>⭐ Мои заказы</h2>

            {orders.length === 0 ? (
              <p className={styles.empty}>У вас пока нет заказов</p>
            ) : (
              orders.slice(0, 3).map((order) => (
                <div className={styles.order} key={order.order_id}>
                  <div className={styles.orderInfo}>
                    <div className={styles.orderHeader}>
                      <strong>#{order.order_id}</strong>
                      <span className={styles.orderDate}>
                        {formatDate(order.order_date)}
                      </span>
                    </div>
                    <div className={styles.orderDetails}>
                      <span className={styles.orderTotal}>
                        {order.total_amount} ₽
                      </span>
                    </div>
                  </div>
                  <span
                    className={`${styles.status} ${getStatusClass(order.status)}`}
                  >
                    {getStatusText(order.status)}
                  </span>
                </div>
              ))
            )}

            {orders.length > 3 && (
              <button
                className={styles.secondaryButton}
                onClick={() => navigate("/orders")}
              >
                Все заказы →
              </button>
            )}
          </section>

          <section className={styles.addressCard}>
            <h2>Мои адреса</h2>

            {addresses.length === 0 ? (
              <p className={styles.empty}>У вас пока нет адресов</p>
            ) : (
              addresses.map((address) => (
                <div className={styles.address} key={address.address_id}>
                  <p>
                    г. {address.city}
                    <br />
                    ул. {address.street}, {address.house}
                    {address.apartment && `, кв. ${address.apartment}`}
                  </p>
                  <button
                    className={styles.deleteButton}
                    onClick={() => handleDeleteAddress(address.address_id)}
                  >
                    Удалить
                  </button>
                </div>
              ))
            )}

            {showAddressForm ? (
              <form className={styles.addressForm} onSubmit={handleAddAddress}>
                <div className={styles.field}>
                  <label>Город</label>
                  <input
                    required
                    value={newAddress.city}
                    onChange={(e) =>
                      setNewAddress({
                        ...newAddress,
                        city: e.target.value,
                      })
                    }
                  />
                </div>

                <div className={styles.field}>
                  <label>Улица</label>
                  <input
                    required
                    value={newAddress.street}
                    onChange={(e) =>
                      setNewAddress({
                        ...newAddress,
                        street: e.target.value,
                      })
                    }
                  />
                </div>

                <div className={styles.field}>
                  <label>Дом</label>
                  <input
                    required
                    value={newAddress.house}
                    onChange={(e) =>
                      setNewAddress({
                        ...newAddress,
                        house: e.target.value,
                      })
                    }
                  />
                </div>

                <div className={styles.field}>
                  <label>Квартира</label>
                  <input
                    value={newAddress.apartment}
                    onChange={(e) =>
                      setNewAddress({
                        ...newAddress,
                        apartment: e.target.value,
                      })
                    }
                  />
                </div>

                <div className={styles.formButtons}>
                  <button className={styles.mainButton} type="submit">
                    Сохранить адрес
                  </button>
                  <button
                    type="button"
                    className={styles.cancelButton}
                    onClick={() => setShowAddressForm(false)}
                  >
                    Отмена
                  </button>
                </div>
              </form>
            ) : (
              <button className={styles.addButton} onClick={() => setShowAddressForm(true)}>
                + Добавить адрес
              </button>
            )}
          </section>
        </main>
      </div>

      <Footer />
    </div>
  );
};

export default Profile;