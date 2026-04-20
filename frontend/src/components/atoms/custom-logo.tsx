interface CustomLogoProps {
  src: string;
  alt: string;
  variant?: "default" | "circle";
  size?: "sm" | "md" | "lg";
  className?: string;
}

export const CustomLogo = ({
  src,
  alt,
  variant = "default",
  size = "md",
  className = ""
}: CustomLogoProps) => { 

  const sizes = {
    sm: "h-8 w-auto",
    md: "h-12 w-auto",
    lg: "h-20 w-auto",
  }

  const variants = {
    default: "rounded-none",
    circle: "rounded-full object-cover",
  };

  const logoClasses = `
    ${sizes[size]}
    ${variants[variant]}
    ${className}
  `.trim();

  return (
    <img
      src={src}
      alt={alt}
      className={logoClasses}
    />
  )
}