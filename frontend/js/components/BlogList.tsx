import React from "react";
import { Container, Row, Col, Card, Spinner } from "react-bootstrap";
import CustomNavLink from "./CustomNavLink"; 
import { Link } from "react-router-dom";
import { getPreview } from "../utils/textUtils";
import type { BlogPost } from "../api/types.gen";

interface BlogListProps {
  posts: BlogPost[];
  loading: boolean;
  error: string | null;
}

const BlogList: React.FC<BlogListProps> = ({ posts, loading, error }) => {
  return (
    <Container className="px-2">
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
              <Card className="h-100 d-flex flex-column">
                <Card.Body className="d-flex flex-column">
                  <Card.Title className="text-center fw-bold mb-3">
                    <Link
                      to={`/blog/${post.slug}`}
                      className="text-decoration-none "
                    >
                      {post.titulo}
                    </Link>
                  </Card.Title>
                  <Card.Text className="flex-grow-1">
                    {getPreview(post.conteudo)}
                  </Card.Text>
                  <div className="tag-list mt-2">
                    {post.tags.map((tag, index) => (
                      <CustomNavLink key={index} to={`/blog/tag/${tag.nome}`}>
                        #{tag.nome}
                      </CustomNavLink>
                    ))}
                  </div>
                </Card.Body>
                <Card.Footer className="text-muted d-flex flex-wrap justify-content-between small gap-2">
                  <span>
                    <strong>Publicado em:</strong>{" "}
                    {new Date(post.criado_em).toLocaleDateString()}
                  </span>
                  <span>
                    <Link className="text-decoration-none" to="/sobre">
                      Por: <strong>{post.nome_autor}</strong>
                    </Link>
                  </span>
                </Card.Footer>
              </Card>
            </Col>
          ))}
        </Row>
      ) : (
        <Row className="justify-content-center">
          <p>Nenhum resultado obtido.</p>
        </Row>
      )}
    </Container>
  );
};

export default BlogList;

