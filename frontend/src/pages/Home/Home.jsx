import React, { useState, useEffect } from 'react';
import { productApi } from '../../services/api';

// Импорты из components (общие компоненты)
import Stickers from '../../components/Stickers/Stickers';
import Header from '../../components/Header/Header';
import Footer from '../../components/Footer/Footer';

// Импорт локального компонента ProductCard и Modal
import ProductCard from './components/ProductCard/ProductCard';
import ProductModal from './components/ProductModal/ProductModal';

import styles from './Home.module.css';

// Массив с текстами-сообщениями
const messageBlocks = [
  {
    type: 'note',
    title: 'Note',
    text: 'Любить себя — значит признать свою душу единственным домом, который у тебя есть, и украшать его с нежностью. Истинная женственность — это не мягкость ради других, а сила воды, которая знает, когда течь, а когда стать зеркалом для звёзд. Быть женщиной — значит носить свою уязвимость как корону, а свою глубину как бескрайнее море, в котором тонет весь мир, но рождается свет. И нет ничего более прекрасного, чем та, что нашла себя и больше не ищет разрешения быть собой.'
  },
  {
    type: 'disk',
    title: 'burnout',
    text: 'Он ослепнет от твоего сияния, пока ты будешь проходить мимо,  даже не обернувшись.'
  },
  {
    type: 'cute',
    text: 'Ты милашка!!!'
  },
  {
    type: 'phone',
    text: 'На ваш телефон пришло новое уведомление<3'
  },
  {
    type: 'quote',
    text: 'А кто сказал что я не могу править миром? Я ведь красавица!!!'
  }
];

// Массив для бегущей строки
const tickerMessages = [
  "✨ SLAY QUEEN ✨",
  "🌸 BE YOUR OWN MUSE 🌸",
  "💖 PRETTY & POWERFUL 💖",
  "🌈 GLOW UP EVERY DAY 🌈",
  "🌟 MAIN CHARACTER ENERGY 🌟",
  "🎀 NOT YOUR BASIC GIRL 🎀"
];

const Home = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await productApi.getProducts(1);
        setProducts(response.data.results || response.data);
      } catch (error) {
        console.error('Ошибка загрузки товаров:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchProducts();
  }, []);

  const handleCardClick = (product) => {
    setSelectedProduct(product);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedProduct(null);
  };

  // Функция для рендера текстового блока (сообщения) по его типу
  const renderMessage = (msg, index) => {
    if (msg.type === 'note') {
      return (
        <div key={`msg-${index}`} className={`${styles.messageBlock} ${styles.noteBlock}`}>
          <div className={styles.noteTitle}>{msg.title}</div>
          <p className={styles.noteText}>{msg.text}</p>
        </div>
      );
    }
    if (msg.type === 'disk') {
      return (
        <div key={`msg-${index}`} className={`${styles.messageBlock} ${styles.diskBlock}`}>
          <div className={styles.diskTextBox}>{msg.text}</div>
        </div>
      );
    }
    if (msg.type === 'cute') {
      return (
        <div key={`msg-${index}`} className={`${styles.messageBlock} ${styles.cuteMessageBlock}`}>
          <div className={styles.cuteMessageText}>{msg.text}</div>
        </div>
      );
    }
    if (msg.type === 'phone') {
      return (
        <div key={`msg-${index}`} className={`${styles.messageBlock} ${styles.phoneMessageBlock}`}>
          {msg.text}
        </div>
      );
    }
    if (msg.type === 'quote') {
      return (
        <div key={`msg-${index}`} className={`${styles.messageBlock} ${styles.bottomQuoteBlock}`}>
          {msg.text}
        </div>
      );
    }
    return null;
  };

  const renderRows = () => {
    if (loading || products.length === 0) return null;
    const rows = [];
    let productIndex = 0;
    let messageIndex = 0;

    while (productIndex < products.length) {
      const pattern = rows.length % 3;
      const currentRow = [];

      // Элемент 1 (Левый)
      if (pattern === 0) {
        const product = products[productIndex];
        if (product) {
          currentRow.push(
            <div key={`prod-${product.product_id}`} className={styles.cardWrapper} onClick={() => handleCardClick(product)}>
              <ProductCard title={product.product_name} price={`${product.price} ₽`} image={product.product_image} />
            </div>
          );
          productIndex++;
        }
      } else if (pattern === 1) {
        const msg = messageBlocks[messageIndex % messageBlocks.length];
        currentRow.push(renderMessage(msg, messageIndex));
        messageIndex++;
      } else if (pattern === 2) {
        const product = products[productIndex];
        if (product) {
          currentRow.push(
            <div key={`prod-${product.product_id}`} className={styles.cardWrapper} onClick={() => handleCardClick(product)}>
              <ProductCard title={product.product_name} price={`${product.price} ₽`} image={product.product_image} />
            </div>
          );
          productIndex++;
        }
      }

      // Элемент 2 (Правый)
      if (pattern === 0) {
        const msg = messageBlocks[messageIndex % messageBlocks.length];
        currentRow.push(renderMessage(msg, messageIndex));
        messageIndex++;
      } else if (pattern === 1) {
        const product = products[productIndex];
        if (product) {
          currentRow.push(
            <div key={`prod-${product.product_id}`} className={styles.cardWrapper} onClick={() => handleCardClick(product)}>
              <ProductCard title={product.product_name} price={`${product.price} ₽`} image={product.product_image} />
            </div>
          );
          productIndex++;
        }
      } else if (pattern === 2) {
        const product = products[productIndex];
        if (product) {
          currentRow.push(
            <div key={`prod-${product.product_id}`} className={styles.cardWrapper} onClick={() => handleCardClick(product)}>
              <ProductCard title={product.product_name} price={`${product.price} ₽`} image={product.product_image} />
            </div>
          );
          productIndex++;
        }
      }
      rows.push(currentRow);
    }

    return rows.map((row, idx) => (
      <div key={`row-${idx}`} className={styles.row}>
        {row}
      </div>
    ));
  };

  return (
    <div className={styles.container}>
      <Stickers />
      {/* === 1. HEADER === */}
      <Header />
      
      {/* === 2. БЕГУЩАЯ СТРОКА (Ticker) === */}
      <div className={styles.tickerWrapper}>
        <div className={styles.tickerTrack}>
          {[...tickerMessages, ...tickerMessages].map((text, i) => (
            <span key={i} className={styles.tickerItem}>{text}</span>
          ))}
        </div>
      </div>

      {/* === 3. ОСНОВНОЙ КОНТЕНТ === */}
      <div className={styles.contentWrapper}>
      <h2 className={styles.catalogTitle}>Каталог</h2>
        
        {/* ПЕРЕМЕСТИЛИ ФОНОВЫЕ ТЕКСТЫ ВНУТРЬ contentWrapper */}
        <div className={styles.bgText}>YOU'RE</div>
        <div className={styles.bgTextSecond}>SLAYYY</div>

        <div className={styles.cardsGrid}>
          {renderRows()}
        </div>

      </div>

      {/* === 4. FOOTER === */}
      <Footer />
      {/* === 5. МОДАЛЬНОЕ ОКНО (вынесено в самый конец для гарантии) === */}
      {isModalOpen && selectedProduct && (
        <div style={{ 
          position: 'fixed', 
          top: 0, left: 0, width: '100vw', height: '100vh', 
          zIndex: 9999, 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center',
          backgroundColor: 'rgba(0,0,0,0.4)'
        }}>
          <ProductModal product={selectedProduct} onClose={closeModal} />
        </div>
      )}
    </div>
  );
};

export default Home;