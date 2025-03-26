import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import BlogList from "../components/BlogList";

interface BlogPost {
  id: number;
  titulo: string;
  conteudo: string;
  criado_em: string;
  tags: { nome: string }[];
  slug: string;
  nome_autor: string;
}

const BlogTag = () => {
  const { tag } = useParams();
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api";

  useEffect(() => {
    fetch(`${API_URL}/blog/?tag=${tag}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Erro ao buscar posts");
        }
        return response.json();
      })
      .then((data) => {
        setPosts(data.results);
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message);
        setLoading(false);
      });
  }, [tag]);

  return (
    <>
      <h2 className="my-4 text-center">Artigos com a tag: #{tag}</h2>
      <BlogList posts={posts} loading={loading} error={error} />
    </>
  );
};

export default BlogTag;

