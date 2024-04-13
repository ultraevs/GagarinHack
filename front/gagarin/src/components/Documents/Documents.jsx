import React, { useState } from "react";
import styles from "./styles.module.scss";
import Modal from "../Modal/Modal";
import { useSelector } from "react-redux";
import nameEncoder from "../../utils/nameEncoder";

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

  if ( amount < 1) {
    return (
      <div className={styles.documents}>
        <p>Список документов пуст</p>
      </div>
    )
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
            <h1 className={styles.modal__title}>{selectedItem.name}</h1>
            <div className={styles.modal__img}>
              <img src={selectedItem.img} alt="" />
            </div>
            <ul>
              <li>Тип: {nameEncoder(selectedItem.info.type)}</li>
              <li>Страница: {selectedItem.info.page}</li>
              <li>Серия: {selectedItem.info.series}</li>
              <li>Номер: {selectedItem.info.number}</li>
            </ul>
          </div>
        </Modal>
      )}
    </div>
  );
};

export default Documents;
