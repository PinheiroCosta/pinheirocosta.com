import React, { useEffect, useState } from "react";
import { Container, Table, Spinner, Alert } from "react-bootstrap";
import { ToolsService } from "../api/services.gen"; 
import { Link } from "react-router-dom";
import type { Tool } from "../api/types.gen";


const Tools = () => {
  const [tools, setTools] = useState<Tool[]>([]); // Inicializa com um array vazio
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    ToolsService.toolsList()
      .then((data) => {
        setTools(data.results || []); // Garante que tools sempre seja um array
        setLoading(false);
      })
      .catch((error) => {
        console.error("Erro ao buscar ferramentas:", error);
        setError("Erro ao carregar ferramentas");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <Container className="text-center mt-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Carregando...</span>
        </Spinner>
      </Container>
    );
  }

  if (error) {
    return <Alert variant="danger">{error}</Alert>;
  }

  if (tools.length === 0) {
    return <Alert variant="warning">Nenhuma ferramenta encontrada.</Alert>;
  }

  return (
    <Container className="mt-5">
      <h2 className="my-4 text-center">Lista de Ferramentas</h2>
      <Table striped bordered hover >
        <thead>
          <tr>
            <th>Nome</th>
            <th>Descrição</th>
          </tr>
        </thead>
        <tbody>
          {tools.map((tool) => (
            <tr key={tool.id}>
              <td className="align-middle">
                <Link to={`/tools/${tool.slug}`} state={{ tool }}>
                    {tool.name}
                </Link>
                </td>
              <td>{tool.description}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </Container>
  );
};

export default Tools;

