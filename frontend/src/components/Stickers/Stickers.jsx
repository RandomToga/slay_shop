import React from 'react';
import styles from './Stickers.module.css';

const sparkles = Array.from({ length: 20 }).map((_, i) => {
  const top = Math.random() * 100;
  const left = Math.random() * 100;
  
  // Размеры от 45px до 70px (стали чуть крупнее для большей заметности)
  const size = 45 + Math.random() * 25; 
  const duration = 2.5 + Math.random() * 1.5; // Медленно: от 2.5 до 4 секунд

  const symbols = ['✦', '✧', '✶', '✴', '✦', '✧', '★', '☆', '✩'];
  const symbol = symbols[Math.floor(Math.random() * symbols.length)];

  // Более яркие, насыщенные цвета (неоново-розовый, белый, фиолетовый, голубой)
  const colors = ['#FF1493', '#FF00FF', '#00FFFF', '#FFD700', '#FFFFFF', '#FF69B4'];
  const color = colors[Math.floor(Math.random() * colors.length)];

  return {
    id: `s-${i}`,
    top: `${top}%`,
    left: `${left}%`,
    size: `${size}px`,
    duration: `${duration}s`,
    symbol,
    color
  };
});

const Stickers = () => {
  return (
    <div className={styles.stickersContainer}>
      {sparkles.map((sparkle) => (
        <div
          key={sparkle.id}
          className={styles.sparkle}
          style={{
            top: sparkle.top,
            left: sparkle.left,
            width: sparkle.size,
            height: sparkle.size,
            animationDuration: sparkle.duration,
            color: sparkle.color,
          }}
        >
          {sparkle.symbol}
        </div>
      ))}
    </div>
  );
};

export default Stickers;