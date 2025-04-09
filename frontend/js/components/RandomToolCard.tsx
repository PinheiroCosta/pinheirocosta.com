import React, { useEffect, useState } from "react";
import { Card, Button } from "react-bootstrap";
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
    <Card className="text-start">
    <Card.Header className="text-center mb-2 pb-3 pt-3 fs-5">Ferramenta em Destaque</Card.Header>
      <Card.Body>

        {loading ? (
          <p>Carregando ferramenta...</p>
        ) : error ? (
          <p>Não foi possível carregar as ferramentas no momento. Tente novamente mais tarde.</p>
        ) : tool ? (
          <>
            <h5>
              <Link className="nav-link text-center" to={`/tools/${tool.slug}`}>
                {tool.name[0].toUpperCase() + tool.name.slice(1)}
              </Link>
            </h5>
            <Card.Text className="text-justify">{tool.description}</Card.Text>
            <div className="text-center fs-5">
              <Link className="nav-link active" to={`/tools/${tool.slug}`}>
                Acessar Ferramenta
              </Link>
            </div>
          </>
        ) : (
          <p>Nenhuma ferramenta disponível no momento.</p>
        )}
      </Card.Body>
    </Card>
  );
};

export default RandomToolCard;

