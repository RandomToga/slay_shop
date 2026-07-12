import React from 'react';
import styles from './ProductCard.module.css';

const ProductCard = ({ title, price, image }) => {
  const imageUrl = image 
    ? (image.startsWith('http') ? image : `http://localhost:8000${image}`) 
    : "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='120' viewBox='0 0 60 120'%3E%3Crect width='60' height='120' fill='%23e3f2fd'/%3E%3Crect x='10' y='10' width='40' height='50' fill='%23ffffff' stroke='%2390caf9' stroke-width='2'/%3E%3Crect x='15' y='70' width='30' height='40' fill='%23e1bee7'/%3E%3C/svg%3E";

  return (
    <div className={styles.card}>
      <div className={styles.imageWrapper}>
        <img src={imageUrl} alt={title} className={styles.productImage} />
      </div>
      <div className={styles.title}>{title}</div>
      <div className={styles.price}>{price}</div>
    </div>
  );
};

export default ProductCard;