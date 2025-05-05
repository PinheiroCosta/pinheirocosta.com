import React from "react";
import { Container, Row, Col, Card, Spinner } from "react-bootstrap";
import CustomNavLink from "./CustomNavLink"; 
import { Link } from "react-router-dom";

interface BlogPost {
  id: number;
  titulo: string;
  conteudo: string;
  criado_em: string;
  tags: { nome: string }[];
  slug: string;
  nome_autor: string;
}

interface BlogListProps {
  posts: BlogPost[];
  loading: boolean;
  error: string | null;
}

const BlogList: React.FC<BlogListProps> = ({ posts, loading, error }) => {
  return (
    <Container className="justify-content-center">
      {loading ? (
        <Row className="justify-content-center">
          <Spinner animation="border" />
        </Row>
      ) : error ? (
        <Row className="justify-content-center">
          <p className="text-danger">{error}</p>
        </Row>
      ) : posts.length > 0 ? (
      <Row>
        {posts.map((post) => (
          <Col md={6} key={post.id} className="mb-4">
            <Card>
              <Card.Body>
                <Card.Title className="text-center fg-primary fw-bold">
                    <Link to={`/blog/${post.slug}`} style={{ textDecoration: "none", color: "inherit" }}>
                    {post.titulo}
                    </Link>
                </Card.Title>
                <Card.Text
                  dangerouslySetInnerHTML={{
                    __html: post.conteudo.substring(0, 200) + "...",
                  }}
                />
                <div className="tag-list"> 
                  {post.tags.map((tag, index) => (
                    <CustomNavLink
                      key={index}
                      to={`/blog/tag/${tag.nome}`}>
                      #{tag.nome}
                    </CustomNavLink>
                  ))}
                </div>
              </Card.Body>
                <Card.Footer className="text-muted d-flex justify-content-between">
                  <span>
                    Publicado em: {new Date(post.criado_em).toLocaleDateString()}
                  </span>
                  <span>
                    <Link className="text-decoration-none" to="/sobre">Por: {post.nome_autor}</Link>
                  </span>
                </Card.Footer>
            </Card>
          </Col>
        ))}
        </Row>
       ) : (
        <Row className="justify-content-center">
        <p> Nenhum resultado obtido.</p>
        </Row>
      )}
    </Container>
  );
};

export default BlogList;

