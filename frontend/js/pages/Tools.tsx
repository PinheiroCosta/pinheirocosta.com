import React, { useEffect, useState } from "react";
import { Container, Table } from "react-bootstrap";
import { ErrorMessage, InfoMessage } from "../MessageCard";
import { ToolsService } from "../api/services.gen"; 
import { Link } from "react-router-dom";
import Pagination from "../components/Pagination";
import type { Tool } from "../api/types.gen";


const Tools = () => {
  const [tools, setTools] = useState<Tool[]>([]); 
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [count, setCount] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [hasNext, setHasNext] = useState(false);
  const [hasPrevious, setHasPrevious] = useState(false);
  const [categoryFilter, setCategoryFilter] = useState<Tool["category"] | null>(null);
  const pageSize= 6;


  useEffect(() => {
    setLoading(true);
    ToolsService.toolsList({ page: currentPage, category: categoryFilter || undefined, })
      .then((data) => {
        setTools(data.results || []); 
        setHasNext(Boolean(data.next));
        setHasPrevious(Boolean(data.previous));
		setCount(data.count);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Erro ao buscar ferramentas:", error);
        setError("Erro ao carregar ferramentas");
        setLoading(false);
      });
  }, [currentPage, categoryFilter]);

  if (loading) {
    return (
      <Container className="text-center mt-5">
          <span className="visually-hidden">Carregando...</span>
      </Container>
    );
  }

  if (error) {
    return <ErrorMessage title="Error" message={error} ></ErrorMessage>;
  }

  if (tools.length === 0) {
    return <ErrorMessage title="Error" message="Nenhuma Ferramenta foi encontrada." ></ErrorMessage>;
  }

  return (
    <Container className="mt-5 ">
      <h2 className="my-4 text-center">Lista de Ferramentas</h2>
        {categoryFilter && (
          <InfoMessage title="" message={`Filtrando por categoria: ${categoryFilter}`} >
            <button
              className="btn btn-sm btn-outline-secondary ms-2"
              onClick={() => {
                setCategoryFilter(null);
                setCurrentPage(1);
              }}
            >
              Limpar filtro
            </button>
          </InfoMessage>
        )}
      <div className="table-wrapper">
      <Table className="my-table">
        <thead>
          <tr>
            <th>Nome</th>
            <th>Categoria</th>
            <th>Descrição</th>
          </tr>
        </thead>
        <tbody>
          {tools.map((tool) => (
            <tr key={tool.id}>
              <td className="align-middle fw-bold">
                <Link to={`/tools/${tool.slug}`} state={{ tool }}>
                    {tool.name}
                </Link>
                </td>
              <td className="align-middle" >
                  <span
                    style={{ textDecoration: "underline", cursor: "pointer" }}
                    onClick={() => {
                      setCategoryFilter(tool.category);
                      setCurrentPage(1); 
                    }}
                  >
                    {tool.category}
                  </span>
              </td>
              <td>{tool.description}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
    <Pagination currentPage={currentPage} pageSize={pageSize} count={count} hasNext={hasNext} hasPrevious={hasPrevious} onPageChange={setCurrentPage} />
    </Container>
  );
};

export default Tools;

