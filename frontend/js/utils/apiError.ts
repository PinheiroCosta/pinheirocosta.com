/**
 * Mensagens de erro padrão para exibição ao usuário.
 */
const GENERIC_ERROR_MESSAGE = "Falha inesperada ao processar a requisição.";
const NETWORK_ERROR_MESSAGE = "Falha de conexão. Verifique sua internet e tente novamente.";
const BAD_REQUEST_MESSAGE = "Requisição inválida.";
const VALIDATION_ERROR_MESSAGE = "Erro de validação nos dados enviados.";
const NOT_FOUND_MESSAGE = "Recurso não encontrado.";
const SERVER_ERROR_MESSAGE = "Erro interno no servidor. Tente novamente mais tarde.";

/**
 * Interface padrão para erro detalhado da API.
 */
interface ApiErrorDetail {
  type?: string;
  loc?: (string | number)[];
  msg: string;
  input?: any;
}

/**
 * Interface para o corpo do erro retornado pela API.
 */
interface ApiErrorBody {
  detail?: string | ApiErrorDetail[];
}

/**
 * Interface para o objeto de erro recebido.
 */
interface ApiError {
  status?: number;
  body?: ApiErrorBody;
}

/**
 * Verifica se o objeto é do tipo ApiError.
 * Agora verifica também tipos internos para maior segurança.
 */
function isApiError(error: any): error is ApiError {
  return (
    typeof error === "object" &&
    error !== null &&
    typeof error.status === "number" &&
    typeof error.body === "object" &&
    error.body !== null &&
    ("detail" in error.body)
  );
}

/**
 * Detecta se o erro é uma falha de conexão ou rede (exemplo fetch sem resposta).
 */
function isNetworkError(error: any): boolean {
  return (
    error &&
    (error.message === "Failed to fetch" || error.message === "Network Error")
  );
}

/**
 * Formata o campo `detail` do erro, quando é um array de objetos detalhados.
 * @param detail Array de objetos com informações do erro.
 * @returns Mensagem formatada para exibição.
 */
function formatDetailArray(detail: ApiErrorDetail[], showLoc = false): string {
  if (!Array.isArray(detail)) return "";
  return detail
    .map((d) =>
      showLoc && Array.isArray(d.loc) ? `${d.loc.join(".")}: ${d.msg}` : d.msg
    )
    .join("; ");
}

/**
 * Analisa um objeto de erro retornado pela API e retorna uma mensagem amigável.
 * Trata erros comuns por status HTTP, falhas de conexão e tenta extrair mensagens detalhadas.
 * Se o formato da resposta for inesperado, retorna mensagem genérica.
 *
 * @param error Objeto de erro retornado pela API.
 * @returns Mensagem de erro para exibição ao usuário.
 */
export function parseApiError(error: any): string {
  if (isNetworkError(error)) {
    return NETWORK_ERROR_MESSAGE;
  }

  if (!isApiError(error)) {
    return GENERIC_ERROR_MESSAGE;
  }

  const status = error.status;
  const detail = error.body?.detail;

  const statusHandlers: Record<number, (detail: any) => string> = {
    400: (detail) =>
      typeof detail === "string"
        ? detail
        : formatDetailArray(detail) || BAD_REQUEST_MESSAGE,
    422: (detail) =>
      Array.isArray(detail)
        ? formatDetailArray(detail, false)
        : VALIDATION_ERROR_MESSAGE,
    404: () => NOT_FOUND_MESSAGE,
    500: () => SERVER_ERROR_MESSAGE,
  };

  if (status && status in statusHandlers) {
    try {
      return statusHandlers[status](detail);
    } catch {
      return GENERIC_ERROR_MESSAGE;
    }
  }

  return GENERIC_ERROR_MESSAGE;
}
