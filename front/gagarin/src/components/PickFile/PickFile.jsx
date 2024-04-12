import React from "react";

const PickFile = ({ imgLink }) => {
  return (imgLink !== null && <li style={{marginTop: 10}}>{imgLink}</li>);
};

export default PickFile;
