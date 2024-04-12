import React from "react";
import styles from "./styles.module.scss";
import imageIcon from "../../assets/svg/image2.svg"

import { useSelector } from "react-redux"

const Documents = () => {

  const {items } = useSelector((store) => store.files)

  console.log(items)

  return (
    <div className={styles.documents}>
      <div className={styles.documents__items}>
        {/* {selectItems?.map((item) => (
          <div key={item.name} className={styles.documents__item}>
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
        ))} */}
      </div>
    </div>
  );
};

export default Documents;
