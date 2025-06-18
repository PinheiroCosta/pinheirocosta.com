import { useState } from "react";
import { useToolSubmit } from "../../hooks/useToolSubmit";
import type { ToolsRetrieveResponse } from "../../api/types.gen";

export const useDynamicToolFormLogic = (tool: ToolsRetrieveResponse) => {
  const [formData, setFormData] = useState<{ [key: string]: any }>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    const parsedValue = type === "number" ? parseFloat(value) : value;
    setFormData(prev => ({ ...prev, [name]: parsedValue }));
  };

  const { submit, loading, result, error, reset } = useToolSubmit(tool);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await submit(formData);
  };

  const handleResetForm = () => {
    setFormData({});
    reset();
  };

  return {
    formData,
    setFormData,
    handleChange,
    handleSubmit,
    handleResetForm,
    loading,
    result,
    error,
  };
};

