import { useState, useEffect } from "react";
import { SubjectEnum } from "../../api/types.gen";
import { ContatoProfissionalService } from "../../api/services.gen";

export function useContactFormLogic(siteKey: string) {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    subject: "hire" as SubjectEnum,
    message: "",
  });

  const [isSending, setIsSending] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const subjectOptions = [
    { value: "hire", label: "Quero contratar" },
    { value: "question", label: "Tenho uma dúvida" },
    { value: "feedback", label: "Gostaria de dar um feedback" },
    { value: "other", label: "Outro assunto" },
  ];

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const utm_source = params.get("utm_source");
    const utm_campaign = params.get("utm_campaign");

    if (utm_source || utm_campaign) {
      setFormData((prev) => ({
        ...prev,
        message: `${prev.message}\n\n[UTM info: ${utm_source ?? ""} | ${utm_campaign ?? ""}]`,
      }));
    }
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSending(true);
    setError(null);

    let token: string;

    // Executa reCAPTCHA
    try {
      if (!window.grecaptcha || !window.grecaptcha.execute) {
        throw new Error("reCAPTCHA não carregado.");
      }
      token = await window.grecaptcha.execute(siteKey, { action: "contact_form" });
    } catch (error) {
        setError("Erro ao executar o reCAPTCHA. Verifique Adblockers ou tente recarregar a página.");
        setIsSending(false);
        return;
    }

    // Envia Formulário
    try {
      const payload = { ...formData, recaptcha_token: token };
      await ContatoProfissionalService.contatoProfissionalCreate({ requestBody: payload });
      setSuccess(true);
    } catch (err: any) {
      setError(err?.message ?? "Erro ao enviar o formulário. Desative Adblocker ou similares.");
    } finally {
      setIsSending(false);
    }
  };

  return {
    formData,
    setFormData,
    subjectOptions,
    isSending,
    setIsSending,
    success,
    setSuccess,
    error,
    setError,
    handleSubmit,
  };
}

