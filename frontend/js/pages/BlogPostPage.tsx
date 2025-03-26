import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { Container } from "react-bootstrap";

interface BlogPost {
  slug: string;
  titulo: string;
  nome_autor: string;
  conteudo: string;
  criado_em: string;
  tags: { nome: string }[];
}

const BlogPostPage: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const [post, setPost] = useState<BlogPost | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api";

  useEffect(() => {
    fetch(`${API_URL}/blog/slug/${slug}/`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Erro ao buscar o post.");
        }
        return response.json();
      })
      .then((data) => {
        setPost(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [slug]);

  if (loading) return <p>Carregando...</p>;
  if (error) return <p className="text-danger">{error}</p>;
  if (!post) return <p>Post não encontrado.</p>;

  return (
    <Container className="blog-post-container">
      <h1 className="blog-post-title">{post.titulo}</h1>
      <p className="blog-post-date">Publicado em: {new Date(post.criado_em).toLocaleDateString("pt-BR")} Por: <Link className="text-decoration-none" to={"/sobre"}> {post.nome_autor}</Link> </p>
      <div className="blog-post-content" dangerouslySetInnerHTML={{ __html: post.conteudo }} />
      <div className="blog-post-tag-list">
        {post.tags.map((tag, index) => (
        <Link key={index} to={`/blog/tag/${tag.nome}`} className="blog-post-tag">
          <span key={index} className="blog-post-tag">#{tag.nome}</span>
        </Link>
        ))}
      </div>
    </Container>
  );
};

export default BlogPostPage;

