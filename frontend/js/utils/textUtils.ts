import striptags from "striptags";
import he from "he";

export const getPreview = (htmlContent: string, maxLength = 200): string => {
  const plainText = he.decode(striptags(htmlContent));
  if (plainText.length <= maxLength) return plainText;

  const truncated = plainText.substring(0, maxLength);
  const lastSpace = truncated.lastIndexOf(" ");
  return (lastSpace > 0 ? truncated.substring(0, lastSpace) : truncated) + "...";
};
