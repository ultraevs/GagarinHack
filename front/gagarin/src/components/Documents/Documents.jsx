import React from "react";
import styles from "./styles.module.scss";
import imageIcon from "../../assets/svg/image2.svg"

const Documents = () => {
  const documentsInfo = [
    {
      name: "Паспорт",
      img: "",
    },
    {
      name: "В/У",
      img: "",
    },
    {
      name: "ПТС",
      img: "",
    },
    {
      name: "СТС",
      img: "",
    },
  ];
  return (
    <div className={styles.documents}>
      <div className={styles.documents__items}>
        {documentsInfo.map((item) => (
          <div className={styles.documents__item}>
            <div>
            <p>{item.name}</p>
            <div className={styles.documents__item__img}>
                <img src={item.img !== "" ? item.img : imageIcon} alt="img" />
            </div>
            </div>
            <div>
                <button>Открыть</button>
            </div>

          </div>
        ))}
      </div>
    </div>
  );
};

export default Documents;
