import React from "react";
import { Form } from "react-bootstrap";
import { BoolInput } from "./BoolInput";
import { TextAreaInput } from "./TextAreaInput";
import { SelectInput } from "./SelectInput";
import { RadioInput } from "./RadioInput";

export const renderInputField = ({
  field,
  formData,
  setFormData,
  handleChange,
}: {
  field: any;
  formData: { [key: string]: any };
  setFormData: React.Dispatch<React.SetStateAction<{ [key: string]: any }>>;
  handleChange: (e: React.ChangeEvent<any>) => void;
}) => {
  const widget = field.widget_type || field.data_type;
  const commonProps = {
    name: field.name,
    value: formData[field.name] ?? "",
    onChange: handleChange,
    required: field.required,
  };

  switch (widget) {
    case "checkbox":
      break;
    case "bool":
      return (
        <BoolInput
          field={field}
          value={formData[field.name] !== undefined ? formData[field.name] : true}
          onChange={(name: string, val: any) => setFormData((prev) => ({ ...prev, [name]: val }))}
        />
      );
    case "textarea":
      break;
    case "text":
      return (
        <TextAreaInput
          name={field.name}
          label={field.label}
          value={formData[field.name] || ""}
          onChange={(value) => setFormData({ ...formData, [field.name]: value })}
        />
      );
    case "number":
      break;
    case "int":
      break;
    case "float":
      return (
        <Form.Group className="mb-1" controlId={field.name} key={`${widget}-${field.name}`}>
          <Form.Label className="fw-bold">{field.label}</Form.Label>
          <Form.Control type="number" {...commonProps} />
        </Form.Group>
      );
    case "radio":
      return (
        <RadioInput
          field={field}
          value={formData[field.name] ?? {}}
          possibleValues={field.max_value ? Array.from({ length: field.max_value }, (_, i) => i + 1) : []}
          onChange={(name, updatedDict) =>
            setFormData((prev) => ({ ...prev, [name]: updatedDict }))
          }
        />
      );
    case "select":
      return (
        <SelectInput
          field={field}
          value={formData[field.name]}
          onChange={(name: string, value: any) => setFormData((prev) => ({ ...prev, [name]: value }))}
        />
      );
    case "input":
      return (
        <Form.Group className="mb-1" controlId={field.name} key={`${widget}-${field.name}`}>
          <Form.Label>{field.label}</Form.Label>
          <Form.Control
            type="text"
            name={field.name}
            value={formData[field.name] || ""}
            onChange={handleChange}
            required={field.required}
          />
        </Form.Group>
      );
    default:
      console.warn("Widget não suportado ou inválido:", field);
      return null;
  }
};

