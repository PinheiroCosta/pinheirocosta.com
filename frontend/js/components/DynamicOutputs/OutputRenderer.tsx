import React, { useState } from "react";
import { Card, Button } from "react-bootstrap";
import { FiClipboard } from "react-icons/fi";
import { ToolField, DataTypeEnum } from "../../api/types.gen";

interface OutputRendererProps {
  outputs: ToolField[];
  result: any;
}

const getDisplayValue = (value: any, fieldType: DataTypeEnum): string => {
  if (value === undefined || value === null) return "";

  switch (fieldType) {
    case "int":
    case "float":
      return new Intl.NumberFormat("pt-BR").format(Number(value));
    case "bool":
      return value ? "Sim" : "Não";
    case "list":
    case "dict":
    case "string":
    default:
      return String(value);
  }
};

const OutputRenderer: React.FC<OutputRendererProps> = ({ outputs, result }) => {
  const [copiedField, setCopiedField] = useState<string | null>(null);

  const handleCopy = (fieldName: string, text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopiedField(fieldName);
      setTimeout(() => setCopiedField(null), 1500);
    });
  };

  if (!result || outputs.length === 0) return null;

  return (
    <>
      {outputs.map((field) => {
        const value = getDisplayValue(result[field.name], field.data_type);
        return (
          <Card bg="light" key={`output-${field.name}`} className="mb-2">
           <Card.Body
              className="p-2 position-relative"
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "flex-start",
                justifyContent: "center",
              }}
            >
              <div className="w-100" style={{ overflowWrap: "anywhere" }}>
                <strong>{field.label}:</strong> {value}
              </div>

              <Button
                variant="link"
                size="sm"
                onClick={() => handleCopy(field.name, value)}
                className="p-0 position-absolute"
                style={{ bottom: 4, right: 4, lineHeight: 1, cursor: "pointer", color: 'white'}}
                title="Copiar"
              >
                <FiClipboard size={16} />
              </Button>
            </Card.Body> 
            {copiedField === field.name && (
              <div className="text-success text-center small mb-1">Copiado!</div>
            )}
          </Card>
        );
      })}
    </>
  );
};

export default OutputRenderer;

