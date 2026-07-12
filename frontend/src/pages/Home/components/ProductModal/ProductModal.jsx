import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './ProductModal.module.css';
import { cartApi } from '../../../../services/api';
import Stickers from '../../../../components/Stickers/Stickers';

const ProductModal = ({ product, onClose }) => {
  const navigate = useNavigate();
  const isAuth = Boolean(localStorage.getItem("accessToken"));
  
  const [isAdding, setIsAdding] = useState(false);
  const [message, setMessage] = useState('');

  const imageUrl = product.product_image 
    ? (product.product_image.startsWith('http') ? product.product_image : `http://localhost:8000${product.product_image}`) 
    : '';

  const handleAddToCart = async () => {
    // Проверяем авторизацию
    if (!isAuth) {
      setMessage('Для добавления товаров необходимо войти в аккаунт 🔒');
      setTimeout(() => setMessage(''), 3000);
      return;
    }

    setIsAdding(true);
    setMessage('');
    try {
      await cartApi.addToCart({ product_id: product.product_id });
      setMessage('Товар успешно добавлен в корзину! 🎀');
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      console.error('Ошибка добавления в корзину:', error);
      setMessage('Ошибка при добавлении товара. Попробуйте позже.');
    } finally {
      setIsAdding(false);
    }
  };

  const handleLoginRedirect = () => {
    navigate('/login');
    onClose();
  };

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <button className={styles.closeButton} onClick={onClose}>×</button>
        
        <div className={styles.content}>
          <Stickers />
          <div className={styles.imageContainer}>
            {imageUrl && <img src={imageUrl} alt={product.product_name} className={styles.image} />}
          </div>
          
          <div className={styles.details}>
            <h2 className={styles.title}>{product.product_name}</h2>
            <p className={styles.price}>{product.price} ₽</p>
            
            <div className={styles.description}>
              <strong>Описание:</strong>
              <p>{product.product_description || 'Описание отсутствует'}</p>
            </div>

            <div className={styles.metaInfo}>
              {product.brand && <span>Бренд ID: {product.brand}</span>}
              {product.stock_quantity !== undefined && (
                <span>В наличии: {product.stock_quantity} шт.</span>
              )}
            </div>

            {isAuth ? (
              <button 
                className={styles.cartButton} 
                onClick={handleAddToCart}
                disabled={isAdding}
              >
                {isAdding ? 'Добавляем...' : 'В корзину'}
              </button>
            ) : (
              <button 
                className={styles.loginButton} 
                onClick={handleLoginRedirect}
              >
                Войдите, чтобы добавить в корзину
              </button>
            )}
            
            {message && <div className={styles.message}>{message}</div>}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductModal;