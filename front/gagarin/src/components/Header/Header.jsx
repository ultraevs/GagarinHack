import React from "react";
import styles from "./styles.module.scss";
import logo from "../../assets/svg/logo.svg";
import user from "../../assets/svg/user.svg";
import chat from "../../assets/svg/chat.svg";

const Header = () => {
  return (
    <header className={styles.header}>
      <nav>
        <ul>
          <div className={styles.header__logo}>
            <img src={logo} alt="logo" />
          </div>
          <li>ОСАГО</li>
          <li>КАСКО</li>
          <li>ШТРАФЫ ГИБДД</li>
          <li>ПРОВЕРКА ДАННЫХ</li>
        </ul>
      </nav>
      <div className={styles.header__links}>
        <div className={styles.header__link}>
          <img src={user} alt="user" />
        </div>
        <div className={styles.header__link}>
          <img src={chat} alt="chat" />
        </div>
      </div>
    </header>
  );
};

export default Header;
