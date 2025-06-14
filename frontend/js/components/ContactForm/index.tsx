import ContactForm from "./ContactForm";
import { useContactFormLogic } from "./useContactFormLogic";

type Props = {
    siteKey: string;
};

export default function ContactFormContainer({ siteKey }: Props) {
  const props = useContactFormLogic(siteKey);
  return <ContactForm siteKey={siteKey}{...props} />;
}

