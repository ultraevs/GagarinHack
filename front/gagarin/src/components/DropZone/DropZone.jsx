import React, { useEffect, useState } from "react";
import styles from "./styles.module.scss";
import profileDocs from "../../assets/svg/profileDocs.svg";
import axios from "axios";
import PickFile from "../PickFile/PickFile";
import { AppDispatch } from "../../state/store";
import { addOrUpdateItem } from "../../state/files/filesSlice";

const DropZone = () => {

  const [imgLink, setImgLink] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  const [drag, setDrag] = useState(false);
  const [currentData, setCurrentData] = useState(null);

  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    const handleResize = () => {
      setWidth(window.innerWidth);
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, [window.innerWidth]);

  const uploadImage = (event) => {
    const file = event.target.files[0];
    console.log(file)
    setSelectedFile(file);
    setImgLink(URL.createObjectURL(file));
  };

  const dragStartHandler = (e) => {
    e.preventDefault();
    setDrag(true);
  };

  const dragLeaveHandler = (e) => {
    e.preventDefault();
    setDrag(false);
  };

  const onDropHandler = (e) => {
    e.preventDefault();
    let file = [...e.dataTransfer.files];
    setImgLink(URL.createObjectURL(file[0]));
    setDrag(false);
  };

  const fileUploaderHandler = () => {
    if (imgLink !== null) {
      const reader = new FileReader();

      reader.onload = function (event) {
        const base64data = event.target.result.split(",")[1];
        axios
          .post("https://gagarin.shmyaks.ru/cv/detect", { image: base64data })
          .then((response) => {
            console.log("Файл успешно загружен!");
            console.log("Response: " + response.data);
            AppDispatch(addOrUpdateItem({img: imgLink, info: response.data}))
            setCurrentData(response.data);
          })
          .catch((error) => {
            console.error("Произошла ошибка при загрузке файла: " + error);
          });
      };

      reader.readAsDataURL(selectedFile);
      setImgLink(null);
    }
  };

  return (
    <div className={styles.dropzone}>
      <div className={styles.dropzone__text}>
        <h3>Документы</h3>
        <p>Загрузите фото документов для упрощенного оформления страховки</p>
        <div
          style={{ border: drag ? "3px dashed black" : "" }}
          className={styles.dropzone__text__dnd}
          onDragStart={(e) => dragStartHandler(e)}
          onDragLeave={(e) => dragLeaveHandler(e)}
          onDragOver={(e) => dragStartHandler(e)}
          onDrop={(e) => onDropHandler(e)}
        >
          <label htmlFor="input-file" id="drop-area">
            <input
              type="file"
              accept="image/*"
              id="input-file"
              hidden
              onChange={uploadImage}
            />
            <div className={styles.dropzone__dnd__zone} id="img-view">
              <p>
                {width > 480
                  ? "Переместите файлы в это окно или кликните сюда"
                  : "Загрузить фото"}
              </p>
              <button onClick={() => fileUploaderHandler()}>Отправить</button>
            </div>
          </label>
        </div>
        <PickFile imgLink={imgLink} />
      </div>
      <div className={styles.dropzone__img}>
        <img src={profileDocs} alt="documents" />
      </div>
    </div>
  );
};

export default DropZone;
