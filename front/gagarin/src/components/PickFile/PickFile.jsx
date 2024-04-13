import React from "react";

const PickFile = ({ imgName, error }) => {
  return (
    <>
      {imgName !== null && <li style={{ marginTop: 10 }}>{imgName}</li>}
      {error && (
        <li style={{ marginTop: 10, color: "red"}}>
          Не удалось распознать документ
        </li>
      )}
    </>
  );
};

export default PickFile;
