import React, { useEffect, useState } from "react";
import BlogList from "../components/BlogList";
import Pagination from "../components/Pagination";

interface BlogPost {
  id: number;
  titulo: string;
  conteudo: string;
  criado_em: string;
  tags: { nome: string }[];
  slug: string;
  nome_autor: string;
}

const Blog = () => {
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api";

  useEffect(() => {
    fetch(`${API_URL}/blog/?page=${currentPage}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Erro ao buscar posts");
        }
        return response.json();
      })
      .then((data) => {
        setPosts(data.results);
        setTotalPages(Math.ceil(data.count / 6));
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message);
        setLoading(false);
      });
  }, [currentPage]);

  return (
    <>
    <h2 className="my-4 text-center mb-5 mt-2">Publicações Recentes</h2>
    <BlogList posts={posts} loading={loading} error={error} />
    <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={setCurrentPage} />
    </>
 )
};

export default Blog;

