import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import BlogTag from "../pages/BlogTag";
import BlogPostPage from "../pages/BlogPostPage";
import MainLayout from "../layouts/MainLayout";
import ToolPage from "../pages/ToolPage";
import NotFoundPage from "../pages/NotFoundPage";
import PrivacyPolicy from "../pages/PrivacyPolicy";

const Blog = React.lazy(() => import("../pages/Blog"));
const Tools = React.lazy(() => import("../pages/Tools"));
const Sobre = React.lazy(() => import("../pages/Sobre"));
const NotFound = React.lazy(() => import("../pages/NotFoundPage"));

const AppRoutes = () => (
  <Router>
    <Routes>
      <Route element={<MainLayout />}>
          {/* Navbar */}
          <Route path="/" element={<Home />} />
          <Route path="/blog" element={<React.Suspense fallback={<p>Carregando...</p>}><Blog /></React.Suspense>} />
          <Route path="/tools" element={<React.Suspense fallback={<p>Carregando...</p>}><Tools /></React.Suspense>} />
          <Route path="/sobre" element={<React.Suspense fallback={<p>Carregando...</p>}><Sobre /></React.Suspense>} />
          <Route path="/privacidade" element={<React.Suspense fallback={<p>Carregando...</p>}><PrivacyPolicy /></React.Suspense>} />
          {/* Blog  */}
          <Route path="/blog/tag/:tag" element={<React.Suspense fallback={<p>Carregando...</p>}><BlogTag /></React.Suspense>} />
          <Route path="/blog/:slug" element={<React.Suspense fallback={<p>Carregando...</p>}><BlogPostPage /></React.Suspense>} />
          {/* Ferramentas */}
          <Route path="/tools/:slug" element={<React.Suspense fallback={<p>Carregando...</p>}><ToolPage /></React.Suspense>} />
          {/* Catch-all para 404 */}
          <Route path="*" element={<React.Suspense fallback={<p>Carregando...</p>}><NotFound /></React.Suspense>} />
      </Route>
    </Routes>
  </Router>
);

export default AppRoutes;
