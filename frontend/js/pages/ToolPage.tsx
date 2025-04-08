import React, { useEffect, useState } from "react";
import { useParams, useLocation, useNavigate } from "react-router-dom";
import DynamicToolForm from "../components/DynamicToolForm";
import { ToolsService } from "../api/services.gen";
import { ToolsRetrieveResponse } from "../api/types.gen";

const ToolPage = () => {
  const { slug } = useParams<{ slug: string }>();
  const location = useLocation();
  const navigate = useNavigate();

  const [tool, setTool] = useState<ToolsRetrieveResponse | null>(
    location.state?.tool || null
  );

  useEffect(() => {
    if (!tool && slug) {
      ToolsService.toolsList()
        .then((tools) => {
          const found = tools.results.find((t) => t.slug === slug);
          if (!found) throw new Error("Ferramenta não encontrada");
          setTool(found);
        })
        .catch((err) => {
          console.error("Erro ao buscar ferramenta por slug:", err);
          navigate("/404");
        });
    }
  }, [tool, slug, navigate]);

  if (!tool) return <p>Carregando...</p>;

  switch (tool.category) {
    case "calculadora":
      return <DynamicToolForm tool={tool} />;
    default:
      return <p>Categoria não suportada ainda.</p>;
  }
};

export default ToolPage;

