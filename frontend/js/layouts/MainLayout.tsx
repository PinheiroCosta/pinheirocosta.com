import React from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import { Outlet } from "react-router-dom";

const MainLayout: React.FC = () => {
  return (
    <>
      <Header />
      <main>
        <Outlet /> {/* Aqui as páginas serão renderizadas */}
      </main>
      <Footer />
    </>
  );
};

export default MainLayout;

