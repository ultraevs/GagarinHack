import React from "react";
import Header from "../Header/Header";

const Layout = ({ children }) => {
  return (
    <>
      <div className="container">
        <Header />
        <main>{children}</main>
      </div>
    </>
  );
};

export default Layout;
