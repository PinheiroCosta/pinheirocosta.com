import { useState } from "react";
import { ToolsService } from "../api/services.gen";
import { ProxyToolData, ProxyToolResponse, ToolsRetrieveResponse } from "../api/types.gen";
import { parseApiError } from "../utils/apiError";


export function useToolSubmit(tool: ToolsRetrieveResponse) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ProxyToolResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const reset = () => {
      setResult(null);
      setError(null);
  };

  const submit = async (formData: Record<string, any>) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const payload: ProxyToolData = { ...formData, slug: tool.slug };
      const data = await ToolsService.proxyTool({
        slug: tool.slug,
        requestBody: payload,
      });

      if (tool.slug === "masquerade" && data.ficha) {
        const ficha = data.ficha;
        const newFormData: Record<string, any> = {};

        for (const input of tool.inputs) {
          const path = input.name.split(".");
          let current: any = ficha;
          for (const segment of path) {
            if (current && segment in current) {
              current = current[segment];
            } else {
              current = undefined;
              break;
            }
          }
          if (current !== undefined) {
            newFormData[input.name] = current;
          }
        }
      }

      setResult(data);
      return data;
    } catch (error) {
      console.log(error);
      setError(parseApiError(error));
    } finally {
      setLoading(false);
    }
  };

  return { submit, loading, result, error, reset };
}

