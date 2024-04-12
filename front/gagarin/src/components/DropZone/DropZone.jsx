import React, { useState } from "react";
import styles from "./styles.module.scss";
import profileDocs from "../../assets/svg/profileDocs.svg";
import axios from "axios";
import PickFile from "../PickFile/PickFile";

const DropZone = () => {
  const [imgLink, setImgLink] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  const [drag, setDrag] = useState(false);

  const uploadImage = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    setImgLink(file.name);
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
    const fd = new FormData();
    fd.append("file", selectedFile);

    axios
      .post("https://gagarin.shmyaks.ru/cv/cv", fd)
      .then((response) => {
        console.log("File uploaded successfully!");
        console.log("Response: " + response.data);
      })
      .catch((error) => {
        console.error("An error occurred while uploading the file: " + error);
      });
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
              <p>Переместите файлы в это окно или кликните сюда</p>
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
