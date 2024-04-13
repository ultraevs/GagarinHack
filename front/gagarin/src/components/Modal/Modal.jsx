import React from "react";
import classNames from "classnames";

import styles from "./Modal.module.css";

const Modal = ({ active, func, children }) => {
  return (
    <div
      className={
        active ? classNames(styles.modal, styles.active) : styles.modal
      }
      onClick={func}
    >
      <div
        className={
          active
            ? classNames(styles.modal_content, styles.active)
            : styles.modal_content
        }
        onClick={(e) => e.stopPropagation()}
      >
        {children}
      </div>
    </div>
  );
};

export default Modal;
