import React, { useEffect, useState } from "react";
import { FaExternalLinkAlt } from "react-icons/fa";
import { Card } from "react-bootstrap";
import { Link } from "react-router-dom";
import { ToolsService } from "../api/services.gen";
import { ToolsRetrieveResponse } from "../api/types.gen";

const RandomToolCard: React.FC = () => {
  const [tool, setTool] = useState<ToolsRetrieveResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    async function fetchRandomTool() {
      try {
        const result = await ToolsService.toolsRandomRetrieve();
        setTool(result);
      } catch (err) {
          console.warn("Erro ao buscar ferramenta:", err);
      } finally {
          setLoading(false);
      }
    }
    fetchRandomTool();
  }, []);

  return (
    <Card className="text-start h-100 w-100" style={{ minHeight: "300px" }}>
      <Card.Header className="text-center mb-2 pb-3 pt-3 fs-5">Ferramenta em Destaque</Card.Header>
      <Card.Body className="d-flex flex-column">
        {loading ? (
          <div style={{ flexGrow: 1 }} className="d-flex align-items-center justify-content-center text-muted">
            Carregando ferramenta...
          </div>
        ) : error ? (
          <div style={{ flexGrow: 1 }} className="d-flex align-items-center justify-content-center text-danger">
            Não foi possível carregar as ferramentas no momento.
          </div>
        ) : tool ? (
          <>
            <h2 className="fs-5">
              <Link className="nav-link text-center" to={`/tools/${tool.slug}`}>
                {tool.name[0].toUpperCase() + tool.name.slice(1)}
              </Link>
            </h2>
            <Card.Text className="text-justify">{tool.description}</Card.Text>
            <div className="text-center fs-5 mt-auto">
              <Link className="nav-link active py-2" to={`/tools/${tool.slug}`}>
                Acessar Ferramenta <FaExternalLinkAlt className="ms-2" />
              </Link>
            </div>
          </>
        ) : (
          <div style={{ flexGrow: 1 }} className="d-flex align-items-center justify-content-center text-muted">
            Nenhuma ferramenta disponível no momento.
          </div>
        )}
      </Card.Body>
    </Card>
  );
};

export default RandomToolCard;

