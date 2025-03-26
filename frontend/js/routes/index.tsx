import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import BlogTag from "../pages/BlogTag";
import BlogPostPage from "../pages/BlogPostPage";
import MainLayout from "../layouts/MainLayout";

const Blog = React.lazy(() => import("../pages/Blog"));
const Ferramentas = React.lazy(() => import("../pages/Ferramentas"));
const Sobre = React.lazy(() => import("../pages/Sobre"));

const AppRoutes = () => (
  <Router>
    <Routes>
      <Route element={<MainLayout />}>
          {/* Navbar */}
          <Route path="/" element={<Home />} />
          <Route path="/blog" element={<React.Suspense fallback={<p>Carregando...</p>}><Blog /></React.Suspense>} />
          <Route path="/ferramentas" element={<React.Suspense fallback={<p>Carregando...</p>}><Ferramentas /></React.Suspense>} />
          <Route path="/sobre" element={<React.Suspense fallback={<p>Carregando...</p>}><Sobre /></React.Suspense>} />
          {/* Blog  */}
          <Route path="/blog/tag/:tag" element={<React.Suspense fallback={<p>Carregando...</p>}><BlogTag /></React.Suspense>} />
          <Route path="/blog/:slug" element={<React.Suspense fallback={<p>Carregando...</p>}><BlogPostPage /></React.Suspense>} />
          {/* Ferramentas */}
      </Route>
    </Routes>
  </Router>
);

export default AppRoutes;
