import React from "react";
import { Form } from "react-bootstrap";

export const SelectInput = ({ field, value, onChange }) => {
  const handleChange = (e) => {
    const rawValue = e.target.value;

    let finalValue;
    if (field.data_type === "int") {
      finalValue = parseInt(rawValue, 10);
    } else {
      finalValue = rawValue;
    }
    onChange(field.name, finalValue);
  };

  return (
    <Form.Group className="mb-1" controlId={field.name} key={`select-${field.name}`}>
      <Form.Label title={field.help_text}>{field.label}</Form.Label>
      <Form.Select
        name={field.name}
        value={value ?? field.default_value ?? ""}
        onChange={handleChange}
        required={field.required}
      >
        {field.options?.map((opt) => (
          <option key={`option-${field.name}-${opt.value}`} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </Form.Select>
    </Form.Group>
  );
};

export default SelectInput;

