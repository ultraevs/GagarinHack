import React from "react";

const PickFile = ({ imgName }) => {
  return (imgName !== null && <li style={{marginTop: 10}}>{imgName}</li>);
};

export default PickFile;
