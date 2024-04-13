import React from "react";
import styles from "./styles.module.scss";
import logo from "../../assets/svg/logo_footer.svg";
import chat from "../../assets/svg/chat_footer.svg";
import mail from "../../assets/svg/mail_footer.svg";
import phone from "../../assets/svg/phone_footer.svg";


const Footer = () => {
    return (
        <footer className={styles.footer}>
            <div className={styles.footer_info}>
                <div className={styles.footer_left}>
                    <img className={styles.footer_logo} src={logo} alt="" />
                    <p>Сравните цены страховых <br /> и оформите полис ОСАГО онлайн</p>
                    <p>ООО «БИП.РУ», ОГРН 1227700720576. <br /> 105066, Москва, ул. Нижняя Красносельская, д. 35, стр. 9,<br /> этаж 6, ком. 14</p>
                </div>
                <div className={styles.footer_center}>
                    <div className={styles.footer_center_block}>
                        <img src={chat} alt="" />
                        <p className={styles.footer_center_block_chat} >Онлайн-чат</p>
                    </div>
                    <div className={styles.footer_center_block}>
                        <img src={mail} alt="" />
                        <a className={styles.footer_center_block_a} href="mailto:support@bip.ru">support@bip.ru</a>
                    </div>
                    <div className={styles.footer_center_block}>
                        <img src={phone} alt="" />
                        <a className={styles.footer_center_block_a} href="tel:8 (800) 333-70-58">8 (800) 333-70-58</a>
                    </div>
                    <p className={styles.footer_center_block_p_time}>время работы службы <br /> поддержки 9:00 - 19:00</p>
                </div>
                <div className={styles.footer_right}>
                    <p className={styles.footer_right_p}>
                        О компании
                    </p>
                    <p className={styles.footer_right_p}>
                        Контакты
                    </p>
                    <p className={styles.footer_right_p}>
                        Гарантии
                    </p>
                    <p className={styles.footer_right_p}>
                        Условия сервиса
                    </p>
                    <p className={styles.footer_right_p}>
                        Карта сайта
                    </p>
                    <p className={styles.footer_right_p}>
                        Политика <br /> конфиденциальности
                    </p>
                </div>
            </div>
        </footer>
    );
}

export default Footer;