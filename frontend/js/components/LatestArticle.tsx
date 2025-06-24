import React, { useState, useEffect } from "react";
import { Card } from "react-bootstrap";
import { Link } from "react-router-dom";
import { BlogService } from "../api/services.gen";
import { getPreview } from "../utils/textUtils";
import type { BlogPost } from "../api/types.gen";

const LatestArticle: React.FC = () => {
  const [latestPost, setLatestPost] = useState<BlogPost | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    BlogService.blogList({ page: 1 })
      .then((data) => {
        if (data.results && data.results.length > 0) {
          setLatestPost(data.results[0]);
        }
      })
      .catch((error) => {
        console.error("Erro ao buscar o último post:", error);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <Card className="text-start h-100 w-100" style={{ minHeight: "300px" }}>
      <Card.Header className="text-center mb-2 pb-3 pt-3 fs-5">Última Publicação</Card.Header>
      <Card.Body className="d-flex flex-column">
        {loading ? (
          <div style={{ flexGrow: 1 }} className="d-flex align-items-center justify-content-center text-muted">
            Carregando...
          </div>
        ) : latestPost ? (
          <>
            <h2 className="fs-5">
              <Link className="nav-link text-center" to={`/blog/${latestPost.slug}`}>
                {latestPost.titulo}
              </Link>
            </h2>
            <Card.Text className="mt-2">
            {getPreview(latestPost.conteudo)}
            </Card.Text>
          </>
        ) : (
          <div style={{ flexGrow: 1 }} className="d-flex align-items-center justify-content-center text-muted">
            Nenhum artigo encontrado.
          </div>
        )}
      </Card.Body>
    </Card>
  );
};

export default LatestArticle;

