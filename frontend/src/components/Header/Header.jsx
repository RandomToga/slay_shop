import { Link, useNavigate } from 'react-router-dom';
import styles from './Header.module.css';

export default function Header() {
  const navigate = useNavigate();
  const isAuthenticated = !!localStorage.getItem('accessToken');
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <header className={styles.header}>
      <div className={styles.logo}>
        slay<span>.</span>
      </div>

      <nav className={styles.nav}>
        <Link to="/">Каталог</Link>
        <Link to="/cart">Корзина</Link>
        
        {isAuthenticated ? (
          <>
            {/* Ссылка на профиль становится более выделенной */}
            <Link to="/profile" className={styles.profileLink}>
              {user.first_name || 'Профиль'}
            </Link>
            
            <button onClick={handleLogout} className={styles.logoutBtn}>
              Выйти
            </button>
          </>
        ) : (
          <Link to="/login">Войти</Link>
        )}
      </nav>
    </header>
  );
}