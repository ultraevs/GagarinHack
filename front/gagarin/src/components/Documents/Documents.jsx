import React, { useState } from "react";
import styles from "./styles.module.scss";
import Modal from "../Modal/Modal";
import { useSelector } from "react-redux";
import nameEncoder from "../../utils/nameEncoder";
import close from "../../assets/svg/close.svg"

const Documents = () => {
  const { items, amount } = useSelector((store) => store.files);

  const [selectedItem, setSelectedItem] = useState(null);

  const [active, setActive] = useState(false);

  const openModal = (item) => {
    setActive(true);
    setSelectedItem(item);
  };

  const closeModal = () => {
    setActive(false);
    setSelectedItem(null);
  };

  if (amount < 1) {
    return (
      <div className={styles.documents}>
        <p>Список документов пуст</p>
      </div>
    );
  }

  return (
    <div className={styles.documents}>
      <div className={styles.documents__items}>
        {items.map((item) => (
          <div key={item.name} className={styles.documents__item}>
            <div>
              <p>{item.name}</p>
              <div className={styles.documents__item__img}>
                <img src={item.img} alt="" />
              </div>
            </div>
            <div>
              <button onClick={() => openModal(item)}>Открыть</button>
            </div>
          </div>
        ))}
      </div>
      {active && selectedItem && (
        <Modal active={active} func={closeModal}>
          <div className={styles.modal}>
            <div className={styles.modal__title}>
              <h1>{selectedItem.name}</h1>
              <button onClick={closeModal}><img src={close} alt="" /></button>
            </div>
            
            <div className={styles.modal__img}>
              <img src={selectedItem.img} alt="" />
            </div>
            <ul>
              {selectedItem.info.type && (
                <li>Тип: {nameEncoder(selectedItem.info.type, selectedItem.info.page_number).split(" ")[0]}</li>
              )}
              {selectedItem.info.page_number >= 0 && (
                <li>Страница: {selectedItem.info.page_number}</li>
              )}
              {selectedItem.info.series && (
                <li>Серия: {selectedItem.info.series}</li>
              )}
              {selectedItem.info.number && (
                <li>Номер: {selectedItem.info.number}</li>
              )}
            </ul>
          </div>
        </Modal>
      )}
    </div>
  );
};

export default Documents;
