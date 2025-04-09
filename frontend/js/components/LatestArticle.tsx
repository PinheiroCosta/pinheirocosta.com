import React, { useState, useEffect } from "react";
import { Card } from "react-bootstrap";
import { Link } from "react-router-dom";

interface BlogPost {
  slug: string;
  titulo: string;
  conteudo: string;
}

const LatestArticle: React.FC = () => {
  const [latestPost, setLatestPost] = useState<BlogPost | null>(null);
  const [loading, setLoading] = useState(true);
  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api";

  useEffect(() => {
    async function fetchLatestPost() {
      try {
        const response = await fetch(`${API_URL}/blog/?limit=1`);
        const data = await response.json();
        if (data.results && data.results.length > 0) {
          setLatestPost(data.results[0]); 
        }
      } catch (error) {
        console.error("Erro ao buscar o último post:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchLatestPost();
  }, []);

  return (
    <Card className="text-start">
      <Card.Body>
        <Card.Header className="text-center mb-2 fs-5">Última Publicação</Card.Header>
        {loading ? (
          <p>Carregando última publicação do blog...</p>
        ) : latestPost ? (
          <>
            <h5>
              <Link className="nav-link text-center" to={`/blog/${latestPost.slug}`}>{latestPost.titulo}</Link>
            </h5>
            <Card.Text
              dangerouslySetInnerHTML={{
                __html: latestPost.conteudo.substring(0, 330) + "...",
              }}
            />
          </>
        ) : (
          <p>Nenhum artigo encontrado.</p>
        )}
      </Card.Body>
    </Card>
  );
};

export default LatestArticle;

