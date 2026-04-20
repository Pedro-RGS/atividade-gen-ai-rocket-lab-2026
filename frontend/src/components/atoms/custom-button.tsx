import type { ButtonHTMLAttributes, ReactNode } from "react";

interface CustomButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: "primary" | "secondary" | "danger";
}

export const CustomButton = ({
  children,
  variant = "primary",
  className = "",
  ...props
}: CustomButtonProps) => {
  const baseStyles =
    "px-[20px] py-[10px] border-none cursor-pointer rounded-[4px] font-bold transition-all duration-200 hover:brightness-90";

  const variants = {
    primary:
      "bg-(--color-primary) text-black hover:bg-(--color-primary-hover) uppercase tracking-tighter",
    secondary:
      "bg-transparent border border-zinc-700 text-white hover:bg-zinc-800",
    danger: "bg-red-600 text-white",
  };

  const buttonClass = `${baseStyles} ${variants[variant]} ${className}`;

  return (
    <button className={buttonClass} {...props}>
      {children}
    </button>
  );
};