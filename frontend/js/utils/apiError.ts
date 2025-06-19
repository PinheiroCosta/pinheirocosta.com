export function parseApiError(error: any): string {
  const status = error?.status;
  const detail = error?.body?.detail;

  if (status === 400) {
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail)) {
      return detail.map((d: any) => (Array.isArray(d.loc) ? `${d.loc.join('.')}: ${d.msg}` : d.msg)).join('; ');
    }
    return "Requisição inválida.";
  }

  if (status === 422) {
    if (Array.isArray(detail)) {
      return detail.map((d: any) => (Array.isArray(d.loc) ? `${d.loc.join('.')}: ${d.msg}` : d.msg)).join('; ');
    }
    return "Erro de validação nos dados enviados.";
  }

  if (status === 404) return "Recurso não encontrado.";
  if (status === 500) return "Erro interno no servidor. Tente novamente mais tarde.";

  return "Falha inesperada ao processar a requisição.";
}

