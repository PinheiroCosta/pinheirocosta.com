import React from "react";

interface BuyMeACoffeeButtonProps {
    className?: string;
}

const BuyMeACoffeeButton: React.FC<BuyMeACoffeeButtonProps> = ({ className }) => {
  return (
    <div className={className}>
       <a href="https://www.buymeacoffee.com/pinheirocosta" target="_blank">
        <img 
            className="bmc-button-img"
            src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png"
            alt="Buy Me A Coffee"
            style={{ width: "130px" }} 
        />
       </a> 
    </div>
  );
};

export default BuyMeACoffeeButton;
